import logging

class LightingTool:
    """A tool for controlling the lighting in the art installation."""

    def control(self, state: str, color: str, intensity: int) -> str:
        """
        Controls the lights.
        :param state: The state of the lights. Can be 'on', 'off', or 'flicker'.
        :param color: The color of the lights.
        :param intensity: The intensity of the lights, from 0 to 100.
        """
        logging.info(f"LIGHTING: Setting lights to state={state}, color={color}, intensity={intensity}")
        return f"Lights set to {state}, color {color}, intensity {intensity}."
