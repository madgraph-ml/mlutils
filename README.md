# mlutils

`mlutils` is a lightweight utility toolkit to make your research and ML projects cleaner and more reproducible.

### Features
- `Documenter`: Automatically logs output and stores files in versioned run folders
- `Tee`: Duplicates `stdout`/`stderr` into a log file
- `timing`: Context manager for timing code blocks
- `gitinfo`: Fetch git commit hash and dirty state
- `metadata`: Collect system-level metadata (Python version, CUDA info, etc.)
- `metrics`: Simple running average tracker
- `checkpoint`: Save/load model checkpoints with optional epoch tracking
- `repro`: Utility for reproducible testing via global seed setting

### Installation
```bash
pip install -e .
```

### Example Usage
```python
from mlutils import logging, timing, gitinfo, metadata, metrics, checkpoint, repro

doc = logging.Documenter("my_experiment")
print("Git commit:", gitinfo.get_git_commit_hash())
print(metadata.collect_metadata())

repro.set_seed(123)

loss_meter = metrics.AverageMeter()
loss_meter.update(0.8, n=32)
print("Avg loss:", loss_meter.avg)

with timing.timing("Training loop"):
    train_model()

checkpoint.save_checkpoint(model, doc.add_file("model.pt"))
```

### Testing
```bash
pytest tests/
```