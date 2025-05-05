from flask import Flask, request
from flask_socketio import SocketIO, emit

#Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"

# Initialize Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

players = [None, None]
player_count = 0
board = []
turn = 0

@app.route('/')
def index():
    return "Flask SocketIO server is running"

@socketio.on("connect")
def handle_connect():
    global player_count

    # Choose what player to assign to, if available slots
    if player_count < 2:
        user = 0
        if (players[0] == None):
            players[0] = request.sid 
            user = 0
            print("Player 1 Connected")

        elif (players[1] == None):
            players[1] = request.sid
            print("Player 2 Connected")
            user = 1

        player_count += 1
        print(players)
        emit("player_connected", {"players": players, "user": user}, broadcast=True)

        if player_count == 2:
            init()

    else:
        emit("room_full", {"message": "Game is full. Try again later."})
        print("A user tried to connect, but the game is full.")

# Create the board and start the game
def init():
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    emit("init_game", {"board": board}, broadcast=True)

    start_game()

# Kick off the game with whoever's turn it is
def start_game():
    global turn
    emit("your_turn", to=players[turn])


# Process move, if valid send to clients
@socketio.on("user_moved")
def process_move(data):
    print("user moved emitted")

    global turn
    user = data["user"]
    r,c = data["r"], data["c"]
    legal = check_move(user, r, c)

    if legal:
        if user == 0:
            board[r][c] = 'X'
        else:
            board[r][c] = 'O'

        emit("move", {"board": board}, broadcast=True)
        status = check_game_over()
        if status != " ":
            emit("game_over", {"status": status}, broadcast=True)
        else:
            turn = 1 - turn  # Switch turn
            emit("your_turn", to=players[turn])  # Notify the next player

    else:
        emit("illegal_move", to=players[user])

# Check validity
def check_move(user, r, c):
    if board[r][c] == ' ':
        return True
    return False

# Check if someone has won/there is a tie
def check_game_over():
    for row in board:
        if row[0] != ' ' and (row[0] == row[1] == row[2]):
            return row[0]

    for col in range(3):
        if board[0][col] != ' ' and (board[0][col] == board[1][col] == board[2][col]):
            return board[0][col]

    if board[0][0] != ' ' and (board[0][0] == board[1][1] == board[2][2]):
        return board[0][0]

    if board[0][2] != ' ' and (board[0][2] == board[1][1] == board[2][0]):
        return board[0][2]
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                return ' '
    return 'TIE'
    
@socketio.on("disconnect")
def handle_disconnect():
    global player_count
    player_count -= 1
    user = -1
    if request.sid == players[0]:
        user = 0
        players[0] = None

    elif request.sid == players[1]:
        user = 1
        players[1] = None

    emit("player_disconnected", {"players": players, "user": user}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)