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
from .utils import backup

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

def copyDirFiles(source: Path, target: Path, usr: str) -> bool:
    try:
        usrinfo = pwd.getpwnam(usr)
        uid = usrinfo.pw_uid
        gid = usrinfo.pw_gid
        if not source.exists():
            errorExit(f"Source directory not found: {source}")
        if source.is_file(follow_symlinks=True):
            errorExit(f"Source must be a directory path")
        if not target.exists():
            target.mkdir(parents=True, exist_ok=True, mode=0o755)
        for item in os.scandir(source):
            src = Path(item.path)
            dst = target / item.name
            try:
                if item.is_file():
                    shutil.copy2(src, dst)
                    os.chown(dst, uid, gid)
                    printDot(f"Copied {item.name}")
                    logger.debug(f"Copied {src} to {dst}")
                elif item.is_dir():
                    shutil.copytree(src, dst)
                    os.chown(dst, uid, gid)
                    printDot(f"Copied {item.name}")
                    logger.debug(f"Copied dir {src} to {dst}")
            except Exception as e:
                outlog.logWarning(f"Failed to copy {item.name}: {e}")
    except Exception as e:
        raise e
    return True

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
                    outlog.logWarning(f"Failed to copy {item.name}: {e}")
        else:
            outlog.logWarning(f"Source dots directory not found: {SYS_DOTS_PATH}")

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
                    outlog.logWarning(f"Failed to copy lib/{item.name}: {e}")
        else:
            outlog.logWarning(f"Source lib directory not found: {SYS_LIB_PATH}")

        line()
        printSuccess("Dotfiles copied successfully!")
        logger.info(f"Dotfiles copied to {target_user}")
        return True
    except Exception as e:
        outlog.logError(f"Error copying dotfiles: {e}")
        return False

def installPackages(packages: list):
    try:
        for pkg in packages:
            if pkg[0] == "#":
                continue
            result = run(f"dpkg -s {pkg}", check=False, capture=True)
            if result.returncode != 0:
                run(f"DEBIAN_FRONTEND=noninteractive apt install -y {pkg}")
                printDot(f"Installed package: {pkg}")
                logger.info(f"Installed package: {pkg}")
            else:
                printDot(f"Package already installed: {pkg}")
                logger.debug(f"Package already installed: {pkg}")
    except Exception as e:
        raise e

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
# INSTALL VIRTUALMIN / WEBMIN
#-------------------------------------------------------------------
def installAdmin() -> bool:
    try:
        printHead("Installing Server Admin Package")
        line()
        logger.info("Installing Server Admin Package")

        printWhite("Server Admin Packages installed")
        printGreen("1. Install Virtualmin")
        printGreen("2. Install Webmin")
        printGreen("3. Skip")

        adminsys = getData("[cyan]Choose an option[/cyan] (1-3): ")

        if adminsys == '1':
            printWhite("Installing Virtualmin")
            run('sh -c "$(curl -fsSL https://software.virtualmin.com/gpl/scripts/virtualmin-install.sh)" -- --bundle LEMP')
            outlog.logSuccess("Virtualmin successfully installed")
            return True
        elif adminsys == '2':
            printWhite("Installing Webmin")
            run('curl -o webmin-setup-repo.sh https://raw.githubusercontent.com/webmin/webmin/master/webmin-setup-repo.sh')
            outlog.logSuccess("Webmin successfully installed")
            adminrepo = getData("[cyan]Do you want to install the Webmin APT Repo?[/cyan] (y/N): ").lower()
            if not adminrepo == 'y':
                return True
            run('sh webmin-setup-repo.sh')
            return True
        else:
            printWarning("User chose not to install server admin package")
            return True
    except Exception as e:
        raise e

