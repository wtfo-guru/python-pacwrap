import pytest

from pacwrap.dnf import DnfHandler
from pacwrap.mkhandler import create_handler
from pacwrap.pkgmgr import PackageHandler


@pytest.fixture
def pwhandler() -> PackageHandler:
    """Return handler name."""
    options = {
        "test": True,
        "osid": "fedora",
        "osvers": "22",
    }
    return create_handler(options)


@pytest.fixture
def refresh() -> PackageHandler:
    """Return handler."""
    options = {
        "refresh": True,
        "test": True,
        "osid": "fedora",
        "osvers": "22",
    }
    return create_handler(options)


@pytest.fixture
def names() -> PackageHandler:
    """Return handler."""
    options = {
        "names_only": True,
        "test": True,
        "osid": "fedora",
        "osvers": "22",
    }
    return create_handler(options)


def test_file_command(
    capfd: pytest.CaptureFixture[str], pwhandler: PackageHandler
) -> None:
    """Test dnf handler file command."""
    assert isinstance(pwhandler, DnfHandler)
    t_res = pwhandler.file_action("/usr/bin/bashbug")
    out, err = capfd.readouterr()
    assert t_res == 0
    assert "noex: rpm -qf /usr/bin/bashbug" in out


def test_list_package(
    capfd: pytest.CaptureFixture[str], pwhandler: PackageHandler
) -> None:
    """Test list package."""
    t_res = pwhandler.list_package("bash")
    out, err = capfd.readouterr()
    assert t_res == 0
    assert "noex: rpm -ql bash" in out


def test_list_packages(
    capfd: pytest.CaptureFixture[str], pwhandler: PackageHandler
) -> None:
    """Test list package."""
    t_res = pwhandler.list_packages()
    out, err = capfd.readouterr()
    assert t_res == 0
    assert (
        "noex: rpm -qa --qf '%{name}-%{version}-%{release}.%{arch}.rpm\\n' | sort"
        in out
    )


def test_find_action(
    capfd: pytest.CaptureFixture[str], pwhandler: PackageHandler
) -> None:
    """Test find action."""
    t_res = pwhandler.find_action("bash")
    out, err = capfd.readouterr()
    assert t_res == 0
    assert "noex: dnf search bash" in out


def test_find_action_refresh(
    capfd: pytest.CaptureFixture[str], refresh: PackageHandler
) -> None:
    """Test find action with refresh."""
    assert isinstance(refresh, DnfHandler)
    t_res = refresh.find_action("bash")
    out, err = capfd.readouterr()
    assert t_res == 0
    assert "noex: dnf --refresh search bash" in out


def test_find_action_names_only(
    capfd: pytest.CaptureFixture[str], names: PackageHandler
) -> None:
    """Test find action with names_only."""
    assert isinstance(names, DnfHandler)
    t_res = names.find_action("bash")
    out, err = capfd.readouterr()
    assert t_res == 0
    assert "noex: dnf search bash" in out


def test_info_action(
    capfd: pytest.CaptureFixture[str], pwhandler: PackageHandler
) -> None:
    """Test find action with names_only."""
    t_res = pwhandler.info_action("bash")
    out, err = capfd.readouterr()
    assert t_res == 0
    assert "noex: rpm -qi bash" in out


def test_install_action(
    capfd: pytest.CaptureFixture[str], pwhandler: PackageHandler
) -> None:
    """Test install action."""
    t_res = pwhandler.install_action("bash")
    out, err = capfd.readouterr()
    assert t_res == 0
    assert "noex: dnf install bash" in out


def test_install_action_refresh(
    capfd: pytest.CaptureFixture[str], refresh: PackageHandler
) -> None:
    """Test install action with refresh."""
    t_res = refresh.install_action("bash")
    out, err = capfd.readouterr()
    assert t_res == 0
    assert "noex: dnf --refresh install bash" in out


def test_uninstall_action(
    capfd: pytest.CaptureFixture[str], pwhandler: PackageHandler
) -> None:
    """Test uninstall action with refresh."""
    t_res = pwhandler.uninstall_action("bash")
    out, err = capfd.readouterr()
    assert t_res == 0
    assert "noex: dnf remove bash" in out
