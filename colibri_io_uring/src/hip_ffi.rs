use std::os::unix::io::RawFd;
use crate::vram_streamer::DirectVramStreamer;

// In ROCm/HIP, direct storage access is often handled by rocPRIM or specific
// filesystem drivers, but a generic approach is to read to pinned host RAM
// and asynchronously copy to HIP VRAM via hipMemcpyAsync.

extern "C" {
    // HIP Memory Management
    fn hipMalloc(ptr: *mut *mut libc::c_void, size: usize) -> i32;
    fn hipFree(ptr: *mut libc::c_void) -> i32;

    // HIP Async Memory Copy (HostToDevice = 1)
    fn hipMemcpyAsync(
        dst: *mut libc::c_void,
        src: *const libc::c_void,
        sizeBytes: usize,
        kind: u32,
        stream: *mut libc::c_void
    ) -> i32;

    fn hipStreamSynchronize(stream: *mut libc::c_void) -> i32;
}

/// Fallback backend for AMD GPUs using standard file I/O and hipMemcpyAsync.
/// In a production environment, this would integrate with the io_uring engine.
pub struct AmdHipStreamer {
    file_fd: RawFd,
    // Pinned host buffer for staging
    host_buffer: *mut libc::c_void,
}

impl DirectVramStreamer for AmdHipStreamer {
    fn new(file_fd: RawFd) -> Result<Self, String> {
        // Allocate a pinned host buffer using posix_memalign (simulated here)
        let mut ptr: *mut libc::c_void = std::ptr::null_mut();
        let ret = unsafe { libc::posix_memalign(&mut ptr, 4096, 1024 * 1024 * 50) }; // 50MB staging
        if ret != 0 {
            return Err("posix_memalign failed".into());
        }

        Ok(Self {
            file_fd,
            host_buffer: ptr,
        })
    }

    unsafe fn read_to_vram_async(
        &mut self,
        offset: u64,
        size: usize,
        gpu_ptr: *mut libc::c_void,
    ) -> Result<(), String> {
        // 1. Read from disk into pinned host buffer (in reality, using io_uring)
        let bytes_read = libc::pread(self.file_fd, self.host_buffer, size, offset as i64);
        if bytes_read < 0 || bytes_read as usize != size {
             return Err("pread failed".into());
        }

        // 2. Asynchronously copy from pinned host buffer to HIP VRAM
        let res = hipMemcpyAsync(
            gpu_ptr,
            self.host_buffer as *const libc::c_void,
            size,
            1, // hipMemcpyHostToDevice
            std::ptr::null_mut(), // default stream
        );

        if res != 0 {
            return Err(format!("hipMemcpyAsync failed with code: {}", res));
        }

        Ok(())
    }

    fn submit_and_wait(&mut self) -> Result<(), String> {
        // Synchronize the default stream to wait for hipMemcpyAsync
        let res = unsafe { hipStreamSynchronize(std::ptr::null_mut()) };
        if res != 0 {
            return Err(format!("hipStreamSynchronize failed with code: {}", res));
        }
        Ok(())
    }
}

impl Drop for AmdHipStreamer {
    fn drop(&mut self) {
        unsafe {
            libc::free(self.host_buffer);
        }
    }
}
