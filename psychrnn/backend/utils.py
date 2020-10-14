from rich.progress import (
    Progress,
    BarColumn,
    TimeRemainingColumn,
    TextColumn,
)
from rich.text import Text



class SpeedColumn(TextColumn):
    _renderable_cache = {}

    def __init__(self, *args):
        pass

    def render(self, task):
        if task.speed is None:
            return Text(" ")
        else:
            return Text(f"{task.speed:.3f} steps/s")


class LossColumn(TextColumn):
    _renderable_cache = {}

    def __init__(self, *args):
        pass

    def render(self, task):
        try:
            return Text(f"loss: {task.loss:.3f}")
        except  AttributeError:
            try:
                return Text(f"loss: {task.fields['loss']:.3f}")
            except AttributeError:
                print(failed)
            return 'no loss'

class PerformanceColumn(TextColumn):
    _renderable_cache = {}

    def __init__(self, *args):
        pass

    def render(self, task):
        if task.fields['performance'] is None or task.fields['performance_cutoff'] is None:
            return Text('Performance: nan')
            
        try:
            return Text(f"Performance: {task.fields['performance']:.3f}/{task.fields['performance_cutoff']:.3f}")
        except AttributeError:
            print(failed)
            return 'no loss'


train_progress = Progress(
    TextColumn("[bold magenta]Step {task.completed}/{task.total}"),
    SpeedColumn(), 
    "•",
    "[progress.description]{task.description}",
    BarColumn(bar_width=None),
    "•",
    "[progress.percentage]{task.percentage:>3.0f}%",
    TimeRemainingColumn(),
    "•",
    LossColumn(),
    "•",
    PerformanceColumn(),

)

