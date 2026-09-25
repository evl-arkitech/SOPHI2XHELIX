"""DoubleHelix Neural Agent Engine Entrypoint.

Delegates execution to the Typer CLI in doublehelix.cli.main.
"""

import sys
from doublehelix.cli.main import app

if __name__ == "__main__":
    app()
