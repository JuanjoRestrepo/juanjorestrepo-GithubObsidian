---
title: "Branching and Merging"
date: 2026-08-27
tags:
  - self-study
  - development-architecture
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

## Branch structure and naming
---
A _branch_ is simply a chain of commits that branch off from the main line of development, like a branch on a tree.

If you're switching to Git from another VCS, you might be accustomed to slightly different terminology. The VCS Subversion names its default branch `trunk`, while Git names it `master`. You can rename the default branch, just as you can rename any other branch. In this module, we name the default branch `main`.

A branch usually starts with a commit on the default branch; in this case, on `main`. The branch grows a separate history chain as commits are added. Eventually, the changes in the branch are merged back into `main`. In this module, you'll learn to make commits in a branch, and merge them into the `main` branch.

Suppose you branch off the `main` branch. Here's how to visualize what happens:

![A diagram that shows the relationship of the main branch and local branches.](https://learn.microsoft.com/en-gb/training/modules/branch-merge-git/media/branch-tree.png)

## Create and switch branches (git branch and git checkout)
---
A common reason to create a new branch is to make changes to an existing feature. A branch for this purpose would commonly be called a _topic branch_ or _feature branch_.

You can create a new branch by using the `git branch` command. Switch between branches by using the `git checkout` command.

## Merge branches (git merge)
---
When you've finalized some work in a branch, perhaps a feature or a bug fix, you'll want to _merge_ that branch back into the main branch. You can use the `git merge` command to merge a specific branch into your current branch.

```Bash
# Switch back to the main branch
git checkout main

# Merge my-feature branch into main
git merge my-feature
```

After using these commands and resolving any _merge conflicts_ (we'll describe merge conflicts later in this module), **all the changes from your `my-feature` branch would be in `main`.**

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Development & Architecture|Desarrollo y arquitectura]].
- Criterio de producción: Conecta el concepto con contratos explícitos, validación de entrada, pruebas automatizadas, observabilidad y despliegues reversibles.
