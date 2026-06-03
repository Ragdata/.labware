#!/usr/bin/env python3
"""
====================================================================
Package: labware
====================================================================
Author:			Ragdata
Date:			19/04/2026
License:		MIT License
Repository:		https://github.com/Ragdata/.labware
Copyright:		Copyright © 2026 Redeyed Technologies
====================================================================
"""
import shutil, grp, sys

from pathlib import Path

BASEDIR = Path(__file__).parents[2]

sys.path.append(str(BASEDIR))

from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from labware.utils import *

TEMPLATES = BASEDIR / config.get("src", "setup")

#-------------------------------------------------------------------
# MODULE VARIABLES
#-------------------------------------------------------------------
loader = Environment(loader=FileSystemLoader(str(TEMPLATES)))
#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def backup(filepath: Path, backupdir: Path = Path.home() / ".backup") -> bool:
    """Backup a file to the specified directory"""
    try:
        if not filepath.exists():
            raise FileNotFoundError(f"{filepath} does not exist")
        if not backupdir.exists():
            backupdir.mkdir(parents=True, exist_ok=True, mode=0o755)
        suffix = '.'.join(filepath.suffixes)
        now = datetime.now()
        backupfile = backupdir / f"{filepath.name}.{suffix}.{now.strftime('%Y%m%d-%H%M.%S')}"
        if shutil.copy2(filepath, backupfile):
            return True
    except Exception as e:
        logger.error(f"Failed to get list: {e}", True)
        raise
    return False

def chmod(tgt: Path, mode: int = 0o644) -> None:
    """Smart / Recursive chmod"""
    if tgt.exists():
        os.chmod(tgt, mode)
        if tgt.is_dir():
            for root, dirs, files in os.walk(tgt):
                for d in dirs:
                    os.chmod(os.path.join(root, d), 0o755)
                for f in files:
                    os.chmod(os.path.join(root, f), mode)

def chown(tgt: Path, user: str, group: str) -> None:
    """Smart / Recursive chown"""
    if tgt.exists():
        uid = pwd.getpwnam(user).pw_uid
        gid = grp.getgrnam(group).gr_gid
        os.chown(tgt, uid, gid)
        if tgt.is_dir():
            for root, dirs, files in os.walk(tgt):
                for name in dirs + files:
                    os.chown(os.path.join(root, name), uid, gid)

def copyFiles(src: Path | list[Path], dst: Path, bkp: bool = False, bkpdir: Path = Path.home() / ".backup", mode: int = 0o644, user: str = "", group: str = "") -> bool | None:
    try:
        if not user:
            user = pwd.getpwuid(os.geteuid()).pw_name
        if not group:
            group = user
        if not userExists(user):
            raise RuntimeError(f"User '{user}' does not exist")
        if isinstance(src, Path) and not src.exists():
            raise FileNotFoundError(f"{src} does not exist")
        if not dst.exists():
            dst.mkdir(parents=True, mode=0o755)
        if isinstance(src, list):
            for path in src:
                dstpath = dst / path.name
                if not path.exists():
                    raise FileNotFoundError(f"{path} does not exist")
                if path.is_file() and bkp:
                    backup(path, bkpdir)
                shutil.copy(path, dstpath)
                chown(dst, user, group)
                chmod(dst, mode)
                printSuccess(f"Copied {path.name}")
                logger.debug(f"Copied {path.name}")
                return True
        else:
            if src.is_file():
                if dst.is_file() and bkp:
                    backup(src, bkpdir)
                shutil.copy(src, dst)
                chown(dst, user, group)
                chmod(dst, mode)
                printSuccess(f"Copied {src.name}")
                logger.debug(f"Copied {src.name}")
                return True
            elif src.is_dir() and dst.is_dir():
                for item in os.scandir(src):
                    dest = dst / item.name
                    if item.is_file():
                        if dest.is_file() and bkp:
                            backup(Path(item), bkpdir)
                        if shutil.copy(item, dest):
                            chown(dest, user, group)
                            chmod(dest, mode)
                            printSuccess(f"Copied '{item.name}'")
                            logger.debug(f"Copied '{item.name}'")
                        else:
                            printWarning(f"Copy Failed '{item.name}'")
                            logger.debug(f"Copy Failed '{item.name}'")
                    elif item.is_dir():
                        if shutil.copytree(item, dest, dirs_exist_ok=True):
                            chown(dest, user, group)
                            chmod(dest, mode)
                            printSuccess(f"Copied Tree '{item.name}'")
                            logger.debug(f"Copied Tree '{item.name}'")
                        else:
                            printWarning(f"Copy Tree Failed '{item.name}'")
                            logger.debug(f"Copy Tree Failed '{item.name}'")
                    else:
                        raise TypeError(f"Invalid type copying {src} -> {dst}")
                return True
            else:
                return False
    except Exception as e:
        logger.error(f"Failed to copy files: {e}", True)
        raise

