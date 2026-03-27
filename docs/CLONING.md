# Cloning the Repository

This document walks through how to clone this repository to your local machine. Pick the method you're most comfortable with.

**Repository URL:** `https://github.com/bkoconnell/datascience-capstone.git`

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

If you have Git installed but not the GitHub CLI, use the standard `git clone` command.

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

---

## After Cloning

Once the repository is on your local machine, check out [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on how to create branches and submit pull requests.
