const net = require('net');
const readline = require('readline');

const host = 'host ip';
const port = 4020;

const server = net.createServer((socket) => {
    console.log(`Client connected from ${socket.remoteAddress}:${socket.remotePort}`);
    socket.write('Hello, client! This is the server. Type "exit" to end the connection.\n');
    socket.setEncoding('utf-8');
    socket.on('data', (data) => {
        console.log(`Received from ${socket.remoteAddress}:${socket.remotePort}: ${data}`);
        broadcastToClients(data);
        if (data.trim().toLowerCase() === 'exit') {
            socket.end('Goodbye, client!\n');
        } else {
            processLedControlMessage(data);
            socket.write(`Server received: ${data}`);
        }
    });

    socket.on('close', () => {
        console.log(`Connection from ${socket.remoteAddress}:${socket.remotePort} closed`);
        clients.splice(clients.indexOf(socket), 1);
    });

    socket.on('error', (err) => {
        console.error(`Socket error: ${err.message}`);
    });
});

const clients = [];

function processLedControlMessage(message) {
    const lowerCaseMessage = message.trim().toLowerCase();
    if (lowerCaseMessage === 'led1on') {
        broadcastToClients('1LEDON');
    } else if (lowerCaseMessage === 'led1off') {
        broadcastToClients('1LEDOFF');
    }
}

function broadcastToClients(data) {
    clients.forEach((client) => {
        client.write(data);
    });
}

server.listen(port, host, () => {
    console.log(`Server listening on ${host}:${port}`);
});

server.on('connection', (socket) => {
    console.log(`New client connected from ${socket.remoteAddress}:${socket.remotePort}`);
    clients.push(socket);
});

server.on('error', (err) => {
    console.error(`Server error: ${err.message}`);
});

server.on('close', () => {
    console.log('Server closed');
});

// Read messages from terminal and broadcast to clients
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
});

rl.on('line', (input) => {
    // When a line of text is entered in the terminal, broadcast it to all clients
    broadcastToClients(input);
});