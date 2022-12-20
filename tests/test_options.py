import pytest

from pacwrap.options import Options

test_opts = {"test": True}
dbg_opts = {"test": False, "debug": 1, "verbose": 0}
verbose_opts = {"test": False, "debug": 0, "verbose": 1}

TSTR = "When it stops hurting it will feel better."


def test_options_debug_flag(capfd):
    """Test options debug flag."""
    oopts = Options(dbg_opts)
    oopts.trace(TSTR)
    assert oopts.isdebug()
    assert not oopts.isverbose()
    assert not oopts.istest()
    oopts._debug(TSTR)
    out, err = capfd.readouterr()
    assert TSTR in out


def test_options_verbose_flag(capfd):
    """Test options verbose flag."""
    oopts = Options(verbose_opts)
    oopts.trace(TSTR)
    assert not oopts.isdebug()
    assert oopts.isverbose()
    assert not oopts.istest()
    oopts._verbose(TSTR)
    out, err = capfd.readouterr()
    assert TSTR in out


def test_default_options(capfd):
    """Test options defaults."""
    oopts = Options()
    oopts.trace(TSTR)
    out, err = capfd.readouterr()
    assert not oopts.isdebug()
    assert not oopts.isverbose()
    assert not oopts.istest()
    assert TSTR not in out


def test_options_test_flag(capfd):
    """Test options test flag."""
    oopts = Options(test_opts)
    oopts.trace(TSTR)
    out, err = capfd.readouterr()
    assert not oopts.isdebug()
    assert not oopts.isverbose()
    assert oopts.istest()
    assert TSTR in out


def test_options_requires_super_user():
    """Test options requires super user."""
    oopts = Options()
    with pytest.raises(PermissionError):
        oopts.requires_super_user()
