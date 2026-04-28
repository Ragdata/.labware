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
import os
import shutil
import subprocess
import typer
import getpass
import pwd
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from passlib.context import CryptContext

from .logger import *
from .console import *

app = typer.Typer(name="install", rich_markup_mode="rich", no_args_is_help=True)


#-------------------------------------------------------------------
# MODULE VARIABLES
#-------------------------------------------------------------------
NEW_USER: str = ""
NEW_USER_PASSWORD: str = ""
SCR_PATH: Path = Path(__file__).resolve()
REPO_PATH: Path = SCR_PATH.parent.parent.parent
TEMPLATES_PATH: Path = SCR_PATH.parent / "templates"
SYS_DOTS_PATH: Path = REPO_PATH / "sys" / "dots"
SYS_LIB_PATH: Path = REPO_PATH / "sys" / "lib"

# Password hashing context using SHA512 (compatible with Linux shadow passwords)
pwd_context = CryptContext(schemes=["sha512_crypt"], deprecated="auto")


#-------------------------------------------------------------------
# MODULE FUNCTIONS
#-------------------------------------------------------------------
def appBanner() -> None:
    logger.info("Labware Installer Started")
    line()
    rule("[bold yellow]Labware Installer")
    line()

def checkPython() -> None:
    if sys.version_info < (3, 12):
        errorExit(f"Requires Python 3.12 or later")
    else:
        printSuccess("Python 3.12 or later confirmed")

def checkRoot() -> None:
    if os.geteuid() != 0:
        errorExit(f"Root privileges required")
    else:
        printSuccess("Root privileges confirmed")

def checkUbuntu() -> None:
    version = run("lsb_release -rs", capture=True).stdout.strip()
    if version != "24.04":
        errorExit(f"Expected Ubuntu 24.04, found '{version}'")
    else:
        printSuccess("Ubuntu 24.04 confirmed")

