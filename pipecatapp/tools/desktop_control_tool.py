import base64
import io

class DesktopControlTool:
    """A tool for controlling the desktop environment.

    This tool allows the agent to see the screen, click, and type, enabling
    it to interact with any application on the desktop.

    Attributes:
        description (str): A brief description of the tool's purpose.
        name (str): The name of the tool.
    """
    def __init__(self):
        """Initializes the DesktopControlTool."""
        self.description = "A tool for controlling the desktop GUI."
        self.name = "desktop_control"


    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": getattr(self, "name", "desktopcontroltool"),
                "description": getattr(self, "description", "Tool DesktopControlTool"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform. Available: get_desktop_screenshot, click_at, type_text"
                        },
                        "kwargs": {
                            "type": "object",
                            "description": "Additional arguments for the action."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    def execute(self, action: str, **kwargs):
        if action == "get_desktop_screenshot":
            return getattr(self, "get_desktop_screenshot")(**kwargs.get("kwargs", kwargs))
        if action == "click_at":
            return getattr(self, "click_at")(**kwargs.get("kwargs", kwargs))
        if action == "type_text":
            return getattr(self, "type_text")(**kwargs.get("kwargs", kwargs))
        else:
            return f"Unknown action: {action}"

    def get_desktop_screenshot(self) -> str:
        """Takes a screenshot of the entire desktop and returns it as a base64 string.

        Returns:
            str: A base64-encoded string of the screenshot PNG, or an error message.
        """
        try:
            import pyautogui
            screenshot = pyautogui.screenshot()
            buffered = io.BytesIO()
            screenshot.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            return img_str
        except Exception as e:
            return f"Error taking desktop screenshot: {e}"

    def click_at(self, x: int, y: int) -> str:
        """Clicks the mouse at a specific (x, y) coordinate on the desktop.

        Args:
            x (int): The x-coordinate to click.
            y (int): The y-coordinate to click.

        Returns:
            str: A confirmation message on success, or an error message.
        """
        try:
            import pyautogui
            pyautogui.click(x, y)
            return f"Successfully clicked at desktop coordinate ({x}, {y})."
        except Exception as e:
            return f"Error clicking at desktop coordinate ({x}, {y}): {e}"

    def type_text(self, text: str) -> str:
        """Types text at the current cursor location.

        Args:
            text (str): The text to type.

        Returns:
            str: A confirmation message on success, or an error message.
        """
        try:
            import pyautogui
            pyautogui.typewrite(text)
            return f"Successfully typed '{text}'."
        except Exception as e:
            return f"Error typing '{text}': {e}"