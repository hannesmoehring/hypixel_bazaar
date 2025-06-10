#!/bin/bash

cd server
python api_handler.py &  
cd ../client
pnpm run dev &          
wait                     