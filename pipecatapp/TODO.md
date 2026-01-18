# VR Mission Control TODO

- [x] **Spatial Audio Node**: Implement a LiteGraph node that plays audio from a 3D location corresponding to the agent.
  - Requires backend metadata about which "agent" is speaking.
  - Requires frontend `a-sound` entity management.

- [x] **Blackout Mode**: Implement a "Focus Mode" voice command.
  - When triggered ("Computer, focus"), dim all A-Frame entities except the one currently looked at.
  - Use `raycaster` intersection to determine the active panel.

- [ ] **VR Keyboard/Input**: Add a virtual keyboard for text input when voice is not suitable.
  - Look into `aframe-keyboard` or similar components.

- [ ] **Performance Optimization**:
  - The LiteGraph canvas (1024x1024) texture upload can be heavy. Consider lowering resolution or updating less frequently if FPS drops.

- [ ] **Multi-Room Navigation**: Create a node graph to switch between different VR "rooms" or contexts.
