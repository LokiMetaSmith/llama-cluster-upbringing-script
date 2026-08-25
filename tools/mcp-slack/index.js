const http = require('http');
const https = require('https');
const url = require('url');

const PORT = process.env.MCP_SLACK_PORT || 8081;
const SLACK_WEBHOOK_URL = process.env.SLACK_WEBHOOK_URL || null;

async function sendSlackNotification(channel, message, level = "info") {
  if (!SLACK_WEBHOOK_URL) {
    console.log(`[MOCK SLACK] Channel: ${channel} | Level: ${level} | Message: ${message}`);
    return { success: true, mode: "mock", channel, message, level };
  }

  const payload = JSON.stringify({
    channel: channel,
    text: `[${level.toUpperCase()}] ${message}`
  });

  const parsedUrl = url.parse(SLACK_WEBHOOK_URL);
  const options = {
    hostname: parsedUrl.hostname,
    port: parsedUrl.port || 443,
    path: parsedUrl.path,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(payload)
    }
  };

  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => resolve({ success: res.statusCode === 200, mode: "live", status: res.statusCode, data }));
    });
    req.on('error', (e) => reject({ success: false, error: e.message }));
    req.write(payload);
    req.end();
  });
}

const server = http.createServer(async (req, res) => {
  if (req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk.toString());
    req.on('end', async () => {
      try {
        const data = JSON.parse(body || '{}');
        const action = data.action || 'send_message';
        const channel = data.channel || '#alerts';
        const message = data.message || 'Default cluster message';
        const level = data.level || 'info';

        if (action === 'send_message' || action === 'send_alert') {
          const result = await sendSlackNotification(channel, message, level);
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ status: 'ok', result }));
        } else {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: `Unknown action: ${action}` }));
        }
      } catch (err) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: err.message }));
      }
    });
  } else if (req.method === 'GET' && req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'healthy', service: 'mcp-slack' }));
  } else {
    res.writeHead(405, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Method not allowed' }));
  }
});

if (require.main === module) {
  server.listen(PORT, () => {
    console.log(`MCP Slack Server listening on port ${PORT}`);
  });
}

module.exports = { server, sendSlackNotification };
