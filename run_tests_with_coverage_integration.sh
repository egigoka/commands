python3 -m pytest \
  --cov=commands \
  --cov-report=term-missing \
  --cov-report=html \
  tests/*_integration.py \
  -v