#-------------------------------------------------------------------
# INSTALL AND CONFIGURE DOCKER
#-------------------------------------------------------------------
def installDocker() -> bool:
    """
    Install and secure Docker with rootful configuration.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        printHead("Installing Docker")
        line()
        logger.info("Installing Docker")

        # Check if already installed
        result = run("which docker", check=False, capture=True)
        if result.returncode == 0:
            printSuccess("Docker already installed")
            logger.debug("Docker already installed")
            return True

        # Install Docker using official method
        run("curl -fsSL https://get.docker.com -o get-docker.sh")
        run("sh get-docker.sh")
        printDot("Docker installed")
        logger.info("Docker installed successfully")

        # Start and enable Docker service
        run("systemctl enable docker")
        run("systemctl start docker")
        printDot("Docker service started and enabled")
        logger.info("Docker service configured")

        # Apply security hardening
        if not hardenDocker():
            printWarning("Some Docker security hardening failed")

        line()
        printSuccess("Docker installation and security hardening complete!")
        return True
    except Exception as e:
        logger.error(f"Error installing Docker: {e}")
        printError(f"Error installing Docker: {e}")
        return False

def hardenDocker() -> bool:
    """
    Apply security hardening to Docker installation.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        printHead("Hardening Docker Security")
        line()
        logger.info("Applying Docker security hardening")

        # Create Docker daemon configuration
        daemon_config = {
            "icc": False,  # Disable inter-container communication
            "no-new-privileges": True,  # Prevent privilege escalation
            "userns-remap": "default",  # Enable user namespace remapping
            "log-driver": "json-file",
            "log-opts": {
                "max-size": "10m",
                "max-file": "3"
            },
            "storage-driver": "overlay2",
            "features": {
                "buildkit": True
            }
        }

        # Write daemon.json
        daemon_path = Path("/etc/docker/daemon.json")
        import json
        daemon_path.write_text(json.dumps(daemon_config, indent=2))
        daemon_path.chmod(0o644)
        printDot("Docker daemon.json configured")
        logger.info("Docker daemon configuration applied")

        # Create Docker security profile
        security_profile = """
# Docker security hardening
* hard nofile 65536
* soft nofile 65536
root hard nofile 65536
root soft nofile 65536
"""

        limits_path = Path("/etc/security/limits.d/docker.conf")
        limits_path.write_text(security_profile.strip())
        limits_path.chmod(0o644)
        printDot("Docker security limits configured")
        logger.info("Docker security limits applied")

        # Restart Docker with new configuration
        run("systemctl restart docker")
        printDot("Docker restarted with security configuration")
        logger.info("Docker restarted with security hardening")

        line()
        printSuccess("Docker security hardening complete!")
        return True
    except Exception as e:
        logger.error(f"Error hardening Docker: {e}")
        printError(f"Error hardening Docker: {e}")
        return False

#-------------------------------------------------------------------
# INSTALL LAZYDOCKER
#-------------------------------------------------------------------
def installLazydocker() -> bool:
    printHead("Installing Lazydocker")
    line()
    logger.info("Installing Lazydocker")
    result = getData("[cyan]Install Lazydocker?[/cyan] (y/N): ").lower()
    if not result == "y":
        return True
    run('curl https://raw.githubusercontent.com/jesseduffield/lazydocker/master/scripts/install_update_linux.sh | bash')
    return True

####################################################################
# SECURITY HARDENING FUNCTIONS
####################################################################