def copyDotfiles(target_user: str, target_home: Path, debug: Optional[bool] = False) -> bool:
    """
    Copy dotfiles from sys/dots and sys/lib to target user's home directory.

    Args:
        target_user (str): Username to set ownership to
        target_home (Path): Target user's home directory
        debug (bool): Enable debug output

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        printHead(f"Copying Dotfiles to {target_user}")
        line()
        logger.info(f"Copying dotfiles to {target_user}")

        # Get user ID and group ID
        user_info = pwd.getpwnam(target_user)
        uid = user_info.pw_uid
        gid = user_info.pw_gid

        # Copy dots directory (.bashrc, .bashrc.d/, .profile)
        if SYS_DOTS_PATH.exists():
            for item in os.scandir(SYS_DOTS_PATH):
                src_path = Path(item.path)
                dst_path = target_home / item.name

                try:
                    if item.is_file():
                        shutil.copy2(src_path, dst_path)
                        os.chown(dst_path, uid, gid)
                        printDot(f"Copied {item.name}")
                        logger.debug(f"Copied {src_path} to {dst_path}")
                    elif item.is_dir() and not dst_path.exists():
                        shutil.copytree(src_path, dst_path)
                        os.chown(dst_path, uid, gid)
                        printDot(f"Copied {item.name}/")
                        logger.debug(f"Copied dir {src_path} to {dst_path}")
                except Exception as e:
                    logger.warning(f"Failed to copy {item.name}: {e}")
                    printWarning(f"Failed to copy {item.name}: {e}")
        else:
            logger.warning(f"Source dots directory not found: {SYS_DOTS_PATH}")
            printWarning(f"Source dots directory not found: {SYS_DOTS_PATH}")

        # Copy lib directory structure (aliases, completions, functions)
        if SYS_LIB_PATH.exists():
            lib_dst = target_home / ".dotfiles" / "lib"
            lib_dst.mkdir(parents=True, exist_ok=True)
            os.chown(lib_dst, uid, gid)

            for item in os.scandir(SYS_LIB_PATH):
                src_path = Path(item.path)
                dst_path = lib_dst / item.name

                try:
                    if item.is_dir() and not dst_path.exists():
                        shutil.copytree(src_path, dst_path)
                        os.chown(dst_path, uid, gid)
                        # Recursively chown all files
                        for root, dirs, files in os.walk(dst_path):
                            for d in dirs:
                                os.chown(os.path.join(root, d), uid, gid)
                            for f in files:
                                os.chown(os.path.join(root, f), uid, gid)
                        printDot(f"Copied lib/{item.name}/")
                        logger.debug(f"Copied lib dir {src_path} to {dst_path}")
                except Exception as e:
                    logger.warning(f"Failed to copy lib/{item.name}: {e}")
                    printWarning(f"Failed to copy lib/{item.name}: {e}")
        else:
            logger.warning(f"Source lib directory not found: {SYS_LIB_PATH}")
            printWarning(f"Source lib directory not found: {SYS_LIB_PATH}")

        line()
        printSuccess("Dotfiles copied successfully!")
        logger.info(f"Dotfiles copied to {target_user}")
        return True
    except Exception as e:
        logger.error(f"Error copying dotfiles: {e}")
        printError(f"Error copying dotfiles: {e}")
        return False

def run(command: str, check=True, capture=False, input_txt=None):
    """ Execute shell command with error handling """
    try:
        if not capture:
            printDot(f"{command}")
        result = subprocess.run(command, shell=True, check=check, text=True, capture_output=capture, input=input_txt)
        return result
    except subprocess.CalledProcessError as e:
        outlog.logError(f"Command failed: {command}\n{e.stderr.strip()}")
        if check:
            sys.exit(1)
        return e

def getSudoUsers():
    """ Get list of users in sudo group """
    result = run("getent group sudo | cut -d: -f4", capture=True)
    return result.stdout.strip().split(',') if result.stdout.strip() else []

# def promptUsername():
#     """ Smart Username Prompt """
#     global NEW_USER
#     existing_users = getSudoUsers()
#     if existing_users and existing_users != ['']:
#         printSuccess(f"Found existing sudo users: {', '.join(existing_users)}")
#         use_existing = input("Use an existing sudo user? (y/N): ").lower()
#         if use_existing == 'y':
#             while True:
#                 user = input("Enter existing username: ").strip().lower()
#                 if user in existing_users:
#                     NEW_USER = user
#                     printSuccess(f"Using existing sudo user: {NEW_USER}")
#                     return
#                 printError(f"User '{user}' not found or not in sudo group.")
#         while True:
#             user = input("New sudo username: ").strip().lower()
#             if user.isalnum() and len(user) <= 32:
#                 NEW_USER = user
#                 break
#             printError(f"Use lowercase alphanumeric, max 32 chars")

def userExists():
    return run(f"id {NEW_USER}", check=False, capture=True).returncode == 0

#-------------------------------------------------------------------
# CREATE NEW SUDO USER
#-------------------------------------------------------------------
def promptNewUser() -> bool:
    """
    Prompt for new user creation with password setup.

    Returns:
        bool: True if user wants to create new user, False otherwise
    """
    global NEW_USER, NEW_USER_PASSWORD

    create_user = getData("[cyan]Create a new sudo user?[/cyan] (y/N): ").lower()
    if create_user != 'y':
        return False

    while True:
        username = getData("[cyan]New sudo username[/cyan] (lowercase alphanumeric, max 32 chars): ").strip().lower()
        if username.isalnum() and len(username) <= 32:
            if not run(f"id {username}", check=False, capture=True).returncode == 0:
                NEW_USER = username
                break
            else:
                printError(f"User '{username}' already exists")
        else:
            printError("Use lowercase alphanumeric characters only, max 32 characters")

    while True:
        password = getpass.getpass(f"Enter password for {NEW_USER}: ")
        password_confirm = getpass.getpass(f"Confirm password for {NEW_USER}: ")
        if password == password_confirm and len(password) >= 8:
            NEW_USER_PASSWORD = password
            break
        elif len(password) < 8:
            printError("Password must be at least 8 characters")
        else:
            printError("Passwords do not match")

    return True

def createSudoUser() -> bool:
    """
    Create a new sudo user with home directory and add to sudo group.

    Returns:
        bool: True if successful, False otherwise
    """
    if not NEW_USER:
        return False

    try:
        printHead(f"Creating New User: {NEW_USER}")
        line()
        logger.info(f"Creating new user: {NEW_USER}")

        # Create user with home directory
        home_dir = Path("/home") / NEW_USER
        run(f"useradd -m -s /bin/bash -d {home_dir} {NEW_USER}")
        printDot(f"User {NEW_USER} created")
        logger.debug(f"User {NEW_USER} created with home directory {home_dir}")

        # Set password using passlib for SHA512 hashing
        encrypted_password = pwd_context.hash(NEW_USER_PASSWORD)
        result = run(f"usermod -p '{encrypted_password}' {NEW_USER}", check=False, capture=True)
        if result.returncode == 0:
            printDot(f"Password set for {NEW_USER}")
            logger.info(f"Password set for {NEW_USER}")
        else:
            printWarning(f"Could not set password: {result.stderr if hasattr(result, 'stderr') else 'Unknown error'}")

        # Add to sudo group
        run(f"usermod -aG sudo {NEW_USER}")
        printDot(f"User {NEW_USER} added to sudo group")
        logger.debug(f"User {NEW_USER} added to sudo group")

        # Copy dotfiles to new user's home
        if not copyDotfiles(NEW_USER, home_dir):
            printWarning("Some dotfiles failed to copy")

        # Ask about passwordless sudo
        allow_nopass = getData("[cyan]Allow sudo without password?[/cyan] (y/N): ").lower()
        if allow_nopass == 'y':
            sudoers_file = Path(f"/etc/sudoers.d/{NEW_USER}")
            sudoers_content = f"{NEW_USER} ALL=(ALL) NOPASSWD:ALL\n"
            sudoers_file.write_text(sudoers_content)
            os.chmod(sudoers_file, 0o440)
            printDot(f"Sudoers entry created for {NEW_USER}")
            logger.info(f"Passwordless sudo configured for {NEW_USER}")

        line()
        printSuccess(f"User {NEW_USER} created successfully!")
        logger.info(f"User {NEW_USER} setup complete")
        return True
    except Exception as e:
        logger.error(f"Error creating user {NEW_USER}: {e}")
        printError(f"Error creating user {NEW_USER}: {e}")
        return False

#-------------------------------------------------------------------
# INSTALL AND CONFIGURE GNUPG2
#-------------------------------------------------------------------
def installGnupg2() -> bool:
    """
    Ensure GNUPG2 is installed.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        printHead("Installing GNUPG2")
        line()
        logger.info("Installing GNUPG2")

        # Check if already installed
        result = run("which gpg", check=False, capture=True)
        if result.returncode == 0:
            printSuccess("GNUPG2 already installed")
            logger.debug("GNUPG2 already installed")
            return True

        # Install gnupg2
        run("apt install -y gnupg2")
        printDot("GNUPG2 installed")
        logger.info("GNUPG2 installed successfully")

        line()
        printSuccess("GNUPG2 installation complete!")
        return True
    except Exception as e:
        logger.error(f"Error installing GNUPG2: {e}")
        printError(f"Error installing GNUPG2: {e}")
        return False

