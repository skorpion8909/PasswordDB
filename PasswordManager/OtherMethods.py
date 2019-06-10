import os
import sys

def install(whatToInstall):
    try:
        os.system(f"python pip install {whatToInstall}")
    except Exception:
        try:
            os.system(f"py pip install {whatToInstall}")
        except Exception:
            try:
                os.system(f"python pip3 install {whatToInstall}")
            except Exception:
                try:
                    os.system(f"python3 pip install {whatToInstall}")
                except Exception:
                    print(f"Installation of {whatToInstall} failed")
                    sys.exit(0)