import sys
import os

# Add the server directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app
