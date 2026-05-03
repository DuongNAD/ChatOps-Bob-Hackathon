"""
Tests for RPA Controller functionality.

This module tests the RPAController class including initialization,
command execution, and concurrency control.
"""

import asyncio
import os
import pytest
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from app.services.rpa_controller import RPAController


class TestRPAControllerInitialization:
    """Test RPAController initialization."""
    
    def test_init_creates_screenshot_directory(self, tmp_path):
        """Test that initialization creates the screenshot directory."""
        # Use temporary directory for testing
        with patch('app.services.rpa_controller.os.makedirs') as mock_makedirs:
            controller = RPAController()
            
            # Verify makedirs was called
            mock_makedirs.assert_called_once_with("data/screenshots", exist_ok=True)
    
    def test_init_sets_default_values(self):
        """Test that initialization sets correct default values."""
        controller = RPAController()
        
        assert controller.is_busy is False
        assert controller.screenshot_dir == "data/screenshots"
        assert controller._lock is not None
    
    @patch('app.services.rpa_controller.pyautogui')
    def test_init_configures_pyautogui(self, mock_pyautogui):
        """Test that pyautogui is configured correctly."""
        controller = RPAController()
        
        # Verify pyautogui settings
        assert mock_pyautogui.PAUSE == 0.5
        assert mock_pyautogui.FAILSAFE is True


class TestRPAControllerExecuteCommand:
    """Test execute_bob_command method."""
    
    @pytest.mark.asyncio
    async def test_execute_returns_correct_format(self):
        """Test that execute_bob_command returns dict with correct keys."""
        controller = RPAController()
        
        # Mock the _run_rpa method
        mock_result = {
            "success": True,
            "screenshot_path": "/path/to/screenshot.png",
            "code_text": "print('hello')",
            "error": ""
        }
        
        with patch.object(controller, '_run_rpa', return_value=mock_result):
            result = await controller.execute_bob_command("test command")
            
            # Verify result has all required keys
            assert "success" in result
            assert "screenshot_path" in result
            assert "code_text" in result
            assert "error" in result
            assert result["success"] is True
    
    @pytest.mark.asyncio
    async def test_execute_sets_busy_flag(self):
        """Test that is_busy flag is set during execution."""
        controller = RPAController()
        busy_states = []
        
        async def mock_run_rpa(func, command):
            # Capture busy state during execution
            busy_states.append(controller.is_busy)
            await asyncio.sleep(0.1)
            return {
                "success": True,
                "screenshot_path": "",
                "code_text": "",
                "error": ""
            }
        
        with patch('asyncio.to_thread', side_effect=mock_run_rpa):
            await controller.execute_bob_command("test")
            
            # Verify is_busy was True during execution
            assert True in busy_states
            # Verify is_busy is False after completion
            assert controller.is_busy is False
    
    @pytest.mark.asyncio
    async def test_execute_handles_exceptions(self):
        """Test that exceptions are caught and returned in result."""
        controller = RPAController()
        
        with patch('asyncio.to_thread', side_effect=Exception("Test error")):
            result = await controller.execute_bob_command("test")
            
            assert result["success"] is False
            assert "Test error" in result["error"]
            assert controller.is_busy is False


class TestRPAControllerConcurrency:
    """Test concurrency control with asyncio.Lock."""
    
    @pytest.mark.asyncio
    async def test_concurrent_commands_are_serialized(self):
        """Test that concurrent commands are executed one at a time."""
        controller = RPAController()
        execution_order = []
        
        async def mock_run_rpa(func, command):
            execution_order.append(f"start_{command}")
            await asyncio.sleep(0.2)
            execution_order.append(f"end_{command}")
            return {
                "success": True,
                "screenshot_path": "",
                "code_text": "",
                "error": ""
            }
        
        with patch('asyncio.to_thread', side_effect=mock_run_rpa):
            # Start two commands concurrently
            task1 = asyncio.create_task(controller.execute_bob_command("cmd1"))
            task2 = asyncio.create_task(controller.execute_bob_command("cmd2"))
            
            await asyncio.gather(task1, task2)
            
            # Verify commands were executed serially (one completes before other starts)
            assert execution_order.index("end_cmd1") < execution_order.index("start_cmd2") or \
                   execution_order.index("end_cmd2") < execution_order.index("start_cmd1")


class TestRPAControllerRunRPA:
    """Test _run_rpa method with mocked external dependencies."""
    
    @patch('app.services.rpa_controller.pyperclip')
    @patch('app.services.rpa_controller.pyautogui')
    @patch('app.services.rpa_controller.time.sleep')
    def test_run_rpa_executes_steps(self, mock_sleep, mock_pyautogui, mock_pyperclip):
        """Test that _run_rpa executes all automation steps."""
        controller = RPAController()
        
        # Mock screenshot
        mock_screenshot = MagicMock()
        mock_pyautogui.screenshot.return_value = mock_screenshot
        
        # Mock clipboard
        mock_pyperclip.paste.return_value = "test code"
        
        result = controller._run_rpa("test command")
        
        # Verify pyautogui calls
        # Note: hotkey('ctrl', 'v') is the only guaranteed hotkey call now
        # alt+tab is only used as fallback, and ctrl+alt+b is only used if no window is found
        mock_pyautogui.hotkey.assert_any_call('ctrl', 'v')
        mock_pyautogui.press.assert_any_call('enter')
        
        # Verify clipboard operations
        mock_pyperclip.copy.assert_called_with("test command")
        
        # Verify screenshot was taken
        mock_pyautogui.screenshot.assert_called_once()
        
        # Verify result
        assert result["success"] is True
        assert "bob_result_" in result["screenshot_path"]
        assert result["code_text"] == "test code"
    
    @patch('app.services.rpa_controller.pyperclip')
    @patch('app.services.rpa_controller.pyautogui')
    @patch('app.services.rpa_controller.time.sleep')
    def test_run_rpa_handles_errors(self, mock_sleep, mock_pyautogui, mock_pyperclip):
        """Test that _run_rpa handles errors gracefully."""
        controller = RPAController()
        
        # Make pyautogui raise an exception
        mock_pyautogui.hotkey.side_effect = Exception("Automation failed")
        
        result = controller._run_rpa("test command")
        
        # Verify error is captured
        assert result["success"] is False
        assert "Automation failed" in result["error"]


# Made with Bob