use candle_core::{DType, Device, Shape};
use colibri_io_uring::tensor_bridge::buffer_to_candle_tensor;

fn main() {
    // Allocate a Vec<f32> to guarantee 4-byte alignment, then view it as bytes.
    let floats = vec![1.0f32, 2.0, 3.0, 4.0];

    // Safely cast the aligned f32 slice into a u8 slice to simulate the I/O buffer
    let buf: &[u8] = unsafe {
        std::slice::from_raw_parts(
            floats.as_ptr() as *const u8,
            floats.len() * std::mem::size_of::<f32>(),
        )
    };

    let shape = Shape::from((2, 2));
    let device = Device::Cpu;

    let tensor = buffer_to_candle_tensor(buf, shape, DType::F32, &device).unwrap();

    println!("Zero-copy tensor:\n{}", tensor);
}
