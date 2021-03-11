import pycodestyle
from pathlib import Path


class TestCodestyle:
    def test_codestyle(self):
        project_root = Path(__file__).parent.parent
        style = pycodestyle.StyleGuide(ignore=["E501", "W503"])
        result = style.check_files([str(project_root)])
        assert result.total_errors == 0
