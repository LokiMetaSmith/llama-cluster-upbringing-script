import json
import os

class Power_Tool:
    def __init__(self):
        self.description = "Control the power management policies of the cluster."
        self.name = "power_tool"
        self.config_path = "/opt/power_manager/config.json"

    def set_idle_threshold(self, service_port: int, idle_seconds: int) -> str:
        """
        Sets the idle time in seconds before a service is put to sleep.

        :param service_port: The port of the service to configure.
        :param idle_seconds: The number of seconds of inactivity before sleeping.
        :return: A confirmation or error message.
        """
        if not os.path.exists(os.path.dirname(self.config_path)):
            return f"Error: Power manager config directory not found at {os.path.dirname(self.config_path)}"

        try:
            # Read the existing config
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
            else:
                # Or create a default if it doesn't exist
                config = {
                    "monitored_services": {}
                }

            # Update the specific service's threshold
            port_str = str(service_port)
            if port_str not in config["monitored_services"]:
                 config["monitored_services"][port_str] = {}

            config["monitored_services"][port_str]["idle_threshold_seconds"] = idle_seconds

            # Write the updated config back to the file
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)

            return f"Successfully set idle threshold for service on port {service_port} to {idle_seconds} seconds. The power agent will apply this setting shortly."

        except Exception as e:
            return f"An error occurred while setting the power policy: {e}"
