## 2026-01-21 - [Semantic Navigation Links]
**Learning:** Buttons used for navigation (opening new tabs) are semantically incorrect and can confuse screen readers. Using `<a>` tags with `role="button"` or simply styled as buttons is preferred for navigation.
**Action:** Replaced `button` elements with `<a>` tags for "Cluster Viz" and "Cluster VR" in `index.html`. Added `rel="noopener noreferrer"` for security and `aria-label` for accessibility.
