from .models.prompt import PromptModel
from .repositories.prompt_repository import PromptRepository


class Prompt:
    """
    Prompt domain for the prompting workbench.
    This class is used to manage the prompt domain, including loading and saving prompt.
    """

    data: PromptModel

    repository: PromptRepository

    def __init__(self, project_id: str, prompt_id: str):
        self.project_id = project_id
        self.prompt_id = prompt_id
        self.repository = PromptRepository()

        self._load()

    def _load(self):
        """
        Load the prompt data from the file system or other storage.
        """

        self.data = self.repository.get_prompt(self.project_id, self.prompt_id)

        print(f"[DEBUG] Prompt loaded: {self.data.id}")

    @staticmethod
    def load(project_id: str, prompt_id: str):
        """
        Load a prompt by its name.
        :param prompt_name: Name of the prompt to load.
        :return: Loaded prompt object.
        """
        return Prompt(project_id, prompt_id)
