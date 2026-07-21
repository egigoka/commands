# Consolidated tests for commands/main.py (unit)

# ---- from test_main_module.py ----


def test_commands_main_import():
    import importlib
    module = importlib.import_module("commands.__main__")
    assert module is not None
