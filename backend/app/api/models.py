"""
Pydantic models for API requests and responses.
"""

from typing import List, Optional, Tuple
from pydantic import BaseModel


class BoardState(BaseModel):
    """Board state model."""
    board: List[List[int]]
    current_player: int
    black_score: int
    white_score: int
    game_over: bool
    winner: Optional[int]
    valid_moves: List[Tuple[int, int]]


class MoveRequest(BaseModel):
    """Move request model."""
    board: List[List[int]]
    row: int
    col: int
    player: int


class CPUMoveRequest(BaseModel):
    """CPU move request model."""
    board: List[List[int]]
    player: int
    difficulty: int = 4


class CPUMoveResponse(BaseModel):
    """CPU move response model."""
    move: Optional[Tuple[int, int]]
    new_board: List[List[int]]
    black_score: int
    white_score: int
    valid_moves: List[Tuple[int, int]]
