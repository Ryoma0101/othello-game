"""
Othello game implementation with CPU player.

This module provides classes for playing Othello with an AI opponent.
"""

from enum import Enum
from typing import List, Optional, Tuple, Union
import numpy as np
import random


class Player(Enum):
    """Represents the players in the game."""
    BLACK = 1
    WHITE = -1
    EMPTY = 0


class OthelloBoard:
    """Represents the Othello game board."""

    def __init__(self, size: int = 8) -> None:
        """Initialize the board with the given size."""
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self._setup_initial_position()

    def _setup_initial_position(self) -> None:
        """Set up the initial position with four pieces in the center."""
        center = self.size // 2
        self.board[center - 1, center - 1] = Player.WHITE.value
        self.board[center - 1, center] = Player.BLACK.value
        self.board[center, center - 1] = Player.BLACK.value
        self.board[center, center] = Player.WHITE.value

    def is_valid_move(self, row: int, col: int, player: Player) -> bool:
        """Check if a move is valid for the given player."""
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False

        if self.board[row, col] != Player.EMPTY.value:
            return False

        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1)]

        for dr, dc in directions:
            if self._can_flip_in_direction(row, col, dr, dc, player):
                return True

        return False

    def _can_flip_in_direction(
        self, row: int, col: int, dr: int, dc: int, player: Player
    ) -> bool:
        """Check if pieces can be flipped in a given direction."""
        r, c = row + dr, col + dc
        found_opponent = False

        while 0 <= r < self.size and 0 <= c < self.size:
            if self.board[r, c] == Player.EMPTY.value:
                return False
            elif self.board[r, c] == player.value:
                return found_opponent
            else:
                found_opponent = True

            r += dr
            c += dc

        return False

    def make_move(self, row: int, col: int, player: Player) -> bool:
        """Make a move and flip the appropriate pieces."""
        if not self.is_valid_move(row, col, player):
            return False

        self.board[row, col] = player.value

        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1)]

        for dr, dc in directions:
            if self._can_flip_in_direction(row, col, dr, dc, player):
                self._flip_pieces_in_direction(row, col, dr, dc, player)

        return True

    def _flip_pieces_in_direction(
        self, row: int, col: int, dr: int, dc: int, player: Player
    ) -> None:
        """Flip pieces in a given direction."""
        r, c = row + dr, col + dc

        while 0 <= r < self.size and 0 <= c < self.size:
            if self.board[r, c] == player.value:
                break
            self.board[r, c] = player.value
            r += dr
            c += dc

    def get_valid_moves(self, player: Player) -> List[Tuple[int, int]]:
        """Get all valid moves for the given player."""
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.is_valid_move(row, col, player):
                    moves.append((row, col))
        return moves

    def get_score(self) -> Tuple[int, int]:
        """Get the current score (black_score, white_score)."""
        black_score = np.sum(self.board == Player.BLACK.value)
        white_score = np.sum(self.board == Player.WHITE.value)
        return black_score, white_score

    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return (len(self.get_valid_moves(Player.BLACK)) == 0 and
                len(self.get_valid_moves(Player.WHITE)) == 0)

    def copy(self) -> "OthelloBoard":
        """Create a copy of the board."""
        new_board = OthelloBoard(self.size)
        new_board.board = self.board.copy()
        return new_board

    def __str__(self) -> str:
        """String representation of the board."""
        symbols = {Player.EMPTY.value: '.', Player.BLACK.value: 'B',
                   Player.WHITE.value: 'W'}
        result = "  " + " ".join(str(i) for i in range(self.size)) + "\n"
        for i, row in enumerate(self.board):
            result += f"{i} " + " ".join(symbols[cell] for cell in row) + "\n"
        return result


