import os
import shutil
import tempfile

import pytest
import torch

from mlutils.checkpoint import load_checkpoint, save_checkpoint
from mlutils.logging import Documenter
from mlutils.metrics import AverageMeter
from mlutils.repro import set_seed


class DummyModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(2, 2)


def test_set_seed_consistency():
    set_seed(123)
    a = torch.randn(2)
    set_seed(123)
    b = torch.randn(2)
    assert torch.allclose(a, b), "Seed did not make torch output deterministic"


def test_average_meter():
    meter = AverageMeter()
    meter.update(1.0, n=2)
    meter.update(2.0, n=2)
    assert meter.avg == pytest.approx(1.5)


def test_documenter_creates_folder_and_file():
    temp_root = tempfile.mkdtemp()
    doc = Documenter("testrun", read_only=False)
    path = doc.add_file("dummy.txt")
    with open(path, "w") as f:
        f.write("hello")
    assert os.path.exists(path)
    doc.close()
    shutil.rmtree(doc.basedir)
    shutil.rmtree(temp_root)


def test_checkpoint_save_and_load():
    model = DummyModel()
    for param in model.parameters():
        param.data.fill_(1.23)

    tmp_path = tempfile.NamedTemporaryFile(delete=False).name
    save_checkpoint(model, tmp_path, epoch=5)

    # reset model
    for param in model.parameters():
        param.data.zero_()

    epoch = load_checkpoint(model, tmp_path)
    for param in model.parameters():
        assert torch.allclose(param.data, torch.full_like(param.data, 1.23))
    assert epoch == 5

    os.remove(tmp_path)
