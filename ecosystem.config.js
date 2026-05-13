/**
 * PM2 process file for Django ASGI (Uvicorn).
 * From repo root: pm2 start ecosystem.config.js
 */
module.exports = {
  apps: [
    {
      name: 'metafit-api',
      cwd: __dirname,
      script: './venv/bin/python',
      args: '-m uvicorn config.asgi:application --host 0.0.0.0 --port 8000',
      interpreter: 'none',
      env: {
        DJANGO_SETTINGS_MODULE: 'config.settings',
      },
    },
  ],
};
