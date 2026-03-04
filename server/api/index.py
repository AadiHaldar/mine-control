import sys
import os

# Add the server directory to Python path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)

from main import app
