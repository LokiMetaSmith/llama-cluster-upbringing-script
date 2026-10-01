use std::process::{Command, Stdio, Child};
use std::time::Duration;
use std::net::TcpStream;
use std::io::{Read, Write};
use ring::hmac;

#[test]
fn test_auth_proxy_flow() {
    let proxy_port_public = 8082;
    let proxy_port_auth = 9082;
    let target_port = 8002;

    // Start dummy server
    let server = Command::new("python3")
        .arg("-c")
        .arg(&format!("import socket; s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); s.bind(('127.0.0.1', {})); s.listen(1); conn, addr = s.accept(); conn.send(b'HELLO FROM TARGET'); conn.close()", target_port))
        .spawn()
        .expect("failed to start target server");

    // Wait for python server to boot
    std::thread::sleep(Duration::from_secs(1));

    // Compile first to ensure proxy starts quickly
    let _ = Command::new("cargo")
        .arg("build")
        .status()
        .expect("failed to build");

    // Start proxy
    let proxy = Command::new("cargo")
        .arg("run")
        .arg("--")
        .arg("--public-port")
        .arg(&proxy_port_public.to_string())
        .arg("--auth-port")
        .arg(&proxy_port_auth.to_string())
        .arg("--target")
        .arg(&format!("127.0.0.1:{}", target_port))
        .arg("--secret")
        .arg("my_secret_key")
        .current_dir(std::env::current_dir().unwrap())
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .spawn()
        .expect("failed to start proxy");

    // Wait for proxy to boot
    std::thread::sleep(Duration::from_secs(5));

    struct Cleanup {
        p1: Child,
        p2: Child,
    }

    impl Drop for Cleanup {
        fn drop(&mut self) {
            let _ = self.p1.kill();
            let _ = self.p2.kill();
        }
    }

    let _cleanup = Cleanup { p1: server, p2: proxy };

    // 1. Unauthenticated attempt -> should fail/be dropped immediately
    let mut public_conn = TcpStream::connect(format!("127.0.0.1:{}", proxy_port_public)).expect("Failed to connect to public port");
    let mut buf = [0u8; 128];
    let res = public_conn.read(&mut buf);
    assert!(res.is_err() || res.unwrap() == 0, "Expected connection to be rejected");

    // 2. Auth attempt
    let mut auth_conn = TcpStream::connect(format!("127.0.0.1:{}", proxy_port_auth)).expect("Failed to connect to auth port");
    let mut buf = [0u8; 128];
    let n = auth_conn.read(&mut buf).expect("Failed to read challenge");
    let challenge = String::from_utf8_lossy(&buf[..n]);
    assert!(challenge.starts_with("CHALLENGE "));

    let nonce_hex = challenge.trim_start_matches("CHALLENGE ").trim();

    let secret_key = hmac::Key::new(hmac::HMAC_SHA256, b"my_secret_key");
    let tag = hmac::sign(&secret_key, nonce_hex.as_bytes());
    let tag_hex = hex::encode(tag.as_ref());

    auth_conn.write_all(format!("{}\n", tag_hex).as_bytes()).expect("Failed to write auth response");

    let n = auth_conn.read(&mut buf).expect("Failed to read auth ok");
    let ok = String::from_utf8_lossy(&buf[..n]);
    assert_eq!(ok.trim(), "OK");

    // 3. Authenticated attempt -> should succeed
    std::thread::sleep(Duration::from_millis(500)); // give state a moment
    let mut public_conn2 = TcpStream::connect(format!("127.0.0.1:{}", proxy_port_public)).expect("Failed to connect to public port again");
    let n = public_conn2.read(&mut buf).expect("Failed to read from target");
    let msg = String::from_utf8_lossy(&buf[..n]);
    assert_eq!(msg, "HELLO FROM TARGET");
}
