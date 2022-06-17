import sys
import os

if os.environ.get("REMOTE_TESTING"):
    import ptvsd

    ptvsd.enable_attach(address=("0.0.0.0", 5678))
    ptvsd.wait_for_attach()

collect_ignore_glob = [".venv/*"]
