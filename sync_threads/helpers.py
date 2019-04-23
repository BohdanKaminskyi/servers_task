from typing import Sequence


class HistoryViewer:
    def __init__(self, history: Sequence[str]):
        self._history = history

    @property
    def as_strings(self):
        return '\n'.join(
            map(
                lambda ind_command: f'{ind_command[0]:>5}  {ind_command[1]}',
                enumerate(self._history, 1)
                )
            )
