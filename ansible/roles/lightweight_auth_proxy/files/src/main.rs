use clap::Parser;
use log::{error, info, warn};
use ring::hmac;
use std::collections::HashMap;
use std::net::SocketAddr;
use std::sync::Arc;
use std::time::{Duration, Instant};
use tokio::io::AsyncWriteExt;
use tokio::io::AsyncReadExt;
use tokio::net::{TcpListener, TcpStream};
use tokio::sync::Mutex;
use rand::{thread_rng, RngCore};

/// A lightweight auth proxy
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Port to listen on for authenticated traffic (splicing proxy)
    #[arg(short, long, default_value_t = 8080)]
    public_port: u16,

    /// Port to listen on for authentication requests
    #[arg(short, long, default_value_t = 9080)]
    auth_port: u16,

    /// Target host and port to forward traffic to after authentication
    #[arg(short, long, default_value = "127.0.0.1:8000")]
    target: String,

    /// Shared secret for HMAC authentication
    #[arg(short, long, env = "PROXY_SHARED_SECRET")]
    secret: String,

    /// Time to live for authenticated IPs (in seconds)
    #[arg(long, default_value_t = 30)]
    ttl: u64,
}

struct AppState {
    allowed_ips: HashMap<std::net::IpAddr, Instant>,
    ttl: Duration,
}

impl AppState {
    fn new(ttl: u64) -> Self {
        Self {
            allowed_ips: HashMap::new(),
            ttl: Duration::from_secs(ttl),
        }
    }

    fn allow_ip(&mut self, ip: std::net::IpAddr) {
        self.allowed_ips.insert(ip, Instant::now() + self.ttl);
    }

    fn is_allowed(&mut self, ip: std::net::IpAddr) -> bool {
        self.cleanup();
        if let Some(&expires) = self.allowed_ips.get(&ip) {
            if Instant::now() < expires {
                return true;
            }
        }
        false
    }

    fn cleanup(&mut self) {
        let now = Instant::now();
        self.allowed_ips.retain(|_, expires| *expires > now);
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    env_logger::init();
    let args = Args::parse();

    let state = Arc::new(Mutex::new(AppState::new(args.ttl)));
    let secret_key = Arc::new(hmac::Key::new(hmac::HMAC_SHA256, args.secret.as_bytes()));

    let auth_addr = format!("0.0.0.0:{}", args.auth_port);
    let public_addr = format!("0.0.0.0:{}", args.public_port);

    info!("Starting auth server on {}", auth_addr);
    info!("Starting public proxy on {}", public_addr);
    info!("Targeting internal service at {}", args.target);

    let auth_listener = TcpListener::bind(&auth_addr).await?;
    let public_listener = TcpListener::bind(&public_addr).await?;

    let state_clone = state.clone();
    let key_clone = secret_key.clone();

    // Auth server task
    tokio::spawn(async move {
        loop {
            match auth_listener.accept().await {
                Ok((stream, addr)) => {
                    let state = state_clone.clone();
                    let key = key_clone.clone();
                    tokio::spawn(async move {
                        if let Err(e) = handle_auth(stream, addr, state, key).await {
                            warn!("Auth failed for {}: {}", addr, e);
                        }
                    });
                }
                Err(e) => error!("Failed to accept auth connection: {}", e),
            }
        }
    });

    // Public proxy task
    let target = Arc::new(args.target);
    loop {
        match public_listener.accept().await {
            Ok((stream, addr)) => {
                let state = state.clone();
                let target = target.clone();
                tokio::spawn(async move {
                    if let Err(e) = handle_proxy(stream, addr, state, target).await {
                        warn!("Proxy connection failed for {}: {}", addr, e);
                    }
                });
            }
            Err(e) => error!("Failed to accept proxy connection: {}", e),
        }
    }
}

async fn handle_auth(
    mut stream: TcpStream,
    addr: SocketAddr,
    state: Arc<Mutex<AppState>>,
    secret_key: Arc<hmac::Key>,
) -> Result<(), Box<dyn std::error::Error>> {
    // Generate a 16-byte nonce
    let mut nonce = [0u8; 16];
    thread_rng().fill_bytes(&mut nonce);
    let nonce_hex = hex::encode(nonce);

    // Send the challenge
    stream.write_all(format!("CHALLENGE {}\n", nonce_hex).as_bytes()).await?;

    // Wait for the response (HMAC-SHA256 hex encoded)
    let mut buf = [0u8; 128];
    let n = tokio::time::timeout(Duration::from_secs(5), stream.read(&mut buf)).await??;
    if n == 0 {
        return Err("Connection closed by peer".into());
    }

    let response_str = String::from_utf8_lossy(&buf[..n]).trim().to_string();

    // Expected HMAC
    let expected_tag = hmac::sign(&secret_key, nonce_hex.as_bytes());
    let expected_hex = hex::encode(expected_tag.as_ref());

    if response_str == expected_hex {
        info!("Authentication successful for IP: {}", addr.ip());
        stream.write_all(b"OK\n").await?;
        let mut st = state.lock().await;
        st.allow_ip(addr.ip());
    } else {
        warn!("Authentication failed for IP: {}", addr.ip());
        stream.write_all(b"UNAUTHORIZED\n").await?;
    }

    Ok(())
}

async fn handle_proxy(
    mut client_stream: TcpStream,
    addr: SocketAddr,
    state: Arc<Mutex<AppState>>,
    target: Arc<String>,
) -> Result<(), Box<dyn std::error::Error>> {
    {
        let mut st = state.lock().await;
        if !st.is_allowed(addr.ip()) {
            warn!("Rejected unauthorized connection from {}", addr);
            return Err("Unauthorized IP".into());
        }
    }

    info!("Proxying authorized connection from {} to {}", addr, target);

    let mut target_stream = match TcpStream::connect(target.as_str()).await {
        Ok(s) => s,
        Err(e) => {
            error!("Failed to connect to target {}: {}", target, e);
            return Err(e.into());
        }
    };

    match tokio::io::copy_bidirectional(&mut client_stream, &mut target_stream).await {
        Ok(_) => {},
        Err(e) => {
            warn!("Connection error for {}: {}", addr, e);
        }
    }

    Ok(())
}