def importGpgKey() -> bool:
    """
    Optionally import a GPG key for the new user.

    Returns:
        bool: True if successful or skipped, False on error
    """
    if not NEW_USER:
        return False

    try:
        import_key = getData("[cyan]Import a GPG key?[/cyan] (y/N): ").lower()
        if import_key != 'y':
            return True

        printHead(f"Importing GPG Key for {NEW_USER}")
        line()
        logger.info(f"Importing GPG key for {NEW_USER}")

        key_file = getData("[cyan]Enter path to GPG public key file[/cyan]: ").strip()
        key_path = Path(key_file)

        if not key_path.exists():
            printError(f"File not found: {key_file}")
            logger.error(f"GPG key file not found: {key_file}")
            return False

        # Import key as new user
        user_gpg_home = Path("/home") / NEW_USER / ".gnupg"
        user_info = pwd.getpwnam(NEW_USER)
        uid = user_info.pw_uid
        gid = user_info.pw_gid

        # Ensure .gnupg directory exists with proper permissions
        user_gpg_home.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chown(user_gpg_home, uid, gid)

        # Import key
        run(f"sudo -u {NEW_USER} gpg --import {key_path}", check=False)
        printDot(f"GPG key imported for {NEW_USER}")
        logger.info(f"GPG key imported for {NEW_USER}")

        line()
        printSuccess("GPG key imported successfully!")
        return True
    except Exception as e:
        logger.error(f"Error importing GPG key: {e}")
        printError(f"Error importing GPG key: {e}")
        return False

