from dataclasses import dataclass
from .entities.paddle import Paddle


@dataclass(frozen=True)
class GameState:

    @dataclass
    class PaddleState:
        is_left: bool
        x: int = -1; y: int = -1
    
    @dataclass
    class BallState:
        x: int = -1; y: int = -1
        xv: int = -1; yv: int = -1
        vel: int = -1
    
    is_updated: bool = False
    paddles: list[PaddleState] = [PaddleState(is_left=True), PaddleState(is_left=False)]
    ball: BallState = BallState()

    def update(self, paddle_left, paddle_right, ball):
        state = self.paddles[0]
        state.x = paddle_left.rect.centerx
        state.y = paddle_left.rect.centery

        state = self.paddles[1]
        state.x = paddle_right.rect.centerx
        state.y = paddle_right.rect.centery

        state = self.ball
        state.x = ball.rect.centerx
        state.y = ball.rect.centery
        state.xv = ball.xv
        state.yv = ball.yv
        state.vel = ball.vel

        self.is_updated = True


@dataclass
class PlayerState:
    
    @dataclass
    class Inputs:
        up: bool = False
        down: bool = False
        fire: bool = False
    
    is_controlling: Paddle
    inputs: Inputs = Inputs()


@dataclass
class Event:
    is_active: bool = False
    is_left: bool = False

    def enable(self, is_left):
        self.is_active = True
        self.is_left = is_left
    
    def disable(self):
        self.is_active = False