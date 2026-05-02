"""
RPA Controller for automating Bob AI interactions.

This module provides RPA (Robotic Process Automation) capabilities to control
VS Code and interact with Bob AI assistant through keyboard and mouse automation.
"""

import asyncio
import logging
import os
import time
from datetime import datetime
from typing import Dict, Any

import pyautogui
import pyperclip

# Try to import pygetwindow for better window management
try:
    import pygetwindow as gw
    HAS_PYGETWINDOW = True
except ImportError:
    HAS_PYGETWINDOW = False

# Configure logging
logger = logging.getLogger(__name__)


class RPAController:
    """
    Controller for automating Bob AI interactions using RPA.
    
    Uses pyautogui for keyboard/mouse automation and manages concurrent
    access through async locks to prevent conflicts.
    """
    
    def __init__(self):
        """Initialize the RPA controller with necessary configurations."""
        # Lock to prevent concurrent RPA operations
        self._lock = asyncio.Lock()
        
        # Track if RPA is currently executing
        self.is_busy = False
        
        # Directory for storing screenshots
        self.screenshot_dir = "data/screenshots"
        
        # Create screenshot directory if it doesn't exist
        os.makedirs(self.screenshot_dir, exist_ok=True)
        logger.info(f"Screenshot directory: {self.screenshot_dir}")
        
        # Configure pyautogui settings
        pyautogui.PAUSE = 0.5  # Add 0.5s pause between pyautogui calls
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
        
        logger.info("RPA Controller initialized")
    
    async def execute_bob_command(self, command: str) -> Dict[str, Any]:
        """
        Execute a command in Bob AI assistant using RPA automation.
        
        This method ensures only one RPA operation runs at a time using an
        async lock, and executes the actual RPA operations in a separate thread
        to avoid blocking the async event loop.
        
        Args:
            command: The command text to send to Bob AI
            
        Returns:
            dict: Result dictionary with keys:
                - success (bool): Whether the operation succeeded
                - screenshot_path (str): Path to the screenshot taken
                - code_text (str): Any code text extracted from clipboard
                - error (str): Error message if operation failed
        """
        # Acquire lock to ensure only one RPA operation at a time
        async with self._lock:
            self.is_busy = True
            logger.info(f"Starting RPA execution for command: {command[:50]}...")
            
            try:
                # Run RPA operations in a separate thread to avoid blocking
                result = await asyncio.to_thread(self._run_rpa, command)
                logger.info("RPA execution completed successfully")
                return result
                
            except Exception as e:
                logger.error(f"RPA execution failed: {e}", exc_info=True)
                return {
                    "success": False,
                    "screenshot_path": "",
                    "code_text": "",
                    "error": str(e)
                }
            finally:
                self.is_busy = False
    
    def _run_rpa(self, command: str) -> Dict[str, Any]:
        """
        Execute the actual RPA automation steps (sync method).
        
        This method runs in a separate thread and performs all pyautogui
        operations. It should NEVER be called directly from async code.
        
        Args:
            command: The command text to send to Bob AI
            
        Returns:
            dict: Result dictionary with success status, screenshot path, and code text
        """
        try:
            # Step 1: Focus VS Code window
            logger.debug("Step 1: Focusing VS Code window")
            vscode_focused = False
            vscode_window = None
            try:
                if HAS_PYGETWINDOW:
                    # Search ONLY for IBM Bob windows
                    all_windows = gw.getAllWindows()
                    for w in all_windows:
                        if 'IBM Bob' in w.title:
                            logger.debug(f"Found IBM Bob window: '{w.title}'")
                            # Save window reference BEFORE activate (activate may throw false error)
                            vscode_window = w
                            vscode_focused = True
                            if w.isMinimized:
                                w.restore()
                                time.sleep(0.5)
                            try:
                                w.activate()
                            except Exception as ae:
                                logger.debug(f"activate() threw error (usually harmless): {ae}")
                            break
                    
                    if not vscode_focused:
                        logger.warning("IBM Bob window not found")
            except Exception as e:
                logger.warning(f"pygetwindow error: {e}")
            
            if not vscode_focused:
                logger.debug("Using Alt+Tab fallback")
                pyautogui.hotkey('alt', 'tab')
            
            time.sleep(1.5)
            
            # Step 2: Ensure Bob chat panel is open, then click input field
            logger.debug("Step 2: Checking if Bob panel is open")
            
            if vscode_window:
                # Check header area at (90% width, 3.5% height)
                # When panel is OPEN: RGB(204,204,204) = white "IBM BOB" text
                # When panel is CLOSED: RGB(31,31,31) = dark empty tab bar
                header_x = vscode_window.left + int(vscode_window.width * 0.90)
                header_y = vscode_window.top + int(vscode_window.height * 0.035)
                
                try:
                    pixel = pyautogui.pixel(header_x, header_y)
                    r, g, b = pixel
                    logger.debug(f"Header pixel at ({header_x},{header_y}): RGB({r},{g},{b})")
                    
                    if r > 150 and g > 150 and b > 150:
                        logger.debug("Bob panel is OPEN (white header text detected)")
                    else:
                        logger.debug("Bob panel appears closed, but skipping Ctrl+Alt+B to prevent accidental closing due to window resizing.")
                except Exception as e:
                    logger.warning(f"Header check failed: {e}")
                
                # Click on the input field at (75%, 90%)
                input_x = vscode_window.left + int(vscode_window.width * 0.75)
                input_y = vscode_window.top + int(vscode_window.height * 0.90)
            else:
                # No window reference - just try Ctrl+Alt+B and estimate
                pyautogui.hotkey('ctrl', 'alt', 'b')
                time.sleep(2)
                screen_w, screen_h = pyautogui.size()
                input_x = int(screen_w * 0.75)
                input_y = int(screen_h * 0.90)
            
            logger.debug(f"Clicking Bob input at ({input_x}, {input_y})")
            pyautogui.click(input_x, input_y)
            time.sleep(0.5)
            
            # Step 3: Paste command using clipboard
            logger.debug("Step 3: Pasting command")
            pyperclip.copy(command)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            
            # Step 4: Send command by pressing Enter
            logger.debug("Step 4: Sending command")
            pyautogui.press('enter')
            time.sleep(0.5)
            
            # Step 5: Wait for Bob and auto-click "Run" buttons
            logger.debug("Step 5: Waiting for Bob and auto-approving actions")
            total_wait = 50
            check_interval = 3
            elapsed = 0
            task_completed = False
            
            while elapsed < total_wait and not task_completed:
                time.sleep(check_interval)
                elapsed += check_interval
                logger.debug(f"Checking for Run button... ({elapsed}s / {total_wait}s)")
                
                try:
                    # Run button is blue RGB(0,120,212) in the Bob panel
                    # Scan from 50% to 85% height (STOP before Plan/Code buttons at bottom)
                    # Scan from 70% to 90% width (Bob panel area)
                    if vscode_window:
                        scan_x_start = vscode_window.left + int(vscode_window.width * 0.72)
                        scan_x_end = vscode_window.left + int(vscode_window.width * 0.88)
                        scan_y_start = vscode_window.top + int(vscode_window.height * 0.50)
                        scan_y_end = vscode_window.top + int(vscode_window.height * 0.85)
                    else:
                        screen_w, screen_h = pyautogui.size()
                        scan_x_start = int(screen_w * 0.72)
                        scan_x_end = int(screen_w * 0.88)
                        scan_y_start = int(screen_h * 0.50)
                        scan_y_end = int(screen_h * 0.85)
                    
                    found_run = False
                    for scan_x in range(scan_x_start, scan_x_end, 40):
                        if found_run or task_completed:
                            break
                        for scan_y in range(scan_y_start, scan_y_end, 12):
                            try:
                                pixel_color = pyautogui.pixel(scan_x, scan_y)
                                r, g, b = pixel_color
                                
                                # Match the EXACT Run button color: RGB(0, 120, 212)
                                # Allow some tolerance
                                is_run_btn = (r < 50 and 80 < g < 180 and b > 160)
                                
                                if is_run_btn:
                                    # Verification step 1: ensure it's a solid button, not a 1px border
                                    # Check the pixel 10 pixels below it
                                    try:
                                        r2, g2, b2 = pyautogui.pixel(scan_x, scan_y + 10)
                                        if r2 < 50 and 80 < g2 < 180 and b2 > 160:
                                            # Verification step 2: ensure it's not the "Start New Task" button
                                            # The "Start New Task" button spans the entire width of the panel.
                                            # The real "Run" button is small and inline.
                                            # If we check 150 pixels to the right and it's STILL blue, it's too wide!
                                            is_wide = False
                                            try:
                                                r3, g3, b3 = pyautogui.pixel(scan_x + 150, scan_y)
                                                if r3 < 50 and 80 < g3 < 180 and b3 > 160:
                                                    is_wide = True
                                            except:
                                                pass
                                                
                                            if is_wide:
                                                if elapsed > 10:
                                                    logger.info(f"Found 'Start New Task' button at ({scan_x}, {scan_y}). Task is COMPLETE!")
                                                    task_completed = True
                                                    break
                                                else:
                                                    logger.debug(f"Ignored 'Start New Task' at ({scan_x}, {scan_y}) because task just started (elapsed: {elapsed}s)")
                                            else:
                                                logger.info(f"Found solid Run button at ({scan_x}, {scan_y}), RGB({r},{g},{b})")
                                                pyautogui.click(scan_x, scan_y)
                                                time.sleep(3)
                                                found_run = True
                                                break
                                        else:
                                            logger.debug(f"Ignored thin blue border at ({scan_x}, {scan_y})")
                                    except:
                                        pass
                            except:
                                pass
                    
                    if not found_run:
                        logger.debug("No Run button found in this scan")
                except Exception as e:
                    logger.debug(f"Run button scan failed: {e}")
            
            # Step 6: Take screenshot of the result
            logger.debug("Step 6: Taking screenshot")
            screenshot = pyautogui.screenshot()
            
            # Generate timestamp-based filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_filename = f"bob_result_{timestamp}.png"
            screenshot_path = os.path.join(self.screenshot_dir, screenshot_filename)
            
            # Save screenshot
            screenshot.save(screenshot_path)
            logger.info(f"Screenshot saved: {screenshot_path}")
            
            # Step 7: Try to extract code from clipboard (simplified approach)
            logger.debug("Step 7: Attempting to extract code from clipboard")
            code_text = ""
            try:
                # Check if there's already code in clipboard from Bob's copy button
                # If user clicked "Copy Code" button in Bob UI, it will be in clipboard
                clipboard_content = pyperclip.paste()
                
                # Only use clipboard content if it looks like code (not the command we sent)
                if clipboard_content and clipboard_content != command:
                    code_text = clipboard_content
                    logger.debug(f"Extracted {len(code_text)} characters from clipboard")
                else:
                    logger.debug("No code found in clipboard")
                
            except Exception as e:
                logger.warning(f"Could not extract code from clipboard: {e}")
            
            # Return success result
            return {
                "success": True,
                "screenshot_path": screenshot_path,
                "code_text": code_text,
                "error": ""
            }
            
        except Exception as e:
            logger.error(f"RPA operation failed: {e}", exc_info=True)
            return {
                "success": False,
                "screenshot_path": "",
                "code_text": "",
                "error": str(e)
            }


# Made with Bob