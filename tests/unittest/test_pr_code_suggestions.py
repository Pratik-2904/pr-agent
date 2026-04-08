from types import SimpleNamespace

from pr_agent.algo.types import EDIT_TYPE, FilePatchInfo
from pr_agent.tools.pr_code_suggestions import PRCodeSuggestions


class TestPRCodeSuggestions:
    def test_validate_replacement_line_range_valid(self):
        git_provider = SimpleNamespace(
            diff_files=[
                FilePatchInfo(
                    base_file="a\nb\nc\n",
                    head_file="a\nb\nc\nd\n",
                    patch="",
                    filename="src/app.py",
                    edit_type=EDIT_TYPE.MODIFIED,
                )
            ]
        )
        git_provider.get_diff_files = lambda: git_provider.diff_files

        tool = PRCodeSuggestions.__new__(PRCodeSuggestions)
        tool.git_provider = git_provider
        tool.diff_files = None

        assert tool.validate_replacement_line_range("src/app.py", 2, 4) is True

    def test_validate_replacement_line_range_invalid_range(self):
        git_provider = SimpleNamespace(diff_files=[])
        git_provider.get_diff_files = lambda: git_provider.diff_files

        tool = PRCodeSuggestions.__new__(PRCodeSuggestions)
        tool.git_provider = git_provider
        tool.diff_files = None

        assert tool.validate_replacement_line_range("src/app.py", 4, 3) is False

    def test_validate_replacement_line_range_out_of_bounds(self):
        git_provider = SimpleNamespace(
            diff_files=[
                FilePatchInfo(
                    base_file="a\n",
                    head_file="a\nb\n",
                    patch="",
                    filename="src/app.py",
                    edit_type=EDIT_TYPE.MODIFIED,
                )
            ]
        )
        git_provider.get_diff_files = lambda: git_provider.diff_files

        tool = PRCodeSuggestions.__new__(PRCodeSuggestions)
        tool.git_provider = git_provider
        tool.diff_files = None

        assert tool.validate_replacement_line_range("src/app.py", 1, 5) is False
