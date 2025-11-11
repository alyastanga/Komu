
set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_ROOT=$( dirname "$SCRIPT_DIR" )

BUILD_DIR="${PROJECT_ROOT}/build"
EXAMPLES_DIR="${PROJECT_ROOT}/examples"

echo "onfiguring Project..."
cmake -B "$BUILD_DIR" -S "$PROJECT_ROOT"

echo "Building Project..."
cmake --build "$BUILD_DIR"

echo "Running Tests..."
ctest --test-dir "$BUILD_DIR" --output-on-failure
echo "All tests passed!"

if [ -z "$1" ]; then
  echo "Usage: $0 <file.komu>"
  exit 1
fi

echo "Running parser..."
cd "$PROJECT_ROOT"
python3 -m src.parser.src.main "$1"


echo "Running interpreter..."
cd "$BUILD_DIR"
./komu


echo "Done."