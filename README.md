# Tic-Tac-Two

A real-time multiplayer Tic-Tac-Toe game built with Flask-SocketIO and JavaScript.

## Features
- Two-player real-time gameplay
- WebSocket communication using Flask-SocketIO
- Turn-based logic with automatic updates for both players
- Win detection and game-over handling
- Simple and interactive UI

## Technologies Used
- **Backend:** Flask, Flask-SocketIO
- **Frontend:** HTML, JavaScript
- **WebSockets:** Socket.IO

## Installation

### Prerequisites
Ensure you have **Python 3.x** and **pip** installed on your system.

### Install Dependencies
```bash
pip install flask flask-socketio
```

## Running the Server
```bash
python app.py
```
The server will start on `http://localhost:5000`.

## Playing the Game
1. Have both players open `client.html` in your browser.
2. Each player will be assigned **Player 1 (X)** or **Player 2 (O)** automatically.
3. Take turns placing marks on the board.
4. The game announces a winner or a draw when the conditions are met.

## Folder Structure
```
📁 TicTacTwo
│── 📄 app.py        # Flask-SocketIO server
│── 📄 client.html      # Frontend UI for the game
│── 📄 README.md        # Project documentation
```

## WebSocket Events
### Server Events
- **`connect`**: Assigns players and starts the game.
- **`disconnect`**: Notifies each client when a player disconnects.
- **`your_turn`**: Notifies a player when it's their turn.
- **`move`**: Broadcasts a player's move to update the board.
- **`game_over`**: Notifies all players when the game ends.

### Client Events
- **`user_moved`**: Sent when a player makes a move.

## TODO / Future Improvements
- Add a **`reset`** button to restart the game.
- Add CSS to improve the design.
- Fix minor bugs with reconnecting.