class OthelloCPU:
    """CPU player for Othello using minimax algorithm with alpha-beta pruning."""

    def __init__(self, player: Player, difficulty: int = 4) -> None:
        """Initialize the CPU player."""
        self.player = player
        self.opponent = Player.WHITE if player == Player.BLACK else Player.BLACK
        self.difficulty = difficulty

        # Position values for heuristic evaluation
        self.position_values = np.array([
            [100, -20, 10, 5, 5, 10, -20, 100],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [10, -2, -1, -1, -1, -1, -2, 10],
            [5, -2, -1, -1, -1, -1, -2, 5],
            [5, -2, -1, -1, -1, -1, -2, 5],
            [10, -2, -1, -1, -1, -1, -2, 10],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [100, -20, 10, 5, 5, 10, -20, 100]
        ])

    def get_move(self, board: OthelloBoard) -> Optional[Tuple[int, int]]:
        """Get the best move for the CPU player."""
        valid_moves = board.get_valid_moves(self.player)
        if not valid_moves:
            return None

        if self.difficulty == 1:
            return self._get_random_move(valid_moves)
        elif self.difficulty == 2:
            return self._get_greedy_move(board, valid_moves)
        else:
            return self._get_minimax_move(board, valid_moves)

    def _get_random_move(self, valid_moves: List[Tuple[int, int]]) -> Tuple[int, int]:
        """Get a random valid move."""
        return random.choice(valid_moves)

    def _get_greedy_move(
        self, board: OthelloBoard, valid_moves: List[Tuple[int, int]]
    ) -> Tuple[int, int]:
        """Get the move that flips the most pieces."""
        best_move = valid_moves[0]
        best_score = -1

        for move in valid_moves:
            test_board = board.copy()
            test_board.make_move(move[0], move[1], self.player)
            score = self._evaluate_board(test_board)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _get_minimax_move(
        self, board: OthelloBoard, valid_moves: List[Tuple[int, int]]
    ) -> Tuple[int, int]:
        """Get the best move using minimax with alpha-beta pruning."""
        best_move = valid_moves[0]
        best_score = float('-inf')

        for move in valid_moves:
            test_board = board.copy()
            test_board.make_move(move[0], move[1], self.player)

            score = self._minimax(
                test_board, self.difficulty - 1, float('-inf'),
                float('inf'), False
            )

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _minimax(
        self, board: OthelloBoard, depth: int, alpha: float,
        beta: float, is_maximizing: bool
    ) -> float:
        """Minimax algorithm with alpha-beta pruning."""
        if depth == 0 or board.is_game_over():
            return self._evaluate_board(board)

        current_player = self.player if is_maximizing else self.opponent
        valid_moves = board.get_valid_moves(current_player)

        if not valid_moves:
            # Pass turn to opponent
            return self._minimax(board, depth - 1, alpha, beta, not is_maximizing)

        if is_maximizing:
            max_score = float('-inf')
            for move in valid_moves:
                test_board = board.copy()
                test_board.make_move(move[0], move[1], current_player)
                score = self._minimax(
                    test_board, depth - 1, alpha, beta, False)
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_score
        else:
            min_score = float('inf')
            for move in valid_moves:
                test_board = board.copy()
                test_board.make_move(move[0], move[1], current_player)
                score = self._minimax(test_board, depth - 1, alpha, beta, True)
                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score

    def _evaluate_board(self, board: OthelloBoard) -> float:
        """Evaluate the board position."""
        if board.is_game_over():
            black_score, white_score = board.get_score()
            if self.player == Player.BLACK:
                if black_score > white_score:
                    return 1000
                elif black_score < white_score:
                    return -1000
                else:
                    return 0
            else:
                if white_score > black_score:
                    return 1000
                elif white_score < black_score:
                    return -1000
                else:
                    return 0

        # Combine multiple heuristics
        score = 0.0

        # Piece difference
        black_score, white_score = board.get_score()
        piece_diff = (black_score - white_score) * \
            (1 if self.player == Player.BLACK else -1)
        score += piece_diff * 10

        # Position values
        position_score = 0
        for row in range(board.size):
            for col in range(board.size):
                if board.board[row, col] == self.player.value:
                    position_score += self.position_values[row, col]
                elif board.board[row, col] == self.opponent.value:
                    position_score -= self.position_values[row, col]
        score += position_score

        # Mobility (number of valid moves)
        cpu_moves = len(board.get_valid_moves(self.player))
        opponent_moves = len(board.get_valid_moves(self.opponent))
        score += (cpu_moves - opponent_moves) * 5

        return score


