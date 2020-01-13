[![Code Jam Banner](https://raw.githubusercontent.com/python-discord/code-jam-6/master/ancient%20tech.png?token=AAQAKVPQ55SEFWYYLYO5YV26ETLTC)](#)

[![Discord](https://img.shields.io/static/v1?label=Python%20Discord&logo=discord&message=%3E30k%20members&color=%237289DA&logoColor=white)](https://discord.gg/2B963hn)
[![License](https://img.shields.io/github/license/python-discord/bot)](LICENSE)
[![Website](https://img.shields.io/badge/website-visit-brightgreen)](https://pythondiscord.com)

Welcome to the sixth Python Discord Code Jam!

By popular choice, the theme for this code jam is **Ancient Technology**. What you do with this theme or how you interpret it is up to you, but it will be your task to come up with something fun using this theme. As the technology for this code jam, we've chosen for [Kivy](https://kivy.org/), a cross-platform framework for making user interfaces. We know that a lot of you are probably relatively new to this framework and that's why some of Kivy's [core developers](https://kivy.org/#aboutus) will be hanging out in the `#winter-code-jam` channel to help you!

## Getting Started

1. Have your team leader [fork](https://github.com/python-discord/code-jam-6/fork) the repository. If your leader is unavailable, it's okay if someone else does it.

2. Open a pull request from your fork's `master` to the `master` branch of this repository. This pull requests will eventually count as your team's submission, but make sure to **open the PR when the code jam starts**. You can use the name of your team as the name of the pull request.

3. Make sure to **only make changes within your team's subdirectory**. The repository should already contain a directory with your team's name as the name.

4. Since you are making a pull request from the `master` of your fork, it would probably be best to use different branches in your repository to work on your project. You can then periodically merge those development branches into the `master` branch.

    For an ideal developer workflow, you should probably be opening pull requests inside of your fork, targeting your own `master` branch. If this doesn't make any sense to you because you're not that well-versed in git, you will probably be okay with all of you just pushing code directly to your master branch, but keep in mind that this may lead to conflicts if you are all working in parallel.

5. The Pull Request will be automatically updated whenever you push code to master on your fork, so all you have to do is keep pushing code to it and make sure you are finished before the code jam ends!

## Important considerations

- Please read [the rules](https://pythondiscord.com/pages/code-jams/code-jam-6/rules/) before starting to work on your project.

- **Write documentation** for your project. Your team folder should already contain a `README.md` file that you should use to document your project. At the very least, make sure to include information on how to set up and run your project so the judges won't have trouble running it. Failure to provide this information may lead to being docked points, or in extreme cases, disqualification.

- We expect you to submit code that has a style that is in accordance with [PEP8](https://www.python.org/dev/peps/pep-0008/). More specifically, pull requests to this repository will be **automatically linted with a tool called [flake8](http://flake8.pycqa.org/en/stable/)** (see below for more information). Your team folder contains a flake8 configuration file, `.flake8`, that allows you to run flake8 with the same settings as we will use. The most notable setting is that we allow for a maximum line length of 100 characters.

    - If you wish to use an autoformatter like `black`, that is absolutely fine. Do note that most autoformatters do not guarantee that your code will pass `flake8` and it's up to you to double check that.

- You may use any third party package that's available on [PyPI](https://pypi.org/), but you should provide a strictly pinned `requirements.txt`, a Pipfile, or some other form of dependency management list so that we can easily install these dependencies.

- You should **make no changes outside of your team's folder**. This means that all of the files you want to include, including your code and assets, should be contained that directory and not in the root level of the repository. This ensures that we can merge your pull request into the repository once the Code Jam is over. This ensures that you will get GitHub contribution credit towards our organization and, most importantly, it will showcase your project on GitHub.

## Code Style and Readability

Code style and readability will be important factors in judging your team's project. We expect you to follow the style recommendations made in [PEP8](https://www.python.org/dev/peps/pep-0008/) and, to check for compliance with PEP8, we will use a linting tool called [flake8](http://flake8.pycqa.org/en/stable/). In case PEP8 and flake8 disagree, the output of the linter will be leading.

We will be using flake8 without additional plugins and with most of default settings enabled. Two notable exceptions are that we will use a maximum line length of 100 characters and ignore error E226. To allow you to run flake8 with the same settings as we will use, we have added a `.flake8` configuration file to your team folder.

Obviously, adhering to PEP8 is not the only factor that determines if your code is readable, so make sure to look [beyond PEP8](https://www.youtube.com/watch?v=wf-BqAjZb8M) as well.

#### Automatic Linting of Pull Requests

To help us check your code for compliance with PEP8, we have set up an automated build pipeline that will lint all pull requests made to this repository. Each time a pull requests is opened or when changes are made to the source branch (`master` on your team's fork) of a PR, the build pipeline will automatically lint the pull request. When the build process has completed, the build status will automatically be reported in the pull request:

![Failing build status](https://raw.githubusercontent.com/python-discord/code-jam-6/master/failing_build.png?token=AH7WUVAZRU56A6RY2KPVUOS6EWJUU)

Please note that **you should not use this pipeline as a remote linter**. Ideally, all changes made to the `master` branch of your team's repository have already been linted locally before they were pushed to the remote repository.

## Useful Information for Participants

Our website contains some pages that may help you get started:

- [How to use git](https://pythondiscord.com/pages/code-jams/using-git/)

- [Making a fork, opening a pull request, & creating a GitHub webhook](https://pythondiscord.com/pages/code-jams/pull-request/)

- [How does judging work?](https://pythondiscord.com/pages/code-jams/judging/)

## Partners and Sponsors

[![kivy_143x80](https://user-images.githubusercontent.com/33516116/72271607-173d4980-361f-11ea-8597-4140d98321f5.png)](https://kivy.org/#home) [![jetbrains_143x80](https://user-images.githubusercontent.com/33516116/72271609-173d4980-361f-11ea-8453-c996d33a649b.png)](https://www.jetbrains.com/) [![do_210x80](https://user-images.githubusercontent.com/33516116/72271610-173d4980-361f-11ea-9f3a-0e8de2b8abd1.png)](https://www.digitalocean.com/) [![linode_202x80](https://user-images.githubusercontent.com/33516116/72271608-173d4980-361f-11ea-82bf-e857efca09df.png)](https://www.linode.com/)
