import pytest

from pacwrap.options import Options

TOPTS = {
    "test": True,
}

DOPTS = {
    "test": False,
    "debug": 1,
    "verbose": 0,
}

VOPTS = {
    "test": False,
    "debug": 0,
    "verbose": 1,
}

TSTR = "When it stops hurting it will feel better."

def test_options_debug_flag(capfd):
    obj = Options(DOPTS)
    obj.trace(TSTR)
    assert obj.isdebug()
    assert not obj.isverbose()
    assert not obj.istest()
    obj._debug(TSTR)
    out, err = capfd.readouterr()
    assert TSTR in out

def test_options_verbose_flag(capfd):
    obj = Options(VOPTS)
    obj.trace(TSTR)
    assert not obj.isdebug()
    assert obj.isverbose()
    assert not obj.istest()
    obj._verbose(TSTR)
    out, err = capfd.readouterr()
    assert TSTR in out

def test_default_options(capfd):
    obj = Options()
    obj.trace(TSTR)
    out, err = capfd.readouterr()
    assert not obj.isdebug()
    assert not obj.isverbose()
    assert not obj.istest()
    assert TSTR not in out


def test_options_test_flag(capfd):
    obj = Options(TOPTS)
    obj.trace(TSTR)
    out, err = capfd.readouterr()
    assert not obj.isdebug()
    assert not obj.isverbose()
    assert obj.istest()
    assert TSTR in out


def test_options_requires_super_user():
    obj = Options()
    with pytest.raises(PermissionError):
        obj.requires_super_user()
