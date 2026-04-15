class Knockback:
    _KNOCKBACK_DURATION: float = 0.125
    def __init__(self, k: float) -> None:
        self._k: float = k
        self._timer: float = self._KNOCKBACK_DURATION

    def decrement_timer(self, dt: float) -> None:
        self._timer -= dt

    def get_remaining_duration(self) -> float:
        return self._timer

    def get_magnitude(self) -> float:
        return self._k