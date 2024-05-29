from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, join_room, leave_room, send
from datetime import datetime

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///matchmaking.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50))
    port = db.Column(db.Integer)
    pseudo = db.Column(db.String(50))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_ip = db.Column(db.String(50))
    player1_port = db.Column(db.Integer)
    player2_ip = db.Column(db.String(50))
    player2_port = db.Column(db.Integer)
    board_state = db.Column(db.String(500), default="initial")
    finished = db.Column(db.Boolean, default=False)
    winner = db.Column(db.String(50), nullable=True)

class Turn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    player = db.Column(db.String(50))
    move = db.Column(db.String(50))

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/enqueue', methods=['POST'])
def enqueue():
    data = request.json
    new_entry = Queue(ip=data['ip'], port=data['port'], pseudo=data['pseudo'])
    db.session.add(new_entry)
    db.session.commit()
    check_for_match()
    return jsonify({'status': 'queued'})

@socketio.on('join_queue')
def handle_join_queue(data):
    new_entry = Queue(ip=data['ip'], port=data['port'], pseudo=data['pseudo'])
    db.session.add(new_entry)
    db.session.commit()
    check_for_match()

def check_for_match():
    queue_entries = Queue.query.all()
    if len(queue_entries) >= 2:
        player1 = queue_entries[0]
        player2 = queue_entries[1]
        new_match = Match(player1_ip=player1.ip, player1_port=player1.port,
                          player2_ip=player2.ip, player2_port=player2.port)
        db.session.add(new_match)
        db.session.delete(player1)
        db.session.delete(player2)
        db.session.commit()
        socketio.emit('match_start', {'player1': player1.pseudo, 'player2': player2.pseudo})

@socketio.on('move')
def handle_move(data):
    match_id = data['match_id']
    move = data['move']
    player = data['player']
    new_turn = Turn(match_id=match_id, player=player, move=move)
    db.session.add(new_turn)
    db.session.commit()
    match = Match.query.get(match_id)
    match.board_state = data['board_state']
    db.session.commit()
    send(data, room=match_id)

@socketio.on('end_match')
def handle_end_match(data):
    match_id = data['match_id']
    winner = data['winner']
    match = Match.query.get(match_id)
    match.finished = True
    match.winner = winner
    db.session.commit()
    send({'status': 'finished', 'winner': winner}, room=match_id)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
