import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import fs from 'fs'

const ROOT = path.resolve(__dirname, '..')

export default defineConfig({
  plugins: [
    react(),
    {
      name: 'local-preview',
      configureServer(server) {
        // Serve template files under /preview/ path
        // e.g. /preview/bakery/index.html → ../bakery/index.html
        server.middlewares.use('/preview/', (req, res, next) => {
          const url = req.url || '';
          // Decode URL and clean it
          const decoded = decodeURIComponent(url);
          // Map /preview/bakery/css/style.css → ../bakery/css/style.css
          const relativePath = decoded.startsWith('/') ? decoded.slice(1) : decoded;
          const filePath = path.join(ROOT, relativePath);

          if (fs.existsSync(filePath) && !fs.statSync(filePath).isDirectory()) {
            const ext = path.extname(filePath).toLowerCase();
            const mimeTypes = {
              '.html': 'text/html; charset=utf-8',
              '.css': 'text/css; charset=utf-8',
              '.js': 'application/javascript; charset=utf-8',
              '.mjs': 'application/javascript; charset=utf-8',
              '.json': 'application/json',
              '.png': 'image/png',
              '.jpg': 'image/jpeg',
              '.jpeg': 'image/jpeg',
              '.gif': 'image/gif',
              '.svg': 'image/svg+xml',
              '.webp': 'image/webp',
              '.ico': 'image/x-icon',
              '.woff': 'font/woff',
              '.woff2': 'font/woff2',
              '.ttf': 'font/ttf',
              '.otf': 'font/otf',
              '.mp4': 'video/mp4',
              '.webm': 'video/webm',
              '.pdf': 'application/pdf',
            };
            const contentType = mimeTypes[ext] || 'application/octet-stream';
            res.writeHead(200, {
              'Content-Type': contentType,
              'Access-Control-Allow-Origin': '*',
              'Cache-Control': 'no-cache',
            });
            fs.createReadStream(filePath).pipe(res);
          } else {
            // If requested path doesn't exist, try index.html as fallback
            const dirPath = path.join(ROOT, relativePath);
            const indexPath = path.join(dirPath, 'index.html');
            if (fs.existsSync(indexPath)) {
              res.writeHead(302, { Location: `${req.url}/index.html` });
              res.end();
            } else {
              next();
            }
          }
        });
      },
    },
  ],
  server: {
    port: 5173,
    open: false,
  },
})