def copyRepoFile(repo: Path, stub: str, bkp: bool = False, bkpdir: Path = Path.home() / ".backup", mode: int = 0o644, user: str = "", group: str = "") -> bool:
    try:
        tmpl = repo / stub
        dest = Path(stub)
        if not user:
            user = pwd.getpwuid(os.geteuid()).pw_name
        if not group:
            group = user
        if not userExists(user):
            raise RuntimeError(f"User '{user}' does not exist")
        if not repo.exists():
            raise FileNotFoundError(f"{repo} does not exist")
        if not tmpl.exists():
            raise FileNotFoundError(f"{tmpl} does not exist")
        if not dest.parent.exists():
            dest.parent.mkdir(parents=True, mode=0o755)
        if dest.exists() and bkp:
            backup(dest, bkpdir)
        shutil.copy(tmpl, dest)
        chown(dest, user, group)
        chmod(dest, mode)
        printSuccess(f"Copied {dest.name}")
        logger.debug(f"Copied {dest.name}")
        return True
    except Exception as e:
        logger.error(f"Failed to copy files: {e}", True)
        raise

def copyRepoFiles(repo: Path, data: list[str], bkp: bool = False, bkpdir: Path = Path.home() / ".backup", mode: int = 0o644, user: str = "", group: str = "") -> bool:
    try:
        for filepath in data:
            if not copyRepoFile(repo, filepath, bkp, bkpdir, mode, user, group):
                logger.error(f"Failed to copy files: {filepath}", True)
                return False
        return True
    except Exception as e:
        logger.error(f"Failed to copy files: {e}", True)
        raise

def findFileString(filepath: Path, string: str) -> bool:
    try:
        if not filepath.exists():
            raise FileNotFoundError(f"File not found '{filepath}'")
        with open(str(filepath), 'r') as f:
            for l in f:
                if string in l:
                    return True
        return False
    except Exception as e:
        logger.error(f"{e}", True)
        raise

def getList(filepath: Path) -> list:
    try:
        if not filepath.exists():
            raise FileNotFoundError(f"{filepath} does not exist")
        with open(str(filepath), 'r') as f:
            lines = [l.strip() for l in f]
            return lines
    except Exception as e:
        logger.error(f"Failed to get list: {e}", True)
        raise

def mergeFiles(files: list[str], file: str) -> bool:
    try:
        seen = set()
        with open(file, 'w', encoding='utf-8') as out:
            for filepath in files:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for l in f:
                        if l not in seen:
                            out.write(l)
                            seen.add(l)
        return True
    except Exception as e:
        logger.error(f"Failed to merge files: {e}", True)
        raise

def perms(src: dict[str, list]) -> None:
    for path, data in src.items():
        chmod(Path(path), data[0])
        chown(Path(path), data[1], data[2])

def writeFile(dst: Path, data: str, mode: int = 0o644, user: str = "", group: str = "") -> bool:
    try:
        if not user:
            user = pwd.getpwuid(os.geteuid()).pw_name
        if not group:
            group = user
        if not userExists(user):
            raise RuntimeError(f"User {user} does not exist")
        if not dst.parent.exists():
            dst.parent.mkdir(parents=True, mode=0o755)
        if dst.exists():
            os.remove(dst)
        with open(str(dst), 'w') as f:
            f.write(data)
        chown(dst, user, group)
        chmod(dst, mode)
        printSuccess(f"Wrote File: {dst}")
        logger.debug(f"Wrote File: {dst}")
        return True
    except Exception as e:
        logger.error(f"File write failed: {e}", True)
        raise

def writeTemplate(tmpl: Path, dest: Path, data: dict, mode: int = 0o644, user: str = "", group: str = "", bkp: bool = True, bkpdir: Path = Path.home() / ".backup") -> bool:
    try:
        if not user:
            user = pwd.getpwuid(os.geteuid()).pw_name
        if not group:
            group = user
        if not userExists(user):
            raise RuntimeError(f"User {user} does not exist")
        if not tmpl.exists():
            raise FileNotFoundError(f"{tmpl} does not exist")
        if not dest.parent.exists():
            dest.parent.mkdir(parents=True, mode=0o755)
        if dest.exists():
            os.remove(str(dest))
        template = loader.get_template(str(tmpl))
        if dest.exists() and bkp:
            backup(dest, bkpdir)
        with open(dest, 'w') as f:
            print(template.render(data), file=f)
        chown(dest, user, group)
        chmod(dest, mode)
        printSuccess(f"Wrote template file to '{dest}'")
        logger.debug(f"Wrote template file to '{dest}'")
        return True
    except Exception as e:
        logger.error(f"Template write failed: {e}", True)
        raise

