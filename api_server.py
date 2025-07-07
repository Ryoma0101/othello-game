"""
FastAPI server for Othello game API.
"""

from typing import List, Optional, Tuple
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from src.python_copilot.othello import OthelloBoard, OthelloCPU, Player

app = FastAPI(title="Othello Game API", version="1.0.0")

# CORS設定（Reactからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001",
                   "http://localhost:3002", "http://localhost:3003", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# リクエスト/レスポンスモデル


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


# グローバル変数でゲーム状態を管理
current_game_board = OthelloBoard()


def board_to_list(board: OthelloBoard) -> List[List[int]]:
    """Convert OthelloBoard to list representation."""
    return board.board.tolist()


def list_to_board(board_list: List[List[int]]) -> OthelloBoard:
    """Convert list representation to OthelloBoard."""
    board = OthelloBoard()
    board.board = np.array(board_list)
    return board


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Othello Game API"}


@app.get("/api/game/new", response_model=BoardState)
async def new_game():
    """Start a new game."""
    global current_game_board
    current_game_board = OthelloBoard()

    black_score, white_score = current_game_board.get_score()
    valid_moves = current_game_board.get_valid_moves(Player.BLACK)

    return BoardState(
        board=board_to_list(current_game_board),
        current_player=Player.BLACK.value,
        black_score=black_score,
        white_score=white_score,
        game_over=current_game_board.is_game_over(),
        winner=None,
        valid_moves=valid_moves
    )


@app.post("/api/game/move", response_model=BoardState)
async def make_move(move_request: MoveRequest):
    """Make a move on the board."""
    try:
        # Convert list to OthelloBoard
        board = list_to_board(move_request.board)
        player = Player(move_request.player)

        # Validate and make move
        if not board.is_valid_move(move_request.row, move_request.col, player):
            raise HTTPException(status_code=400, detail="Invalid move")

        success = board.make_move(move_request.row, move_request.col, player)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to make move")

        # Calculate new state
        black_score, white_score = board.get_score()
        next_player = Player.WHITE if player == Player.BLACK else Player.BLACK
        valid_moves = board.get_valid_moves(next_player)

        # Check if game is over
        game_over = board.is_game_over()
        winner = None
        if game_over:
            if black_score > white_score:
                winner = Player.BLACK.value
            elif white_score > black_score:
                winner = Player.WHITE.value

        return BoardState(
            board=board_to_list(board),
            current_player=next_player.value,
            black_score=black_score,
            white_score=white_score,
            game_over=game_over,
            winner=winner,
            valid_moves=valid_moves
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/game/cpu-move", response_model=CPUMoveResponse)
async def get_cpu_move(cpu_request: CPUMoveRequest):
    """Get CPU move."""
    try:
        # Convert list to OthelloBoard
        board = list_to_board(cpu_request.board)
        player = Player(cpu_request.player)

        # Create CPU player
        cpu = OthelloCPU(player, cpu_request.difficulty)

        # Get CPU move
        move = cpu.get_move(board)

        if move is None:
            # No valid moves for CPU
            return CPUMoveResponse(
                move=None,
                new_board=board_to_list(board),
                black_score=board.get_score()[0],
                white_score=board.get_score()[1],
                valid_moves=board.get_valid_moves(player)
            )

        # Make the CPU move
        success = board.make_move(move[0], move[1], player)
        if not success:
            raise HTTPException(status_code=500, detail="CPU move failed")

        # Calculate new state
        black_score, white_score = board.get_score()
        next_player = Player.WHITE if player == Player.BLACK else Player.BLACK
        valid_moves = board.get_valid_moves(next_player)

        return CPUMoveResponse(
            move=move,
            new_board=board_to_list(board),
            black_score=black_score,
            white_score=white_score,
            valid_moves=valid_moves
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/game/valid-moves/{player}")
async def get_valid_moves(player: int, board_state: str = None):
    """Get valid moves for a player."""
    try:
        player_enum = Player(player)

        if board_state:
            # Use provided board state
            import json
            board_list = json.loads(board_state)
            board = list_to_board(board_list)
        else:
            # Use current game board
            board = current_game_board

        valid_moves = board.get_valid_moves(player_enum)
        return {"valid_moves": valid_moves}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
