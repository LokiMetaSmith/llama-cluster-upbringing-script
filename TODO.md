# TODO

- [x] State Export/Import: Allowing tasks to be saved and resumed.
- [x] Interactive approval of actions: For enhanced safety and user control.
- [x] Enhanced Debugging Modes: For better transparency.
- [x] WebBrowserTool: For browsing the web.
- [ ] Web UI: Replace the placeholder ASCII art with a more expressive cartoon robot face.

All major features are implemented. Please see the README.md for a complete list of features and usage instructions.

## For Future Review

- [ ] Review `llama.cpp` optimization guide for server performance tuning: <https://blog.steelph0enix.dev/posts/llama-cpp-guide/#llamacpp-server-settings>
- [ ] Investigate re-enabling Consul Connect (`sidecar_service`) for Nomad jobs once the base cluster is stable. This was disabled to resolve initial scheduling failures in the bootstrap environment.
- [ ] Consider adding a pre-flight check to detect a read-only filesystem. Investigate if a safe, non-destructive diagnostic can be run automatically. (Note: Direct filesystem repair tools like e2fsck are likely too dangerous to automate).
- [ ] Consolidate all AI models (LLM, Whisper, Vision) into a single, unified directory to avoid duplication.
- [ ] Implement a graceful failover mechanism for LLM services, allowing them to fall back to a smaller model if the primary one fails to load.
- [ ] Add the remaining LiquidAI nano models from the collection: <https://huggingface.co/collections/LiquidAI/liquid-nanos-68b98d898414dd94d4d5f99a>
