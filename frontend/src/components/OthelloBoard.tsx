import { Player, BoardProps } from '../types/game'
import './OthelloBoard.css'

const OthelloBoard = ({ 
  board, 
  validMoves, 
  currentPlayer, 
  onMove, 
  isHumanTurn, 
  isLoading = false 
}: BoardProps) => {
  const isValidMove = (row: number, col: number): boolean => {
    return validMoves.some(([r, c]) => r === row && c === col)
  }

  const getCellClass = (row: number, col: number): string => {
    const baseClass = 'cell'
    const piece = board[row][col]
    
    let classes = [baseClass]
    
    if (piece === Player.BLACK) {
      classes.push('black')
    } else if (piece === Player.WHITE) {
      classes.push('white')
    }
    
    if (isValidMove(row, col) && isHumanTurn && !isLoading) {
      classes.push('valid-move')
    }
    
    return classes.join(' ')
  }

  const handleCellClick = (row: number, col: number): void => {
    if (isHumanTurn && !isLoading && isValidMove(row, col)) {
      onMove(row, col)
    }
  }

  const renderPiece = (piece: Player) => {
    if (piece === Player.EMPTY) return null
    
    return (
      <div className={`piece ${piece === Player.BLACK ? 'black' : 'white'}`}>
        {piece === Player.BLACK ? '●' : '○'}
      </div>
    )
  }

  return (
    <div className={`board-container ${isLoading ? 'loading' : ''}`}>
      {isLoading && (
        <div className="loading-overlay">
          <div className="loading-spinner">⭘</div>
          <p>CPUが考え中...</p>
        </div>
      )}
      <div className="board">
        {board.map((row, rowIndex) => (
          <div key={rowIndex} className="row">
            {row.map((cell, colIndex) => (
              <div
                key={`${rowIndex}-${colIndex}`}
                className={getCellClass(rowIndex, colIndex)}
                onClick={() => handleCellClick(rowIndex, colIndex)}
              >
                {renderPiece(cell)}
                {isValidMove(rowIndex, colIndex) && isHumanTurn && !isLoading && (
                  <div className="valid-move-indicator">
                    <div className={`preview-piece ${currentPlayer === Player.BLACK ? 'black' : 'white'}`}>
                      {currentPlayer === Player.BLACK ? '●' : '○'}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}

export default OthelloBoard
