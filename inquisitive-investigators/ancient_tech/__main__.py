import sys
from pathlib import Path
from .core.main import AncientTechApp

if __name__ == "__main__":
    AncientTechApp().run()
    
    with open(Path('ancient_tech') / 'errors.log', 'w') as f:
        sys.stderr = sys.stdout = f
