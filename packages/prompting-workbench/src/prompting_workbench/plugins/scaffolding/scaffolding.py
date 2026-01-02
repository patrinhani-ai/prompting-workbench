from prompting_workbench.plugins._base_cli_plugin import BaseCliPlugin


class ScaffoldingCliPlugin(BaseCliPlugin):
    """
    Plugin for scaffolding new projects and prompts.
    """

    def get_plugin_name(self):
        return "scaffolding"

    def get_plugin_description(self):
        return "Scaffold new projects and prompts with proper structure"

    def get_plugin_help(self):
        return "Create new projects and prompts using templates"

    def get_plugin_file_path(self):
        return __file__

    def prepare(self, *args, **kwargs):
        super().prepare(*args, **kwargs)

    def run(self):
        pass
