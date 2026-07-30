use io_uring::{opcode, IoUring};
use std::fs::File;
use std::os::fd::{AsRawFd, RawFd};
use std::os::unix::fs::OpenOptionsExt;
use std::ptr;

pub struct AsyncWeightStreamer {
    ring: IoUring,
    file: File,
    file_fd: RawFd,
    buffer_pool: Vec<*mut libc::c_void>,
    queue_depth: u32,
    buffer_size: usize,
}

impl AsyncWeightStreamer {
    pub fn new(weight_file_path: &str, queue_depth: u32, buffer_size: usize) -> std::io::Result<Self> {
        // Open file with O_DIRECT to bypass OS page cache for true zero-copy DMA to host RAM
        let file = std::fs::OpenOptions::new()
            .read(true)
            .custom_flags(libc::O_DIRECT)
            .open(weight_file_path)?;

        let file_fd = file.as_raw_fd();
        let ring = IoUring::new(queue_depth)?;

        let mut buffer_pool = Vec::with_capacity(queue_depth as usize);
        let alignment = 4096; // Page alignment required for O_DIRECT

        // Allocate pinned aligned host memory buffers
        for _ in 0..queue_depth {
            let mut ptr: *mut libc::c_void = ptr::null_mut();
            let ret = unsafe { libc::posix_memalign(&mut ptr, alignment, buffer_size) };
            if ret != 0 {
                return Err(std::io::Error::last_os_error());
            }
            // Zero-initialize to prevent undefined behavior if an async read fails or is skipped
            unsafe {
                std::ptr::write_bytes(ptr, 0, buffer_size);
            }
            buffer_pool.push(ptr);
        }

        Ok(Self {
            ring,
            file,
            file_fd,
            buffer_pool,
            queue_depth,
            buffer_size,
        })
    }

    /// Submits an asynchronous read request for an expert weight chunk.
    pub unsafe fn queue_expert_read(&mut self, offset: u64, size: usize, slot_idx: usize) -> Result<(), &'static str> {
        if slot_idx >= self.queue_depth as usize {
            return Err("Slot index exceeds queue depth");
        }
        if size > self.buffer_size {
            return Err("Requested read size exceeds pinned buffer size");
        }

        let buf_ptr = self.buffer_pool[slot_idx] as *mut u8;

        let read_e = opcode::Read::new(
            io_uring::types::Fd(self.file_fd),
            buf_ptr,
            size as u32,
        )
        .offset(offset)
        .build()
        .user_data(slot_idx as u64); // Use slot_idx as user_data to map completions to buffers

        self.ring
            .submission()
            .push(&read_e)
            .map_err(|_| "Submission queue full")?;

        Ok(())
    }

    pub fn submit_and_wait(&mut self, expected_completions: usize) -> std::io::Result<usize> {
        self.ring.submit_and_wait(expected_completions)
    }

    pub fn check_completions(&mut self) -> Vec<u64> {
        let mut completed_slots = Vec::new();
        let mut cq = self.ring.completion();
        while let Some(cqe) = cq.next() {
            if cqe.result() >= 0 {
                completed_slots.push(cqe.user_data());
            } else {
                eprintln!("io_uring read error: {}", cqe.result());
            }
        }
        completed_slots
    }

    /// Provides safe access to the raw byte slice of a specific DMA buffer slot
    /// so it can be transmutted into a Tensor.
    pub fn get_buffer_slice<'a>(&'a self, slot_idx: usize, size: usize) -> Result<&'a [u8], &'static str> {
        if slot_idx >= self.queue_depth as usize {
            return Err("Slot index exceeds queue depth");
        }
        if size > self.buffer_size {
            return Err("Requested size exceeds buffer size");
        }
        let ptr = self.buffer_pool[slot_idx] as *const u8;
        let slice = unsafe { std::slice::from_raw_parts(ptr, size) };
        Ok(slice)
    }
}

impl Drop for AsyncWeightStreamer {
    fn drop(&mut self) {
        for &ptr in &self.buffer_pool {
            unsafe {
                libc::free(ptr);
            }
        }
    }
}
