# Git Interview Questions & Answers

## 🚀 **Git Fundamentals**

### 1. What is Git and how does it differ from other version control systems?

**Answer:**
Git is a distributed version control system (DVCS) designed for speed, efficiency, and support for non-linear workflows.

**Key Differences:**

| Feature | Git | SVN | CVS |
|---------|-----|-----|-----|
| **Architecture** | Distributed | Centralized | Centralized |
| **Speed** | Very fast | Moderate | Slow |
| **Branching** | Cheap and easy | Expensive | Limited |
| **Offline Work** | Full support | Limited | Limited |
| **Merge** | Excellent | Good | Basic |

**Advantages:**
- **Distributed**: Every clone is a full backup
- **Fast**: Operations are local
- **Branching**: Cheap and efficient
- **Non-linear**: Supports complex workflows
- **Open source**: Free and widely adopted

---

### 2. What is the difference between Git and GitHub?

**Answer:**
- **Git**: Version control system (software)
- **GitHub**: Web-based hosting service for Git repositories

**Git** is the tool, **GitHub** is a service that hosts Git repositories and provides collaboration features (pull requests, issues, etc.).

**Alternatives to GitHub:**
- GitLab
- Bitbucket
- Azure DevOps
- Self-hosted Git servers

---

### 3. Explain the Git workflow and three-tree architecture.

**Answer:**
Git uses a three-tree architecture:

1. **Working Directory**: Your current files
2. **Staging Area (Index)**: Files prepared for commit
3. **Repository (HEAD)**: Committed snapshots

**Basic Workflow:**
```bash
# 1. Modify files (Working Directory)
echo "Hello" > file.txt

# 2. Stage changes (Staging Area)
git add file.txt

# 3. Commit (Repository)
git commit -m "Add file.txt"
```

**Visual Representation:**
```
Working Directory → git add → Staging Area → git commit → Repository
     (modified)                    (staged)              (committed)
```

---

### 4. What are the basic Git commands?

**Answer:**
**Initialization:**
```bash
git init                    # Initialize repository
git clone <url>            # Clone repository
```

**Status and Information:**
```bash
git status                  # Show working tree status
git log                     # Show commit history
git log --oneline          # Compact log
git show <commit>          # Show commit details
git diff                    # Show changes
git diff --staged          # Show staged changes
```

**Staging and Committing:**
```bash
git add <file>             # Stage file
git add .                  # Stage all changes
git commit -m "message"      # Commit changes
git commit -a -m "message" # Stage and commit
```

**Branching:**
```bash
git branch                 # List branches
git branch <name>         # Create branch
git checkout <branch>     # Switch branch
git checkout -b <branch>  # Create and switch
git merge <branch>        # Merge branch
```

**Remote Operations:**
```bash
git remote -v             # List remotes
git fetch                 # Fetch from remote
git pull                  # Fetch and merge
git push                  # Push to remote
```

---

### 5. What is the difference between git pull and git fetch?

**Answer:**
- **git fetch**: Downloads changes from remote but doesn't merge
- **git pull**: Downloads changes AND merges into current branch

**git fetch:**
```bash
git fetch origin          # Fetch all branches
git fetch origin main    # Fetch specific branch
# Changes are in origin/main, not merged yet
git merge origin/main    # Merge manually
```

**git pull:**
```bash
git pull origin main     # Fetch and merge in one step
# Equivalent to:
# git fetch origin main
# git merge origin/main
```

**Best Practice:**
- Use `git fetch` to review changes before merging
- Use `git pull` when you're ready to merge immediately

---

### 6. Explain Git branching and merging strategies.

**Answer:**
**Branching:**
```bash
# Create branch
git branch feature-branch

# Switch branch
git checkout feature-branch
# or
git switch feature-branch

# Create and switch
git checkout -b feature-branch
# or
git switch -c feature-branch
```

**Merging:**
```bash
# Merge branch into current
git checkout main
git merge feature-branch

# Fast-forward merge (linear history)
git merge --ff-only feature-branch

# No fast-forward (creates merge commit)
git merge --no-ff feature-branch
```

**Branching Strategies:**
1. **Git Flow**: main, develop, feature, release, hotfix branches
2. **GitHub Flow**: main branch + feature branches
3. **Trunk-based**: Single main branch, short-lived feature branches

---

### 7. What is the difference between git merge and git rebase?

**Answer:**
**git merge:**
- Creates a merge commit
- Preserves branch history
- Non-destructive

```bash
git checkout main
git merge feature-branch
# Creates merge commit combining both branches
```

**git rebase:**
- Replays commits on top of another branch
- Linear history
- Rewrites commit history

```bash
git checkout feature-branch
git rebase main
# Replays feature-branch commits on top of main
```

**When to Use:**
- **Merge**: When you want to preserve branch history
- **Rebase**: When you want linear history (before merging)

**Interactive Rebase:**
```bash
git rebase -i HEAD~3  # Rebase last 3 commits
# Options: pick, reword, edit, squash, drop
```

---

### 8. How do you resolve merge conflicts?

**Answer:**
**When Conflicts Occur:**
```bash
git merge feature-branch
# Auto-merging file.txt
# CONFLICT (content): Merge conflict in file.txt
```

**Resolving:**
```bash
# 1. Check status
git status

# 2. Open conflicted file
# File contains conflict markers:
<<<<<<< HEAD
Current branch content
=======
Incoming branch content
>>>>>>> feature-branch

# 3. Edit file to resolve conflict
# Remove markers and keep desired content

# 4. Stage resolved file
git add file.txt

# 5. Complete merge
git commit
```

