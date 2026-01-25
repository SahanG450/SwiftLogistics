// SwiftLogistics ROS Mock
// REST API Simulator

const express = require('express');
const app = express();
const PORT = process.env.PORT || 4001;

app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'ros-mock' });
});

app.post('/optimize-route', (req, res) => {
  console.log('📨 ROS Mock received route optimization request');
  res.json({
    route: [
      { lat: 6.9271, lng: 79.8612, order: 1 },
      { lat: 7.2906, lng: 80.6337, order: 2 }
    ],
    distance: 115.5,
    duration: 150,
    status: 'SUCCESS'
  });
});

app.listen(PORT, () => {
  console.log(`✅ ROS Mock (REST) listening on port ${PORT}`);
});
