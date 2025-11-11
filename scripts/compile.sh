#!/bin/bash
set -e

# --- Standard setup: Find the project root ---
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_ROOT=$( dirname "$SCRIPT_DIR" )
BUILD_DIR="${PROJECT_ROOT}/build"

# --- Remember where the USER is and what file they want ---
USER_CWD=$(pwd)
FILE_ARG="$1"

# --- Check if a file was provided ---
if [ -z "$FILE_ARG" ]; then
  echo "Usage: $0 <file.komu>"
  exit 1
fi

# --- Convert the provided file path to an absolute path ---
case "$FILE_ARG" in
  /*) FULL_FILE_PATH="$FILE_ARG" ;;  # It's already an absolute path
  *)  FULL_FILE_PATH="${USER_CWD}/${FILE_ARG}" ;; # It's relative, so make it absolute
esac

# --- Run the build (output suppressed to be less "noisy") ---
echo "Configuring & Building Project..."
cmake -B "$BUILD_DIR" -S "$PROJECT_ROOT" > /dev/null
cmake --build "$BUILD_DIR" > /dev/null

# --- Run tests ---
echo "Running Tests..."
ctest --test-dir "$BUILD_DIR" --output-on-failure
echo "All tests passed!"

# --- Run the parser with the new, correct full path ---
echo "Running parser..."
cd "$PROJECT_ROOT"
python3 -m src.parser.src.main "$FULL_FILE_PATH"

# --- Run the interpreter ---
echo "Running interpreter..."
cd "$BUILD_DIR"
./komu

echo ""
echo "Done."