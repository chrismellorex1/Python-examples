# Using Git version control for code projects

## Creating a new code repo from a local working copy

### with the [Github for Mac app](http://mac.github.com/)

1. From the repositories view in the app, drag the project folder to the bottom of the left sidebar.
2. Hit "Yes" when it asks if you want to create a local git repository
3. Go to "Changes" view (⌘2)
4. Select the files that you want to commit their current state to the repository. You can view the changes of the file by clicking on the double up arrow on the file name bar.
5. Type a commit summary, usually a description of what you've just added or changed.
6. Click 'Commit'. This commits the current state of the code to your local repository. Do this every time to do something significant like fix a bug or develop a feature. Commit early and often. Each  state of code is available to you at any time via the History view (⌘1).

### with the command line

1. Open Terminal.app
2. "cd" to directory
>     cd path/to/directory

3. Initiate a git repository
>     git init .

4. Add existing files
>     git add .

5. Commit all files (-a) and add a message (-m)
>     git commit -a -m "commit message goes here"

## Cloning (checking out) someone else's repository

### with the [Github for Mac app](http://mac.github.com/)

* Visit the repo on Github.com and click the "clone to Mac" button, or...
* Select the repo in the Repositories list within the app, under the cremalab account.

### with the command line

1. "cd" to desired directory
2. clone the repo with the clone url
>     git clone git@github.com:albatrocity/gratuitator.git

## Syncing repository branches with a remote repository

### with the [Github for Mac app](http://mac.github.com/)

1. Make sure you have committed the current state of your code
2. Drill into your repo in the app and click Sync Branch in the upper right corner. **This pulls down the latest code from the remote repository, merges your code with it, and pushes your changes to the remote repository.**

If you only want to get the latest code from the remote repo, select Repository > Pull (⇧⌘P) from the menu bar. This merges the remote code with your local code but does not push up your changes. 

If you only want to push up your current state to the remote reop, select Repository > Push (⌘P). This will only work if you already have the most up to date code from the repo.

### with the command line

1. Make sure you have committed your current state.
2. Get the most up to date code from the remote repo
>     git pull origin master

3. Push your local code to the remote repo
>     git push origin master
