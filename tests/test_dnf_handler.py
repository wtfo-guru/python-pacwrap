import pytest

from packaging import version

from pacwrap.mkhandler import create_handler
from pacwrap.pkgmgr import PackageHandler
from pacwrap.dnf import DnfHandler

@pytest.fixture()
def pwhandler() -> PackageHandler:
    """Return handler name."""
    options = {
        "test": True,
        "osid": "fedora",
        "osvers": "22",
    }
    return create_handler(options)

@pytest.fixture()
def refresh() -> PackageHandler:
    """Return handler."""
    options = {
        "refresh": True,
        "test": True,
        "osid": "fedora",
        "osvers": "22",
    }
    return create_handler(options)

@pytest.fixture()
def names() -> PackageHandler:
    """Return handler."""
    options = {
        "names_only": True,
        "test": True,
        "osid": "fedora",
        "osvers": "22",
    }
    return create_handler(options)

def test_file_command(capfd, pwhandler):
    """Test dnf handler file command."""
    assert isinstance(pwhandler, DnfHandler)
    tresult = pwhandler.file_action("/usr/bin/bashbug")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: rpm -qf /usr/bin/bashbug" in out


def test_list_package(capfd, pwhandler):
    """Test list package."""
    tresult = pwhandler.list_package("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: rpm -ql bash" in out


def test_list_packages(capfd, pwhandler):
    """Test list package."""
    tresult = pwhandler.list_packages()
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: rpm -qa --qf '%{name}-%{version}-%{release}.%{arch}.rpm\\n' | sort" in out


def test_find_action(capfd, pwhandler):
    """Test find action."""
    tresult = pwhandler.find_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: dnf search bash" in out


def test_find_action_refresh(capfd, refresh):
    """Test find action with refresh."""
    assert isinstance(refresh, DnfHandler)
    tresult = refresh.find_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: dnf --refresh search bash" in out


def test_find_action_names_only(capfd, names):
    """Test find action with names_only."""
    assert isinstance(names, DnfHandler)
    tresult = names.find_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: dnf search bash" in out


def test_info_action(capfd, pwhandler):
    """Test find action with names_only."""
    tresult = pwhandler.info_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: rpm -qi bash" in out


def test_install_action(capfd, pwhandler):
    """Test install action."""
    tresult = pwhandler.install_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: dnf install bash" in out


def test_install_action_refresh(capfd, refresh):
    """Test install action with refresh."""
    tresult = refresh.install_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: dnf --refresh install bash" in out


def test_uninstall_action(capfd, pwhandler):
    """Test uninstall action with refresh."""
    tresult = pwhandler.uninstall_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: dnf remove bash" in out
