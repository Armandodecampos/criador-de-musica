from playwright.sync_api import sync_playwright
import os

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Using the file path directly
        path = os.path.abspath("index.htm")
        page.goto(f"file://{path}")

        # Take a screenshot of the initial state
        page.screenshot(path="verification/final_state.png")

        # Select a preset
        page.click("text=Techno Rave")
        page.wait_for_timeout(500)
        page.screenshot(path="verification/final_preset.png")

        browser.close()

if __name__ == "__main__":
    verify()
