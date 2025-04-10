import platform
import socket

import torch


def collect_metadata():
    return {
        "hostname": socket.gethostname(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "cuda_available": torch.cuda.is_available(),
        "num_gpus": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        "cuda_device": (
            torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
        ),
    }
