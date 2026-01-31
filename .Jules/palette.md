## 2025-02-18 - Missing Submit Button on Chat Input
**Learning:** Users often rely on a visible submit button rather than implicit "Enter" key submission. Screen readers and mobile users particularly benefit from an explicit action button.
**Action:** Always include a "Send" or "Submit" button for input fields, even if Enter key support exists. Ensure it has an accessible label.
## 2026-01-09 - Accessible Sidebar Tabs
**Learning:** Using `<div>` elements for interactive tabs excludes keyboard users and screen readers. Replacing them with `<button>` elements inside a container with `role="tablist"` immediately improves accessibility by providing native focus handling and semantic meaning.
**Action:** Always use semantic `<button>` or `<a>` tags for clickable UI elements, and ensure custom tab implementations follow the WAI-ARIA Authoring Practices for Tabs (using `role="tab"`, `aria-selected`, and `aria-controls`).
## 2024-03-22 - Keyboard Accessible History List
**Learning:** `onclick` on `<li>` elements is a common pattern that completely excludes keyboard users. Adding `tabindex="0"`, `role="button"`, and a `keydown` handler is a standard remediation pattern that is robust and easy to implement.
**Action:** Always check `onclick` elements for keyboard accessibility. If they are not `<button>` or `<a>`, they likely need remediation. Use `event.key === 'Enter' || event.key === ' '` to trigger the click logic.
## 2026-01-14 - Accessible ASCII Art Animation
**Learning:** Animated ASCII art (like spinners or faces) creates a chaotic experience for screen readers, announcing every punctuation mark repeatedly.
**Action:** Use `role="img"` and `aria-label` to describe the *meaning* of the art/animation, and update the label only when the semantic state changes, not on every animation frame.
## 2025-11-26 - Save/Load State Interaction
**Learning:** Users can fail to provide required input for "Save/Load State" actions, leading to error messages in the terminal that might be missed.
**Action:** Prevent the error by disabling the action buttons until valid input is provided, using standard HTML `disabled` attribute and visual cues. This follows the "prevention over cure" UX principle.
## 2025-05-15 - Command History in Terminal Interfaces
**Learning:** In "Mission Control" or terminal-like web interfaces, users instinctively expect Up/Down arrow keys to cycle through command history. Missing this feature breaks the immersive "terminal" illusion and frustrates power users.
**Action:** Implement a history buffer and Up/Down key listeners for terminal-style inputs. Ensure standard text input behavior (cursor movement) is preserved when not navigating history.
## 2026-06-18 - Navigation Buttons vs Links
**Learning:** Using `<button onclick="...">` for navigation breaks middle-click (open in new tab), right-click, and search engine crawling. It confuses the semantic distinction between "doing" (button) and "going" (link).
**Action:** Use `<a>` tags styled as buttons for any action that primarily performs navigation (URL change). Ensure they have valid `href` attributes.
## 2026-01-21 - [Semantic Navigation Links]
**Learning:** Buttons used for navigation (opening new tabs) are semantically incorrect and can confuse screen readers. Using `<a>` tags with `role="button"` or simply styled as buttons is preferred for navigation.
**Action:** Replaced `button` elements with `<a>` tags for "Cluster Viz" and "Cluster VR" in `index.html`. Added `rel="noopener noreferrer"` for security and `aria-label` for accessibility.

## 2026-01-22 - Non-blocking Status Notifications
**Learning:** Native `alert()` calls block the UI and disrupt user flow. Replacing them with non-blocking status text provides feedback without interruption.
**Action:** Use a callback pattern (like `onStatusUpdate`) to allow logic components (like `WorkflowEditor`) to trigger UI updates in the parent view, maintaining separation of concerns.

## 2026-02-12 - Invisible Keyboard Shortcuts
**Learning:** Users cannot discover powerful keyboard shortcuts (like Ctrl+K to clear) if they are not exposed in the UI. Relying on documentation is insufficient for real-time usage.
**Action:** Expose shortcuts via tooltips (`title` attribute) and accessible labels (`aria-label`) on the relevant controls. This provides "just-in-time" learning for users.

## 2026-02-14 - Visual Hierarchy in Action Prompts
**Learning:** In high-contrast terminal interfaces, generic grey buttons for critical binary choices (Approve/Deny) lack "visual affordance" and can lead to hesitation or errors. Color-coding and semantic labeling significantly reduce cognitive load.
**Action:** Use standard semantic colors (Green/Red) and explicit `aria-label`s for critical decision buttons to provide instant visual and assistive feedback on the action's consequence.

## 2026-02-16 - Accessible Drag-and-Drop Alternatives
**Learning:** Drag-and-drop interfaces for adding items (like nodes in a graph editor) are inherently inaccessible to keyboard users. Relying solely on this interaction pattern excludes a significant user group.
**Action:** Implement keyboard-accessible alternatives (e.g., Enter key to "add" the item to a default location) and ensure the draggable source elements have `tabindex="0"`, `role="button"`, and appropriate ARIA labels.

## 2026-02-18 - Search Empty States
**Learning:** When search results (like filtering a node library) are empty, displaying nothing can look like a bug. An explicit "No results found" message provides confirmation that the system is working and the search just yielded no matches.
**Action:** Always check for empty results in filter/search functions and display a friendly, styled empty state message (e.g., "No nodes found matching 'xyz'").
