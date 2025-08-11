class WrkbnchContext:
    """
    Context manager for the prompting workbench.
    This class is used to manage the context of the prompting workbench,
    including the loaded project, prompts, etc.
    """

    def __init__(self):
        self.project = None
