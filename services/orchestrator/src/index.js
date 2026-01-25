// SwiftLogistics Orchestrator
// Transaction management and order lifecycle coordination

const express = require('express');
const app = express();
const PORT = process.env.PORT || 3001;

app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'orchestrator' });
});

app.get('/', (req, res) => {
  res.json({ 
    message: 'SwiftLogistics Orchestrator', 
    version: '1.0.0',
    status: 'running'
  });
});

app.listen(PORT, () => {
  console.log(`✅ Orchestrator listening on port ${PORT}`);
});