#-------------------------------------------------------------------
# INSTALL AND CONFIGURE GIT
#-------------------------------------------------------------------
def installGit() -> bool:
    """
    Ensure Git is installed.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        printHead("Installing Git")
        line()
        logger.info("Installing Git")

        # Check if already installed
        result = run("which git", check=False, capture=True)
        if result.returncode == 0:
            printSuccess("Git already installed")
            logger.debug("Git already installed")
            return True

        # Install git
        run("apt install -y git")
        printDot("Git installed")
        logger.info("Git installed successfully")

        line()
        printSuccess("Git installation complete!")
        return True
    except Exception as e:
        logger.error(f"Error installing Git: {e}")
        printError(f"Error installing Git: {e}")
        return False

def configureGit() -> bool:
    """
    Configure Git using the .gitconfig template for the new user.

    Returns:
        bool: True if successful or skipped, False on error
    """
    if not NEW_USER:
        return False

    try:
        configure_git = getData("[cyan]Configure Git for this user?[/cyan] (y/N): ").lower()
        if configure_git != 'y':
            return True

        printHead(f"Configuring Git for {NEW_USER}")
        line()
        logger.info(f"Configuring Git for {NEW_USER}")

        # Collect git configuration
        user_name = getData("[cyan]Git user name[/cyan]: ").strip()
        user_email = getData("[cyan]Git user email[/cyan]: ").strip()

        # Ask for GPG signing key
        use_gpg = getData("[cyan]Use GPG signing for commits?[/cyan] (y/N): ").lower()
        signing_key = ""
        if use_gpg == 'y':
            signing_key = getData("[cyan]GPG signing key ID[/cyan]: ").strip()

        # Render template
        env = Environment(loader=FileSystemLoader(TEMPLATES_PATH))
        template = env.get_template(".gitconfig")
        gitconfig_content = template.render(
            user_name=user_name,
            user_email=user_email,
            signing_key=signing_key if signing_key else "KEY_ID"
        )

        # Write to user's home directory
        gitconfig_path = Path("/home") / NEW_USER / ".gitconfig"
        gitconfig_path.write_text(gitconfig_content)

        # Set proper ownership
        user_info = pwd.getpwnam(NEW_USER)
        os.chown(gitconfig_path, user_info.pw_uid, user_info.pw_gid)
        gitconfig_path.chmod(0o644)

        printDot(f".gitconfig created for {NEW_USER}")
        logger.info(f"Git configured for {NEW_USER}")

        line()
        printSuccess("Git configuration complete!")
        return True
    except Exception as e:
        logger.error(f"Error configuring Git: {e}")
        printError(f"Error configuring Git: {e}")
        return False

#-------------------------------------------------------------------
# INSTALL AND CONFIGURE SSHD
#-------------------------------------------------------------------
def installSshd() -> bool:
    """
    Ensure SSH server is installed.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        printHead("Installing OpenSSH Server")
        line()
        logger.info("Installing OpenSSH Server")

        # Check if already installed
        result = run("which sshd", check=False, capture=True)
        if result.returncode == 0:
            printSuccess("OpenSSH Server already installed")
            logger.debug("OpenSSH Server already installed")
            return True

        # Install openssh-server
        run("apt install -y openssh-server")
        printDot("OpenSSH Server installed")
        logger.info("OpenSSH Server installed successfully")

        line()
        printSuccess("OpenSSH Server installation complete!")
        return True
    except Exception as e:
        logger.error(f"Error installing OpenSSH Server: {e}")
        printError(f"Error installing OpenSSH Server: {e}")
        return False

