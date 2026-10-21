"""Expose CPU wheels' upstream versions to the registry advisory scanner.

PyPI does not index official +cpu wheel labels. Check the upstream release;
retain full installed versions in the environment audit as well. This does not
assess CPU-specific build-chain risks.
"""

from importlib.metadata import version

from packaging.version import Version

for package in ("torch", "torchvision"):
    installed = Version(version(package))
    if installed.local not in (None, "cpu"):
        raise ValueError(f"Unreviewed wheel variant: {package} {installed}")
    print(f"{package}=={installed.public}")
