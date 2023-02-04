class WakeupState:
    def __init__(self):
        self._wakeup_running = False

    @property
    def wakeup_running(self) -> bool:
        return self._wakeup_running

    @wakeup_running.setter
    def wakeup_running(self, state: bool):
        self._wakeup_running = state
