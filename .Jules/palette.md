## 2025-02-18 - Missing Submit Button on Chat Input
**Learning:** Users often rely on a visible submit button rather than implicit "Enter" key submission. Screen readers and mobile users particularly benefit from an explicit action button.
**Action:** Always include a "Send" or "Submit" button for input fields, even if Enter key support exists. Ensure it has an accessible label.
## 2026-01-09 - Accessible Sidebar Tabs
**Learning:** Using `<div>` elements for interactive tabs excludes keyboard users and screen readers. Replacing them with `<button>` elements inside a container with `role="tablist"` immediately improves accessibility by providing native focus handling and semantic meaning.
**Action:** Always use semantic `<button>` or `<a>` tags for clickable UI elements, and ensure custom tab implementations follow the WAI-ARIA Authoring Practices for Tabs (using `role="tab"`, `aria-selected`, and `aria-controls`).
## 2024-03-22 - Keyboard Accessible History List
**Learning:** `onclick` on `<li>` elements is a common pattern that completely excludes keyboard users. Adding `tabindex="0"`, `role="button"`, and a `keydown` handler is a standard remediation pattern that is robust and easy to implement.
**Action:** Always check `onclick` elements for keyboard accessibility. If they are not `<button>` or `<a>`, they likely need remediation. Use `event.key === 'Enter' || event.key === ' '` to trigger the click logic.
