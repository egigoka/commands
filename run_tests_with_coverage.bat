echo pip install pytest-cov
python3 -m pytest --cov=commands --cov-report=term-missing --cov-report=html -v
