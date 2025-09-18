// server.ts - Next.js Standalone + Socket.IO (relative-import safe)
import { createServer } from 'http';
import { Server } from 'socket.io';
import next from 'next';

// relative import to avoid tsconfig path alias at runtime
import { setupSocket } from './src/lib/socket';

const dev = process.env.NODE_ENV !== 'production';
const currentPort = Number(process.env.PORT || 3000);
const hostname = '0.0.0.0';

async function createCustomServer() {
  try {
    // Create Next.js app
    const nextApp = next({
      dev,
      dir: process.cwd(),
      // In production, use the current directory where .next is located
      conf: dev ? undefined : { distDir: './.next' },
    });

    await nextApp.prepare();
    const handle = nextApp.getRequestHandler();

    // Create HTTP server that will handle both Next.js and Socket.IO
    const server = createServer((req, res) => {
      // Let Next.js handle the request
      return handle(req, res);
    });

    // Attach Socket.IO on the same server
    const io = new Server(server, {
      path: '/api/socketio',
      cors: {
        origin: '*',
        methods: ['GET', 'POST'],
      },
    });

    // Hook your socket setup
    setupSocket(io);

    // Start the server
    server.listen(currentPort, hostname, () => {
      console.log(`> Ready on http://${hostname}:${currentPort}`);
      console.log(`> Socket.IO server running at ws://${hostname}:${currentPort}/api/socketio`);
    });

    // handle graceful shutdown signals
    const shutdown = () => {
      console.log('Shutting down server...');
      io.close(() => {
        server.close(() => {
          console.log('Server closed.');
          process.exit(0);
        });
      });
      // fallback forced exit
      setTimeout(() => process.exit(1), 10000).unref();
    };
    process.on('SIGINT', shutdown);
    process.on('SIGTERM', shutdown);

  } catch (err) {
    console.error('Server startup error:', err);
    process.exit(1);
  }
}

// Start the server
createCustomServer();
