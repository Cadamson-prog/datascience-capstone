# Contributing Guidelines

Below are guidelines for users to follow when contributing to our GitHub project.

> This document assumes the repository has already been cloned to your local machine. If you haven't done that yet, see [CLONING.md](CLONING.md) for instructions.

## Branching and Pull Request Workflow

This project uses a simple branch-and-PR workflow. All changes go through a pull request before merging into `main`. This keeps `main` stable and gives the team a chance to review each other's work.

### Overview

1. Pull the latest `main`
2. Create a new branch
3. Make changes, commit, and push
4. Open a pull request (PR)
5. Keep committing and pushing to your branch as needed (the PR updates automatically)
6. Before merging, update your branch with the latest `main`
7. Merge your PR
8. Start your next task on a new branch or continue on your current one (after syncing with `main`)

---

## Quick Reference

| Step | GitHub Desktop | CLI |
|------|----------------|-----|
| Pull latest main | Switch to main, Fetch origin, Pull origin | `git checkout main && git pull origin main` |
| Create branch | Branch dropdown > New Branch | `git checkout -b branch-name` |
| Commit changes | Write summary, click Commit | `git add . && git commit -m "message"` |
| Push to remote | Click Push origin | `git push origin branch-name` |
| Open PR | Click Create Pull Request | `gh pr create --base main` |
| Update branch from main | Branch > Update from Default Branch | `git fetch origin && git merge origin/main` |
| Merge PR | On github.com, click Merge pull request | `gh pr merge --merge` |

---

### Step-by-Step

#### 1. Start from the latest main

Before creating a branch, make sure you have the most recent version of `main`.

**GitHub Desktop:**
- Make sure "main" is selected as your current branch (top of the window)
- Click "Fetch origin" then "Pull origin"

**CLI:**
```bash
git checkout main
git pull origin main
```

#### 2. Create a new branch

Keep branch names simple, like using your first name in lowercase (e.g., `kristin`, `brendan`, `carlos`). If you want to be more specific you can add a short description (e.g., ``kristin_nnmodel`, `brendan_eda`, `carlos_xgboost`).

**GitHub Desktop:**
- Click the current branch dropdown at the top
- Click "New Branch"
- Type your branch name and make sure it's based on `main`
- Click "Create Branch"

**CLI:**
```bash
git checkout -b your-branch-name
```

#### 3. Make changes, commit, and push

Work on your files as normal. When you're ready to save a checkpoint, commit your changes and push them to GitHub.

**GitHub Desktop:**
- Your changed files will show up in the left panel
- Write a short summary of what you did in the "Summary" box at the bottom left
- Click "Commit to [your-branch-name]"
- Click "Push origin" (or "Publish branch" if this is your first push on a new branch)

**CLI:**
```bash
git add .
git commit -m "short description of what you changed"
git push origin your-branch-name
```

#### 4. Open a pull request

Once you've pushed at least one commit, open a PR on GitHub so the team can see your work.

**GitHub Desktop:**
- After pushing, click the blue "Create Pull Request" button (or go to Branch > Create Pull Request)
- This opens GitHub in your browser
- Set the base branch to `main` and the compare branch to your branch
- Add a title and a brief description of what you're working on
- Click "Create pull request"

**CLI / Browser:**
- Go to the repository on github.com
- You should see a banner saying your branch had recent pushes with a "Compare & pull request" button -- click it
- Set base to `main`, add a title and description, and click "Create pull request"

Or use the GitHub CLI:
```bash
gh pr create --base main --title "Your PR title" --body "Brief description"
```

#### 5. Keep working (optional)

You don't have to merge right away. You can keep making changes, committing, and pushing to your branch. The PR updates automatically with each push, and other team members can review your code in progress.

Just repeat Step 3 as many times as you need.

#### 6. Update your branch with the latest main

Before merging your PR, pull in any changes that others have merged into `main` since you started your branch. This avoids merge conflicts and makes sure your code works with the latest version of everything.

See [Updating Your Branch with Latest Main](#updating-your-branch-with-latest-main) below for detailed instructions.

#### 7. Merge your PR

Once your branch is up to date with `main` and you're happy with your changes, merge the PR.

**Browser:**
- Go to your PR on github.com
- Click the green "Merge pull request" button
- Click "Confirm merge"

**CLI:**
```bash
gh pr merge --merge
```

#### 8. Start your next task

After merging, you have two options:

**Option A: Create a new branch** (recommended for a new task)

Follow Steps 1 and 2 again -- pull the latest `main` and create a new branch.

**Option B: Keep working on your current branch** (if continuing the same work)

Update your branch with the latest `main` first (see below), then keep going.

---

## Updating Your Branch with Latest Main

This is something you should do regularly, especially before merging a PR. It pulls in any changes that teammates have merged into `main` so your branch stays current.

### GitHub Desktop

1. Make sure your working branch is selected (not `main`)
2. Click "Fetch origin" in the top bar to download the latest remote changes
3. Go to Branch > Update from Default Branch (or Branch > Merge into Current Branch and select `origin/main`)
4. If there are conflicts, GitHub Desktop will walk you through resolving them
5. After the merge, click "Push origin" to push the updated branch to GitHub

### CLI

```bash
# Make sure you're on your working branch
git checkout your-branch-name

# Fetch the latest changes from the remote
git fetch origin

# Merge the latest main into your branch
git merge origin/main
```

If there are merge conflicts, git will tell you which files need attention. Open those files, resolve the conflicts (look for the `<<<<<<<`, `=======`, `>>>>>>>` markers), then:

```bash
git add .
git commit -m "resolved merge conflicts with main"
git push origin your-branch-name
```