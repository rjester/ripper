from __future__ import annotations
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.console import Console
from typing import Any


class RichProgressReporter:
    def __init__(self, description: str = "Operation"):
        self.console = Console()
        self.progress = Progress(
            TextColumn("{task.description}"),
            BarColumn(),
            TextColumn("{task.percentage:>5.1f}%"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=self.console,
            transient=False,
        )
        self.task_id = None
        self.last_milestone = -1
        self.description = description

    def __enter__(self):
        self.progress.start()
        self.task_id = self.progress.add_task(self.description, total=100)
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            self.progress.update(self.task_id, completed=100)
        except Exception:
            pass
        self.progress.stop()

    def handle_event(self, evt: Any) -> None:
        # evt expected to be dict with 'percent' numeric
        pct = None
        try:
            pct = float(evt.get('percent'))
        except Exception:
            return
        if self.task_id is None:
            return
        try:
            self.progress.update(self.task_id, completed=pct)
        except Exception:
            pass

        # report milestones at 25/50/75
        if pct >= 25 and self.last_milestone < 25:
            self.console.log(f"→ Progress: 25%")
            self.last_milestone = 25
        elif pct >= 50 and self.last_milestone < 50:
            self.console.log(f"→ Progress: 50%")
            self.last_milestone = 50
        elif pct >= 75 and self.last_milestone < 75:
            self.console.log(f"→ Progress: 75%")
            self.last_milestone = 75
