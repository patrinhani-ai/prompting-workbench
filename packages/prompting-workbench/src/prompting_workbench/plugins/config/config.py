from prompting_workbench.plugins._base_cli_plugin import BaseCliPlugin
from prompting_workbench.settings import settings


class ConfigCliPlugin(BaseCliPlugin):
    def __init__(self):
        super().__init__()

    def get_plugin_name(self):
        return "config"

    def get_plugin_description(self):
        return "View and manage configuration settings"

    def get_plugin_help(self):
        return "View and manage configuration settings for the Prompting Workbench"

    def get_plugin_file_path(self):
        return __file__

    def prepare(self, context: dict):
        super().prepare(context=context)

    def run(self):
        """Display current configuration settings"""
        try:
            self.notify_status_update(
                key="config", status="running", text="Retrieving configuration settings"
            )

            # Get all settings from the settings object
            config_data = settings.model_dump()

            self.notify_status_update(
                key="config", status="done", text="Configuration retrieved successfully"
            )

            return config_data

        except Exception as e:
            self.notify_status_update(
                key="config",
                status="error",
                text=f"Failed to retrieve configuration: {e}",
            )
            raise

    def __repr__(self):
        return f"<{self.__class__.__name__}>"
