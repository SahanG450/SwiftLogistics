// SwiftLogistics CMS Adapter
// SOAP/XML Protocol Translator

console.log('🔌 CMS Adapter starting...');
console.log('📡 Connecting to RabbitMQ:', process.env.RABBITMQ_URL || 'amqp://localhost');
console.log('🎯 Target CMS URL:', process.env.CMS_SOAP_URL || 'http://cms-mock:4000');

setInterval(() => {
  console.log('💚 CMS Adapter heartbeat...');
}, 30000);

console.log('✅ CMS Adapter running');
