use candle_core::{DType, Device, Shape};
use colibri_io_uring::tensor_bridge::buffer_to_candle_tensor;

fn main() {
    let mut buf = vec![0u8; 16]; // 16 bytes = 4 f32s

    // Write 4 f32s: 1.0, 2.0, 3.0, 4.0
    buf[0..4].copy_from_slice(&1.0f32.to_ne_bytes());
    buf[4..8].copy_from_slice(&2.0f32.to_ne_bytes());
    buf[8..12].copy_from_slice(&3.0f32.to_ne_bytes());
    buf[12..16].copy_from_slice(&4.0f32.to_ne_bytes());

    let shape = Shape::from((2, 2));
    let device = Device::Cpu;

    // We pass the buf as a slice, simulating the O_DIRECT DMA buffer we'd get from streamer
    let tensor = buffer_to_candle_tensor(&buf, shape, DType::F32, &device).unwrap();

    println!("Zero-copy tensor:\n{}", tensor);
}
