import pytest

from pacwrap.options import Options

test_opts = {"test": True}
dbg_opts = {"test": False, "debug": 1, "verbose": 0}
verbose_opts = {"test": False, "debug": 0, "verbose": 1}

CONST_TEST_STRING = "When it stops hurting it will feel better."


def test_options_debug_flag(capfd: pytest.CaptureFixture[str]) -> None:
    """Test options debug flag."""
    oopts = Options(dbg_opts)
    oopts.trace(CONST_TEST_STRING)
    assert oopts.isdebug()
    assert not oopts.isverbose()
    assert not oopts.istest()
    oopts._debug(CONST_TEST_STRING)
    out, err = capfd.readouterr()
    assert CONST_TEST_STRING in out


def test_options_verbose_flag(capfd: pytest.CaptureFixture[str]) -> None:
    """Test options verbose flag."""
    oopts = Options(verbose_opts)
    oopts.trace(CONST_TEST_STRING)
    assert not oopts.isdebug()
    assert oopts.isverbose()
    assert not oopts.istest()
    oopts._verbose(CONST_TEST_STRING)
    out, err = capfd.readouterr()
    assert CONST_TEST_STRING in out


def test_default_options(capfd: pytest.CaptureFixture[str]) -> None:
    """Test options defaults."""
    oopts = Options()
    oopts.trace(CONST_TEST_STRING)
    out, err = capfd.readouterr()
    assert not oopts.isdebug()
    assert not oopts.isverbose()
    assert not oopts.istest()
    assert CONST_TEST_STRING not in out


def test_options_test_flag(capfd: pytest.CaptureFixture[str]) -> None:
    """Test options test flag."""
    oopts = Options(test_opts)
    oopts.trace(CONST_TEST_STRING)
    out, err = capfd.readouterr()
    assert not oopts.isdebug()
    assert not oopts.isverbose()
    assert oopts.istest()
    assert CONST_TEST_STRING in out


def test_options_requires_super_user() -> None:
    """Test options requires super user."""
    oopts = Options()
    with pytest.raises(PermissionError):
        oopts.requires_super_user()
