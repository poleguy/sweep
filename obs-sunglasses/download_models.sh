#!/usr/bin/env bash
set -e

# Directory where models will be stored
MODEL_DIR="./models"

# Base URL for face-api.js models
BASE_URL="https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights"

# Models we want
MODELS=(
  "tiny_face_detector_model-shard1"
  "tiny_face_detector_model-weights_manifest.json"
  "face_landmark_68_tiny_model-shard1"
  "face_landmark_68_tiny_model-weights_manifest.json"
)

mkdir -p "$MODEL_DIR"

echo "Downloading face-api.js models into $MODEL_DIR ..."

for file in "${MODELS[@]}"; do
  echo "Fetching $file ..."
  curl -L -o "$MODEL_DIR/$file" "$BASE_URL/$file"
done

echo "✅ Done. Models are saved in $MODEL_DIR"
