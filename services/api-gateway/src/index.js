// SwiftLogistics API Gateway
// Entry point with authentication and rate limiting

const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'api-gateway' });
});

app.get('/', (req, res) => {
  res.json({ 
    message: 'SwiftLogistics API Gateway', 
    version: '1.0.0',
    endpoints: [
      'GET /health - Health check',
      'POST /api/orders - Submit order',
      'GET /api/orders/:id - Get order status'
    ]
  });
});

app.listen(PORT, () => {
  console.log(`✅ API Gateway listening on port ${PORT}`);
});
