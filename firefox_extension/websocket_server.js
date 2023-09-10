const http = require('http');
const WebSocketServer = require('websocket').server;

const server = http.createServer((req, res) => {
  // Handle HTTP requests if needed
});

const wsServer = new WebSocketServer({
  httpServer: server,
  autoAcceptConnections: true,
});

// Store a reference to the connected WebSocket client (the extension)
let extensionConnection = null;

wsServer.on('request', (request) => {
  const connection = request.accept(null, request.origin);

  connection.on('message', (message) => {
    if (message.type === 'utf8') {
      const data = JSON.parse(message.utf8Data);
      // Handle incoming WebSocket messages here
      console.log('Received WebSocket message:', data);

      // Forward the message to the extension (if connected)
      if (extensionConnection) {
        extensionConnection.send(JSON.stringify(data));
      }
    }
  });

  connection.on('close', (reasonCode, description) => {
    // Handle WebSocket connection closure
    if (extensionConnection === connection) {
      extensionConnection = null;
    }
  });

  // Save the WebSocket connection as the extension connection
  extensionConnection = connection;
});

server.listen(3000, () => {
  console.log('WebSocket server is listening on port 3000');
});
