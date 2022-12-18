import re

import distro
from packaging import version
from wtforglib.kinds import StrAnyDict

from pacwrap.apt import AptHandler
from pacwrap.dnf import DnfHandler
from pacwrap.pacman import PacmanHandler
from pacwrap.pkgmgr import PackageHandler
from pacwrap.yum import YumHandler


def get_oslike() -> str:
    """Returns disrto like sanely."""
    osid = distro.id()
    if osid == "debian":
        return osid
    elif osid == "fedora":
        return "rhel"
    elif osid == "pop":
        return "debian"
    return distro.like()


def create_rhel_handler(options: StrAnyDict) -> PackageHandler:
    """Returns package handler for redhat family."""
    # should probably check for older fedora
    if version.parse(distro.version()) < version.parse("8"):
        return YumHandler(options)
    return DnfHandler(options)


def create_handler(options: StrAnyDict) -> PackageHandler:
    """Returns package handler for distro."""
    oslike = get_oslike()

    phandler: PackageHandler

    if oslike == "arch":
        phandler = PacmanHandler(options)
    elif oslike == "debian":
        phandler = AptHandler(options)
    elif re.search("rhel", oslike):
        phandler = create_rhel_handler(options)
    else:
        raise ValueError("Unsupported distro like => {0}".format(oslike))
    return phandler
