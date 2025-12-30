#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

// Function to start a process
function startProcess(name, command, args, cwd) {
  return new Promise((resolve, reject) => {
    console.log(`Starting ${name}...`);

    const process = spawn(command, args, {
      cwd: path.join(__dirname, cwd),
      stdio: 'inherit',
      shell: true
    });

    process.on('error', (err) => {
      console.error(`Failed to start ${name}:`, err.message);
      reject(err);
    });

    process.on('close', (code) => {
      if (code !== 0) {
        console.error(`${name} exited with code ${code}`);
        reject(new Error(`${name} failed with exit code ${code}`));
      } else {
        console.log(`${name} closed`);
        resolve();
      }
    });
  });
}

// Start both servers concurrently
async function startServers() {
  console.log('Starting Physical AI & Humanoid Robotics application...');
  console.log('Starting backend server on port 8000...');

  // Start backend server
  const backendPromise = startProcess(
    'Backend Server',
    'python',
    ['-c', 'from api import app; import uvicorn; uvicorn.run(app, host="0.0.0.0", port=8000)'],
    'backend'
  );

  // Wait a moment for backend to start
  await new Promise(resolve => setTimeout(resolve, 3000));

  console.log('Starting frontend server on port 3000...');

  // Start frontend server
  const frontendPromise = startProcess(
    'Frontend Server',
    'npx',
    ['docusaurus', 'start'],
    'website'
  );

  try {
    await Promise.all([backendPromise, frontendPromise]);
    console.log('Both servers shut down gracefully');
  } catch (error) {
    console.error('One or more servers failed:', error.message);
    process.exit(1);
  }
}

startServers();