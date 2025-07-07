export enum Player {
  EMPTY = 0,
  BLACK = 1,
  WHITE = -1,
}

export interface GameState {
  board: Player[][]
  currentPlayer: Player
  blackScore: number
  whiteScore: number
  gameOver: boolean
  winner: Player | null
  validMoves: [number, number][]
  difficulty: number
  humanPlayer: Player
}

export interface BoardProps {
  board: Player[][]
  validMoves: [number, number][]
  currentPlayer: Player
  onMove: (row: number, col: number) => void
  isHumanTurn: boolean
  isLoading?: boolean
}

export interface GameInfoProps {
  gameState: GameState
  onReset: () => void
  onChangeDifficulty?: (difficulty: number) => void
  isLoading?: boolean
}
