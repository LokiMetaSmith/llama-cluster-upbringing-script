/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import WebSocket from 'ws';

const server = new McpServer({
  name: 'pipecat-agent-server',
  version: '1.0.0',
});

let ws: WebSocket | null = null;
let connectionPromise: Promise<WebSocket> | null = null;

function getWebSocket(): Promise<WebSocket> {
  if (ws && ws.readyState === WebSocket.OPEN) {
    return Promise.resolve(ws);
  }

  if (connectionPromise) {
    return connectionPromise;
  }

  connectionPromise = new Promise((resolve, reject) => {
    const socket = new WebSocket('ws://localhost:8000/ws');

    socket.on('open', () => {
      ws = socket;
      connectionPromise = null;
      resolve(socket);
    });

    socket.on('error', (error) => {
      if (connectionPromise) {
        connectionPromise = null;
        reject(error);
      }
    });

    socket.on('close', () => {
      ws = null;
    });
  });

  return connectionPromise;
}

server.registerTool(
  'send_message',
  {
    description: 'Sends a message to the pipecat agent.',
    inputSchema: z.object({
      message: z.string(),
    }).shape,
  },
  async ({ message }) => {
    const socket = await getWebSocket();

    // We don't wait for a response here as per original implementation,
    // but we ensure the socket is open before sending.
    socket.send(JSON.stringify({ type: 'user_message', data: message }));

    return {
      content: [
        {
          type: 'text',
          text: `Message "${message}" sent to the pipecat agent.`,
        },
      ],
    };
  },
);

const transport = new StdioServerTransport();
await server.connect(transport);
