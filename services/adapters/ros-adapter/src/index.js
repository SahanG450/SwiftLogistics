// SwiftLogistics ROS Adapter
// REST/JSON Protocol Translator

console.log('🔌 ROS Adapter starting...');
console.log('📡 Connecting to RabbitMQ:', process.env.RABBITMQ_URL || 'amqp://localhost');
console.log('🎯 Target ROS URL:', process.env.ROS_API_URL || 'http://ros-mock:4001');

setInterval(() => {
  console.log('💚 ROS Adapter heartbeat...');
}, 30000);

console.log('✅ ROS Adapter running');
