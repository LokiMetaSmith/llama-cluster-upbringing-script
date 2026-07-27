use candle_core::{DType, Device, Shape, Tensor, Result};

/// Converts a raw DMA-filled buffer slice into a Candle Tensor.
/// Note: While the I/O transfer from NVMe to host RAM is zero-copy (via DMA),
/// Candle requires constructing from typed slices, which currently incurs a host-RAM copy
/// unless using safetensors mmap directly.
pub fn buffer_to_candle_tensor(
    buf: &[u8],
    shape: Shape,
    dtype: DType,
    device: &Device,
) -> Result<Tensor> {
    match dtype {
        DType::F32 => {
            // Unsafe transmute to avoid copying memory during cast, then feed into Candle
            let (prefix, floats, suffix) = unsafe { buf.align_to::<f32>() };
            assert!(prefix.is_empty() && suffix.is_empty(), "Buffer must be properly aligned for f32");

            match device {
                Device::Cpu => Tensor::from_slice(floats, shape.dims(), device),
                Device::Cuda(_) => {
                    let cpu_tensor = Tensor::from_slice(floats, shape.dims(), &Device::Cpu)?;
                    cpu_tensor.to_device(device)
                }
                _ => unimplemented!("Device not supported for buffer streaming"),
            }
        }
        _ => unimplemented!("Only F32 streaming is mocked in this prototype"),
    }
}
