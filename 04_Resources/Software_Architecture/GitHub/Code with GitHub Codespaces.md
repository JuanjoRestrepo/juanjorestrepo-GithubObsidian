---
title: "Code with GitHub Codespaces"
date: 2026-08-27
tags:
  - self-study
  - development-architecture
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

# The Codespace lifecycle


GitHub Codespaces is configurable, allowing you to create a customized development environment for your project. By configuring a custom development environment for your project, you can have a repeatable Codespace configuration for all users of your project.

A Codespace's lifecycle begins when you create a Codespace and ends when you delete it. You can disconnect and reconnect to an active Codespace without affecting its running processes. You can stop and restart a Codespace without losing the changes that you make to your project.

![Diagram of a circular lifecycle of a Codespace that starts with creating and ends with deleting.](https://learn.microsoft.com/en-gb/training/github/code-with-github-codespaces/media/codespace-circular-lifecycle.png)

## Create a Codespace
---
You can create a Codespace on GitHub.com, in Visual Studio Code, or by GitHub CLI. There are four ways to create a Codespace:

- From a GitHub template or any template repository on GitHub.com to start a new project.
- From a branch in your repository for new feature work.
- From an open pull request to explore work-in-progress.
- From a commit in a repository's history to investigate a bug at a specific point in time.

You can temporarily use a Codespace in order to test code or you can return to the same Codespace to work on long-running feature work.

You can create more than one Codespace per repository or even per branch. However, there are limits to the number of Codespaces you can create and run at the same time. If you reach the maximum number of Codespaces and try to create another, a message displays that an existing Codespace needs to be removed/deleted before a new Codespace can be created.

You can create a new Codespace each time you develop in GitHub Codespaces or keep a long-running Codespace for a feature. If starting a new project, create a Codespace from a template and publish it to a repository on GitHub later.

When creating a new Codespace each time you work on a project, you should regularly push your changes to ensure that any new commits are on GitHub. When using a long-running Codespace for a new project, pull from the repository's default branch each time you start working in Codespace. This enables the environment to get the latest commits. The workflow is similar to working with a project on a local machine.

Repository administrators can enable GitHub Codespaces prebuilds for a repository to speed up Codespace creation.

For an in-depth walkthrough and step-by-step guidance, see the resources titled **A beginner’s guide to learning to code with GitHub Codespaces** and **Developing in a Codespace** located in the Summary unit at the end of this module.

### Codespace creation process
---
![Diagram of a github codespace and how it connects from your code editor and into a docker container.](https://learn.microsoft.com/en-gb/training/github/code-with-github-codespaces/media/codespace-connection-editor.png)

When creating a GitHub Codespace, four processes occur:

1. VM and storage are assigned to your Codespace.
2. A container is created.
3. A connection to the Codespace is made.
4. A post-creation setup is made.

### Save changes in a Codespace

When you connect to a Codespace through the web, AutoSave is automatically enabled to save changes after a specific amount of time has passed. When you connect to a Codespace through Visual Studio Code running on your desktop, you must enable AutoSave.

Your work saves to a virtual machine in the cloud. You can close and stop a Codespace and return to the saved work at a later time. If you have unsaved changes, you receive a prompt to save them before exiting. However, if your Codespace is deleted, then your work is lost. To save your work, you must commit your changes and push them to your remote repository or publish your work to a new one if you created your Codespace from a template.

### Open an existing Codespace

You can reopen any of your active or stopped Codespaces on GitHub.com, in a JetBrains IDE, in Visual Studio Code, or by using GitHub CLI.

To resume an existing Codespace you can either go to the repository where the Codespace exists and press "," key on your keyboard and **select Resume this codespace** or open [https://github.com/codespaces](https://github.com/codespaces) in the browser, select the repository, and then select the existing Codespace.

### Timeouts for a Codespace

If a Codespace is inactive, or if you exit your Codespace without explicitly stopping, the application times out after a period of inactivity and stops running. The default timeout is after 30 minutes of inactivity. You can't customize the duration of the timeout period for new Codespaces. When a Codespace times out, your data is kept from the last time your changes were saved.

### Internet connection while using GitHub Codespaces

A Codespace requires an internet connection. If the connection to the internet is lost while working in a Codespace, you won't be able to access your Codespace. However, any uncommitted changes are saved. When you reestablish the internet connection, you can access the Codespace in the same state that it was left in when the connection was lost.

If you have an unstable internet connection, you should frequently commit and push your changes.

## Close or stop a Codespace

If you exit the Codespace without running the stop command (for example, by closing the browser tab) or leave the Codespace running without interaction, the Codespace and its running processes continue during the inactivity timeout period. The default inactivity timeout period is 30 minutes. You can define your personal timeout setting for Codespaces you create, but this may be overruled by an organization's timeout policy.

Only running Codespaces incur CPU charges. A stopped Codespace incurs only storage costs.

You can stop and restart a Codespace to apply changes. For example, if you change the machine type used for your Codespace, you need to stop and restart it for the change to take effect. When you close or stop your Codespace, all uncommitted changes are preserved until you connect to the Codespace again.

You can also stop Codespace and choose to restart or delete it if you encounter an error or something unexpected.

## Rebuild a Codespace

You can rebuild your Codespace to implement changes to your dev container configuration. For most uses, you can create a new Codespace as an alternative to rebuilding a Codespace. When you rebuild your Codespace, images from the cache speed-up the rebuild process. You can also perform a full rebuild to clear the cache and rebuild the container with fresh images.

When you rebuild the container in a Codespace, changes you made outside the /workspaces directory are cleared. Changes you made inside the /workspaces directory, including the clone of the repository or template you created the Codespace from, are preserved over a rebuild.

## Delete a Codespace

You can create a Codespace for a particular task. After you push your changes to a remote branch, then you can safely delete that Codespace.

If you try to delete a Codespace with unpushed git commits, the editor notifies you that you have changes that haven't been pushed to a remote branch. You can push any desired changes and then delete your Codespace. You can also continue to delete your Codespace and any uncommitted changes or export the code to a new branch without creating a new Codespace.

Stopped Codespaces that remain inactive for a specified amount of time are deleted automatically. Inactive Codespaces delete after 30 days, but you can customize your Codespace retention intervals.


# Personalize your Codespace

GitHub Codespaces is a dedicated environment for you. You can configure your repositories with a dev container to define their default GitHub Codespaces environment and personalize your development experience across all of your Codespaces with dotfiles and Settings Sync.

## What you can customize
---
There are many ways you can customize your Codespace. Let's review each one.

- **Settings Sync:** You can synchronize your Visual Studio Code (VS Code) settings between the desktop application and the VS Code web client.
- **Dotfiles:** You can use a dotfiles repository to specify scripts, shell preferences, and other configurations.
- **Rename a Codespace:** When you create a Codespace, it's assigned an autogenerated display name. If you have multiple Codespaces, the display name helps you to differentiate between Codespaces. You can change the display name for your Codespace.
- **Change your shell:** You can change your shell in a Codespace to keep the setup you're used to. When you're working in a Codespace, you can open a new terminal window with a shell of your choice, change your default shell for new terminal windows, or install a new shell. You can also use dotfiles to configure your shell.
- **Change the machine type:** You can change the type of machine that's running your Codespace, so that you're using resources appropriate for the work you're doing.
- **Set the default editor:** You can set your default editor for Codespaces in your personal settings page. Set your editor preference so that when you create a Codespace or open an existing Codespace, it opens to your default editor.
    - Visual Studio Code (desktop application)
    - Visual Studio Code (web client application)
    - JetBrains Gateway - for opening Codespaces in a JetBrains IDE
    - JupyterLab - the web interface for Project Jupyter
- **Set the default region:** You can set your default region in the GitHub Codespaces profile settings page to personalize where your data is held.
- **Set the timeout:** A Codespace will stop running after a period of inactivity. By default this period is 30 minutes, but you can specify a longer or shorter default timeout period in your personal settings on GitHub. The updated setting applies to any new Codespaces you create, or to existing Codespaces the next time you start them.
- **Configure automatic deletion:** Inactive Codespaces are automatically deleted. You can choose how long your stopped Codespaces are retained, up to a maximum of 30 days.

Additional information and step-by-step instructions regarding customization are located in the Summary unit at the end of this module.

## Add to your Codespace with extensions or plugins
---
You can add plugins and extensions within a Codespace to personalize your experience in JetBrains and VS Code.

### VS Code extensions
---
If you work on your Codespaces in the VS Code desktop application or the web client, you can add any extensions you need from the Visual Studio Code Marketplace. Refer to [Supporting Remote Development and GitHub Codespaces](https://code.visualstudio.com/api/advanced-topics/remote-extensions) in the VS Code documentation for information on how extensions run in GitHub Codespaces.

If you already use VS Code, you can use Settings Sync to automatically sync extensions, settings, themes, and keyboard shortcuts between your local instance and any Codespaces you create.

### JetBrains plugins
---
If you work on your Codespaces in a JetBrains IDE, you can add plugins from the JetBrains Marketplace.


# Codespaces versus GitHub.dev editor

You're probably asking yourself, when should I use GitHub Codespaces and when should I use GitHub.dev?

You can use GitHub.dev to navigate files and sources code repositories from GitHub, and make and commit code changes. You can open any repository, fork, or pull request in GitHub.dev editor.

If you want to do more heavy lifting like testing your code, use GitHub Codespaces. It has compute associated with it so you can build your code, run your code, and have terminal access. GitHub.dev doesn't have compute in it. With GitHub Codespaces, you get the power of a personal Virtual Machine (VM) with terminal access, the same way you could use your local environment, just in the cloud.

### Comparison of Codespaces and GitHub.dev
----
The following table lists the main differences between Codespaces and GitHub.dev:

| |GitHub.dev|GitHub Codespaces|
|---|---|---|
|Cost|Free|Free monthly quota of usage for personal accounts|
|Availability|Available to everyone on GitHub.com|Available to everyone on GitHub.com|
|Startup|GitHub.dev opens instantly with a key-press and you can start using it right away without having to wait for configuration or installation|When you create or resume a Codespace, the Codespace is assigned a VM, and the container is configured based on the contents of a devcontainer.json file. This setup takes a few minutes to create the development environment.|
|Compute|There's no associated compute, so you can't build and run your code or use the integrated terminal.|With GitHub Codespaces, you get the power of a dedicated VM to run and debug your application.|
|Terminal access|None|GitHub Codespaces provides a common set of tools by default, meaning that you can use the Terminal exactly as you would in your local environment.|
|Extensions|Only a subset of extensions that can run on the web appear in the extensions view and can be installed|With GitHub Codespaces, you can use most extensions from the Visual Studio Code Marketplace.|

### Continue working on Codespaces
---
You can start your workflow in GitHub.dev and continue working on a Codespace. If you try to access the Run and Debug View or the Terminal, you're notified that they're not available in GitHub.dev.

To continue your work in a Codespace, select **Continue Working on…**. Select **Create New Codespace** to create a Codespace on your current branch. Before you choose this option, you must commit any changes.

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Development & Architecture|Desarrollo y arquitectura]].
- Criterio de producción: Conecta el concepto con contratos explícitos, validación de entrada, pruebas automatizadas, observabilidad y despliegues reversibles.
