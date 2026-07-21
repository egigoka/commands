"""Lazy module loading for fast startup and optional dependencies."""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any


def _import_module(name: str, package: Any) -> Any:
    importlib = __import__("importlib", fromlist=["import_module"])
    return importlib.import_module(name, package)


def _find_spec(name: str, package: Any) -> Any:
    importlib_util = __import__("importlib.util", fromlist=["find_spec"])
    return importlib_util.find_spec(name, package)


class LazyModule:
    """
    A lazy-loading module wrapper that imports only on first attribute access.

    Usage:
        np = LazyModule("numpy")
        pd = LazyModule("pandas")

        # Module is NOT imported yet - fast startup!

        np.array([1, 2, 3])  # Now numpy is imported

    For optional dependencies:
        pyautogui = LazyModule("pyautogui", optional=True)

        if pyautogui:  # checks if available without importing
            pyautogui.click(100, 100)

    For package-relative modules:
        base64 = LazyModule(".base64")
    """

    __slots__ = ("_name", "_module", "_optional", "_available", "_package", "_overrides")

    def __init__(self, name: str, *, optional: bool = False, package: str | None = None) -> None:
        object.__setattr__(self, "_name", name)
        object.__setattr__(self, "_module", None)
        object.__setattr__(self, "_optional", optional)
        object.__setattr__(self, "_available", None)
        object.__setattr__(self, "_overrides", {})
        if name.startswith(".") and package is None:
            inspect = __import__("inspect")
            frame = inspect.currentframe()
            caller = frame.f_back if frame is not None else None
            package = caller.f_globals.get("__package__") if caller is not None else None
            del frame
        object.__setattr__(self, "_package", package)

    def _load(self) -> Any:
        module = object.__getattribute__(self, "_module")
        name = object.__getattribute__(self, "_name")
        # Check if module was replaced in sys.modules (for test mocking support)
        sys = __import__("sys")
        current = sys.modules.get(name)
        if name in sys.modules and current is None:
            module = None
            object.__setattr__(self, "_module", None)
        elif module is not None and current is not None and module is not current:
            module = current
            object.__setattr__(self, "_module", module)
            object.__setattr__(self, "_available", True)
        elif module is None:
            optional = object.__getattribute__(self, "_optional")
            try:
                package = object.__getattribute__(self, "_package")
                # import_module waits for any in-progress import to finish. Reading
                # sys.modules directly here can expose a partially initialized module
                # when two lazy consumers resolve it concurrently.
                module = _import_module(name, package)
                object.__setattr__(self, "_module", module)
                object.__setattr__(self, "_available", True)
            except ImportError:
                if optional:
                    object.__setattr__(self, "_available", False)
                    return None
                raise
        return module

    def __getattr__(self, attr: str) -> Any:
        # Check overrides first (for mocking support)
        overrides = object.__getattribute__(self, "_overrides")
        if attr in overrides:
            return overrides[attr]
        module = self._load()
        if module is None:
            name = object.__getattribute__(self, "_name")
            raise ImportError(f"Optional module '{name}' is not available")
        return getattr(module, attr)

    def __setattr__(self, attr: str, value: Any) -> None:
        # Only allow setting our own slots
        if attr in ("_name", "_module", "_optional", "_available", "_package", "_overrides"):
            object.__setattr__(self, attr, value)
        else:
            # Store everything else in overrides dict (for mocking support)
            overrides = object.__getattribute__(self, "_overrides")
            overrides[attr] = value

    def __delattr__(self, attr: str) -> None:
        overrides = object.__getattribute__(self, "_overrides")
        if attr in overrides:
            del overrides[attr]
        else:
            module = self._load()
            if module is not None:
                delattr(module, attr)

    def __bool__(self) -> bool:
        """Check if module is available without fully importing (for optional deps)."""
        available = object.__getattribute__(self, "_available")
        if available is None:
            name = object.__getattribute__(self, "_name")
            package = object.__getattribute__(self, "_package")
            # Check sys.modules first (for mocked modules)
            sys = __import__("sys")
            if name in sys.modules:
                available = True
            else:
                try:
                    available = _find_spec(name, package) is not None
                except (ValueError, AttributeError):
                    # Handle modules with missing __spec__ (e.g., mocks)
                    available = False
            object.__setattr__(self, "_available", available)
        return bool(available)

    def __repr__(self) -> str:
        name = object.__getattribute__(self, "_name")
        module = object.__getattribute__(self, "_module")
        if module is not None:
            return repr(module)
        return f"<LazyModule '{name}' (not loaded)>"

    def __dir__(self) -> list[str]:
        module = self._load()
        if module is None:
            return []
        return dir(module)


