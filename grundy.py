import runpy
import os
import shutil


def clean_pycache(start_dir='.'):
    for root, dirs, files in os.walk(start_dir, topdown=False):
        if '__pycache__' in dirs:
            pycache_dir = os.path.join(root, '__pycache__')
            print(f"Removing {pycache_dir}")
            shutil.rmtree(pycache_dir)


if __name__ == "__main__":
    runpy.run_module('grundy', run_name='__main__')
    clean_pycache()