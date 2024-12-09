import chess
import chess.svg
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io

class ChessGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Chess Game")
        
        self.board = chess.Board()
        self.moves_history = []
        self.selected_square = None
        
        self.canvas = tk.Canvas(master, width=600, height=600)
        self.canvas.pack()
        
        self.canvas.bind("<Button-1>", self.on_square_click)
        self.draw_board()
        
        self.update_status()
    
    def draw_board(self):
        """Draw the chess board."""
        self.canvas.delete("all")
        colors = ["#eee", "#ddd"]
        
        # Draw squares
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                self.canvas.create_rectangle(col * 75, row * 75, (col + 1) * 75, (row + 1) * 75, fill=color)

        # Draw pieces
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                self.draw_piece(piece, square)

    def draw_piece(self, piece, square):
        """Draw a piece on the board."""
        piece_map = {
            chess.PAWN: "P", chess.ROOK: "R", chess.KNIGHT: "N",
            chess.BISHOP: "B", chess.QUEEN: "Q", chess.KING: "K"
        }
        color = "white" if piece.color == chess.WHITE else "black"
        piece_symbol = piece_map[piece.piece_type]
        
        x = (square % 8) * 75 + 37.5
        y = (7 - square // 8) * 75 + 37.5
        
        self.canvas.create_text(x, y, text=piece_symbol, font=("Arial", 36), fill=color)

    def on_square_click(self, event):
        """Handle square clicks."""
        col = event.x // 75
        row = 7 - (event.y // 75)
        square = chess.square(col, row)

        if self.selected_square is None:
            # Select the square
            if self.board.piece_at(square) and self.board.turn == self.board.piece_at(square).color:
                self.selected_square = square
                self.highlight_square(square)
        else:
            # Make the move
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.moves_history.append(move.uci())
                self.selected_square = None
                self.update_status()
            else:
                messagebox.showinfo("Invalid Move", "This move is not allowed.")
                self.selected_square = None

        self.draw_board()
    
    def highlight_square(self, square):
        """Highlight the selected square."""
        x = (square % 8) * 75
        y = (7 - square // 8) * 75
        self.canvas.create_rectangle(x, y, x + 75, y + 75, outline="red", width=5)
    
    def update_status(self):
        """Update the game status."""
        if self.board.is_checkmate():
            messagebox.showinfo("Game Over", "Checkmate! Game over.")
            self.master.quit()
        elif self.board.is_stalemate():
            messagebox.showinfo("Game Over", "Stalemate! Game over.")
            self.master.quit()
        elif self.board.is_insufficient_material():
            messagebox.showinfo("Game Over", "Insufficient material! Game over.")
            self.master.quit()
        elif self.board.is_check():
            messagebox.showinfo("Check", "Your King is in Check!")

def main():
    root = tk.Tk()
    game = ChessGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
