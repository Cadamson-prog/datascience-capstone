# Cloning the Repository

### Prerequisite: Install Git (CLI only)

> This prerequisite only applies if using a CLI method.
GitHub Desktop and VS Code bundle their own Git. 

Skip this section if `git --version` already works in your terminal.

- **Windows:** download from [git-scm.com/download/win](https://git-scm.com/download/win) and run the installer.
- **macOS:** `brew install git`, or just run `git --version` once and accept the Xcode Command Line Tools prompt.
- **Linux:** `sudo apt install git` (Debian/Ubuntu) or `sudo dnf install git` (Fedora).

---

## Quick Reference

| Method | Command / Action |
|--------|-----------------|
| GitHub CLI | `gh repo clone bkoconnell/datascience-capstone` |
| Git (HTTPS) | `git clone https://github.com/bkoconnell/datascience-capstone.git` |
| GitHub Desktop | File > Clone Repository > GitHub.com tab |
| VS Code | Command Palette > Git: Clone |

---

## Option 1: GitHub CLI

The GitHub CLI (`gh`) is the fastest option if you already have it installed. If not, download it from [cli.github.com](https://cli.github.com) and run `gh auth login` once to authenticate.

```bash
gh repo clone bkoconnell/datascience-capstone
```

This clones the repo into a new folder called `datascience-capstone` in your current directory.

To clone into a specific folder:

```bash
gh repo clone bkoconnell/datascience-capstone my-folder-name
```

---

## Option 2: Git (Command Line)

If you have Git installed but not the GitHub CLI, use the standard `git clone` command in a local terminal. This will clone the repo into a new folder in your current directory.

```bash
git clone https://github.com/bkoconnell/datascience-capstone.git
```

Then navigate into the project folder:

```bash
cd datascience-capstone
```

---

## Option 3: GitHub Desktop

1. Open GitHub Desktop
2. Go to **File > Clone Repository**
3. Click the **GitHub.com** tab
4. Search for `datascience-capstone` or select it from the list if you're already a collaborator
5. Choose a local path where you want the folder to be created
6. Click **Clone**

Once cloned, the repo will appear in your GitHub Desktop sidebar and you can start working with branches right away.

---

## Option 4: VS Code

VS Code has built-in Git support that lets you clone directly from the editor.

1. Open VS Code (no folder needs to be open)
2. Open the Command Palette: `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
3. Type **Git: Clone** and select it
4. Paste the repository URL:
   ```
   https://github.com/bkoconnell/datascience-capstone.git
   ```
5. Choose a folder on your machine to clone into
6. When prompted, click **Open** to open the cloned repo in VS Code

> **Tip:** If you have the [GitHub Pull Requests](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github) extension installed, you can also clone from the Source Control panel directly by signing into GitHub.
