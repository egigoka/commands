#!/bin/sh
set -eu

sh run_test_file_matrix_check.sh
sh run_tests_with_coverage.sh
sh run_styling_check.sh
sh run_typing_check.sh
sh run_linting_check.sh
