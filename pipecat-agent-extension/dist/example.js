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
server.registerTool('send_message', {
    description: 'Sends a message to the pipecat agent.',
    inputSchema: z.object({
        message: z.string(),
    }).shape,
}, async ({ message }) => {
    const ws = new WebSocket('ws://localhost:8000/ws');
    await new Promise((resolve, reject) => {
        ws.on('open', () => {
            ws.send(JSON.stringify({ type: 'user_message', data: message }));
            ws.close();
            resolve(void 0);
        });
        ws.on('error', (error) => {
            reject(error);
        });
    });
    return {
        content: [
            {
                type: 'text',
                text: `Message "${message}" sent to the pipecat agent.`,
            },
        ],
    };
});
const transport = new StdioServerTransport();
await server.connect(transport);
