// models.js
const mongoose = require('mongoose');
const { Schema } = mongoose;

const queueSchema = new Schema({
  communication: {
    ip: String,
    port: Number
  },
  pseudo: String,
  dateJoined: { type: Date, default: Date.now }
});

const matchSchema = new Schema({
  player1: {
    communication: {
      ip: String,
      port: Number
    },
    pseudo: String
  },
  player2: {
    communication: {
      ip: String,
      port: Number
    },
    pseudo: String
  },
  board: String, // Serialized board state
  isFinished: { type: Boolean, default: false },
  result: { type: String, enum: ['player1', 'player2', 'draw', 'ongoing'], default: 'ongoing' }
});

const turnSchema = new Schema({
  match: { type: Schema.Types.ObjectId, ref: 'Match' },
  player: { type: String, enum: ['player1', 'player2'] },
  move: String, // Describe the move
  timestamp: { type: Date, default: Date.now }
});

const Queue = mongoose.model('Queue', queueSchema);
const Match = mongoose.model('Match', matchSchema);
const Turn = mongoose.model('Turn', turnSchema);

module.exports = { Queue, Match, Turn };
