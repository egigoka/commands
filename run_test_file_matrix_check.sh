#!/bin/sh
set -e

missing=0
extra=0
expected_files=$(mktemp)
trap 'rm -f "$expected_files"' EXIT

for path in commands/*.py; do
  base=$(basename "$path" .py)

  if [ "$base" = "__init__" ]; then
    continue
  fi

  if [ "$base" = "__main__" ]; then
    mod=main
  elif [ "${base#_}" != "$base" ]; then
    mod=${base#_}
  else
    mod=$base
  fi

  for suffix in "" "_negative" "_integration" "_integration_negative"; do
    test_file="tests/test_${mod}${suffix}.py"
    echo "$test_file" >> "$expected_files"
    if [ ! -f "$test_file" ]; then
      echo "Missing $test_file (for commands/$base.py)"
      missing=1
    fi
  done
done

for test_file in tests/test_*.py; do
  if [ ! -e "$test_file" ]; then
    continue
  fi
  if ! grep -qx "$test_file" "$expected_files"; then
    echo "Extra $test_file (not in test matrix)"
    extra=1
  fi
done

if [ "$missing" -ne 0 ] || [ "$extra" -ne 0 ]; then
  exit 1
fi

echo "All module test files present."
