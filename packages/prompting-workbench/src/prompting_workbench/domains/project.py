from .models.project import ProjectModel
from .prompt import Prompt
from .repositories.project_repository import ProjectRepository
from .repositories.prompt_repository import PromptRepository


class Project:
    """
    Project domain for the prompting workbench.
    This class is used to manage the project domain, including loading and saving projects.
    """

    data: ProjectModel

    repository: ProjectRepository
    prompts_repository: PromptRepository

    project_id: str
    prompts: list[Prompt]

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.prompts = []

        self.repository = ProjectRepository()
        self.prompts_repository = PromptRepository()

        self._load()

    def _load(self):
        """
        Load the project data from the file system or other storage.
        """

        self.data = self.repository.get_project(self.project_id)

        print(f"[DEBUG] Project loaded: {self.data.id}")

    def load_prompts(self, prompt_ids: list[str] = []):
        """
        Load prompts associated with the project.
        This method should be implemented to load prompts from the project directory.
        """

        if prompt_ids is None or len(prompt_ids) == 0:
            prompt_ids = self.prompts_repository.get_all_prompt_ids(self.project_id)

        # Here you would implement the logic to load prompts from the project directory

        for prompt_id in prompt_ids:
            prompt = Prompt.load(self.project_id, prompt_id)
            self.prompts.append(prompt)

        print(f"[DEBUG] Prompts loaded for project: {self.project_id}")
        for prompt in self.prompts:
            print(f"[DEBUG] Prompt ID: {prompt.prompt_id}, Data: {prompt.data}")

    @staticmethod
    def load(project_id: str):
        """
        Load a project by its name.
        :param project_name: Name of the project to load.
        :return: Loaded project object.
        """
        return Project(project_id)

    # String representation
    def __repr__(self):
        return f"Project(id={self.project_id}, prompts={self.prompts})"
