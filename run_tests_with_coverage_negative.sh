python3 -m pytest \
  --cov=commands \
  --cov-report=term-missing \
  --cov-report=html \
  tests/*_negative.py \
  --ignore-glob='tests/*_integration_negative.py' \
  -v
