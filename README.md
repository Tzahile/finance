# Finance

This Repo is open for contributions, there's
much work to be done here and any help is highly
appreciated - feel free to reach out and talk :smiley:

This project aims to become a rich (no pan intended) financial dashboard -

- automatically(/manually) integrating with your financial accounts and reports
- providing the user with detailed infographics and alerts
- featuring planners, calculators, simulators
- while allowing complete anonymity

###### We currently focus our efforts in creating an end-to-end integration with ordernet spark investing platform

#### Prerequisite

1. python 3.8
2. Dependencies: `cd server && pip install -r requirements.txt`
3. # Or, if you want to contribute - dev-Dependencies: `cd server && pip install -r requirements/dev.txt`

#### Run

_Currently, docker engine is required_

```bash
find ./deployment -type f -iname "*.sh" -exec chmod +x {} \;
chmod +x ./run.sh

./run.sh
```

#### Code Quality

Our code base is being strictly checked with the following tools:

- flake8
- mypy
- bandit
- pylint
- black
- pytest

##### Running static-analysis locally

```bash
./static-analysis [--stop-on-failure|mypy|flake8|black|bandit|pylint]
```

- Run all of the tools to get a summary -

```bash
(venv) mp@x:~/code/finance$ ./static_analysis.sh
mypy......FAIL
flake8....PASS
pylint....PASS
black.....PASS
bandit....PASS
```

- Run all of the tools until the first failure is encounted, and print its output -

```bash
(venv) mp@x:~/code/finance$ ./static_analysis.sh --stop-on-failure
mypy......FAIL
--------------
finance/data/parser.py:8: error: Function is missing a return type annotation
```

- Or specify a single tool to run directly and view its elaborated output -

```bash
./static-analysis mypy
(venv) mp@x:~/code/finance$ ./static_analysis.sh mypy
finance/data/parser.py:8: error: Function is missing a return type annotation
Found 1 error in 1 file (checked 9 source files)
```

##### Code Formating

We've adopted Black as our main python formatter.
We recommend you bundle it inside your IDE, or alternatively run it from the command line.

To reformat the code and run it with the same configuration as we do with our CI, use -

```bash
./format.sh
```