#-------------------------------------------------------------------
# INSTALL AND CONFIGURE AIDE (ADVANCED INTRUSION DETECTION ENVIRONMENT)
#-------------------------------------------------------------------
def installAide() -> bool:
    """
    Install and configure AIDE (Advanced Intrusion Detection Environment).

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        printHead("Installing AIDE (Intrusion Detection)")
        line()
        logger.info("Installing AIDE")

        # Install AIDE
        run("apt install -y aide")
        printDot("AIDE installed")
        logger.info("AIDE installed successfully")

        # Initialize AIDE database
        run("aideinit")
        printDot("AIDE database initialized")
        logger.info("AIDE database initialized")

        # Move database to correct location
        run("mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db")
        printDot("AIDE database moved to production location")
        logger.info("AIDE database configured")

        # Configure daily AIDE check
        cron_job = "0 2 * * * /usr/bin/aide.wrapper --config /etc/aide/aide.conf --check"
        with open("/etc/cron.d/aide", "w") as f:
            f.write(f"{cron_job}\n")
        Path("/etc/cron.d/aide").chmod(0o644)
        printDot("AIDE daily check scheduled")
        logger.info("AIDE cron job configured")

        line()
        printSuccess("AIDE installation and configuration complete!")
        printInfo("AIDE will check system integrity daily at 2 AM")
        return True
    except Exception as e:
        logger.error(f"Error installing AIDE: {e}")
        printError(f"Error installing AIDE: {e}")
        return False

#-------------------------------------------------------------------
# INSTALL AND CONFIGURE APPARMOR
#-------------------------------------------------------------------
def installAppArmor() -> bool:
    """
    Install and configure AppArmor for mandatory access control.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        printHead("Installing AppArmor (MAC)")
        line()
        logger.info("Installing AppArmor")

        # Install AppArmor
        run("apt update")
        run("apt install -y apparmor apparmor-utils apparmor-profiles")
        printDot("AppArmor installed")
        logger.info("AppArmor installed successfully")

        # Enable AppArmor in GRUB
        grub_cmdline = Path("/etc/default/grub")
        content = grub_cmdline.read_text()
        if "apparmor=1" not in content:
            content = content.replace('GRUB_CMDLINE_LINUX_DEFAULT="', 'GRUB_CMDLINE_LINUX_DEFAULT="apparmor=1 ')
            content = content.replace('GRUB_CMDLINE_LINUX="', 'GRUB_CMDLINE_LINUX="apparmor=1 ')
            grub_cmdline.write_text(content)
            printDot("AppArmor enabled in GRUB")
            logger.info("AppArmor enabled in GRUB configuration")

        # Update GRUB
        run("update-grub")
        printDot("GRUB updated")
        logger.info("GRUB configuration updated")

        # Enable AppArmor service
        run("systemctl enable apparmor")
        run("systemctl start apparmor")
        printDot("AppArmor service enabled and started")
        logger.info("AppArmor service configured")

        line()
        printSuccess("AppArmor installation and configuration complete!")
        printInfo("Reboot required for AppArmor to take full effect")
        return True
    except Exception as e:
        logger.error(f"Error installing AppArmor: {e}")
        printError(f"Error installing AppArmor: {e}")
        return False

#-------------------------------------------------------------------
# INSTALL AND CONFIGURE AUDITD
#-------------------------------------------------------------------
def installAuditd() -> bool:
    """
    Install and configure auditd for system auditing.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        printHead("Installing auditd (System Auditing)")
        line()
        logger.info("Installing auditd")

        # Install auditd
        run("apt update")
        run("apt install -y auditd audispd-plugins")
        printDot("auditd installed")
        logger.info("auditd installed successfully")

        # Configure audit rules
        audit_rules = """
# Docker audit rules
-w /usr/bin/docker -p rwxa -k docker
-w /var/lib/docker -p rwxa -k docker
-w /etc/docker -p rwxa -k docker
-w /usr/lib/systemd/system/docker.service -p rwxa -k docker
-w /usr/lib/systemd/system/docker.socket -p rwxa -k docker

# SSH audit rules
-w /etc/ssh/sshd_config -p rwxa -k sshd
-w /etc/ssh -p rwxa -k ssh

# System audit rules
-w /etc/passwd -p rwxa -k passwd
-w /etc/shadow -p rwxa -k shadow
-w /etc/group -p rwxa -k group
-w /etc/sudoers -p rwxa -k sudoers

# Kernel module loading
-w /sbin/insmod -p x -k modules
-w /sbin/rmmod -p x -k modules
-w /sbin/modprobe -p x -k modules
-a always,exit -F arch=b64 -S init_module -S delete_module -k modules

# File system mounts
-a always,exit -F arch=b64 -S mount -S umount -S umount2 -k mount

# Privilege escalation
-a always,exit -F arch=b64 -S su -S sudo -k priv_esc

