# Litigious Liberators

Please use this README to document your team's project. Make sure to include a general description, information on how to set-up and run your project, and anything else you think may be interesting for a README. The README is usually the first document people read when they visit a project on GitHub, so it's a good idea to make it appealing.

## Contents

- [Dev](#dev)
  * [Project Management](#project-management)
  * [Code organisation](#code-organisation)
  * [Setting up your repo](#setting-up-your-repo)
- [Useful links](#useful-links)
- [License](#license)

## Dev

### Project Management

- **Trello Board**: [https://trello.com/b/OUo1YWft](https://trello.com/b/OUo1YWft)

### Code organisation

- Dev dependencies go in `dev-requirements.txt`
- Normal dependencies go in `requirements.txt`

### Setting up your repo

Clone this repo:

```bash
$ git clone git@github.com:duarteocarmo/code-jam-6.git
```

Create a virtualenv:

```bash
$ python -m venv <name_of_virtualenv>
```

Activate it:

```bash
$ . <name_of_virtualenv>/env/activate
```

Install dependencies

```bash
(env) $ cd litigious-liberators # navigate to our folder
(env) $ pip install -r requirements.txt # install normal requirements
(env) $ pip install -r requirements-dev.txt # install dev as well
```

Set up pre-commit hooks

```bash
(env) $ pre-commit --version # make sure this outputs something
(env) $ pre-commit install 
```

Now it should run before your commit :) 

## Running the App:
```bash
python main.py -m screen:phone_iphone_6_plus,portrait,scale=0.40
```

## Useful links


- **Code Jam Rules:** [https://pythondiscord.com/pages/code-jams/code-jam-6/rules/](https://pythondiscord.com/pages/code-jams/code-jam-6/rules/)

- **General Code Jam info:** [https://pythondiscord.com/pages/code-jams/code-jam-6/](https://pythondiscord.com/pages/code-jams/code-jam-6/)

- **Kivy:** [https://kivy.org/#home](https://kivy.org/#home)

## License

All projects will merged into our Code Jam repository, which uses the [MIT license](../LICENSE). Please make sure that if you add assets, the licenses of those assets are compatible with the MIT license.


There we go :) 
