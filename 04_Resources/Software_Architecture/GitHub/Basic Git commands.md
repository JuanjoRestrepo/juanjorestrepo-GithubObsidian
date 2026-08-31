---
title: "Basic Git commands"
date: 2026-08-27
tags:
  - self-study
  - development-architecture
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

# Basic Git commands

Git works by remembering the changes to your files as if it's taking snapshots of your file system.

We'll cover a few basic commands to start tracking files in your repo. Then, you'll save your first "snapshot" for Git to compare against.

### git status
---
The first and most commonly used Git command is `git status`. You've already used it once, in the preceding exercise, to see that you had initialized your Git repo properly.

`git status` displays the state of the working tree (and of the staging area—we'll talk more about the staging area soon). It lets you see which changes are currently being tracked by Git, so you can decide whether you want to ask Git to take another snapshot.

### git add
---
`git add` is the command you use to tell Git to start keeping track of changes in certain files.

The technical term is _staging_ these changes. You'll use `git add` to stage changes to prepare for a commit. All changes in files that have been added but not yet committed are stored in the _staging area_.

### git commit
---
After you've staged some changes for commit, you can save your work to a snapshot by invoking the `git commit` command.

_Commit_ is both a verb and a noun. It has essentially the same meaning as when you commit to a plan or commit a change to a database. As a verb, committing changes means you put a copy (of the file, directory, or other "stuff") in the repository as a new version. As a noun, a commit is the small chunk of data that gives the changes you committed a unique identity. The data that's saved in a commit includes the author's name and e-mail address, the date, comments about what you did (and why), an optional digital signature, and the unique identifier of the preceding commit.

### git log
---
The `git log` command allows you to see information about previous commits. Each commit has a message attached to it (a commit message), and the `git log` command prints information about the most recent commits, like their time stamp, the author, and a commit message. This command helps you keep track of what you've been doing and what changes have been saved.

### git help
---
You've already tried out the `git help` command, but it's worth reminding you about. Use this command to easily get information about all the commands you've learned so far, and more.

Remember, each command comes with its _own_ help page, too. You can find these help pages by typing `git <command> --help`. For example, `git commit --help` brings up a page that tells you more about the `git commit` command and how to use it.

### git diff
---
The default is for `git diff` to compare the working tree to the index. In other words, it shows you all the changes that haven't been staged (added to Git's index) yet. To compare the working tree to the last commit, you can use `git diff HEAD`.

### --amend flag
---
When you refresh the page in your browser, you notice that your CSS style sheet isn't applied. After you investigate, you realize that you entered the path values incorrectly.

So, you update _index.html_ with the correct path to the style sheet. At this point, you could just commit the corrected version of _index.html_, but instead, you prefer to put it in the same commit as the original. The `--amend` option to `git commit` lets you change history (and how often does one get the chance to change history?).
```Bash
git commit --amend --no-edit
```

## Recover a deleted file: git checkout
---
Imagine that you made a change to a source code file that broke the entire project, so you want to revert to the previous version of that file. Or perhaps you accidentally deleted a file altogether. Git makes it easy to retrieve an earlier version, even if the current version no longer exists. Your best friend in this situation is the [git checkout](https://git-scm.com/docs/git-checkout) command.

`git checkout` has multiple uses, but in the next exercise, we'll use it to recover a deleted file. `git checkout` updates files in the working tree to match the version in the index or in the specified tree.

If you've accidentally deleted a file, you can recover it by bringing the version from the index back into the working tree by using this command:
```bash
git checkout -- <file_name>
```

## Recover files: git reset
---
You also can delete a file by using `git rm`. This command deletes the file on your disk, but it also has Git record the file deletion in the index.
So, if you ran this command:
```Bash
git rm index.html
git checkout -- index.html
```
Git would _not_ happily restore _index.html_! Instead, you'd get an error like this example:
```Bash
error: pathspec 'index.html' did not match any file(s) known to git.
```


To recover _index.html_, we would have to use a different technique: `git reset`. You can use `git reset` to unstage changes.

You could recover _index.html_ by using these two commands:
```Bash
git reset HEAD index.html
git checkout -- index.html
```
Here, `git reset` unstages the file deletion from Git. This command brings the file back to the index, but the file is still deleted on disk. You can then restore it to the disk from the index by using `git checkout`.

## Revert a commit: git revert
---
The last important command to know for fixing mistakes with Git is `git revert`. `git checkout` works only in situations where the changes to undo are in the index. After you've committed changes, you need to use a different strategy to undo them. In this case, we can use `git revert` to revert our previous commit. It works by making _another_ commit that cancels out the first commit.

We can use `git revert HEAD` to make a commit that's the exact _opposite_ of our last commit, undoing the previous commit while leaving all history intact. The `HEAD` part of the command just tells Git that we want to "undo" only the last commit.

As an aside, you can also remove the most recent commit by using the `git reset` command:
```Bash
git reset --hard HEAD^
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Development & Architecture|Desarrollo y arquitectura]].
- Criterio de producción: Conecta el concepto con contratos explícitos, validación de entrada, pruebas automatizadas, observabilidad y despliegues reversibles.
