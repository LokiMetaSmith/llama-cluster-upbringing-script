# MCP Migration Plan

This document outlines the strategy for migrating the current custom tool interface in `pipecatapp/tools/` to the open Model Context Protocol (MCP).

## Current State

The `pipecatapp/tools/` directory contains numerous custom tools (e.g., `shell_tool.py`, `file_editor_tool.py`, `rag_tool.py`, `mcp_tool.py`). These tools currently rely on tight coupling with internal services, such as:

*   Direct references to `TwinService` or `WorkflowRunner`.
*   Custom method definitions (`run`, `execute`) without standardized inputs or outputs.
*   In-process execution or custom `subprocess` abstractions.

## Migration Strategy

The migration to MCP will decouple tools from the core agentic framework, treating them as independent, standardized "Servers" and our agents as "Clients".

### Phase 1: Core MCP Infrastructure
1.  **Introduce MCP SDK:** Add the official MCP Python SDK (`mcp`) to the project dependencies.
2.  **Build a Universal MCP Client Wrapper:** Create a new tool adapter in `pipecatapp/tools/mcp_client_adapter.py`. This class will implement our existing internal `Tool` interface but proxy all calls via JSON-RPC to a target MCP Server using the standard MCP protocol.
3.  **Establish Server Runner:** Define a standard mechanism (e.g., a Nomad job template or a local process manager) to launch tools as independent MCP servers over stdio or HTTP/SSE.

### Phase 2: Refactoring Existing Tools
We will migrate tools iteratively. For each tool:
1.  Create a standalone server script (e.g., `servers/shell_server.py`) using the MCP `@server.tool()` decorators.
2.  Define explicit Pydantic schemas for the tool's inputs and outputs, replacing loose `**kwargs`.
3.  Remove internal `TwinService` dependencies. If a tool needs state, it must receive it via the MCP context or request it explicitly.
4.  Update the tool registry in `agent_factory.py` to map the old tool name to an instantiation of the new `MCPClientAdapter` pointing to the new server.

**Priority Tools for Migration:**
1.  `shell_tool.py` and `code_runner_tool.py` (High risk, immediate benefit from sandbox decoupling).
2.  `file_editor_tool.py` and `document_tool.py`.
3.  `rag_tool.py` (Requires establishing an MCP pattern for streaming large contexts or standardizing resource templates).

### Phase 3: Deprecation and Cleanup
1.  Once all active tools are migrated to MCP servers, remove the legacy tool implementations from `pipecatapp/tools/`.
2.  Refactor `ToolExecutorNode` in the workflow engine to natively support querying the MCP client for available tools, instead of relying on a hardcoded internal registry.
3.  Review and update agent prompts to utilize the standardized tool descriptions exposed by the MCP protocol.

## Security Considerations
*   MCP servers must run in sandboxed environments (e.g., Docker containers via Nomad).
*   Implement strict validation on all MCP JSON-RPC messages.
*   Avoid exposing sensitive MCP endpoints on public network interfaces; bind strictly to `localhost` or the internal tailscale overlay.
