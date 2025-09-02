from prompting_workbench.domains.project import Project


class WrkbnchContext:
    project: Project | None = None
    debug: bool = False
    dry_run: bool = False
