use std::fs::File;
use std::io::{BufWriter, Write};
use std::path::Path;

/// Generate a synthetic MoE weight file.
/// `num_experts` * `expert_size_bytes` determines the total file size.
/// Writes aligned blocks of pseudo-random data to simulate a serialized model.
pub fn generate_synthetic_weights(
    file_path: &Path,
    num_experts: usize,
    expert_size_bytes: usize,
) -> std::io::Result<()> {
    let file = File::create(file_path)?;
    let mut writer = BufWriter::with_capacity(1024 * 1024 * 4, file); // 4MB buffer

    let block_size = 4096; // Write in 4KB aligned blocks
    let mut dummy_block = vec![0u8; block_size];

    // Fill dummy block with some pattern to simulate weight bytes
    for (i, byte) in dummy_block.iter_mut().enumerate() {
        *byte = (i % 255) as u8;
    }

    for _ in 0..num_experts {
        let mut written_for_expert = 0;
        while written_for_expert < expert_size_bytes {
            let to_write = std::cmp::min(block_size, expert_size_bytes - written_for_expert);
            writer.write_all(&dummy_block[..to_write])?;
            written_for_expert += to_write;
        }
    }

    writer.flush()?;
    Ok(())
}