def configureSshd() -> bool:
    """
    Configure SSHD using the sshd_config template.

    Returns:
        bool: True if successful, False otherwise
    """
    if not NEW_USER:
        return False

    try:
        configure_sshd = getData("[cyan]Configure SSH Server?[/cyan] (y/N): ").lower()
        if configure_sshd != 'y':
            return True

        printHead("Configuring SSH Server")
        line()
        logger.info("Configuring SSH Server")

        # Backup original sshd_config
        sshd_config_path = Path("/etc/ssh/sshd_config")
        backup_path = Path("/etc/ssh/sshd_config.bak")

        if sshd_config_path.exists() and not backup_path.exists():
            shutil.copy2(sshd_config_path, backup_path)
            printDot("Original sshd_config backed up")
            logger.debug("Backed up original sshd_config")

        # Render template
        env = Environment(loader=FileSystemLoader(TEMPLATES_PATH))
        template = env.get_template("sshd_config")
        sshd_content = template.render(NEW_USER=NEW_USER)

        # Write new config
        sshd_config_path.write_text(sshd_content)
        sshd_config_path.chmod(0o600)

        printDot("sshd_config updated")
        logger.info("sshd_config configured")

        # Validate and restart SSH
        result = run("sshd -t", check=False, capture=True)
        if result.returncode == 0:
            run("systemctl restart ssh")
            printDot("SSH server restarted")
            logger.info("SSH server restarted successfully")
        else:
            printWarning("SSH config validation failed - check manually")
            logger.warning(f"SSH config validation failed: {result.stderr if hasattr(result, 'stderr') else 'Unknown error'}")

        line()
        printSuccess("SSH Server configuration complete!")
        return True
    except Exception as e:
        logger.error(f"Error configuring SSH Server: {e}")
        printError(f"Error configuring SSH Server: {e}")
        return False

#-------------------------------------------------------------------
# MODULE COMMANDS
#-------------------------------------------------------------------
def cmd(debug: Optional[bool] = False) -> None:
    """ Installer Entrypoint - orchestrates all setup steps """
    homedir = Path.home()
    run("clear")
    appBanner()
    checkRoot()
    checkUbuntu()
    checkPython()

    line()
    rule("[bold cyan]Step 1: Create New Sudo User")
    line()
    if promptNewUser():
        if not createSudoUser():
            printWarning("User creation encountered issues")
    else:
        printInfo("Skipping user creation")

    line()
    rule("[bold cyan]Step 2: Install and Configure GNUPG2")
    line()
    if installGnupg2():
        importGpgKey()
    else:
        printWarning("GNUPG2 installation failed")

    line()
    rule("[bold cyan]Step 3: Install and Configure Git")
    line()
    if installGit():
        configureGit()
    else:
        printWarning("Git installation failed")

    line()
    rule("[bold cyan]Step 4: Install and Configure SSH Server")
    line()
    if installSshd():
        configureSshd()
    else:
        printWarning("SSH installation failed")

    line()
    rule("[bold green]Installation Complete!")
    line()
    printSuccess("System setup complete!")
    if NEW_USER:
        printInfo(f"New user '{NEW_USER}' has been created and configured")
    logger.info("Installation completed successfully")

