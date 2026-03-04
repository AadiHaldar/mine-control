import importlib.util
import os

# Absolute path to main.py
main_path = os.path.join(os.path.dirname(__file__), "..", "main.py")

spec = importlib.util.spec_from_file_location("main", main_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

app = module.app
