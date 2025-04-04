from dataclasses import dataclass, field
from .entities.paddle import Paddle


@dataclass(frozen=True)
class GameState:

    @dataclass
    class PaddleState:
        is_left: bool
        x: int = -1; y: int = -1
        score: int = 0
    
    @dataclass
    class BallState:
        is_left: bool = False
        is_rolling: bool = False
        x: int = -1; y: int = -1
        xv: int = -1; yv: int = -1
        vel: int = -1
    
    is_updated: bool = False
    paddles: list[PaddleState] = (
        field(default_factory = lambda: [GameState.PaddleState(is_left=True), GameState.PaddleState(is_left=False)]))
    ball: BallState = field(default_factory=BallState)

    def update(self, paddle_left, paddle_right, ball):
        state = self.paddles[0]
        state.x = paddle_left.rect.centerx
        state.y = paddle_left.rect.centery
        state.score = paddle_left.score

        state = self.paddles[1]
        state.x = paddle_right.rect.centerx
        state.y = paddle_right.rect.centery
        state.score = paddle_right.score

        state = self.ball
        state.is_left = ball.is_left
        state.is_rolling = ball.is_rolling
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
    
    is_controlling: Paddle = None
    inputs: Inputs = field(default_factory=Inputs)


@dataclass
class Event:
    is_active: bool = False
    is_left: bool = False

    def enable(self, is_left):
        self.is_active = True
        self.is_left = is_left
    
    def disable(self):
        self.is_active = False