import os

def take_screenshot(driver, name):
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    filename = f"{name}.png"
    path = os.path.join(screenshots_dir, filename)

    success = driver.save_screenshot(path)
    if success:
        print(f"[📸 Screenshot saved]: {path}")
    else:
        print(f"[⚠️ Failed to capture screenshot]: {path}")

    return path
