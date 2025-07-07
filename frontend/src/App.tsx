import { useState, useEffect } from 'react'
import OthelloBoard from './components/OthelloBoard'
import GameInfo from './components/GameInfo'
import { Player, GameState } from './types/game'
import { othelloAPI } from './api/othelloAPI'
import './App.css'

function App() {
  const [gameState, setGameState] = useState<GameState>({
    board: Array(8).fill(null).map(() => Array(8).fill(Player.EMPTY)),
    currentPlayer: Player.BLACK,
    blackScore: 2,
    whiteScore: 2,
    gameOver: false,
    winner: null,
    validMoves: [],
    difficulty: 4,
    humanPlayer: Player.BLACK,
  })

  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // 初期ゲームの開始
  useEffect(() => {
    startNewGame()
  }, [])

  const startNewGame = async (): Promise<void> => {
    try {
      setIsLoading(true)
      setError(null)
      
      const apiState = await othelloAPI.newGame()
      
      setGameState({
        board: apiState.board.map(row => row.map(cell => cell as Player)),
        currentPlayer: apiState.current_player as Player,
        blackScore: apiState.black_score,
        whiteScore: apiState.white_score,
        gameOver: apiState.game_over,
        winner: apiState.winner as Player | null,
        validMoves: apiState.valid_moves,
        difficulty: 4,
        humanPlayer: Player.BLACK,
      })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start new game')
    } finally {
      setIsLoading(false)
    }
  }

  // 手を実行
  const makeMove = async (row: number, col: number): Promise<void> => {
    if (isLoading || gameState.gameOver) return

    try {
      setIsLoading(true)
      setError(null)

      // 人間の手をAPIに送信
      const apiState = await othelloAPI.makeMove(
        gameState.board.map(row => row.map(cell => cell)),
        row,
        col,
        gameState.currentPlayer
      )

      const newGameState: GameState = {
        board: apiState.board.map(row => row.map(cell => cell as Player)),
        currentPlayer: apiState.current_player as Player,
        blackScore: apiState.black_score,
        whiteScore: apiState.white_score,
        gameOver: apiState.game_over,
        winner: apiState.winner as Player | null,
        validMoves: apiState.valid_moves,
        difficulty: gameState.difficulty,
        humanPlayer: gameState.humanPlayer,
      }

      setGameState(newGameState)

      // CPUの手を実行（人間の手の後で、ゲームが終了していない場合）
      if (!apiState.game_over && apiState.current_player !== gameState.humanPlayer) {
        setTimeout(() => {
          makeCPUMove(apiState.board, apiState.current_player as Player)
        }, 500)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to make move')
    } finally {
      setIsLoading(false)
    }
  }

  // CPUの手を実行
  const makeCPUMove = async (board: number[][], player: Player): Promise<void> => {
    try {
      setIsLoading(true)
      
      const cpuResponse = await othelloAPI.getCPUMove(board, player, gameState.difficulty)
      
      if (cpuResponse.move === null) {
        // CPUに有効な手がない場合はパス
        console.log('CPU has no valid moves, passing turn')
        return
      }

      const newGameState: GameState = {
        board: cpuResponse.new_board.map(row => row.map(cell => cell as Player)),
        currentPlayer: gameState.humanPlayer, // CPUの後は人間のターン
        blackScore: cpuResponse.black_score,
        whiteScore: cpuResponse.white_score,
        gameOver: cpuResponse.valid_moves.length === 0, // 有効手がなければゲーム終了
        winner: null, // 勝者判定はサーバー側で行う
        validMoves: cpuResponse.valid_moves,
        difficulty: gameState.difficulty,
        humanPlayer: gameState.humanPlayer,
      }

      // 勝者判定
      if (newGameState.gameOver) {
        if (newGameState.blackScore > newGameState.whiteScore) {
          newGameState.winner = Player.BLACK
        } else if (newGameState.whiteScore > newGameState.blackScore) {
          newGameState.winner = Player.WHITE
        }
      }

      setGameState(newGameState)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get CPU move')
    } finally {
      setIsLoading(false)
    }
  }

  // ゲームをリセット
  const resetGame = (): void => {
    startNewGame()
  }

  // 難易度を変更
  const changeDifficulty = (difficulty: number): void => {
    setGameState(prev => ({ ...prev, difficulty }))
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>オセロゲーム</h1>
        {error && (
          <div className="error-message">
            エラー: {error}
          </div>
        )}
      </header>
      <main className="app-main">
        <div className="game-container">
          <GameInfo 
            gameState={gameState}
            onReset={resetGame}
            onChangeDifficulty={changeDifficulty}
            isLoading={isLoading}
          />
          <OthelloBoard 
            board={gameState.board}
            validMoves={gameState.validMoves}
            currentPlayer={gameState.currentPlayer}
            onMove={makeMove}
            isHumanTurn={gameState.currentPlayer === gameState.humanPlayer && !isLoading}
            isLoading={isLoading}
          />
        </div>
      </main>
    </div>
  )
}

export default App
