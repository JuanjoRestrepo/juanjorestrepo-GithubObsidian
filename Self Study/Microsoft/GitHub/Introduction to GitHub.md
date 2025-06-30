# Components of the GitHub flow

In this unit, we're reviewing the following components of the GitHub flow:

- Branches
- Commits
- Pull Requests
- The GitHub Flow

## What are branches
---
In the last section, we created a new file in the last section, along the way to you also created a new branch in your repositories.

Branches are an essential part to the GitHub experience because they're where we can make changes without affecting the entire project we're working on.

Your branch is a safe place to experiment with new features or fixes. If you make a mistake, you can revert your changes or push more changes to fix the mistake. Your changes won't update on the default branch until you merge your branch.

#### Note
Alternatively, you can create a new branch and check it out by simply using git in a terminal the command would be `git checkout -b newBranchName`

## What are commits
---
As you might have noticed in the previous unit, adding in a new file into the repository, you needed to push a commit.

Let’s briefly review what commits are.

A **commit** is a change to one or more files on a branch. Every time a commit is created, it's assigned a unique ID and tracked, along with the time and contributor. Commits provide a clear audit trail for anyone reviewing the history of a file or linked item, such as an issue or pull request.

![A screenshot of a list of GitHub commits to a main branch.](https://learn.microsoft.com/en-gb/training/github/introduction-to-github/media/2-commits.png)

Within a git repository, a file can exist in several valid states as it goes through the version control process:

The primary states for a file in a Git repository are:

Untracked: An initial state of a file when it isn't yet part of the Git repository. Git is unaware of its existence.

Tracked: A tracked file is one that Git is actively monitoring. It can be in one of the following substates:

- Unmodified: The file is tracked, but it hasn't been modified since the last commit.
- Modified: The file has been changed since the last commit, but these changes aren't yet staged for the next commit.
- Staged: The file has been modified, and the changes have been added to the staging area (also known as the index). These changes are ready to be committed.
- Committed: The file is in the repository's database. It represents the latest committed version of the file.

These states and substates are important to collaborating with your team to know where each and every commit is in the process of your project.

Now let’s move on to pull requests.

## What are pull requests?
---
Now that we know what a commit is, let’s review a pull request.

A **pull request** is the mechanism used to signal that the commits from one branch are ready to be merged into another branch.

The team member submitting the **pull request** requests one or more reviewers to verify the code and approve the merge. These reviewers have the opportunity to comment on changes, add their own, or use the pull request itself for further discussion.

Once the changes have been approved (if approval is required), the pull request's source branch (the compare branch) is merged into the base branch.

![A screenshot of a pull request and a comment within the pull request.](https://learn.microsoft.com/en-gb/training/github/introduction-to-github/media/2-pull-request.png)

Now that we know of all the ingredients, let’s review the GitHub flow.

## The GitHub flow
---
![Screenshot showing a visual representation of the GitHub Flow in a linear format that includes a new branch, commits, pull request, and merging the changes back to main in that order.](https://learn.microsoft.com/en-gb/training/github/introduction-to-github/media/2-branching.png)

The GitHub flow can be defined as a lightweight workflow that allows for safe experimentation. You can test new ideas and collaboration with your team by using branching, pull requests, and merging.

Now that we know the basics of GitHub we can walk through the GitHub flow and its components.

1. The first step of the GitHub flow is creating a branch so that the changes, features, and fixes you create don't affect the main branch.
2. The second step is to make your changes. We recommend deploying changes to your feature branch before merging into the main branch. Doing so ensures the changes are valid in a production environment.
3. The third step is to create a pull request to ask collaborators for feedback. Pull request review is so valuable that some repositories require an approving review before pull requests can be merged.
4. Next is the fourth step of reviewing and implementing your feedback from your collaborators.
5. The fifth step, once you’re feeling great about your changes now it's time to get your pull request approved and merge it into the main branch.
6. The sixth and final step is to delete your branch. Deleting your branch signals your work on the branch is completed and prevents you or others from accidentally using old branches.

## Issues
---
GitHub Issues were created to track ideas, feedback, tasks, or bugs for work on GitHub.

Issues can be created in various ways, so you can choose the most convenient method for your workflow.

For the walk-through in the next portion, we'll go over how to create an issue from a repository but just know there are a myriad of ways. Here's a list of all the ways you can create issues from.

The different ways to create an issue from:

- a repository
- an item in a task list
- a note in a project
- a comment in an issue or pull request
- a specific line of code
- or a URL query

### Creating an issue from a repository
---
1. On GitHub.com, navigate to the main page of the repository.
2. Under your repository name, click (insert issues Icon) Issues.
    ![Screenshot showing the top portion of the main page of a repository with the Issues section highlighted.](https://learn.microsoft.com/en-gb/training/github/introduction-to-github/media/issues-tab.png)
    
3. Click New issue.
4. If your repository uses issue templates, next to the type of issue you'd like to open, click Get started.
    
    If the type of issue you'd like to open isn't included in the available options, click Open a blank issue.
    ![A screenshot of the issue templates menu, with the Open a blank issue option highlighted.](https://learn.microsoft.com/en-gb/training/github/introduction-to-github/media/open-a-blank-issue.png)
    
5. In the "Title" field, type a title for your issue.
6. In the comment body field, type a description of your issue.
7. If you're a project maintainer, you can assign the issue to someone, add it to a project board, associate it with a milestone, or apply a label.
8. When you're finished, click Submit new issue.
    
Some conversations are more suitable for GitHub Discussions.

You can use GitHub Discussions to ask and answer questions, share information, make announcements, and conduct or participate in conversations about a project.

In the next section, we’ll review Discussions and how to best utilize the feature.

## Discussions
---
Discussions are for conversations that need to be accessible to everyone and aren't related to code. Discussions enable fluid, open conversation in a public forum.

In this section we are be going over:

- Enabling a discussion in your repository
- Creating a new discussion and various discussion categories

Let’s dive into enabling a discussion in your repository.

### Enabling a discussion in your repository
---
Repository owners and people with Write access can enable GitHub Discussions for a community on their public and private repositories. The visibility of a discussion is inherited from the repository the discussion is created in.

When you first enable GitHub Discussions, you're invited to configure a welcome post.

1. On GitHub.com, navigate to the main page of the repository.
2. Under your repository name, click (gear icon) Settings.
    ![A screenshot of the top portion of the main page of a repository with the Settings section highlighted.](https://learn.microsoft.com/en-gb/training/github/introduction-to-github/media/settings-tab.png)
3. Scroll down to the "Features" section and click Setup discussions.
    ![A screenshot of the Discussions box with the green Setup discussion button highlighted.](https://learn.microsoft.com/en-gb/training/github/introduction-to-github/media/set-up-discussion.png)
    
4. Under "Start a new discussion," edit the template to align with the resources and tone you want to set for your community.
5. Click Start discussion.
    
### Create a new discussion
---
Any authenticated user who can view the repository can create a discussion in that repository.

Similarly, since organization discussions are based on a source repository, any authenticated user who can view the source repository can create a discussion in that organization.

1. On GitHub.com, navigate to the main page of the repository or organization where you want to start a discussion.
    
2. Under your repository or organization name, click Discussions.
    
    ![A screenshot of the top portion of the main page of a repository with the Discussions section highlighted.](https://learn.microsoft.com/en-gb/training/github/introduction-to-github/media/discussions-tab.png)
    
3. On the right side of the page, click New discussion.
    
4. Select a discussion category by clicking Get started. All discussions must be created in a category. For repository discussions, people with maintain or admin permissions to the repository define the categories for discussions in that repository.
    
    ![A screenshot of the select a discussion category menu selection, with the top option Announcements and the get started button highlighted.](https://learn.microsoft.com/en-gb/training/github/introduction-to-github/media/announcements.png)
    

Each category must have a unique name and emoji pairing, and be accompanied by a detailed description stating its purpose. Categories help maintainers organize how conversations are filed and are customizable to help distinguish categories that are Q&A or more open-ended conversations. The following table shows the default categories for discussions and their purpose.

|**Category**|**Purpose**|**Format**|
|---|---|---|
|📣 Announcements|Updates and news from project maintainers|Announcement|
| ️General |Anything and everything relevant to the project|Open-ended discussion|
|💡 Ideas|Ideas to change or improve the project|Open-ended discussion|
|🗳️ Polls|Polls with multiple options for the community to vote for and discuss|Polls|
|🙏 Q&A|Questions for the community to answer, with a question/answer format|Question and Answer|
|🙌 Show and tell|Creations, experiments, or tests relevant to the project|Open-ended discussion|

5. Under "Discussion title" type a title for your discussion, and under "Write" type the body of your discussion.
    
    ![A screenshot of starting a new discussion page with the Discussion title box and content box empty.](https://learn.microsoft.com/en-gb/training/github/introduction-to-github/media/start-a-new-discussion.png)
    
6. Click Start discussion.
    
