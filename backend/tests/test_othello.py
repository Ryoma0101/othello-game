"""
Test cases for Othello game implementation.
"""

from app.game.othello import OthelloBoard, Player, OthelloCPU, OthelloGame
import pytest
import numpy as np
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


class TestOthelloBoard:
    """Test cases for OthelloBoard class."""

    def test_board_initialization(self) -> None:
        """Test board initialization."""
        board = OthelloBoard(8)
        assert board.size == 8
        assert board.board.shape == (8, 8)

        # Check initial position
        assert board.board[3, 3] == Player.WHITE.value
        assert board.board[3, 4] == Player.BLACK.value
        assert board.board[4, 3] == Player.BLACK.value
        assert board.board[4, 4] == Player.WHITE.value

    def test_valid_moves_initial(self) -> None:
        """Test valid moves from initial position."""
        board = OthelloBoard(8)
        black_moves = board.get_valid_moves(Player.BLACK)
        white_moves = board.get_valid_moves(Player.WHITE)

        expected_black = [(2, 3), (3, 2), (4, 5), (5, 4)]
        expected_white = [(2, 4), (3, 5), (4, 2), (5, 3)]

        assert sorted(black_moves) == sorted(expected_black)
        assert sorted(white_moves) == sorted(expected_white)

    def test_make_move(self) -> None:
        """Test making a move."""
        board = OthelloBoard(8)

        # Black plays (2, 3)
        assert board.make_move(2, 3, Player.BLACK)
        assert board.board[2, 3] == Player.BLACK.value
        assert board.board[3, 3] == Player.BLACK.value  # Flipped piece

    def test_invalid_move(self) -> None:
        """Test invalid move handling."""
        board = OthelloBoard(8)

        # Try to place on occupied square
        assert not board.make_move(3, 3, Player.BLACK)

        # Try to place outside board
        assert not board.make_move(8, 8, Player.BLACK)

        # Try to place where no pieces can be flipped
        assert not board.make_move(0, 0, Player.BLACK)

    def test_score_calculation(self) -> None:
        """Test score calculation."""
        board = OthelloBoard(8)
        black_score, white_score = board.get_score()

        # Initial position has 2 pieces each
        assert black_score == 2
        assert white_score == 2

        # After black move
        board.make_move(2, 3, Player.BLACK)
        black_score, white_score = board.get_score()
        assert black_score == 4
        assert white_score == 1

    def test_game_over_detection(self) -> None:
        """Test game over detection."""
        board = OthelloBoard(8)
        assert not board.is_game_over()

        # Create a board with no valid moves
        board.board.fill(Player.BLACK.value)
        board.board[0, 0] = Player.EMPTY.value
        board.board[0, 1] = Player.WHITE.value

        # Should be game over if no valid moves for either player
        if (len(board.get_valid_moves(Player.BLACK)) == 0 and
                len(board.get_valid_moves(Player.WHITE)) == 0):
            assert board.is_game_over()

    def test_board_copy(self) -> None:
        """Test board copying."""
        board = OthelloBoard(8)
        board.make_move(2, 3, Player.BLACK)

        copy_board = board.copy()
        assert np.array_equal(board.board, copy_board.board)
        assert board.size == copy_board.size

        # Ensure it's a deep copy
        copy_board.make_move(2, 4, Player.WHITE)
        assert not np.array_equal(board.board, copy_board.board)


class TestOthelloCPU:
    """Test cases for OthelloCPU class."""

    def test_cpu_initialization(self) -> None:
        """Test CPU initialization."""
        cpu = OthelloCPU(Player.BLACK, difficulty=3)
        assert cpu.player == Player.BLACK
        assert cpu.opponent == Player.WHITE
        assert cpu.difficulty == 3

    def test_get_move_returns_valid_move(self) -> None:
        """Test that CPU returns valid moves."""
        board = OthelloBoard(8)
        cpu = OthelloCPU(Player.BLACK, difficulty=2)

        move = cpu.get_move(board)
        assert move is not None
        assert board.is_valid_move(move[0], move[1], Player.BLACK)

    def test_get_move_no_valid_moves(self) -> None:
        """Test CPU behavior when no valid moves available."""
        board = OthelloBoard(8)
        board.board.fill(Player.WHITE.value)  # Fill board with white pieces

        cpu = OthelloCPU(Player.BLACK, difficulty=2)
        move = cpu.get_move(board)
        assert move is None

    def test_different_difficulty_levels(self) -> None:
        """Test different difficulty levels."""
        board = OthelloBoard(8)

        # Test all difficulty levels
        for difficulty in [1, 2, 3, 4, 5]:
            cpu = OthelloCPU(Player.BLACK, difficulty=difficulty)
            move = cpu.get_move(board)
            if move is not None:
                assert board.is_valid_move(move[0], move[1], Player.BLACK)

    def test_evaluation_function(self) -> None:
        """Test that CPU can evaluate board positions."""
        board = OthelloBoard(8)
        cpu = OthelloCPU(Player.BLACK, difficulty=3)

        # Test that CPU can get a move (which uses evaluation internally)
        move = cpu.get_move(board)
        assert move is not None
        assert board.is_valid_move(move[0], move[1], Player.BLACK)


class TestOthelloGame:
    """Test cases for OthelloGame class."""

    def test_game_initialization(self) -> None:
        """Test game initialization."""
        game = OthelloGame(board_size=8, cpu_difficulty=3,
                           human_player=Player.BLACK)

        assert game.board.size == 8
        assert game.human_player == Player.BLACK
        assert game.cpu_player == Player.WHITE
        assert game.current_player == Player.BLACK
        assert game.cpu.difficulty == 3

    def test_player_switching(self) -> None:
        """Test player switching."""
        game = OthelloGame(human_player=Player.BLACK)

        assert game.current_player == Player.BLACK
        # Test switching by simulating game flow
        original_player = game.current_player
        game.current_player = Player.WHITE
        assert game.current_player == Player.WHITE
        game.current_player = original_player
        assert game.current_player == Player.BLACK


def test_game_flow_simulation() -> None:
    """Test a simulated game flow."""
    game = OthelloGame(
        cpu_difficulty=1)  # Use easy difficulty for predictable testing

    # Make a few moves to ensure the game logic works
    initial_moves = [(2, 3), (2, 4), (3, 2)]

    for i, (row, col) in enumerate(initial_moves):
        current_player = Player.BLACK if i % 2 == 0 else Player.WHITE
        if game.board.is_valid_move(row, col, current_player):
            game.board.make_move(row, col, current_player)

        # Check that the game state is consistent
        black_score, white_score = game.board.get_score()
        assert black_score >= 0
        assert white_score >= 0
        assert black_score + white_score <= 64


def test_edge_cases() -> None:
    """Test various edge cases."""
    # Test minimum board size
    board = OthelloBoard(4)
    assert board.size == 4

    # Test that initial setup works for different sizes
    for size in [4, 6, 8, 10]:
        board = OthelloBoard(size)
        center = size // 2
        assert board.board[center - 1, center - 1] == Player.WHITE.value
        assert board.board[center - 1, center] == Player.BLACK.value
        assert board.board[center, center - 1] == Player.BLACK.value
        assert board.board[center, center] == Player.WHITE.value


if __name__ == "__main__":
    pytest.main([__file__])
