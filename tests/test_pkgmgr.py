import shutil
import tempfile
from pathlib import Path

import pytest

from pacwrap.pkgmgr import PackageHandler

OPATH = Path(tempfile.mkdtemp()) / "wtf-pkgmgr-test.txt"

test_opts = {"test": True, "debug": 0, "verbose": 0}
out_opts = {"test": False, "output": str(OPATH)}


LBASH = "bash"


def test_handler_file_action():
    """Test file action."""
    ohndlr = PackageHandler()
    with pytest.raises(NotImplementedError):
        ohndlr.file_action("/bin/bash")


def test_handler_info_action():
    """Test info action."""
    ohndlr = PackageHandler()
    with pytest.raises(NotImplementedError):
        ohndlr.info_action(LBASH)


def test_handler_install_action():
    """Test install action."""
    ohndlr = PackageHandler(test_opts)
    with pytest.raises(NotImplementedError):
        ohndlr.install_action(LBASH)


def test_handler_uninstall_action():
    """Test uninstall action."""
    ohndlr = PackageHandler(test_opts)
    with pytest.raises(NotImplementedError):
        ohndlr.uninstall_action(LBASH)


def test_handler_find_action():
    """Test find action."""
    ohndlr = PackageHandler()
    with pytest.raises(NotImplementedError):
        ohndlr.find_action(LBASH)


def test_handler_list_packages():
    """Test list packages."""
    ohndlr = PackageHandler()
    with pytest.raises(NotImplementedError):
        ohndlr.list_packages()


def test_handler_list_package():
    """Test list package."""
    ohndlr = PackageHandler()
    with pytest.raises(NotImplementedError):
        ohndlr.list_package(LBASH)


def test_handler_run_pipes_script_good():
    """Test run pipes script good result."""
    cmds = ("ls -l {0}".format(tempfile.gettempdir()), "sort")
    ohndlr = PackageHandler()
    assert ohndlr.run_pipes_script(cmds) == 0


def test_handler_run_pipes_script_bad():
    """Test run pipes script bad result."""
    cmds = ("ls -l {0}".format(tempfile.gettempdir()), "sort", "false")
    ohndlr = PackageHandler()
    assert ohndlr.run_pipes_script(cmds) == 1


def test_handler_run_pipes_script_output():
    """Test run pipes script file output."""
    cmds = ("ls -l {0}".format(tempfile.gettempdir()), "sort")
    ohndlr = PackageHandler(out_opts)
    assert ohndlr.run_pipes_script(cmds) == 0
    assert OPATH.is_file()
    assert OPATH.stat().st_size > 0
    shutil.rmtree(OPATH.parent)
