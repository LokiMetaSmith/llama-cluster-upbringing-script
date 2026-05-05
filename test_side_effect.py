import sys
import os
sys.path.insert(0, os.path.abspath('tests/unit'))
import conftest
from unittest.mock import patch
import yaml as mock_yaml
import yaml as real_yaml # wait, conftest mocked it

print(mock_yaml)
