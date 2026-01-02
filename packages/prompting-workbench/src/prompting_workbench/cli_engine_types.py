from typing import List, Protocol, runtime_checkable

from prompting_workbench.domains.project import Project
from prompting_workbench.domains.wrkbnch_context import WrkbnchContext
from prompting_workbench.plugins._base_cli_plugin import BaseCliPlugin


@runtime_checkable
class ICliEngine(Protocol):
    plugins: dict[str, BaseCliPlugin]

    @property
    def project(self) -> Project | None: ...

    @property
    def context(self) -> WrkbnchContext: ...

    def prepare(self) -> None: ...

    def start(self, project: str, prompts: List[str]) -> None: ...
