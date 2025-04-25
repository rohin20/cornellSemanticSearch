#!/bin/bash

# Build frontend
echo "Building frontend..."
cd frontend
npm run build
cd ..

# Start backend
echo "Starting backend..."
cd backend
python production.py 