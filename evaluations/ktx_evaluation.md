# Kaelio/ktx Evaluation: Project Inclusion vs. Feature Augmentation

This report evaluates the architecture, footprint, and integration viability of **Kaelio/ktx** compared to our current Python-based real-time streaming agent platform (`pipecatapp`). It analyzes whether we should fully include the project or instead update/augment our existing tools.

---

## 1. Overview of Kaelio/ktx

`ktx` is designed as a **self-improving context layer for data agents**. Its core promise is to teach AI agents how to query analytical databases accurately by maintaining approved metric definitions, database schemas, and business knowledge (wikis/Notion) in a unified, searchable surface.

### How it Works
* **Ingestion:** `ktx` crawls SQL warehouses, samples tables, captures metadata, infers joinable columns (resolving fan/chasm traps), and ingests business documentation (Markdown, Notion) into a unified local wiki and semantic-layer YAML.
* **Serving:** At runtime, agents query `ktx` via a CLI or an Model Context Protocol (MCP) server. `ktx` performs combined full-text and semantic search across the wiki and semantic-layer, translating declarative metric requests into read-only SQL executed against the database.

---

## 2. Technical Footprint & "Heaviness" Analysis

`ktx` is a modern, high-capability project, but it carries a **substantial architectural footprint**:

### A. Development Footprint (Monorepo Complexity)
`ktx` is structured as a multi-language monorepo using a hybrid packaging setup:
* **TypeScript Frontend/CLI (`packages/cli`):** The primary user-facing CLI and MCP server built in TypeScript, managed via `pnpm`.
* **Python Backend Engine (`python/ktx-sl` and `python/ktx-daemon`):** Handles semantic-layer query planning, join graph resolution, and portable compute, managed via `uv`.
* **Impact on Our System:** To include `ktx` as a full project, we would need to maintain `pnpm`, `tsconfig.json`, and dual node/python runtime environments within our build system. This introduces significant package build and compiler overhead to our lightweight Python virtualenv.

### B. Runtime Footprint & Orchestration
* **Daemon Dependency:** `ktx` runs a background local compute daemon (`ktx-daemon`) and an on-demand MCP server (`ktx mcp start`).
* **State Management:** It stores local configuration, raw connection artifacts, reports, and secrets under `.ktx/`, `semantic-layer/`, and `wiki/` directories.
* **Impact on Our System:** Running `ktx` in our Nomad/Consul cluster would require packaging a new dual-runtime Docker container, managing secrets/credentials securely across nodes, and orchestrating yet another long-running daemon task with persistent host volumes.

### C. Connection Friction (Target Audience Alignment)
* `ktx` is heavily optimized for large-scale data stacks: PostgreSQL, Snowflake, BigQuery, ClickHouse, and integrations with dbt, Looker, and MetricFlow.
* **Overkill for Small/Embedded DBs:** If our agent workflows do not involve a heavy enterprise SQL warehouse or dbt modeling layer, the complex join graph generators, chasm/fan trap resolvers, and multi-table compilation pipelines of `ktx` remain entirely unused, while still carrying their build and execution costs.

---

## 3. Comparison of Integration Options

| Evaluation Dimension | Option A: Full Project Inclusion | Option B: Feature Augmentation (Recommended) |
| --- | --- | --- |
| **Architectural Complexity** | High (hybrid `pnpm` monorepo + TypeScript CLI + Python daemon) | Very Low (pure Python, zero-dependency helper tool) |
| **System Orchestration** | High (new Nomad service, secret-sharing, daemon processes) | None (native tool execution within existing `pipecatapp` runner) |
| **Runtime Footprint** | Moderate-to-high memory/disk usage for daemon and local state | Negligible memory footprint, executed on-demand |
| **Integration Friction** | High (demands complex warehouse database / dbt environment setup) | Extremely low (runs locally, directly inspects workspace databases) |
| **Customizability** | Low (locked into `ktx`'s specific CLI and YAML structure) | High (fully controlled database exploration tailored to our agents) |

### Option A: Project Inclusion
We would pull the `ktx` source into our workspace or deploy its published NPM/PyPI packages, scheduling `ktx mcp start` inside Nomad.
* *When to use:* If we are actively deploying a massive distributed SQL analytics platform (e.g., ClickHouse/Snowflake cluster with dbt modeling) and want agents to run highly complex multi-table analytical reports natively.

### Option B: Feature Augmentation (Our Choice)
Instead of importing a heavy hybrid monorepo, we **extract `ktx`'s core architectural insight**: data agents perform substantially better when provided with an automated "schema mapper" or "database database context" to explore active databases, extract metadata, count records, sample tables, and deduce relationship heuristics.
* We can implement a pure-Python, zero-dependency **`SchemaMapperTool`** directly inside `pipecatapp/tools/`.
* *When to use:* Best for keeping our cluster lightweight, highly portable, and incredibly fast, while giving our agents the exact context-awareness they need to safely query and interact with databases (like local SQLite instances).

---

## 4. The Path Forward: Augmenting Our Toolset

By choosing **Option B**, we will design and implement a native Python-based **`SchemaMapperTool`** (`pipecatapp/tools/schema_mapper_tool.py`) with the following lightweight features:

1. **Workspace Scanning:** Automatically find any active `.sqlite` or `.db` databases within the project directories.
2. **Schema Introspection:** Read the SQLite catalog to extract full table lists, column definitions (name, type, nullability), and default values.
3. **Smart Heuristics (Relationship Detection):** Analyze column names and primary keys to auto-detect potential foreign-key join relationships (e.g., if `orders.user_id` matches `users.id`, flag a potential join path).
4. **Read-Only Data Sampling:** Safely fetch a small sample (e.g., 3-5 rows) of each table so the LLM gets an accurate picture of actual data formats, column names, and values.
5. **Clean Markdown Representation:** Compile this entire schema graph into a highly readable, compact Markdown database context dictionary. This matches the exact style that LLMs excel at parsing and using for generating correct queries.

This approach keeps our pipeline highly secure, maintains zero external dependencies, avoids the complex `pnpm/uv` monorepo overhead, and delivers 90% of the practical value of a context layer with 1% of the technical debt.
