import logging

class SoundTool:
    """A tool for controlling the sound system in the art installation."""

    def control(self, sound: str, action: str) -> str:
        """
        Controls the sound system.
        :param sound: The sound to play. Can be 'engine_hum', 'alarm', 'static', or 'ambient_music'.
        :param action: The action to perform. Can be 'play', 'stop', 'volume_up', or 'volume_down'.
        """
        logging.info(f"SOUND: Performing action '{action}' on sound '{sound}'")
        return f"Sound system action '{action}' performed for sound '{sound}'."
