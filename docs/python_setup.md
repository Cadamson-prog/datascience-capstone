# Python Setup

This document walks through installing Python on your local machine. This project requires **Python 3.9 or higher** (as defined in [pyproject.toml](../pyproject.toml)).

## Check if Python is already installed

Open a terminal and run:

```bash
python --version
```

or

```bash
python3 --version
```

If you see `Python 3.9.x` or higher, you're set. Otherwise, install Python using one of the options below.

---

## Windows

1. Go to the official Python downloads page: [python.org/downloads/windows](https://www.python.org/downloads/windows/)
2. Download the latest stable installer for Python 3.9 or higher (64-bit recommended)
3. Run the installer
4. **IMPORTANT:** On the first installer screen, check the box for **"Add python.exe to PATH"** before clicking *Install Now*
5. Verify the install by opening a new PowerShell or Command Prompt window and running:
   ```powershell
   python --version
   ```

---

## macOS

The easiest way is via [Homebrew](https://brew.sh):

```bash
brew install python
```

Verify the install:

```bash
python3 --version
```

Alternatively, download the macOS installer directly from [python.org/downloads/macos](https://www.python.org/downloads/macos/).

---

## Linux

Most Linux distributions ship with Python pre-installed. If you need a newer version, use your distribution's package manager.

**Debian / Ubuntu:**
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

**Fedora / RHEL:**
```bash
sudo dnf install python3 python3-pip
```

Verify the install:

```bash
python3 --version
```

---

## Next Steps

Once Python is installed, continue with [DEVELOPER_SETUP.md](DEVELOPER_SETUP.md) to set up the project's virtual environment and dependencies.
