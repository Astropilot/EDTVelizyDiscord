from threading import Event, Thread
from typing import Any, Callable, Dict, Optional, Sequence


class RepeatTimer(Thread):
    def __init__(
        self,
        interval: float,
        function: Callable[..., None],
        args: Optional[Sequence[Any]] = None,
        kwargs: Optional[Dict[Any, Any]] = None,
    ):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.finished = Event()

    def run(self) -> None:
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

    def cancel(self) -> None:
        self.finished.set()
