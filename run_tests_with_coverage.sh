set -e

./run_tests_with_coverage_unit.sh
./run_tests_with_coverage_negative.sh
./run_tests_with_coverage_integration.sh
./run_tests_with_coverage_integration_negative.sh
