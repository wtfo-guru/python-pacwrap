import pytest
import tempfile
from pathlib import Path
from pacwrap.pkgmgr import PackageHandler

OPATH = Path(tempfile.mkdtemp()) / "wtf-pkgmgr-test.txt"

OOPTS = {
    "test": False,
    "output": str(OPATH),
}

VOPTS = {
    "test": False,
    "debug": 0,
    "verbose": 1,
}

TSTR = "When it stops hurting it will feel better."
LBASH = "bash"

def test_handler_find_action():
    obj = PackageHandler()
    with pytest.raises(NotImplementedError):
        obj.find_action(LBASH)

def test_handler_list_packages():
    obj = PackageHandler()
    with pytest.raises(NotImplementedError):
        obj.list_packages()

def test_handler_run_pipes_good():
    cmds = ("ls -l {0}".format(tempfile.gettempdir()), "sort")
    obj = PackageHandler()
    assert obj.run_pipes(cmds) == 0

def test_handler_run_pipes_bad():
    cmds = ("ls -l {0}".format(tempfile.gettempdir()), "sort", "false")
    obj = PackageHandler()
    assert obj.run_pipes(cmds) == 1

def test_handler_run_pipes_output():
    cmds = ("ls -l {0}".format(tempfile.gettempdir()), "sort")
    obj = PackageHandler(OOPTS)
    assert obj.run_pipes(cmds) == 0
    assert OPATH.is_file()
    assert OPATH.stat().st_size > 0
