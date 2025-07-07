import { Player, GameInfoProps } from '../types/game'
import './GameInfo.css'

const GameInfo = ({ 
  gameState, 
  onReset, 
  onChangeDifficulty, 
  isLoading = false 
}: GameInfoProps) => {
  const getPlayerName = (player: Player): string => {
    return player === Player.BLACK ? '黒' : '白'
  }

  const getCurrentPlayerDisplay = (): string => {
    if (gameState.gameOver) {
      if (gameState.winner === null) {
        return '引き分け'
      }
      return `${getPlayerName(gameState.winner)}の勝利！`
    }
    
    const playerName = getPlayerName(gameState.currentPlayer)
    const isHumanTurn = gameState.currentPlayer === gameState.humanPlayer
    
    return `${playerName}の番 ${isHumanTurn ? '(あなた)' : '(CPU)'}`
  }

  const difficultyNames = ['', 'かんたん', 'ふつう', 'むずかしい', 'とてもむずかしい', 'エキスパート']

  return (
    <div className="game-info">
      <div className="score-section">
        <h2>スコア</h2>
        <div className="scores">
          <div className="score-item">
            <span className="score-label">黒 (●)</span>
            <span className="score-value">{gameState.blackScore}</span>
          </div>
          <div className="score-item">
            <span className="score-label">白 (○)</span>
            <span className="score-value">{gameState.whiteScore}</span>
          </div>
        </div>
      </div>
      
      <div className="status-section">
        <h3 className="current-player">
          {getCurrentPlayerDisplay()}
        </h3>
        {gameState.validMoves.length > 0 && !gameState.gameOver && (
          <p className="valid-moves-count">
            有効な手: {gameState.validMoves.length}個
          </p>
        )}
        {isLoading && (
          <p className="loading-indicator">
            処理中...
          </p>
        )}
      </div>
      
      {onChangeDifficulty && (
        <div className="difficulty-section">
          <h4>CPU難易度</h4>
          <select 
            value={gameState.difficulty} 
            onChange={(e) => onChangeDifficulty(parseInt(e.target.value))}
            disabled={isLoading}
          >
            {[1, 2, 3, 4, 5].map(level => (
              <option key={level} value={level}>
                {level}. {difficultyNames[level]}
              </option>
            ))}
          </select>
        </div>
      )}
      
      <div className="controls-section">
        <button 
          className="reset-button"
          onClick={onReset}
          disabled={isLoading}
        >
          ゲームリセット
        </button>
      </div>
      
      {gameState.gameOver && (
        <div className="game-over-section">
          <h3>ゲーム終了</h3>
          <p className="final-result">
            {gameState.winner === null 
              ? '引き分けです！' 
              : `${getPlayerName(gameState.winner)}の勝利です！`
            }
          </p>
        </div>
      )}
    </div>
  )
}

export default GameInfo
