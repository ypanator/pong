from dataclasses import dataclass

@dataclass
class Message:
    type: int
    data: any