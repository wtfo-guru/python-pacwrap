import pytest

from pacwrap.apt import AptHandler
from pacwrap.dnf import DnfHandler
from pacwrap.mkhandler import create_handler
from pacwrap.pacman import PacmanHandler
from pacwrap.yum import YumHandler

gt_opts = {
    "test": True,
    "osid": "gentoo",
    "oslike": "gentoo",
}

apt_opts = {
    "test": True,
    "osid": "linuxmint",
    "oslike": "ubuntu debian",
}

pm_opts = {
    "test": True,
    "osid": "arch",
    "oslike": "arch",
}

yum_opts = {
    "test": True,
    "osid": "fedora",
    "oslike": "rhel",
    "osvers": "21",
}

dnf_opts = {
    "test": True,
    "osid": "rocky",
    "oslike": "rhel",
    "osvers": "9",
}


def test_create_apt_handler() -> None:
    """Test create apt handler."""
    pwh = create_handler(apt_opts)
    assert isinstance(pwh, AptHandler)


def test_create_pacman_handler() -> None:
    """Test create apt handler."""
    pwh = create_handler(pm_opts)
    assert isinstance(pwh, PacmanHandler)


def test_create_yum_handler() -> None:
    """Test create yum handler."""
    pwh = create_handler(yum_opts)
    assert isinstance(pwh, YumHandler)


def test_create_dnf_handler() -> None:
    """Test create dnf handler."""
    pwh = create_handler(dnf_opts)
    assert isinstance(pwh, DnfHandler)


def test_create_gentoo_handler() -> None:
    """Test create gentoo handler."""
    with pytest.raises(ValueError, match="Unsupported distro"):
        create_handler(gt_opts)
