# Consolidated tests for commands/mouse.py (unit)

# ---- from test_mouse9.py ----


import pytest


def test_mouse9_import():
    import commands.mouse as mouse
    assert mouse is not None


# Coverage improvement tests
class TestMouseLegacyCoverage:
    """Tests to improve coverage for mouse9.py"""

    def test_set_mouse_move_duration(self):
        """Test SettingsMouse.set_mouse_move_duration (lines 15-20)"""
        from commands.mouse import SettingsMouse

        # Set duration
        SettingsMouse.set_mouse_move_duration(1.5)
        assert SettingsMouse.mouse_move_duration == 1.5

        # Reset to default
        SettingsMouse.set_mouse_move_duration(0.5)

    def test_scroll_up(self, monkeypatch, capsys):
        """Test Mouse.Scroll.scroll with up=True (lines 30-42)"""
        from commands.mouse import Mouse

        # Mock pyautogui
        scroll_called = []
        def mock_vscroll(clicks):
            scroll_called.append(clicks)

        import sys
        from unittest.mock import MagicMock
        mock_pyautogui = MagicMock()
        mock_pyautogui.vscroll = mock_vscroll
        sys.modules['pyautogui'] = mock_pyautogui

        Mouse.Scroll.scroll(100, up=True)

        assert len(scroll_called) == 1
        assert scroll_called[0] == 100

        captured = capsys.readouterr()
        assert "scrolled 100" in captured.out

    def test_scroll_down(self, monkeypatch, capsys):
        """Test Mouse.Scroll.scroll with up=False (lines 39-40)"""
        from commands.mouse import Mouse

        # Mock pyautogui
        scroll_called = []
        def mock_vscroll(clicks):
            scroll_called.append(clicks)

        import sys
        from unittest.mock import MagicMock
        mock_pyautogui = MagicMock()
        mock_pyautogui.vscroll = mock_vscroll
        sys.modules['pyautogui'] = mock_pyautogui

        Mouse.Scroll.scroll(50, up=False)

        assert len(scroll_called) == 1
        assert scroll_called[0] == -50  # Should be negative

    def test_scroll_up_method(self, monkeypatch):
        """Test Mouse.Scroll.up method (lines 45-50)"""
        from commands.mouse import Mouse

        scroll_called = []
        def mock_scroll(value, up):
            scroll_called.append((value, up))

        monkeypatch.setattr(Mouse.Scroll, "scroll", mock_scroll)

        Mouse.Scroll.up(200)
        assert scroll_called == [(200, True)]

    def test_scroll_down_method(self, monkeypatch):
        """Test Mouse.Scroll.down method (lines 53-58)"""
        from commands.mouse import Mouse

        scroll_called = []
        def mock_scroll(value, up):
            scroll_called.append((value, up))

        monkeypatch.setattr(Mouse.Scroll, "scroll", mock_scroll)

        Mouse.Scroll.down(150)
        assert scroll_called == [(150, False)]

    def test_click_with_position_verbose_false(self, monkeypatch):
        """Test Mouse.Click.click with position and verbose=False (lines 64-80)"""
        from commands.mouse import Mouse

        # Mock pyautogui and Time.sleep
        click_called = []
        def mock_click(x, y, button):
            click_called.append((x, y, button))

        sleep_called = []
        def mock_sleep(duration, verbose=False):
            sleep_called.append((duration, verbose))

        import sys
        from unittest.mock import MagicMock
        mock_pyautogui = MagicMock()
        mock_pyautogui.click = mock_click
        sys.modules['pyautogui'] = mock_pyautogui

        from commands.time import Time
        monkeypatch.setattr(Time, "sleep", mock_sleep)

        Mouse.Click.click("left", [100, 200], verbose=False, sleep_before_click=0.1)

        assert len(click_called) == 1
        assert click_called[0] == (100, 200, "left")
        assert len(sleep_called) == 1

    def test_click_without_position(self, monkeypatch, capsys):
        """Test Mouse.Click.click without position (lines 77-80)"""
        from commands.mouse import Mouse

        # Mock pyautogui
        click_called = []
        def mock_click(button):
            click_called.append(button)

        def mock_sleep(duration, verbose=False):
            pass

        import sys
        from unittest.mock import MagicMock
        mock_pyautogui = MagicMock()
        mock_pyautogui.click = mock_click
        sys.modules['pyautogui'] = mock_pyautogui

        from commands.time import Time
        monkeypatch.setattr(Time, "sleep", mock_sleep)

        Mouse.Click.click("right", None, verbose=True)

        assert len(click_called) == 1
        captured = capsys.readouterr()
        assert "click mouse right" in captured.out

    def test_click_right(self, monkeypatch):
        """Test Mouse.Click.right method (lines 83-89)"""
        from commands.mouse import Mouse

        click_called = []
        def mock_click(button, position, verbose, sleep_before_click):
            click_called.append((button, position, verbose, sleep_before_click))

        monkeypatch.setattr(Mouse.Click, "click", mock_click)

        Mouse.Click.right([50, 60], verbose=False)
        assert len(click_called) == 1
        assert click_called[0][0] == "right"
        assert click_called[0][1] == [50, 60]

    def test_click_left(self, monkeypatch):
        """Test Mouse.Click.left method (lines 92-98)"""
        from commands.mouse import Mouse

        click_called = []
        def mock_click(button, position, verbose, sleep_before_click):
            click_called.append((button, position, verbose, sleep_before_click))

        monkeypatch.setattr(Mouse.Click, "click", mock_click)

        Mouse.Click.left([100, 150])
        assert len(click_called) == 1
        assert click_called[0][0] == "left"

    def test_click_middle(self, monkeypatch):
        """Test Mouse.Click.middle method (lines 101-107)"""
        from commands.mouse import Mouse

        click_called = []
        def mock_click(button, position, verbose, sleep_before_click):
            click_called.append((button, position, verbose, sleep_before_click))

        monkeypatch.setattr(Mouse.Click, "click", mock_click)

        Mouse.Click.middle([200, 250])
        assert len(click_called) == 1
        assert click_called[0][0] == "middle"

    def test_move_basic(self, monkeypatch, capsys):
        """Test Mouse.move basic (lines 110-148)"""
        from commands.mouse import Mouse

        # Mock pyautogui
        move_called = []
        def mock_moveTo(x, y, duration, tween):
            move_called.append(("moveTo", x, y, duration))

        def mock_easeInOutQuad(x):
            return x

        import sys
        from unittest.mock import MagicMock
        mock_pyautogui = MagicMock()
        mock_pyautogui.moveTo = mock_moveTo
        mock_pyautogui.easeInOutQuad = mock_easeInOutQuad
        sys.modules['pyautogui'] = mock_pyautogui

        Mouse.move(100, 200, verbose=True)

        assert len(move_called) == 1
        assert move_called[0][1:3] == (100, 200)
        captured = capsys.readouterr()
        assert "moved mouse to 100 200" in captured.out

    def test_move_tuple_2_elements(self, monkeypatch):
        """Test Mouse.move with tuple (x, y) (lines 127-130)"""
        from commands.mouse import Mouse

        move_called = []
        def mock_moveTo(x, y, duration, tween):
            move_called.append((x, y))

        import sys
        from unittest.mock import MagicMock
        mock_pyautogui = MagicMock()
        mock_pyautogui.moveTo = mock_moveTo
        mock_pyautogui.easeInOutQuad = lambda x: x
        sys.modules['pyautogui'] = mock_pyautogui

        Mouse.move((150, 250), verbose=False)
        assert move_called[0] == (150, 250)

    def test_move_tuple_4_elements(self, monkeypatch):
        """Test Mouse.move with rectangle (x, y, x2, y2) (lines 131-137)"""
        from commands.mouse import Mouse

        move_called = []
        def mock_moveTo(x, y, duration, tween):
            move_called.append((x, y))

        def mock_center(rect):
            # Return center of rectangle
            return ((rect[0] + rect[2]) // 2, (rect[1] + rect[3]) // 2)

        import sys
        from unittest.mock import MagicMock
        mock_pyautogui = MagicMock()
        mock_pyautogui.moveTo = mock_moveTo
        mock_pyautogui.center = mock_center
        mock_pyautogui.easeInOutQuad = lambda x: x
        sys.modules['pyautogui'] = mock_pyautogui

        Mouse.move((10, 20, 100, 200), verbose=False)
        # Should move to center of rectangle
        assert len(move_called) == 1

    def test_move_with_x2_y2(self, monkeypatch):
        """Test Mouse.move with x2, y2 parameters (lines 136-137)"""
        from commands.mouse import Mouse

        move_called = []
        def mock_moveTo(x, y, duration, tween):
            move_called.append((x, y))

        def mock_center(rect):
            return (50, 50)

        import sys
        from unittest.mock import MagicMock
        mock_pyautogui = MagicMock()
        mock_pyautogui.moveTo = mock_moveTo
        mock_pyautogui.center = mock_center
        mock_pyautogui.easeInOutQuad = lambda x: x
        sys.modules['pyautogui'] = mock_pyautogui

        Mouse.move(10, 20, x2=100, y2=200, verbose=False)
        assert move_called[0] == (50, 50)

    def test_move_relative(self, monkeypatch, capsys):
        """Test Mouse.move with rel=True (lines 139-146)"""
        from commands.mouse import Mouse

        move_called = []
        def mock_moveRel(x, y, duration, tween):
            move_called.append(("moveRel", x, y))

        import sys
        from unittest.mock import MagicMock
        mock_pyautogui = MagicMock()
        mock_pyautogui.moveRel = mock_moveRel
        mock_pyautogui.easeInOutQuad = lambda x: x
        sys.modules['pyautogui'] = mock_pyautogui

        Mouse.move(50, 75, rel=True, verbose=True)

        assert len(move_called) == 1
        assert move_called[0] == ("moveRel", 50, 75)
        captured = capsys.readouterr()
        assert "moved mouse relative 50 75" in captured.out

    def test_get_position(self, monkeypatch):
        """Test Mouse.get_position (lines 151-157)"""
        from commands.mouse import Mouse

        def mock_position():
            return (300, 400)

        import sys
        from unittest.mock import MagicMock
        mock_pyautogui = MagicMock()
        mock_pyautogui.position = mock_position
        sys.modules['pyautogui'] = mock_pyautogui

        result = Mouse.get_position()
        assert result == (300, 400)


# ---- from test_mouse_coverage.py ----


import pytest
from commands.mouse import Mouse
from unittest.mock import MagicMock, patch


class TestMouseCoverage:
    """Tests to improve Mouse module coverage"""

    def test_mouse_init(self):
        """Test Mouse.__init__() (line 27)"""
        m = Mouse()
        assert m is not None

    def test_mouse_instance_scroll(self):
        """Test Mouse instance scroll method (line 163)"""
        m = Mouse()
        # Mock the Scroll.scroll class method that the instance method delegates to
        with patch.object(Mouse.Scroll, 'scroll', return_value=None) as mock_scroll:
            result = m.scroll(10, up=True)
            mock_scroll.assert_called_once_with(10, up=True)

    def test_mouse_instance_click(self):
        """Test Mouse instance click method (line 166)"""
        m = Mouse()
        # Mock the Click.click class method that the instance method delegates to
        with patch.object(Mouse.Click, 'click', return_value=None) as mock_click:
            result = m.click(button="left", position=None)
            mock_click.assert_called_once()

    def test_mouse_instance_move_to(self):
        """Test Mouse instance move_to method (line 170)"""
        m = Mouse()
        # Mock the Mouse.move class method
        with patch.object(Mouse, 'move', return_value=None) as mock_move:
            result = m.move_to(100, 200)
            mock_move.assert_called_once()

    def test_mouse_instance_position(self):
        """Test Mouse instance position method (line 173)"""
        m = Mouse()
        # Mock the Mouse.get_position class method
        with patch.object(Mouse, 'get_position', return_value=(100, 200)) as mock_position:
            result = m.position()
            assert result == (100, 200)
            mock_position.assert_called_once()
