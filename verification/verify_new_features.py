from playwright.sync_api import sync_playwright
import os

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        path = os.path.abspath("index.htm")
        page.goto(f"file://{path}")

        # Check if "Novo Projeto (Vazio)" exists
        empty_preset = page.get_by_text("Novo Projeto (Vazio)")
        if empty_preset.is_visible():
            print("Novo Projeto preset is visible")
        else:
            print("Novo Projeto preset is NOT visible")

        # Hover over a preset to see the delete button
        page.hover("text=Techno Rave")
        page.wait_for_timeout(500)
        page.screenshot(path="verification/hover_preset.png")

        # Click the delete button of "Techno Rave"
        # Since there are multiple delete buttons (one per preset), we need to find the one inside the Techno Rave container.
        # But for simplicity, let's just check if any button with text "×" is visible on hover.
        delete_btn = page.locator("button:has-text('×')").first
        if delete_btn.is_visible():
            print("Delete button is visible on hover")
        else:
            print("Delete button is NOT visible on hover")

        # Mock the confirm dialog to return true
        page.on("dialog", lambda dialog: dialog.accept())

        # Click delete on "Techno Rave"
        # We need to be more specific to hit the right X
        techno_rave_wrapper = page.locator("div.relative.group:has-text('Techno Rave')")
        techno_rave_wrapper.locator("button:has-text('×')").click()

        page.wait_for_timeout(500)

        # Check if "Techno Rave" is gone
        if page.get_by_text("Techno Rave").is_visible():
            print("Techno Rave is STILL visible (Delete failed)")
        else:
            print("Techno Rave is GONE (Delete successful)")

        page.screenshot(path="verification/after_delete.png")

        browser.close()

if __name__ == "__main__":
    verify()