class LazyProperty:
    """Lazy attribute lookup from a module, resolved on first access."""

    __slots__ = ("_module", "_attr", "_value", "_loaded")

    def __init__(self, module: str, attr: str, *, package: str | None = None) -> None:
        object.__setattr__(self, "_module", LazyModule(module, optional=False, package=package))
        object.__setattr__(self, "_attr", attr)
        object.__setattr__(self, "_value", None)
        object.__setattr__(self, "_loaded", False)

    def _load(self) -> Any:
        module = object.__getattribute__(self, "_module")
        attr = object.__getattribute__(self, "_attr")
        value = getattr(module, attr)
        object.__setattr__(self, "_value", value)
        object.__setattr__(self, "_loaded", True)
        return value

    def _bin_op(self, other: Any, op_name: str, *, reverse: bool = False) -> Any:
        op_module = __import__("operator")
        op = getattr(op_module, op_name)
        value = self._load()
        if reverse:
            return op(other, value)
        return op(value, other)

    def __getattr__(self, attr: str) -> Any:
        value = self._load()
        return getattr(value, attr)

    def __setattr__(self, attr: str, value: Any) -> None:
        if attr in ("_module", "_attr", "_value", "_loaded"):
            object.__setattr__(self, attr, value)
            return
        target = self._load()
        setattr(target, attr, value)

    def __delattr__(self, attr: str) -> None:
        if attr in ("_module", "_attr", "_value", "_loaded"):
            object.__delattr__(self, attr)
            return
        target = self._load()
        delattr(target, attr)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Resolve and call the wrapped attribute."""
        value = self._load()
        return value(*args, **kwargs)

    def __bool__(self) -> bool:
        return bool(self._load())

    def __int__(self) -> int:
        return int(self._load())

    def __float__(self) -> float:
        return float(self._load())

    def __index__(self) -> int:
        op_module = __import__("operator")
        return int(op_module.index(self._load()))

    def __str__(self) -> str:
        return str(self._load())

    def __bytes__(self) -> bytes:
        return bytes(self._load())

    def __format__(self, spec: str) -> str:
        return format(self._load(), spec)

    def __hash__(self) -> int:
        return hash(self._load())

    def __len__(self) -> int:
        return len(self._load())

    def __iter__(self) -> Any:
        return iter(self._load())

    def __contains__(self, item: Any) -> bool:
        return item in self._load()

    def __eq__(self, other: Any) -> bool:
        return bool(self._load() == other)

    def __lt__(self, other: Any) -> bool:
        return bool(self._load() < other)

    def __le__(self, other: Any) -> bool:
        return bool(self._load() <= other)

    def __gt__(self, other: Any) -> bool:
        return bool(self._load() > other)

    def __ge__(self, other: Any) -> bool:
        return bool(self._load() >= other)

    def __add__(self, other: Any) -> Any:
        return self._bin_op(other, "add")

    def __radd__(self, other: Any) -> Any:
        return self._bin_op(other, "add", reverse=True)

    def __sub__(self, other: Any) -> Any:
        return self._bin_op(other, "sub")

    def __rsub__(self, other: Any) -> Any:
        return self._bin_op(other, "sub", reverse=True)

    def __mul__(self, other: Any) -> Any:
        return self._bin_op(other, "mul")

    def __rmul__(self, other: Any) -> Any:
        return self._bin_op(other, "mul", reverse=True)

    def __truediv__(self, other: Any) -> Any:
        return self._bin_op(other, "truediv")

    def __rtruediv__(self, other: Any) -> Any:
        return self._bin_op(other, "truediv", reverse=True)

    def __floordiv__(self, other: Any) -> Any:
        return self._bin_op(other, "floordiv")

    def __rfloordiv__(self, other: Any) -> Any:
        return self._bin_op(other, "floordiv", reverse=True)

    def __mod__(self, other: Any) -> Any:
        return self._bin_op(other, "mod")

    def __rmod__(self, other: Any) -> Any:
        return self._bin_op(other, "mod", reverse=True)

    def __pow__(self, other: Any) -> Any:
        return self._bin_op(other, "pow")

    def __rpow__(self, other: Any) -> Any:
        return self._bin_op(other, "pow", reverse=True)

    def __neg__(self) -> Any:
        return -self._load()

    def __pos__(self) -> Any:
        return +self._load()

    def __abs__(self) -> Any:
        return abs(self._load())

    def __repr__(self) -> str:
        if self._loaded:
            return repr(self._value)
        return f"<LazyProperty '{self._module}.{self._attr}' (not loaded)>"
