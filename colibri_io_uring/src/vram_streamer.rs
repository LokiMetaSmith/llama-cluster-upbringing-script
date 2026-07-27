use std::os::unix::io::RawFd;

/// Represents an abstract engine for streaming weights directly into GPU VRAM.
pub trait DirectVramStreamer {
    /// Initialize the streaming engine for a specific file descriptor.
    fn new(file_fd: RawFd) -> Result<Self, String> where Self: Sized;

    /// Read asynchronously from the disk directly into a GPU device pointer.
    ///
    /// For NVIDIA (cuFile), `gpu_ptr` must be allocated via `cudaMalloc`.
    /// For AMD (HIP), `gpu_ptr` must be allocated via `hipMalloc`.
    unsafe fn read_to_vram_async(
        &mut self,
        offset: u64,
        size: usize,
        gpu_ptr: *mut libc::c_void,
    ) -> Result<(), String>;

    /// Block until all pending asynchronous reads are completed.
    fn submit_and_wait(&mut self) -> Result<(), String>;
}
