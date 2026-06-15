import pytest
import sys
import os

# Add ansible directory to sys.path since it doesn't have an __init__.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ansible')))

# Use importlib to import the module since the path has plugins which isn't a standard package
import importlib.util
spec = importlib.util.spec_from_file_location("safe_flatten", os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ansible/filter_plugins/safe_flatten.py')))
safe_flatten_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(safe_flatten_module)

safe_flatten = safe_flatten_module.safe_flatten
FilterModule = safe_flatten_module.FilterModule

def test_safe_flatten_none():
    assert safe_flatten(None) == []

def test_safe_flatten_dict():
    data = {"a": 1, "b": 2}
    assert safe_flatten(data) == [1, 2]

def test_safe_flatten_list():
    data = [1, [2, 3], [4, [5]]]
    assert safe_flatten(data) == [1, 2, 3, 4, 5]

def test_safe_flatten_strings_omitted():
    data = [1, "test", [2, "string"]]
    assert safe_flatten(data) == [1, 2]

def test_safe_flatten_strings_included():
    data = [1, "test", [2, "string"]]
    assert safe_flatten(data, include_strings=True) == [1, "test", 2, "string"]

def test_safe_flatten_string_alone():
    assert safe_flatten("test") == ["test"]
    assert safe_flatten("test", include_strings=True) == ["test"]

def test_safe_flatten_tuple():
    data = (1, (2, 3))
    assert safe_flatten(data) == [1, 2, 3]

def test_filter_module():
    fm = FilterModule()
    filters = fm.filters()
    assert 'safe_flatten' in filters
    assert filters['safe_flatten'] == safe_flatten
