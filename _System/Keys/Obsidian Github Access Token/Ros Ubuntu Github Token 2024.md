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


    For a Linux-based OS ⤴

    For Linux, you need to configure the local GIT client with a username and email address,

    $ git config --global user.name "your_github_username"
    $ git config --global user.email "your_github_email"
    $ git config -l

    Once GIT is configured, we can begin using it to access GitHub. Example:

    $ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
    > Cloning into `YOUR-REPOSITORY`...
    Username: <type your username>
    Password: <type your password or personal access token (GitHub)

    Now cache the given record in your computer to remembers the token:

    $ git config --global credential.helper cache

    If needed, anytime you can delete the cache record by:

    $ git config --global --unset credential.helper
    $ git config --system --unset credential.helper

    Now try to pull with -v to verify

    $ git pull -v

