from playwright.sync_api import sync_playwright, Page, expect
import time

def verify_workflow_save(page: Page):
    # Mock APIs
    page.route("**/api/workflows/definition/default_agent_loop.yaml", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"nodes": []}'
    ))
    page.route("**/api/workflows/history?limit=20", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='[]'
    ))
    page.route("**/api/workflows/active", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{}'
    ))
    page.route("**/api/workflows/save", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"message": "Workflow saved successfully."}'
    ))

    # Go to workflow page
    # Note: workflow.html is in static/workflow.html relative to pipecatapp root
    page.goto("http://localhost:8000/static/workflow.html")

    # Wait for editor to init
    time.sleep(1)

    # Click Save
    save_btn = page.get_by_role("button", name="Save / Deploy")
    save_btn.click()

    # Verify status text
    status_text = page.locator("#status-text")
    expect(status_text).to_have_text("Workflow saved successfully.")
    # Class check might need strict match or partial. Logic in code: statusText.classList.add('status-success');
    # But we cleared it first: statusText.className = '';
    # So it should be just 'status-success'.
    expect(status_text).to_have_class("status-success")

    # Take screenshot of success state
    page.screenshot(path="verification/save_success.png")
    print("Success screenshot taken.")

    # Wait for revert (3s timeout in code)
    # Use expect with timeout to avoid sleep
    expect(status_text).to_have_text("Ready", timeout=4000)
    expect(status_text).to_have_class("status-ready")

    print("Revert verified.")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_workflow_save(page)
        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="verification/failure.png")
            raise
        finally:
            browser.close()
