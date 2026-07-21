# Consolidated tests for commands/instance.py (negative)

# ---- from test_instance_negative.py ----

# Placeholder for future tests.
import pytest
from commands._instance import add_instance_shortcuts

class TestInstanceCoverage:
    """Tests to improve _instance module coverage"""

    def test_delegate_raises_attribute_error_for_non_callable(self):
        """Test that _delegate raises AttributeError when attribute is not callable"""

        class TestClass:
            non_callable_class_attr = "not callable"

            @classmethod
            def class_method(cls):
                return "method"

        # Add instance shortcuts - this adds __getattr__
        add_instance_shortcuts(TestClass)

        instance = TestClass()

        # Directly call the __getattr__ that was added
        # Test that it works for callables
        result = instance.__getattr__('class_method')
        assert callable(result)

        # Test that it raises AttributeError for non-callables
        with pytest.raises(AttributeError, match="non_callable_class_attr"):
            instance.__getattr__('non_callable_class_attr')
