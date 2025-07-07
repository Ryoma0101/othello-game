// API client for communicating with Python backend
const API_BASE_URL = 'http://localhost:8000'

export interface ApiGameState {
  board: number[][]
  current_player: number
  black_score: number
  white_score: number
  game_over: boolean
  winner: number | null
  valid_moves: [number, number][]
}

export interface CPUMoveResponse {
  move: [number, number] | null
  new_board: number[][]
  black_score: number
  white_score: number
  valid_moves: [number, number][]
}

class OthelloAPI {
  async newGame(): Promise<ApiGameState> {
    const response = await fetch(`${API_BASE_URL}/api/game/new`)
    if (!response.ok) {
      throw new Error('Failed to start new game')
    }
    return response.json()
  }

  async makeMove(board: number[][], row: number, col: number, player: number): Promise<ApiGameState> {
    const response = await fetch(`${API_BASE_URL}/api/game/move`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        board,
        row,
        col,
        player,
      }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to make move')
    }

    return response.json()
  }

  async getCPUMove(board: number[][], player: number, difficulty: number = 4): Promise<CPUMoveResponse> {
    const response = await fetch(`${API_BASE_URL}/api/game/cpu-move`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        board,
        player,
        difficulty,
      }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to get CPU move')
    }

    return response.json()
  }

  async getValidMoves(player: number, boardState?: number[][]): Promise<[number, number][]> {
    let url = `${API_BASE_URL}/api/game/valid-moves/${player}`
    
    if (boardState) {
      url += `?board_state=${encodeURIComponent(JSON.stringify(boardState))}`
    }

    const response = await fetch(url)
    if (!response.ok) {
      throw new Error('Failed to get valid moves')
    }

    const data = await response.json()
    return data.valid_moves
  }
}

export const othelloAPI = new OthelloAPI()
