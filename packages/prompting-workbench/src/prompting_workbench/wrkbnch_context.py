from prompting_workbench.domains.project import Project


class WrkbnchContext:
    project: Project | None = None
    debug: bool = False
    dry_run: bool = False

    def __init__(
        self, project: Project | None = None, debug: bool = False, dry_run: bool = False
    ):
        self.project = project
        self.debug = debug
        self.dry_run = dry_run
