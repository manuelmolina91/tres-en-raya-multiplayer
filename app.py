from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Variables globales del juego.
players = ['X', 'O', 'Y']  # Tres jugadores.
board = [[' ' for _ in range(3)] for _ in range(3)]
current_player = None
game_over = False

@app.route('/')
def index():
    return render_template('index.html')

# Reiniciar el juego.
@app.route('/restart', methods=['POST'])
def restart_game():
    global board, current_player, game_over
    board = [[' ' for _ in range(3)] for _ in range(3)]
    game_over = False
    return jsonify({"board": board, "current_player": current_player, "game_over": game_over})

# Obtener el tablero y estado del juego.
@app.route('/roll_dice', methods=['POST'])
def roll_dice():
    global current_player
    rolls = {player: random.randint(1, 6) for player in players}
    sorted_rolls = sorted(rolls.items(), key=lambda x: x[1], reverse=True)
    current_player = sorted_rolls[0][0]
    return jsonify({"rolls": rolls, "first_player": current_player})

# Manejo de turnos y movimiento.
@app.route('/move', methods=['POST'])
def make_move():
    global current_player, game_over
    data = request.json
    row, col = data['row'], data['col']

    if board[row][col] == ' ' and not game_over:
        board[row][col] = current_player
        if check_winner():
            game_over = True
            return jsonify({"winner": current_player})
        current_player = players[(players.index(current_player) + 1) % 3]  # Cambiar al siguiente jugador.
        return jsonify({"status": "moved", "next_player": current_player})
    return jsonify({"status": "invalid"})

# Verificar si hay un ganador.
def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return True
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return True
    if board[0][0] == board[1][1] == board[2][2] != ' ' or board[0][2] == board[1][1] == board[2][0] != ' ':
        return True
    return False

if __name__ == '__main__':
    app.run(debug=True)