# mlutils

`mlutils` is a lightweight utility toolkit to make your research and ML projects cleaner and more reproducible.

### Features
- `Documenter`: Automatically logs output and stores files in versioned run folders
- `Tee`: Duplicates `stdout`/`stderr` into a log file
- `timing`: Context manager for timing code blocks
- `gitinfo`: Fetch git commit hash and dirty state

### Installation
```bash
# clone the repository
git clone https://github.com/madgraph-ml/mlutils.git
# then install
pip install .
```

### Example Usage
```python
from mlutils.logging import Documenter
from mlutils.timing import timing
from mlutils.gitinfo import get_git_commit_hash

doc = Documenter("my_experiment")
print("Git commit:", get_git_commit_hash())

with timing("Training loop"):
    train_model()
```

---
