// SwiftLogistics WMS Adapter
// TCP Socket Protocol Translator

console.log('🔌 WMS Adapter starting...');
console.log('📡 Connecting to RabbitMQ:', process.env.RABBITMQ_URL || 'amqp://localhost');
console.log('🎯 Target WMS:', `${process.env.WMS_TCP_HOST || 'wms-mock'}:${process.env.WMS_TCP_PORT || 4002}`);

setInterval(() => {
  console.log('💚 WMS Adapter heartbeat...');
}, 30000);

console.log('✅ WMS Adapter running');
