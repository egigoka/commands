python3 -m pytest \
  --cov=commands \
  --cov-report=term-missing \
  --cov-report=html \
  --ignore-glob='tests/*_negative.py' \
  --ignore-glob='tests/*_integration*.py' \
  -v