**Abort Merge:**
```bash
git merge --abort
```

**Tools:**
- `git mergetool`: Opens merge tool
- VS Code, vimdiff, meld, etc.

---

### 9. What is .gitignore and how do you use it?

**Answer:**
`.gitignore` specifies files Git should ignore.

**Example .gitignore:**
```
# Compiled files
*.class
*.o
*.so

# Dependencies
node_modules/
vendor/

# IDE files
.vscode/
.idea/
*.swp

# OS files
.DS_Store
Thumbs.db

# Environment files
.env
.env.local

# Logs
*.log
logs/
```

**Patterns:**
```
# Ignore all .txt files
*.txt

# Ignore in specific directory
logs/*.log

# Ignore directory
node_modules/

# Don't ignore (negation)
!important.txt

# Ignore in root only
/README.md
```

**Remove Tracked Files:**
```bash
# Remove from Git but keep locally
git rm --cached file.txt
```

---

### 10. What are Git hooks and how do you use them?

**Answer:**
Git hooks are scripts that run automatically at certain points.

**Common Hooks:**
- **pre-commit**: Before commit
- **commit-msg**: Before commit message is accepted
- **post-commit**: After commit
- **pre-push**: Before push

**Example pre-commit hook:**
```bash
#!/bin/sh
# .git/hooks/pre-commit

# Run tests
npm test
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi

# Run linter
npm run lint
if [ $? -ne 0 ]; then
    echo "Linting failed. Commit aborted."
    exit 1
fi
```

**Make executable:**
```bash
chmod +x .git/hooks/pre-commit
```

**Using Husky (Node.js):**
```json
{
  "husky": {
    "hooks": {
      "pre-commit": "npm test",
      "pre-push": "npm run lint"
    }
  }
}
```

---

### 11. How do you undo changes in Git?

**Answer:**
**Working Directory (Unstaged):**
```bash
# Discard changes to file
git checkout -- file.txt
# or
git restore file.txt

# Discard all changes
git checkout -- .
# or
git restore .
```

**Staging Area (Staged):**
```bash
# Unstage file
git reset HEAD file.txt
# or
git restore --staged file.txt

# Unstage all
git reset HEAD
```

**Committed Changes:**
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Revert commit (creates new commit)
git revert HEAD
```

**Amend Commit:**
```bash
# Modify last commit
git commit --amend -m "New message"

# Add changes to last commit
git add file.txt
git commit --amend --no-edit
```

---

### 12. What is Git stash and how do you use it?

**Answer:**
Stash temporarily saves uncommitted changes.

**Basic Usage:**
```bash
# Stash changes
git stash
# or with message
git stash save "WIP: working on feature"

# List stashes
git stash list

# Apply stash (keeps stash)
git stash apply
git stash apply stash@{0}

# Pop stash (removes stash)
git stash pop

# Drop stash
git stash drop stash@{0}

# Clear all stashes
git stash clear
```

**Stash Options:**
```bash
# Include untracked files
git stash -u

# Include ignored files
git stash -a

# Create branch from stash
git stash branch feature-branch
```

---

### 13. How do you work with remote repositories?

**Answer:**
**Viewing Remotes:**
```bash
git remote -v
```

**Adding Remotes:**
```bash
git remote add origin https://github.com/user/repo.git
git remote add upstream https://github.com/original/repo.git
```

**Fetching:**
```bash
git fetch origin
git fetch origin main
```

**Pushing:**
```bash
# Push to remote
git push origin main

# Push new branch
git push -u origin feature-branch

# Push all branches
git push --all origin

# Force push (dangerous)
git push --force origin main
```

**Removing Remotes:**
```bash
git remote remove origin
```

---

### 14. What are Git tags and how do you use them?

**Answer:**
Tags mark specific points in history (releases).

**Creating Tags:**
```bash
# Lightweight tag
git tag v1.0.0

# Annotated tag (recommended)
git tag -a v1.0.0 -m "Release version 1.0.0"

# Tag specific commit
git tag -a v1.0.0 <commit-hash>
```

**Listing Tags:**
```bash
git tag
git tag -l "v1.*"
```

**Pushing Tags:**
```bash
git push origin v1.0.0
git push --tags  # Push all tags
```

**Checking Out Tags:**
```bash
git checkout v1.0.0
# Creates detached HEAD state
```

**Deleting Tags:**
```bash
git tag -d v1.0.0
git push origin --delete v1.0.0
```

---

### 15. How do you use Git submodules?

**Answer:**
Submodules allow including one repository in another.

**Adding Submodule:**
```bash
git submodule add https://github.com/user/repo.git path/to/submodule
```

**Cloning with Submodules:**
```bash
git clone --recursive https://github.com/user/repo.git
# or
git clone https://github.com/user/repo.git
git submodule init
git submodule update
```

**Updating Submodules:**
```bash
git submodule update --remote
```

**Removing Submodule:**
```bash
git submodule deinit path/to/submodule
git rm path/to/submodule
```

---

## 📝 **Best Practices**

1. **Commit often**: Small, logical commits
2. **Write good messages**: Clear, descriptive commit messages
3. **Use branches**: Keep main branch stable
4. **Review before merge**: Use pull requests
5. **Don't force push to main**: Protect main branch
6. **Use .gitignore**: Don't commit unnecessary files
7. **Tag releases**: Mark important versions
8. **Backup**: Regular backups of repositories
9. **Documentation**: Keep README updated
10. **Security**: Don't commit secrets

---

**Good luck with your Git interview preparation!**
