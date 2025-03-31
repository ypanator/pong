from dataclasses import dataclass
from .entities.paddle import Paddle


@dataclass(frozen=True)
class State:

    @dataclass
    class _Paddle:
        is_left: bool
        x: int = -1; y: int = -1
    
    @dataclass
    class _Ball:
        x: int = -1; y: int = -1
        xv: int = -1; yv: int = -1
        vel: int = -1
    
    paddles: list[_Paddle] = [_Paddle(is_left=False), _Paddle(is_left=True)]
    ball: _Ball = _Ball()


@dataclass
class Player:
    
    @dataclass
    class _Inputs:
        up: bool = False
        down: bool = False
        fire: bool = False
    
    is_controlling: Paddle
    inputs: _Inputs = _Inputs()


@dataclass
class Event:
    is_active: bool = False
    is_left: bool = False