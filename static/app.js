const socket = io();

document.getElementById('queueForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const pseudo = document.getElementById('pseudo').value;
    socket.emit('join_queue', { ip: '127.0.0.1', port: 5000, pseudo });
});

socket.on('match_start', function(data) {
    document.getElementById('queue').style.display = 'none';
    document.getElementById('game').style.display = 'block';
    // Initialize the game board and handle game logic here
});

socket.on('move', function(data) {
    // Update the board with the new move
});

document.getElementById('endGame').addEventListener('click', function() {
    const matchId = 1; // Example match ID
    socket.emit('end_match', { match_id: matchId, winner: 'player1' });
});
