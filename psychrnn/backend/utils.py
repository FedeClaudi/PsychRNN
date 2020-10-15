from rich.progress import (
    Progress,
    BarColumn,
    TimeRemainingColumn,
    TextColumn,
)
from rich.text import Text

import psutil 
import os 
import GPUtil as GPU 



GPUs = GPU.getGPUs()
if GPUs:
    gpu = GPUs[0]
else:
    gpu = None

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if "log_time" in kw:
            name = kw.get("log_name", method.__name__.upper())
            kw["log_time"][name] = int((te - ts) * 1000)
        else:
            print(f"{method.__name__}  {round( (te - ts) * 1000, 2)} ms")
        return result

    return timed
    
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
            return Text(f"loss: {task.loss:e}")
        except  AttributeError:
            try:
                return Text(f"loss: {task.fields['loss']:e}")
            except AttributeError:
                print(failed)
            return 'no loss'

class GPUColumn(TextColumn):
    _renderable_cache = {}

    def __init__(self, *args):
        pass

    def render(self, task):
        if gpu is None:
            return Text('no gpu')
        else:
            process = psutil.Process(os.getpid())
            return Text(f'Used mem: {gpu.memoryUsed} / Tot mem: {gpu.memoryTotal}')

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

