#For running test
#usage: ./scripts/run_test.sh

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_ROOT=$( dirname "$SCRIPT_DIR" )
BUILD_DIR="${PROJECT_ROOT}/build"

echo "Running Tests..."
ctest --test-dir "$BUILD_DIR" --output-on-failure
echo "All tests passed!"