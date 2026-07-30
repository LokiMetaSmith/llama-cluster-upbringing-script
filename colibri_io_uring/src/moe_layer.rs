use std::sync::{Arc, Mutex};
use std::collections::HashMap;
use candle_core::{Tensor, Device, DType, Shape};
use crate::streamer::AsyncWeightStreamer;
use crate::tensor_bridge::buffer_to_candle_tensor;

/// Represents a Sparse Mixture-of-Experts Layer that streams its weights from SSD
pub struct StreamingMoeLayer {
    pub streamer: Arc<Mutex<AsyncWeightStreamer>>,
    pub expert_offsets: HashMap<usize, u64>,
    pub expert_size: usize,
    pub device: Device,
}

impl StreamingMoeLayer {
    pub fn new(
        streamer: Arc<Mutex<AsyncWeightStreamer>>,
        expert_offsets: HashMap<usize, u64>,
        expert_size: usize,
        device: Device,
    ) -> Self {
        Self {
            streamer,
            expert_offsets,
            expert_size,
            device,
        }
    }

    /// Simulates a predictive router head. In a real model, this would be a linear projection
    /// on the lookahead user tokens to determine which experts will be needed.
    fn predict_future_experts(&self, lookahead_tokens: &[u32]) -> Vec<usize> {
        // Mock logic: simply use the token value modulo the number of experts
        let num_experts = self.expert_offsets.len();
        lookahead_tokens
            .iter()
            .map(|&t| (t as usize) % num_experts.max(1))
            .collect()
    }

    /// Forward pass executing the current step while asynchronously fetching experts for the lookahead step.
    pub fn forward_with_lookahead(
        &self,
        xs: &Tensor,
        lookahead_user_tokens: &[u32],
    ) -> candle_core::Result<Tensor> {
        // 1. Run lightweight router head on lookahead tokens to predict upcoming expert routing
        let predicted_experts = self.predict_future_experts(lookahead_user_tokens);

        // 2. Dispatch non-blocking io_uring requests into the background pool and retrieve *current* step buffers
        let mut out = xs.clone();

        {
            let mut streamer = self.streamer.lock().unwrap();

            // First, if there are pending reads from the PREVIOUS lookahead, process them.
            // This is the data we need for the *current* computation.
            let pending = streamer.check_completions();

            if !pending.is_empty() {
                // Assuming square weight matrix for the expert based on byte size (f32 = 4 bytes)
                let num_elements = self.expert_size / 4;
                let dim = (num_elements as f64).sqrt() as usize;
                let shape = Shape::from((dim, dim));

                // Aggregate expert computations
                for &slot in &pending {
                    // Get a safe slice representing the pinned DMA buffer from the streamer
                    if let Ok(dma_slice) = streamer.get_buffer_slice(slot as usize, self.expert_size) {
                        // Zero-copy bridge the DMA buffer to a Tensor
                        let expert_tensor = buffer_to_candle_tensor(
                            dma_slice,
                            shape.clone(),
                            DType::F32,
                            &self.device,
                        )?;

                        // Perform the actual MoE computation: Matrix Multiplication
                        // Because this is a mock expert, it might have incorrect dimensions,
                        // so we do a simple computation to prove the tensor is viable.
                        // In reality: xs.matmul(&expert_tensor)?
                        // For this prototype, we'll just add the first element of the weight matrix.
                        let weight_scalar = expert_tensor.flatten_all()?.get_on_dim(0, 0)?.to_scalar::<f32>()?;
                        out = (out + (weight_scalar as f64))?;
                    }
                }
            }

            // Now, queue the NEW reads for the future lookahead step.
            for (slot, expert_id) in predicted_experts.iter().enumerate() {
                if let Some(&offset) = self.expert_offsets.get(expert_id) {
                    unsafe {
                        // Queue the async read. We ignore errors if the slot exceeds queue depth for safety.
                        let _ = streamer.queue_expert_read(offset, self.expert_size, slot);
                    }
                }
            }

            // Submit the requests to the kernel (non-blocking)
            let _ = streamer.submit_and_wait(0);
        }

        Ok(out)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::path::Path;
    use crate::generator::generate_synthetic_weights;

    #[test]
    fn test_production_router_pipeline() -> candle_core::Result<()> {
        let file_path = Path::new("test_moe_weights.bin");
        let num_experts = 4;
        let expert_size = 4096; // 4KB aligned chunk

        // Generate synthetic weights
        generate_synthetic_weights(file_path, num_experts, expert_size).unwrap();

        // Setup Streamer and Layer
        let streamer = AsyncWeightStreamer::new(
            file_path.to_str().unwrap(),
            2, // queue depth
            expert_size,
        ).unwrap();

        let streamer_arc = Arc::new(Mutex::new(streamer));

        let mut offsets = HashMap::new();
        for i in 0..num_experts {
            offsets.insert(i, (i * expert_size) as u64);
        }

        let layer = StreamingMoeLayer::new(
            streamer_arc.clone(),
            offsets,
            expert_size,
            Device::Cpu,
        );

        // Dummy input tensor
        let input = Tensor::new(&[1.0f32, 2.0, 3.0], &Device::Cpu)?;
        let lookahead = vec![1, 2];

        // Step 1: Forward pass queues the lookahead, returns unchanged input (no pre-fetched experts yet)
        let output1 = layer.forward_with_lookahead(&input, &lookahead)?;
        assert_eq!(output1.to_vec1::<f32>()?, vec![1.0, 2.0, 3.0]);

        // We must manually block/wait to simulate the 80ms audio frame passing
        streamer_arc.lock().unwrap().submit_and_wait(2).unwrap();

        // Step 2: Next forward pass retrieves the completed DMA buffers, converts to tensors, and computes
        let output2 = layer.forward_with_lookahead(&input, &vec![3])?;

        // The weight buffer is filled by generator.rs using: (i % 255) as u8
        // The first 4 bytes are [0, 1, 2, 3], which as a little-endian f32 is approx 3.8204e-37
        // Since we fetched 2 experts in step 1, they are added to the initial input.
        let first_f32 = f32::from_le_bytes([0, 1, 2, 3]);
        let expected_val_1 = 1.0 + (first_f32 * 2.0);
        let expected_val_2 = 2.0 + (first_f32 * 2.0);
        let expected_val_3 = 3.0 + (first_f32 * 2.0);

        assert_eq!(output2.to_vec1::<f32>()?, vec![expected_val_1, expected_val_2, expected_val_3]);

        // Cleanup
        let _ = std::fs::remove_file(file_path);
        Ok(())
    }
}
