from prompting_workbench.domains.project import Project
from prompting_workbench.wrkbnch_context import WrkbnchContext

from prompting_workbench.plugins._base_cli_plugin import BaseCliPlugin

from typing import Protocol, runtime_checkable, List


@runtime_checkable
class ICliEngine(Protocol):
    plugins: dict[str, BaseCliPlugin]
    context: WrkbnchContext
    project: Project

    def prepare(self) -> None: ...

    def start(self, project: str, prompts: List[str]) -> None: ...
