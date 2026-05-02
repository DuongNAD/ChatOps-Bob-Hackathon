import pyautogui
import pygetwindow as gw
import time
import sys

def run_diagnostics():
    print("=== RPA DIAGNOSTICS TEST MODE ===")
    print("You have 3 seconds to bring VS Code to the main screen...")
    time.sleep(3)

    # 1. Find VS Code window
    vscode_window = None
    for w in gw.getAllWindows():
        if 'Visual Studio Code' in w.title or 'IBM Bob' in w.title:
            vscode_window = w
            break

    if not vscode_window:
        print("❌ VS Code window not found!")
        sys.exit(1)

    print(f"\n✅ Window found: {vscode_window.title}")
    print(f"📍 Coordinates: left={vscode_window.left}, top={vscode_window.top}, width={vscode_window.width}, height={vscode_window.height}")

    try:
        vscode_window.activate()
        time.sleep(1)
    except:
        pass

    # 2. Test Check Header (Do we need Ctrl+Alt+B?)
    header_x = vscode_window.left + int(vscode_window.width * 0.90)
    header_y = vscode_window.top + int(vscode_window.height * 0.035)

    print(f"\n🔍 Step 1: Check Bob Panel status")
    print(f"   Moving mouse to Header position: ({header_x}, {header_y})")
    pyautogui.moveTo(header_x, header_y, duration=1.0)
    time.sleep(0.5)

    try:
        pixel = pyautogui.pixel(header_x, header_y)
        r, g, b = pixel
        print(f"   Color code at Header: RGB({r}, {g}, {b})")

        if r > 150 and g > 150 and b > 150:
            print("   ✅ Conclusion: Panel is OPEN (Bright pixel -> White header text)")
            print("   👉 Bot WILL NOT press Ctrl+Alt+B")
        else:
            print("   ❌ Conclusion: Panel is CLOSED (Dark pixel)")
            print("   👉 Bot WILL press Ctrl+Alt+B to open panel")
    except Exception as e:
        print(f"   ⚠️ Error reading pixel: {e}")

    # 3. Test Click Input
    input_x = vscode_window.left + int(vscode_window.width * 0.75)
    input_y = vscode_window.top + int(vscode_window.height * 0.90)

    print(f"\n🎯 Step 2: Check Chat Input position")
    print(f"   Moving mouse to Input: ({input_x}, {input_y})")
    pyautogui.moveTo(input_x, input_y, duration=1.0)
    time.sleep(0.5)
    print("   👉 Bot will CLICK and paste 'Hello world' here.")
    pyautogui.click(input_x, input_y)
    time.sleep(0.5)
    import pyperclip
    pyperclip.copy("Hello world")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)

    # 4. Test Scan Run Button
    print("\n🔎 Step 3: Scanning for Run button...")
    run_button_found = False
    run_x, run_y = 0, 0

    # Scan limits: Width 72% -> 85%, Height 50% -> 85%
    start_x = vscode_window.left + int(vscode_window.width * 0.72)
    end_x = vscode_window.left + int(vscode_window.width * 0.85)
    start_y = vscode_window.top + int(vscode_window.height * 0.50)
    end_y = vscode_window.top + int(vscode_window.height * 0.85)

    print(f"   Scan area: X({start_x} -> {end_x}), Y({start_y} -> {end_y})")

    for y in range(start_y, end_y, 10):
        for x in range(start_x, end_x, 10):
            try:
                r, g, b = pyautogui.pixel(x, y)
                # CHECK 1: Run button is a thick blue block (~30px).
                try:
                    r2, g2, b2 = pyautogui.pixel(x, y + 10)
                    if r2 < 50 and 80 < g2 < 180 and b2 > 160:
                        # CHECK 2: Run button is a SMALL button.
                        # "Start New Task" button is very wide, spanning the entire panel.
                        # Check pixel 150px to the right. If still blue -> Button too large, skip!
                        is_wide = False
                        try:
                            r3, g3, b3 = pyautogui.pixel(x + 150, y)
                            if r3 < 50 and 80 < g3 < 180 and b3 > 160:
                                is_wide = True
                        except:
                            pass
                        
                        if is_wide:
                            print(f"   ⚠️ Skipped TOO LARGE blue button (possibly 'Start New Task') at ({x}, {y})")
                        else:
                            run_button_found = True
                            run_x, run_y = x, y
                            break
                except:
                    pass
            except:
                pass
        if run_button_found:
            break

    if run_button_found:
        print(f"   ✅ Run button found at ({run_x}, {run_y})!")
        print("   Moving mouse to Run button...")
        pyautogui.moveTo(run_x, run_y, duration=1.0)
        print("   👉 Bot will CLICK HERE to execute the command.")
    else:
        print("   ❌ No blue Run button found in scan area!")
        print("   👉 Try manually moving your mouse to the Run button and use a color tool (like PowerToys) to check if the RGB color matches the condition (R<50, 80<G<180, B>160).")

    print("\n🎉 TEST COMPLETED!")

if __name__ == "__main__":
    run_diagnostics()

# Made with Bob