class OthelloGame:
    """Main game class for Othello."""

    def __init__(
        self, board_size: int = 8, cpu_difficulty: int = 4,
        human_player: Player = Player.BLACK
    ) -> None:
        """Initialize the game."""
        self.board = OthelloBoard(board_size)
        self.human_player = human_player
        self.cpu_player = Player.WHITE if human_player == Player.BLACK else Player.BLACK
        self.cpu = OthelloCPU(self.cpu_player, cpu_difficulty)
        self.current_player = Player.BLACK  # Black always starts

    def play(self) -> None:
        """Main game loop."""
        print("Welcome to Othello!")
        print(
            f"You are playing as {'Black (B)' if self.human_player == Player.BLACK else 'White (W)'}")
        print(
            f"CPU is playing as {'White (W)' if self.cpu_player == Player.WHITE else 'Black (B)'}")
        print("\nEnter moves as 'row col' (e.g., '3 4')")
        print("Enter 'q' to quit\n")

        while not self.board.is_game_over():
            print(self.board)
            black_score, white_score = self.board.get_score()
            print(f"Score - Black: {black_score}, White: {white_score}")

            valid_moves = self.board.get_valid_moves(self.current_player)

            if not valid_moves:
                print(
                    f"No valid moves for {self.current_player.name}. Passing turn.")
                self._switch_player()
                continue

            if self.current_player == self.human_player:
                if not self._handle_human_move():
                    break
            else:
                self._handle_cpu_move()

            self._switch_player()

        self._show_final_result()

    def _handle_human_move(self) -> bool:
        """Handle human player move."""
        valid_moves = self.board.get_valid_moves(self.current_player)
        print(f"\nValid moves for {self.current_player.name}: {valid_moves}")

        while True:
            try:
                move_input = input(f"Enter your move (row col): ").strip()
                if move_input.lower() == 'q':
                    return False

                row, col = map(int, move_input.split())

                if self.board.make_move(row, col, self.current_player):
                    print(f"Move made: ({row}, {col})")
                    return True
                else:
                    print("Invalid move. Try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter 'row col' or 'q' to quit.")

    def _handle_cpu_move(self) -> None:
        """Handle CPU player move."""
        print(f"\nCPU ({self.cpu_player.name}) is thinking...")
        move = self.cpu.get_move(self.board)

        if move:
            self.board.make_move(move[0], move[1], self.current_player)
            print(f"CPU played: ({move[0]}, {move[1]})")
        else:
            print("CPU has no valid moves.")

    def _switch_player(self) -> None:
        """Switch to the other player."""
        self.current_player = (
            Player.WHITE if self.current_player == Player.BLACK else Player.BLACK
        )

    def _show_final_result(self) -> None:
        """Show the final game result."""
        print("\nFinal Board:")
        print(self.board)

        black_score, white_score = self.board.get_score()
        print(f"\nFinal Score - Black: {black_score}, White: {white_score}")

        if black_score > white_score:
            winner = "Black"
        elif white_score > black_score:
            winner = "White"
        else:
            winner = "Tie"

        print(f"Winner: {winner}")

        if winner == "Tie":
            print("It's a tie!")
        elif (winner == "Black" and self.human_player == Player.BLACK) or \
             (winner == "White" and self.human_player == Player.WHITE):
            print("Congratulations! You won!")
        else:
            print("CPU won! Better luck next time.")


def main() -> None:
    """Main function to start the game."""
    print("Othello Game Setup")
    print("1. Play as Black (you go first)")
    print("2. Play as White (CPU goes first)")

    while True:
        try:
            choice = input("Choose (1 or 2): ").strip()
            if choice == "1":
                human_player = Player.BLACK
                break
            elif choice == "2":
                human_player = Player.WHITE
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            return

    print("\nDifficulty levels:")
    print("1. Easy (Random moves)")
    print("2. Medium (Greedy moves)")
    print("3. Hard (Minimax depth 3)")
    print("4. Very Hard (Minimax depth 4)")
    print("5. Expert (Minimax depth 5)")

    while True:
        try:
            difficulty = int(input("Choose difficulty (1-5): ").strip())
            if 1 <= difficulty <= 5:
                break
            else:
                print("Invalid choice. Please enter 1-5.")
        except (ValueError, KeyboardInterrupt):
            print("Invalid input. Please enter a number 1-5.")

    game = OthelloGame(human_player=human_player, cpu_difficulty=difficulty)
    game.play()


if __name__ == "__main__":
    main()
