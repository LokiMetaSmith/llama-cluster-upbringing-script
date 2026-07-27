use std::os::unix::io::RawFd;
use crate::vram_streamer::DirectVramStreamer;

// Minimal C-FFI bindings for Intel Level Zero (ze_api.h) for direct memory streaming
#[allow(non_camel_case_types)]
type ze_result_t = i32;
#[allow(non_camel_case_types)]
type ze_command_queue_handle_t = *mut libc::c_void;
#[allow(non_camel_case_types)]
type ze_command_list_handle_t = *mut libc::c_void;

extern "C" {
    // Level Zero Memory Copy (Host to Device)
    fn zeCommandListAppendMemoryCopy(
        hCommandList: ze_command_list_handle_t,
        dstptr: *mut libc::c_void,
        srcptr: *const libc::c_void,
        size: usize,
        hSignalEvent: *mut libc::c_void,
        numWaitEvents: u32,
        phWaitEvents: *mut *mut libc::c_void,
    ) -> ze_result_t;

    // Level Zero Queue Synchronization
    fn zeCommandQueueSynchronize(
        hCommandQueue: ze_command_queue_handle_t,
        timeout: u64,
    ) -> ze_result_t;
}

/// Fallback backend for Intel GPUs using standard file I/O and Intel Level Zero Memory Copies.
pub struct IntelLevelZeroStreamer {
    file_fd: RawFd,
    host_buffer: *mut libc::c_void,
    cmd_queue: ze_command_queue_handle_t,
    cmd_list: ze_command_list_handle_t,
}

impl DirectVramStreamer for IntelLevelZeroStreamer {
    fn new(file_fd: RawFd) -> Result<Self, String> {
        let mut ptr: *mut libc::c_void = std::ptr::null_mut();
        // Allocate pinned host buffer for staging
        let ret = unsafe { libc::posix_memalign(&mut ptr, 4096, 1024 * 1024 * 50) };
        if ret != 0 {
            return Err("posix_memalign failed".into());
        }

        Ok(Self {
            file_fd,
            host_buffer: ptr,
            cmd_queue: std::ptr::null_mut(), // Dummy for prototype
            cmd_list: std::ptr::null_mut(),  // Dummy for prototype
        })
    }

    unsafe fn read_to_vram_async(
        &mut self,
        offset: u64,
        size: usize,
        gpu_ptr: *mut libc::c_void,
    ) -> Result<(), String> {
        let bytes_read = libc::pread(self.file_fd, self.host_buffer, size, offset as i64);
        if bytes_read < 0 || bytes_read as usize != size {
             return Err("pread failed".into());
        }

        let res = zeCommandListAppendMemoryCopy(
            self.cmd_list,
            gpu_ptr,
            self.host_buffer as *const libc::c_void,
            size,
            std::ptr::null_mut(),
            0,
            std::ptr::null_mut(),
        );

        if res != 0 {
            return Err(format!("zeCommandListAppendMemoryCopy failed with code: {}", res));
        }

        Ok(())
    }

    fn submit_and_wait(&mut self) -> Result<(), String> {
        let res = unsafe { zeCommandQueueSynchronize(self.cmd_queue, u64::MAX) };
        if res != 0 {
            return Err(format!("zeCommandQueueSynchronize failed with code: {}", res));
        }
        Ok(())
    }
}

impl Drop for IntelLevelZeroStreamer {
    fn drop(&mut self) {
        unsafe {
            libc::free(self.host_buffer);
        }
    }
}
