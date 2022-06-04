# -*- Mode: Python; tab-width: 4; indent-tabs-mode: nil -*-

import os
import re
import subprocess

import click
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
    def validate_arg_count(self, action, args, expected, extra=False):
        nbr = len(args)
        if nbr < expected:
            raise UsageError("action %s requires %d arguments" % (action, expected))
        if (not extra) and (nbr > expected):
            raise UsageError(
                "action %s requires exactly %d arguments" % (action, expected)
            )

    def unhandled(self, action):
        print("class %s doesn't handle a file %s!" % (self.__class__.__name__, action))
        return 1

    def file_action(self, fpath):
        return self.execute(self._file_cmd_args(fpath))

    def find_action(self, args):
        return self.unhandled("find")

    def info_action(self, args):
        return self.unhandled("info")

    def install_action(self, args):
        return self.unhandled("install")

    def uninstall_action(self, args):
        return self.unhandled("uninstall")

    def list_package(self, package_nm):
        args = self.get_list_package_args(package_nm)
        if self.options["debug"] > 0:
            print(f"list_package({package_nm}) called")
            print(f"running command: {args}")
        return self.run_command(args)

    def get_list_package_args(self, package_nm):
        return self.unhandled("get_list_package_cmd")

    def list_packages(self):
        return self.unhandled("list packages")

    # def action(self, action, args):
    #     if (self.options["debug"] > 0) or (self.options["verbose"] > 0):
    #         print("action: " + action)
    #         print("args: ", args)
    #     if action == "file":
    #         self.validate_arg_count(action, args, 1)
    #         result = self.file_action(args)
    #     elif (action == "find") or (action == "search"):
    #         self.validate_arg_count(action, args, 1)
    #         result = self.find_action(args)
    #     elif action == "info":
    #         self.validate_arg_count(action, args, 1)
    #         result = self.info_action(args)
    #     elif action == "install":
    #         self.validate_arg_count(action, args, 1, True)
    #         result = self.install_action(args)
    #     elif action == "uninstall":
    #         self.validate_arg_count(action, args, 1, True)
    #         result = self.uninstall_action(args)
    #     elif action == "list":
    #         if len(args) > 0:
    #             self.validate_arg_count(action, args, 1)
    #             result = self.list_package(args)
    #         else:
    #             print("calling list packages")
    #             result = self.list_packages()
    #     else:
    #         raise ValueError(action + " is not a valid action!!!")
    #     return result

    def execute(self, cmd):
        try:
            subprocess.check_call(cmd)
            result = 0
        except subprocess.CalledProcessError as cpex:
            if (self.options["debug"] > 0) or (self.options["verbose"] > 0):
                print(cpex)
            result = cpex.returncode
        except Exception as ex:
            print(ex)
            result = 1
        return result

    def run_command(self, args):
        result = subprocess.run(args, shell=False, capture_output=True)
        # print(result)
        ostr = result.stdout.decode("utf-8")
        if self.options["output"] is not None:
            with open(self.options["output"], "w") as out:
                out.write(ostr)
        click.echo(ostr)
        return result.returncode

    def output_if(self, cmd):
        if self.options["output"] is not None:
            if self.options["quiet"]:
                cmd += " > %s" % self.options["output"]
            else:
                cmd += " | tee %s" % self.options["output"]
        return os.system(cmd)

    @staticmethod
    def create_handler(options):
        osid = distro.id()

        if osid == "debian":
            oslike = osid
        else:
            oslike = distro.like()

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
    def get_list_package_args(self, package_nm):
        return ["pacman", "-Q", "-l", package_nm]

    def list_packages(self):
        result = self.output_if("pacman -Qe")
        return result

    def file_action(self, fpath):
        return self.execute(["pacman", "-Qo", fpath])

    def info_action(self, args):
        return self.execute(["pacman", "-Qi", args[0]])

    def find_action(self, args):
        switches = "-Ss"
        if self.options["refresh"]:
            Options.requires_super_user()
            switches += "y"
        return self.execute(["pacman", switches, args[0]])

    def install_action(self, args):
        Options.requires_super_user()()
        switches = "-S"
        if self.options["refresh"]:
            switches = +"y"
        cmd = ["pacman", switches]
        for i in args:
            cmd.append(i)
        return self.execute(cmd)

    def uninstall_action(self, args):
        Options.requires_super_user()
        cmd = ["pacman", "-R"]
        for i in args:
            cmd.append(i)
        return self.execute(cmd)


class AptHandler(PackageHandler):
    def list_package(self, package_nm):
        return self.output_if(f"dpkg -L {package_nm}")

    def list_packages(self):
        result = self.output_if(r"apt list --installed | sort")
        return result

    def file_action(self, fpath):
        return self.execute(["dpkg", "-S", fpath])

    def info_action(self, args):
        return self.execute(["apt-cache", "show", args[0]])

    def find_action(self, args):
        if self.options["refresh"]:
            Options.requires_super_user()
            self.execute(["apt", "update"])
        cmd = ["apt", "search"]
        if self.options["names-only"] is not None:
            cmd.append("--names-only")
        cmd.append(args[0])
        return self.execute(cmd)

    def install_action(self, args):
        Options.requires_super_user()
        if self.options["refresh"]:
            self.execute(["apt", "update"])
        cmd = ["apt", "install"]
        for i in args:
            cmd.append(i)
        return self.execute(cmd)

    def uninstall_action(self, args):
        Options.requires_super_user()
        cmd = ["apt", "remove"]
        for i in args:
            cmd.append(i)
        return self.execute(cmd)


class YumHandler(PackageHandler):
    def __init__(self, opts={}):
        PackageHandler.__init__(self, opts)  # python2 compatibility
        self.pkgcmd = "yum"

    def list_package(self, package_nm):
        return self.output_if(f"rpm -ql {package_nm}")

    def list_packages(self):
        result = self.output_if(
            "rpm -qa --qf '%{name}-%{version}-%{release}.%{arch}.rpm\\n' | sort"
        )
        return result

    def file_action(self, fpath):
        return self.execute(["rpm", "-qf", fpath])

    def info_action(self, args):
        return self.execute(["rpm", "-qi", args[0]])

    def find_action(self, args):
        cmd = [self.pkgcmd, "search", args[0]]
        if self.options["refresh"]:
            Options.requires_super_user()
            cmd.insert(1, "--refresh")
        return self.execute(cmd)

    def install_action(self, args):
        Options.requires_super_user()
        cmd = [self.pkgcmd, "install"]
        for i in args:
            cmd.append(i)
        if self.options["refresh"]:
            cmd.insert(1, "--refresh")
        return self.execute(cmd)

    def uninstall_action(self, args):
        Options.requires_super_user()
        cmd = [self.pkgcmd, "remove"]
        for i in args:
            cmd.append(i)
        return self.execute(cmd)


class DnfHandler(YumHandler):
    def __init__(self, opts={}):
        YumHandler.__init__(self, opts)  # python2 compatibility
        self.pkgcmd = "dnf"
        if self.options["test"]:
            print("created instance of DnfHandler")
