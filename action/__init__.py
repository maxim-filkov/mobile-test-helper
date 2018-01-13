"""
This module imports all other modules into framework.
"""

import os
from importlib import import_module

for python_file in os.listdir(__path__[0]):
    if python_file.endswith(".py") and python_file not in ("__init__.py", "ActionFactory.py", "ActionRegistry.py"):
        class_name = os.path.splitext(os.path.basename(python_file))[0]
        import_module(__name__ + "." + class_name)
