import pytest
from architect_reviewer import collect_project_files, read_files
from pathlib import Path


def test_collect_files(tmp_path):
    # Create dummy files
    (tmp_path / "a.py").write_text("print('hello')")
    (tmp_path / "b.txt").write_text("ignore me")
    (tmp_path / "__pycache__" / "c.py").mkdir(parents=True, exist_ok=True)

    files = collect_project_files(str(tmp_path))
    assert any("a.py" in f for f in files)
    assert all("__pycache__" not in f for f in files)


def test_read_files(tmp_path):
    test_file = tmp_path / "a.py"
    content = "print('hi')"
    test_file.write_text(content)
    result = read_files([str(test_file)])
    assert content in result