# Login/logout events
-w /var/log/auth.log -p rwxa -k auth
"""

        audit_rules_path = Path("/etc/audit/rules.d/labware.rules")
        audit_rules_path.write_text(audit_rules.strip())
        audit_rules_path.chmod(0o640)
        printDot("Audit rules configured")
        logger.info("Audit rules configured")

        # Restart auditd
        run("systemctl enable auditd")
        run("systemctl restart auditd")
        printDot("auditd service restarted")
        logger.info("auditd service configured")

        line()
        printSuccess("auditd installation and configuration complete!")
        return True
    except Exception as e:
        logger.error(f"Error installing auditd: {e}")
        printError(f"Error installing auditd: {e}")
        return False

#-------------------------------------------------------------------
# INSTALL AND CONFIGURE UNATTENDED-UPGRADES
#-------------------------------------------------------------------
def installUnattendedUpgrades() -> bool:
    """
    Install and configure unattended-upgrades for automatic security updates.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        printHead("Installing unattended-upgrades")
        line()
        logger.info("Installing unattended-upgrades")

        # Install unattended-upgrades
        run("apt update")
        run("apt install -y unattended-upgrades apt-listchanges")
        printDot("unattended-upgrades installed")
        logger.info("unattended-upgrades installed successfully")

        # Configure unattended-upgrades
        config_content = """
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "1";

Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}";
    "${distro_id}:${distro_codename}-security";
    "${distro_id}ESMApps:${distro_codename}-apps-security";
    "${distro_id}ESM:${distro_codename}-infra-security";
};

Unattended-Upgrade::Package-Blacklist {
};

Unattended-Upgrade::AutoFixInterruptedDpkg "true";
Unattended-Upgrade::MinimalSteps "true";
Unattended-Upgrade::InstallOnShutdown "false";
Unattended-Upgrade::Mail "root";
Unattended-Upgrade::MailOnlyOnError "true";
Unattended-Upgrade::Remove-Unused-Kernel-Packages "true";
Unattended-Upgrade::Remove-New-Unused-Dependencies "true";
Unattended-Upgrade::Automatic-Reboot "false";
Unattended-Upgrade::Automatic-Reboot-WithUsers "false";
"""

        config_path = Path("/etc/apt/apt.conf.d/50unattended-upgrades")
        config_path.write_text(config_content.strip())
        config_path.chmod(0o644)
        printDot("unattended-upgrades configured")
        logger.info("unattended-upgrades configuration applied")

        # Enable unattended-upgrades
        run("systemctl enable unattended-upgrades")
        run("systemctl start unattended-upgrades")
        printDot("unattended-upgrades service enabled")
        logger.info("unattended-upgrades service configured")

        line()
        printSuccess("unattended-upgrades installation and configuration complete!")
        printInfo("System will automatically install security updates")
        return True
    except Exception as e:
        logger.error(f"Error installing unattended-upgrades: {e}")
        printError(f"Error installing unattended-upgrades: {e}")
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
    rule("[bold cyan]Create New Sudo User")
    line()
    if promptNewUser():
        if not createSudoUser():
            printWarning("User creation encountered issues")
    else:
        printInfo("Skipping user creation")

    line()
    rule("[bold cyan]Install and Configure GNUPG2")
    line()
    if installGnupg2():
        importGpgKey()
    else:
        printWarning("GNUPG2 installation failed")

    line()
    rule("[bold cyan]Install and Configure Git")
    line()
    if installGit():
        configureGit()
    else:
        printWarning("Git installation failed")

    line()
    rule("[bold cyan]Install and Configure SSH Server")
    line()
    if installSshd():
        configureSshd()
    else:
        printWarning("SSH installation failed")

    line()
    rule("[bold cyan]Install and Configure Docker")
    line()
    if installDocker():
        printSuccess("Docker installed and secured")
    else:
        printWarning("Docker installation failed")

    line()
    rule("[bold cyan]Install Lazydocker")
    line()
    if installLazydocker():
        printSuccess("Lazydocker installed")
    else:
        printWarning("Lazydocker installation failed")

    line()
    rule("[bold cyan]Install and Configure AIDE")
    line()
    if installAide():
        printSuccess("AIDE installed and configured")
    else:
        printWarning("AIDE installation failed")

    line()
    rule("[bold cyan]Install and Configure AppArmor")
    line()
    if installAppArmor():
        printSuccess("AppArmor installed and configured")
    else:
        printWarning("AppArmor installation failed")

    line()
    rule("[bold cyan]Install and Configure auditd")
    line()
    if installAuditd():
        printSuccess("auditd installed and configured")
    else:
        printWarning("auditd installation failed")

    line()
    rule("[bold cyan]Install and Configure unattended-upgrades")
    line()
    if installUnattendedUpgrades():
        printSuccess("unattended-upgrades installed and configured")
    else:
        printWarning("unattended-upgrades installation failed")

    line()
    rule("[bold green]Installation Complete!")
    line()
    printSuccess("System setup complete!")
    if NEW_USER:
        printInfo(f"New user '{NEW_USER}' has been created and configured")
    logger.info("Installation completed successfully")

#-------------------------------------------------------------------
# INSTALL AND CONFIGURE OTHER COMPONENTS (TODO)
#-------------------------------------------------------------------


