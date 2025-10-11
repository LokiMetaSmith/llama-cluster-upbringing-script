from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Navigate to the web UI
            page.goto("http://localhost:8000")

            # Wait for the robot art to be visible
            robot_art = page.locator("#robot-art")
            expect(robot_art).to_be_visible(timeout=10000)

            # 1. Capture initial idle state
            page.screenshot(path="jules-scratch/verification/01_idle.png")

            # Find the message input and send a message
            message_input = page.locator("#message-input")
            message_input.fill("Hello, this is a test.")
            message_input.press("Enter")

            # 2. Capture the "thinking" state
            # The thinking animation should start immediately after sending the message
            expect(robot_art).to_contain_text("(o.o?)", timeout=2000)
            page.screenshot(path="jules-scratch/verification/02_thinking.png")

            # Wait for the agent's response, which will trigger the idle animation
            # This is a bit tricky as we don't know how long the agent will take
            # We will wait for the idle frame to appear
            expect(robot_art).to_contain_text("(^_^)", timeout=30000)

            # 3. Capture the final idle state
            page.screenshot(path="jules-scratch/verification/03_idle_after_response.png")

            print("Successfully captured screenshots of the new animations.")

        except Exception as e:
            print(f"An error occurred: {e}")
            page.screenshot(path="jules-scratch/verification/error.png")

        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()