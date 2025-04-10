import torch


def save_checkpoint(model, path, epoch=None):
    torch.save({"model_state_dict": model.state_dict(), "epoch": epoch}, path)


def load_checkpoint(model, path, map_location=None):
    checkpoint = torch.load(path, map_location=map_location, weights_only=True)
    model.load_state_dict(checkpoint["model_state_dict"])
    return checkpoint.get("epoch", None)
