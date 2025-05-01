import pygame
import sys
import math
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 780, 780
SQUARE_SIZE = WIDTH // 8
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
LIGHT_GRAY = (200, 200, 200)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Load piece images
def load_image(name):
    img = pygame.image.load(f"images/{name}.png")
    return pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))

# Piece class
class ChessPiece:
    def __init__(self, color, type, image_name):
        self.color = color
        self.type = type
        self.image = load_image(image_name)
        self.has_moved = False

    def __repr__(self):
        return f"{self.color[0].upper()}{self.type[0].upper()}"

# Game state
board = [[None for _ in range(8)] for _ in range(8)]
current_player = 'white'
selected_piece = None
selected_pos = None
game_mode = None

# Initialize board
def init_board():
    global board, current_player
    board = [[None for _ in range(8)] for _ in range(8)]
    current_player = 'white'
    for col in range(8):
        board[1][col] = ChessPiece('black', 'pawn', 'black_pawn')
        board[6][col] = ChessPiece('white', 'pawn', 'white_pawn')
    board[0][0] = board[0][7] = ChessPiece('black', 'rook', 'black_rook')
    board[7][0] = board[7][7] = ChessPiece('white', 'rook', 'white_rook')
    board[0][1] = board[0][6] = ChessPiece('black', 'knight', 'black_knight')
    board[7][1] = board[7][6] = ChessPiece('white', 'knight', 'white_knight')
    board[0][2] = board[0][5] = ChessPiece('black', 'bishop', 'black_bishop')
    board[7][2] = board[7][5] = ChessPiece('white', 'bishop', 'white_bishop')
    board[0][3] = ChessPiece('black', 'queen', 'black_queen')
    board[7][3] = ChessPiece('white', 'queen', 'white_queen')
    board[0][4] = ChessPiece('black', 'king', 'black_king')
    board[7][4] = ChessPiece('white', 'king', 'white_king')

