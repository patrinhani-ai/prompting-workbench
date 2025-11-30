from prompting_workbench.core.p_singleton import ThreadSafeSingleton
from prompting_workbench.domains.project import Project


class WrkbnchContext(ThreadSafeSingleton["WrkbnchContext"]):
    args__project: str | None = None
    args__prompts: list[str] | None = None

    project: Project | None = None

    debug: bool = False
    dry_run: bool = False

    def load_project(self) -> None:
        project_id = (
            ""
            if not self.args__project or self.args__project == "NONE"
            else self.args__project
        )

        self.project = Project.load(project_id)

        self.load_prompts()

    def load_prompts(self) -> None:
        if self.project and self.args__prompts is not None:
            self.project.load_prompts(self.args__prompts)

    def update_data(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if key == "project":
                continue

            if not hasattr(self, key):
                continue

            setattr(self, key, value)
