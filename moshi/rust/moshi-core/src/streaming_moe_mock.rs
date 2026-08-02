use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use candle::{Device, Result};
use colibri_io_uring::streamer::AsyncWeightStreamer;
use colibri_io_uring::moe_layer::StreamingMoeLayer;
use colibri_io_uring::generator::generate_synthetic_weights;
use std::path::Path;

pub fn create_mock_streaming_moe(expert_size: usize, num_experts: usize, device: Device) -> Result<Arc<StreamingMoeLayer>> {
    let file_path = Path::new("mock_moe_weights.bin");

    // Only generate if it doesn't exist to avoid constant rewrites
    if !file_path.exists() {
        generate_synthetic_weights(file_path, num_experts, expert_size)
            .map_err(|e| candle::Error::Msg(format!("Failed to generate synthetic weights: {:?}", e)))?;
    }

    let streamer = AsyncWeightStreamer::new(
        file_path.to_str().unwrap(),
        2, // queue depth
        expert_size,
    ).map_err(|e| candle::Error::Msg(format!("Failed to create streamer: {:?}", e)))?;

    let streamer_arc = Arc::new(Mutex::new(streamer));

    let mut offsets = HashMap::new();
    for i in 0..num_experts {
        offsets.insert(i, (i * expert_size) as u64);
    }

    let layer = StreamingMoeLayer::new(
        streamer_arc,
        offsets,
        expert_size,
        device,
    );

    Ok(Arc::new(layer))
}
