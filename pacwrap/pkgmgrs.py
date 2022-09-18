import re
import shlex
import subprocess
import tempfile
from pathlib import Path

import distro
from packaging import version

from .options import Options


class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class UsageError(Error):
    """Exception raised for errors with supplied arguments or parameters

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class PackageHandler(Options):
    def unhandled(self, action):
        print("class %s doesn't handle a file %s!" % (self.__class__.__name__, action))
        return 1

    def file_action(self, fpath):
        return self.run_command(self._file_cmd_args(fpath))

    def find_action(self, package):
        return self.unhandled("find")

    def info_action(self, package):
        return self.run_command(self._info_cmd_args(package))

    def install_action(self, package):
        self.requires_super_user()
        return self._install_action(package)

    def uninstall_action(self, package):
        self.requires_super_user()
        return self._uninstall_action(package)

    def list_package(self, package_nm):
        self.run_command(self._list_package_args(package_nm))

    def _list_package_args(self, package_nm):
        return self.unhandled("_list_package_args")

    def _info_cmd_args(self, package_nm):
        return self.unhandled("_info_cmd_args")

    def list_packages(self):
        return self.unhandled("list packages")

    def run_pipes_script(self, cmds):
        """
        Create a script file of piped commands and run it
        """
        joined = " | ".join(cmds)
        if self.options["test"]:
            print(f"noex: {joined}")
            return 0
        script = f"#!/bin/sh\n\n{joined}"
        fp = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False)
        sname = Path(fp.name)
        print(script, file=fp)
        fp.close()
        sname.chmod(0o755)
        self.run_command([str(sname)])
        sname.unlink(missing_ok=True)

    def run_pipes(self, cmds):
        """
        Run commands in PIPE, return the last process in chain
        """
        if self.options["test"]:
            print("noex: {}".format(" | ".join(cmds)))
            return 0
        cmds = map(shlex.split, cmds)
        first_cmd, *rest_cmds = cmds
        procs = [subprocess.Popen(first_cmd, stdout=subprocess.PIPE)]
        for cmd in rest_cmds:
            last_stdout = procs[-1].stdout
            proc = subprocess.Popen(cmd, stdin=last_stdout, stdout=subprocess.PIPE)
            procs.append(proc)
        last_proc = procs[-1]
        rtnVal = last_proc.wait()
        sout = last_proc.stdout
        if rtnVal != 0:
            serr = last_proc.stderr
        else:
            serr = False
        if self.options["output"] is not None:
            outf = open(self.options["output"], "w")
        else:
            outf = None
        for line in sout:
            line = line.decode()
            if not self.options["quiet"]:
                print(line, end="")
            if outf:
                print(line, end="", file=outf)
        if serr:
            if not self.options["quiet"]:
                print("stderr:")
            if outf:
                print("stderr:", file=outf)
            for line in serr:
                line = line.decode()
                if not self.options["quiet"]:
                    print(line, end="")
                if outf:
                    print(line, end="", file=outf)
        return rtnVal

    def run_command(self, args):
        if self.options["test"]:
            print("noex: {}".format(" ".join(args)))
            return 0
        result = subprocess.run(args, shell=False, capture_output=True)
        rtnVal = result.returncode
        ostr = result.stdout.decode("utf-8")
        if rtnVal != 0:
            estr = result.stderr.decode("utf-8")
        else:
            estr = False
        if self.options["output"] is not None:
            with open(self.options["output"], "w") as out:
                out.write(ostr)
                if estr:
                    print("stderr:", file=out)
                    out.write(estr)
        if not self.options["quiet"]:
            print(ostr)
            if estr:
                print("stderr:")
                print(estr)
        return result.returncode

    @staticmethod
    def create_handler(options):
        osid = distro.id()
        # print(f"osid: {osid}")
        if osid == "debian":
            oslike = osid
        elif osid == "fedora":
            oslike = "rhel"
        elif osid == "pop":
            oslike = "debian"
        else:
            oslike = distro.like()
        # print(f"oslike: {oslike}")

        if oslike == "arch":
            handler = PacmanHandler(options)
        elif oslike == "debian":
            handler = AptHandler(options)
        elif re.search("rhel", oslike):
            # should probably check for older fedora
            if version.parse(distro.version()) < version.parse("8"):
                handler = YumHandler(options)
            else:
                handler = DnfHandler(options)
        else:
            raise Exception(f"Unsupported distro like => {oslike}")
        return handler


class PacmanHandler(PackageHandler):
    def _list_package_args(self, package_nm):
        return ["pacman", "-Ql", package_nm]

    def list_packages(self):
        return self.run_command(["pacman", "-Qe"])

    def _file_cmd_args(self, fpath):
        return ["pacman", "-Qo", fpath]

    def _info_cmd_args(self, package):
        return ["pacman", "-Qi", package]

    def find_action(self, package):
        switches = "-Ss"
        if self.options["refresh"]:
            self.requires_super_user()
            switches += "y"
        return self.run_command(["pacman", switches, package])

    def _install_action(self, package):
        switches = "-S"
        if self.options["refresh"]:
            switches = +"y"
        cmd = ["pacman", switches, package]
        return self.run_command(cmd)

    def _uninstall_action(self, package):
        cmd = ["pacman", "-R", package]
        return self.run_command(cmd)


class AptHandler(PackageHandler):
    def _list_package_args(self, package_nm):
        return ["dpkg", "-L", package_nm]

    def list_packages(self):
        return self.run_pipes_script(["apt list --installed", "sort"])

    def _file_cmd_args(self, fpath):
        return ["dpkg", "-S", fpath]

    def _info_cmd_args(self, package):
        return ["apt", "show", package]

    def find_action(self, package):
        if self.options["refresh"]:
            self.requires_super_user()
            self.run_command(["apt", "update"])
        cmd = ["apt", "search"]
        if self.options["names_only"] is not None:
            cmd.append("--names-only")
        cmd.append(package)
        return self.run_command(cmd)

    def _install_action(self, package):
        if self.options["refresh"]:
            self.run_command(["apt", "update"])
        cmd = ["apt", "install", package]
        return self.run_command(cmd)

    def _uninstall_action(self, package):
        cmd = ["apt", "remove", package]
        return self.run_command(cmd)


class YumHandler(PackageHandler):
    def __init__(self, opts={}):
        PackageHandler.__init__(self, opts)  # python2 compatibility
        self.pkgcmd = "yum"

    def _list_package_args(self, package_nm):
        return ["rpm", "-ql", package_nm]

    def list_packages(self):
        cmds = ["rpm -qa --qf '%{name}-%{version}-%{release}.%{arch}.rpm\\n'", "sort"]
        return self.run_pipes(cmds)

    def _file_cmd_args(self, fpath):
        return ["rpm", "-qf", fpath]

    def _info_cmd_args(self, package):
        return ["rpm", "-qi", package]

    def find_action(self, package):
        cmd = [self.pkgcmd, "search", package]
        if self.options["refresh"]:
            self.requires_super_user()
            cmd.insert(1, "--refresh")
        return self.run_command(cmd)

    def _install_action(self, package):
        cmd = [self.pkgcmd, "install", package]
        if self.options["refresh"]:
            cmd.insert(1, "--refresh")
        return self.run_command(cmd)

    def _uninstall_action(self, package):
        cmd = [self.pkgcmd, "remove", package]
        return self.run_command(cmd)


class DnfHandler(YumHandler):
    def __init__(self, opts={}):
        YumHandler.__init__(self, opts)  # python2 compatibility
        self.pkgcmd = "dnf"
