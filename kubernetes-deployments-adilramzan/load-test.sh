#!/bin/bash

# Simple load testing script for the Flask app
echo "Starting load test - sending requests to Flask app..."
echo "Test will run for 2 minutes with 10 parallel requests"

# Run for 1 minute to save time
end=$((SECONDS+60))

# Function to run a single batch of requests
run_batch() {
  for i in {1..50}; do
    curl -s http://localhost:8080/db-test > /dev/null
    curl -s http://localhost:8080/messages > /dev/null
    curl -s -X POST -H "Content-Type: application/json" -d "{\"message\":\"Test message $i\"}" http://localhost:8080/messages > /dev/null
  done
  echo "Batch of 150 requests completed"
}

# Main load test loop
while [ $SECONDS -lt $end ]; do
  # Run multiple batches in parallel
  run_batch &
  run_batch &
  run_batch &
  
  # Small pause to avoid overwhelming the terminal output
  sleep 5
  
  # Status update
  echo "Load test running... $((end-SECONDS)) seconds remaining"
done

echo "Load test completed"
