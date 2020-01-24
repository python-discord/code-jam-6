import sys
from .core.main import AncientTechApp

if __name__ == "__main__":
    try:
        sys.exit(AncientTechApp().run())
    
    finally:
        # An attempt to supress empty
        # thread exceptions

        try:
            sys.stdout.close()
        except:
            pass

        try:
            sys.stderr.close()
        except:
            pass
