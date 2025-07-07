import subprocess
from pathlib import Path
import sys

def test_pylint_log():
    """Run pylint on the backend package and store the log."""
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pylint'], check=True)
    result = subprocess.run(
        ['pylint', 'backend', '--exit-zero', '-sn'],
        capture_output=True,
        text=True,
        check=False,
    )
    Path('logs').mkdir(exist_ok=True)
    Path('logs/pylint.log').write_text(result.stdout)
    assert result.returncode == 0
