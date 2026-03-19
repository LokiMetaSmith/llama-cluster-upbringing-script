1. **Create Skill Library Service (Memory-based)**
   - Utilize the existing SQLite-backed memory schema (`PMMMemoryClient` and `MemoryStore`) to persist skills.
   - We will add functions to manage skills via `PMMMemoryClient` (which talks to the `MemoryStore`).
   - Actually, since `MemoryStore` is for text embeddings, maybe we can just create a new table for `skills` in the `long_term_memory.sqlite` database and update `PMMMemoryClient` + `memory_service.py` to handle skills, OR just store it locally for the agent. Wait, looking at the Todo: "Create a simple file-based or database-backed Skill Library service (or use the existing Memory service)". We can just add a simple SQLite or file-based `SkillLibrary` in a new file `pipecatapp/skill_library.py`.

2. **Add `save_skill` tool**
   - Create `pipecatapp/tools/save_skill_tool.py`.
   - Takes `skill_name`, `description`, and `code_or_steps` (the actual skill content).
   - Saves it to the skill library.

3. **Add `search_skills` tool**
   - Create `pipecatapp/tools/search_skills_tool.py`.
   - Takes a query string and searches the skill library for relevant skills.

4. **Update `AgentFactory`**
   - Add `save_skill` and `search_skills` to `create_tools()` in `pipecatapp/agent_factory.py`.

5. **Update `TechnicianAgent` reflection phase**
   - Modify `phase_3_reflect` in `pipecatapp/technician_agent.py` to optionally suggest saving a skill if the task was novel/successful.

6. **Pre-commit Checks & Submission**
   - Run tests, check syntax, etc.
