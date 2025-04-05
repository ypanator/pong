from dataclasses import dataclass, field
from .entities.paddle import Paddle


def PaddleState(is_left):
    return {
        'is_left': is_left,
        'x': -1,
        'y': -1,
        'score': 0
    }

def BallState():
    return {
        'is_left': False,
        'is_rolling': False,
        'x': -1,
        'y': -1,
        'xv': -1,
        'yv': -1,
        'vel': -1
    }

def GameState():
    return {
        'is_updated': False,
        'paddles': [
            PaddleState(False),
            PaddleState(True)
        ],
        'ball': BallState()
    }

def Inputs():
    return {
        'up': False,
        'down': False,
        'fire': False
    }

def PlayerState():
    return {
        'is_controlling': None,
        'inputs': Inputs()
    }

def Event():
    return {
        'is_active': False,
        'is_left': False
    }

def update_game_state(state, paddle_left, paddle_right, ball):
    paddle_state = state['paddles'][0]
    paddle_state['x'] = paddle_left.rect.centerx
    paddle_state['y'] = paddle_left.rect.centery
    paddle_state['score'] = paddle_left.score

    paddle_state = state['paddles'][1]
    paddle_state['x'] = paddle_right.rect.centerx
    paddle_state['y'] = paddle_right.rect.centery
    paddle_state['score'] = paddle_right.score

    ball_state = state['ball']
    ball_state['is_left'] = ball.is_left
    ball_state['is_rolling'] = ball.is_rolling
    ball_state['x'] = ball.rect.centerx
    ball_state['y'] = ball.rect.centery
    ball_state['xv'] = ball.xv
    ball_state['yv'] = ball.yv
    ball_state['vel'] = ball.vel

    state['is_updated'] = True
    return state

def enable_event(event, is_left):
    event['is_active'] = True
    event['is_left'] = is_left
    return event

def disable_event(event):
    event['is_active'] = False
    return event