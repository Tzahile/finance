# Finance

#### Prerequisite
1. python3.8
2. `pip install -r requirements.txt`

#### Run
```bash
find ./deployment -type f -iname "*.sh" -exec chmod +x {} \; 
chmod +x ./run.sh

./run.sh
```

#### Code Quality
Our code base is being strictly checked with the following tools:
- flake8
- mypy (--ignore-missing-imports)
- bandit 
- pylint
- black (line-length=120 --target-version=py38)
- pytest

To run these checks locally, you can use the provided tool:
```bash
./static-analysis
```