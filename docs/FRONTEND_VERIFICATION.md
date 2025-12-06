# Frontend Verification Instructions with Playwright

After you make any frontend change, you **must** attempt to visually verify it by following this workflow. The goal is to start the application, write a temporary Playwright script to demonstrate your change, take a screenshot, and confirm it looks correct before finalizing.

## Step-by-Step Verification Workflow

Follow these steps in order to test and verify your frontend changes.

### 1. Start the Application 🚀

- Before you can verify your changes, you must **start the local development server**. Or, if you made static changes that do not require a build, you may be able to navigate to them directly using `filepath://` in your script.
  - Look for a command in the `package.json` or project documentation, such as `npm run dev`, `npm start`, or `yarn dev`.
- **Execute this command**. You may need to run it as a background process so you can continue to issue other commands.

### 2. Create a Verification Script ✍️ and Screenshot 📸

- First, create a temporary directory for your work: `mkdir -p /home/jules/verification`.
- Write a new Playwright script that navigates to the relevant page, makes relevant selections, and demonstrates your change. Be sure to write a headless playwright script.
- **Crucially, your script must take a screenshot** to demonstrate at least some of your changes.
- Save the script as something like `/home/jules/verification/verify_feature_x.py`.
- Save the screenshot as something like `/home/jules/verification/verification.png`.
- You can run your script and generate the screenshot with the command: `python /home/jules/verification/verify_feature_x.py`.
- The script should run successfully, otherwise debug it.

### 3. Visually Inspect Your Work 👀

- Use the `read_image_file` tool to load the screenshot you just created (e.g., `read_image_file(filepath='/home/jules/verification/verification.png')`).
- Analyze the image in your context. Does the feature look exactly as intended? Is the styling correct? Is the text right?
- If it does **not** look correct, return to your implementation, make code changes, and repeat this workflow from Step 2.

### 4. Confirm Completion ✅

- Once you have visually confirmed that the screenshot looks perfect, call the `frontend_verification_complete()` function, which I have **added to your Standard Tools**. Documentation is below:
  - `frontend_verification_complete(screenshot_path: str) -> None`: Marks the frontend verification as complete, with a path to the screenshot.
- Pass the **path to the final, correct screenshot** as the argument. This signals that your work is done and the result is ready for review.
- Example: `frontend_verification_complete(screenshot_path='/home/jules/verification/verification.png')`
- If you are unable to complete the verification workflow, you can let the user know that you weren't able to verify the frontend screenshots, and then continue with the plan or submission.

## Debugging Failed Scripts 🐛

If your Playwright script fails to run, **do not guess**. Systematically debug the issue by analyzing the error output.

| Error Type | Likely Cause & Solution |
| :--- | :--- |
| **Timeout / Selector Not Found** | The element you're trying to find doesn't exist or hasn't appeared yet. **Solution:** Double-check your locator. Is it correct? Use `page.get_by_role()` or another user-facing locator. View the page source to find the right selector. |
| **Assertion Failed** | The element was found, but it's in the wrong state (e.g., wrong text, not visible). **Solution:** Your web application code is likely incorrect. The element exists, but your change didn't produce the right result. Fix your application code. |
| **Navigation or Network Error** | The script couldn't load the page. **Solution:** Ensure the dev server is running (Step 1) and the URL in your `page.goto()` call is correct. |

If you are having trouble, you can visit https://playwright.dev/python/docs/library and browse the website to learn more.

## Playwright Best Practices

-   **Use Web-First Assertions:** Always use `expect(locator)` with matchers like `.to_be_visible()` or `.to_have_text()`. This makes Playwright automatically wait for the condition to be true, preventing flaky tests.
-   **Prefer User-Facing Locators:** Select elements like a user would. Use this priority:
    1.  `page.get_by_role()` (e.g., `button`, `heading`)
    2.  `page.get_by_text()`
    3.  `page.get_by_label()`
-   **Avoid Brittle Selectors:** Do not use auto-generated class names or long, complex CSS paths (e.g., `div > div > div:nth-child(3)`). They break easily.

## Important: Playwright Verification Scripts vs. Repository Tests

It's crucial to understand the difference between the two types of scripts you might write.

-   **Verification Scripts (Temporary):** This is what you'll create for **this workflow**. They live in `/home/jules/verification`, are often simple, and their only goal is to help you take a screenshot to verify your work and show the user what you built or fixed. **They are disposable.**
-   **Repository Tests (Permanent):** You write these as part of your typical code changes you have already made by now. You should follow typical unit testing patterns you observe in the repository. You may write playwright tests in the repository if the user asks you to, or if exsiting tests in the repository indicate you should.

## Example Playwright Script

Remember that you are calling this function using `python` directly, so you must have some code that runs in the main body of the script.

```python
from playwright.sync_api import Page, expect, sync_playwright

def test_google_images_navigation(page: Page):
  """
  This test verifies that a user can navigate from the Google homepage
  to the Google Images page by clicking the 'Images' link.
  """
  # 1. Arrange: Go to the Google homepage.
  page.goto("https://www.google.com")

  # 2. Act: Find the "Images" link and click it.
  # We use get_by_role('link') because it's a robust, user-facing locator.
  images_link = page.get_by_role("link", name="Images")
  images_link.click()

  # 3. Assert: Confirm the navigation was successful.
  # We expect the page title to change to "Google Images".
  # This confirms the new page has loaded before we take the screenshot.
  expect(page).to_have_title("Google Images")

  # 4. Screenshot: Capture the final result for visual verification.
  page.screenshot(path="/home/jules/verification/google-images-page.png")

if __name__ == "__main__":
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    try:
      test_google_images_navigation(page)
    finally:
      browser.close()
```