# Draw board
def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    if selected_pos:
        pygame.draw.rect(screen, YELLOW, (selected_pos[1] * SQUARE_SIZE, selected_pos[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

# Draw pieces
def draw_pieces():
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                screen.blit(piece.image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Get valid moves
def get_valid_moves(piece, row, col):
    moves = []
    if piece:
        if piece.type == 'pawn':
            direction = -1 if piece.color == 'white' else 1
            # Move forward one square
            new_row = row + direction
            if 0 <= new_row < 8 and board[new_row][col] is None:
                moves.append((new_row, col))
                # Move forward two squares on first move
                if not piece.has_moved and 0 <= row + 2 * direction < 8 and board[row + 2 * direction][col] is None:
                    moves.append((row + 2 * direction, col))
            # Capture diagonally
            for dc in [-1, 1]:
                new_col = col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8 and board[new_row][new_col] and board[new_row][new_col].color != piece.color:
                    moves.append((new_row, new_col))
        elif piece.type == 'rook':
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                for i in range(1, 8):
                    new_row, new_col = row + dr * i, col + dc * i
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        target = board[new_row][new_col]
                        if target is None:
                            moves.append((new_row, new_col))
                        else:
                            if target.color != piece.color:
                                moves.append((new_row, new_col))
                            break
                    else:
                        break
        elif piece.type == 'knight':
            for dr, dc in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8 and (board[new_row][new_col] is None or board[new_row][new_col].color != piece.color):
                    moves.append((new_row, new_col))
        elif piece.type == 'bishop':
            for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                for i in range(1, 8):
                    new_row, new_col = row + dr * i, col + dc * i
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        target = board[new_row][new_col]
                        if target is None:
                            moves.append((new_row, new_col))
                        else:
                            if target.color != piece.color:
                                moves.append((new_row, new_col))
                            break
                    else:
                        break
        elif piece.type == 'queen':
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                for i in range(1, 8):
                    new_row, new_col = row + dr * i, col + dc * i
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        target = board[new_row][new_col]
                        if target is None:
                            moves.append((new_row, new_col))
                        else:
                            if target.color != piece.color:
                                moves.append((new_row, new_col))
                            break
                    else:
                        break
        elif piece.type == 'king':
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    if dr == 0 and dc == 0:
                        continue
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < 8 and 0 <= new_col < 8 and (board[new_row][new_col] is None or board[new_row][new_col].color != piece.color):
                        moves.append((new_row, new_col))
    return moves

# Evaluate the board
def evaluate_board():
    value_map = {'pawn': 1, 'rook': 5, 'knight': 3, 'bishop': 3, 'queen': 9, 'king': 1000}
    value = 0
    for row in board:
        for piece in row:
            if piece:
                if piece.color == 'white':
                    value -= value_map[piece.type]
                else:
                    value += value_map[piece.type]
    return value

def minimax(depth, alpha, beta, maximizing_player):
    if depth == 0:
        return evaluate_board(), None  # Return evaluation and no move

    if maximizing_player:
        max_eval = -math.inf
        best_move = None
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece and piece.color == 'black':
                    for move_r, move_c in get_valid_moves(piece, r, c):
                        original_piece = board[move_r][move_c]
                        board[move_r][move_c] = piece
                        board[r][c] = None
                        piece.has_moved = True
                        eval, _ = minimax(depth - 1, alpha, beta, False)
                        board[r][c] = piece
                        board[move_r][move_c] = original_piece
                        piece.has_moved = False
                        if eval > max_eval:
                            max_eval = eval
                            best_move = (r, c, move_r, move_c)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        best_move = None
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece and piece.color == 'white':
                    for move_r, move_c in get_valid_moves(piece, r, c):
                        original_piece = board[move_r][move_c]
                        board[move_r][move_c] = piece
                        board[r][c] = None
                        piece.has_moved = True
                        eval, _ = minimax(depth - 1, alpha, beta, True)
                        board[r][c] = piece
                        board[move_r][move_c] = original_piece
                        piece.has_moved = False
                        if eval < min_eval:
                            min_eval = eval
                            best_move = (r, c, move_r, move_c)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            if beta <= alpha:
                break
        return min_eval, best_move

# AI move
def ai_make_move():
    global current_player
    _, move = minimax(3, -math.inf, math.inf, True)  # Increased depth for better AI
    if move:
        r, c, move_r, move_c = move
        piece = board[r][c]
        board[move_r][move_c] = piece
        board[r][c] = None
        piece.has_moved = True
        current_player = 'white'

# Handle click
def handle_click(pos):
    global selected_piece, selected_pos, current_player
    col = pos[0] // SQUARE_SIZE
    row = pos[1] // SQUARE_SIZE
    if selected_piece is None:
        piece = board[row][col]
        if piece and piece.color == current_player:
            selected_piece = piece
            selected_pos = (row, col)
    else:
        if (row, col) in get_valid_moves(selected_piece, selected_pos[0], selected_pos[1]):
            board[row][col] = selected_piece
            board[selected_pos[0]][selected_pos[1]] = None
            selected_piece.has_moved = True
            selected_piece = None
            selected_pos = None
            current_player = 'black' if current_player == 'white' else 'white'
        else:
            # Deselect if clicked on an empty square or a square with an opponent's piece
            piece = board[row][col]
            if not piece or piece.color != current_player:
                selected_piece = None
                selected_pos = None
            # Select a new piece if clicked on a square with the current player's piece
            elif piece.color == current_player:
                selected_piece = piece
                selected_pos = (row, col)

# Game mode screen
def draw_game_mode_selection():
    screen.fill(LIGHT_GRAY)
    font = pygame.font.SysFont(None, 60)
    title = font.render("Select Game Mode", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
    pygame.draw.rect(screen, GREEN, (250, 300, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=20)
    pygame.draw.rect(screen, RED, (250, 450, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=20)
    button_font = pygame.font.SysFont(None, 40)
    pvp = button_font.render("Player vs Player", True, WHITE)
    pva = button_font.render("Player vs AI", True, WHITE)
    screen.blit(pvp, (WIDTH//2 - pvp.get_width()//2, 330))
    screen.blit(pva, (WIDTH//2 - pva.get_width()//2, 480))

# Main loop
init_board()
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_mode is None:
                x, y = event.pos
                if 250 <= x <= 550 and 300 <= y <= 400:
                    game_mode = 'player_vs_player'
                    init_board()
                elif 250 <= x <= 550 and 450 <= y <= 550:
                    game_mode = 'player_vs_ai'
                    init_board()
            else:
                handle_click(event.pos)

    if game_mode is None:
        draw_game_mode_selection()
    else:
        draw_board()
        draw_pieces()
        if game_mode == 'player_vs_ai' and current_player == 'black':
            pygame.time.delay(300)
            ai_make_move()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()