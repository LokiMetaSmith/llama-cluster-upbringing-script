use clap::Parser;
use colibri_io_uring::generator::generate_synthetic_weights;
use colibri_io_uring::streamer::AsyncWeightStreamer;
use std::path::Path;
use std::time::Instant;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Number of experts to simulate
    #[arg(short, long, default_value_t = 64)]
    num_experts: usize,

    /// Size of each expert in bytes (default: 25MB to simulate INT3 7B MoE experts)
    #[arg(short, long, default_value_t = 25 * 1024 * 1024)]
    expert_size: usize,

    /// Queue depth for io_uring (batch size for speculative pre-fetching)
    #[arg(short, long, default_value_t = 4)]
    queue_depth: u32,

    /// Number of iterations to run the benchmark
    #[arg(short, long, default_value_t = 100)]
    iterations: usize,
}

fn main() {
    let args = Args::parse();
    let file_path = Path::new("synthetic_weights.bin");

    // 1. Generate Synthetic Weights
    if !file_path.exists() {
        println!("Generating synthetic weights file: {} experts, {} bytes each...", args.num_experts, args.expert_size);
        generate_synthetic_weights(file_path, args.num_experts, args.expert_size).unwrap();
        println!("Done generating.");
    } else {
        println!("Using existing synthetic weights file.");
    }

    // 2. Initialize io_uring streamer
    let mut streamer = AsyncWeightStreamer::new(
        file_path.to_str().unwrap(),
        args.queue_depth,
        args.expert_size,
    )
    .expect("Failed to initialize AsyncWeightStreamer. Does your filesystem support O_DIRECT?");

    println!("Starting benchmark ({} iterations, queue depth: {})", args.iterations, args.queue_depth);

    let start_time = Instant::now();
    let mut total_bytes_read = 0;

    for _ in 0..args.iterations {
        // Simulate picking random experts to prefetch
        // In reality, this comes from the early-layer predictive router
        let mut selected_experts = Vec::new();
        for _ in 0..args.queue_depth {
            selected_experts.push(rand::random::<u64>() as usize % args.num_experts);
        }

        // Queue reads
        for (slot_idx, &expert_id) in selected_experts.iter().enumerate() {
            let offset = (expert_id * args.expert_size) as u64;
            unsafe {
                streamer.queue_expert_read(offset, args.expert_size, slot_idx).unwrap();
            }
        }

        // Submit and wait for all to complete
        streamer.submit_and_wait(args.queue_depth as usize).unwrap();

        let completions = streamer.check_completions();
        assert_eq!(completions.len(), args.queue_depth as usize);

        total_bytes_read += (args.queue_depth as usize * args.expert_size) as u64;
    }

    let duration = start_time.elapsed();
    let duration_secs = duration.as_secs_f64();
    let throughput_mb = (total_bytes_read as f64 / 1_048_576.0) / duration_secs;
    let throughput_gb = (total_bytes_read as f64 / 1_073_741_824.0) / duration_secs;

    println!("--------------------------------------------------");
    println!("Benchmark Complete");
    println!("Total Bytes Read: {} ({} MB)", total_bytes_read, total_bytes_read / 1_048_576);
    println!("Time Elapsed:     {:.3} seconds", duration_secs);
    println!("Throughput:       {:.2} MB/s ({:.2} GB/s)", throughput_mb, throughput_gb);
    println!("Avg Latency/Iter: {:.2} ms (loading {} experts)", (duration_secs * 1000.0) / args.iterations as f64, args.queue_depth);

    // Clean up
    let _ = std::fs::remove_file(file_path);
}
