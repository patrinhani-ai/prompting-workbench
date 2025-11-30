from prompting_workbench.plugins._base_cli_plugin import BaseCliPlugin


class BoilerplateCliPlugin(BaseCliPlugin):
    """
    Plugin for generating boilerplate code and project structures.
    Helps create new projects and prompts with proper directory structure.
    """

    def get_plugin_name(self):
        return "boilerplate"

    def get_plugin_description(self):
        return "Generate boilerplate code for projects and prompts"

    def get_plugin_help(self):
        return "Create new projects and prompts with proper directory structure"

    def get_plugin_file_path(self):
        return __file__

    def run(self):
        pass
