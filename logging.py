from rich.console import Console
from typing import Any

class SimpleLogger:
    def __init__(self, name: str):
        self.name = name
        self.console = Console()

    def info(self, msg: Any) -> None:
        self.console.print(f"[bold green]INFO[/] [{self.name}] {msg}")

    def warn(self, msg: Any) -> None:
        self.console.print(f"[bold yellow]WARN[/] [{self.name}] {msg}")

    def error(self, msg: Any) -> None:
        self.console.print(f"[bold red]ERROR[/] [{self.name}] {msg}")

def get_logger(name: str) -> SimpleLogger:
    """Return a SimpleLogger instance with the given name."""
    return SimpleLogger(name)

log = get_logger("global")
info = log.info
warn = log.warn
error = log.error