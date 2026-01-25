// SwiftLogistics Notification Service
// Real-time WebSocket updates

const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);
const PORT = process.env.PORT || 3002;

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'notification-service' });
});

app.get('/', (req, res) => {
  res.json({ 
    message: 'SwiftLogistics Notification Service', 
    version: '1.0.0',
    websocket: 'active'
  });
});

io.on('connection', (socket) => {
  console.log('📱 Client connected:', socket.id);
  
  socket.on('disconnect', () => {
    console.log('📴 Client disconnected:', socket.id);
  });
});

server.listen(PORT, () => {
  console.log(`✅ Notification Service listening on port ${PORT}`);
});
