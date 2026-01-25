// SwiftLogistics WMS Mock
// TCP Server Simulator

const net = require('net');
const PORT = process.env.PORT || 4002;

const server = net.createServer((socket) => {
  console.log('📨 WMS Mock: Client connected');

  socket.on('data', (data) => {
    console.log('📦 WMS Mock received:', data.toString());
    const response = JSON.stringify({
      status: 'SUCCESS',
      shelfLocation: 'A-15-03',
      pickTime: new Date().toISOString()
    });
    socket.write(response);
  });

  socket.on('end', () => {
    console.log('👋 WMS Mock: Client disconnected');
  });

  socket.on('error', (err) => {
    console.error('❌ WMS Mock error:', err.message);
  });
});

server.listen(PORT, () => {
  console.log(`✅ WMS Mock (TCP) listening on port ${PORT}`);
});
