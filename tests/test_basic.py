import pytest
from codeanalyzer.utils import scan_files, read_file
from codeanalyzer.analyzer import CodeAnalyzer
from codeanalyzer.cli import analyze_command


@pytest.fixture
def mock_repo(tmp_path):
    repo_dir = tmp_path / "fake_repo"
    repo_dir.mkdir()
    (repo_dir / "valid.py").write_text("print('test')")
    (repo_dir / "large_file.py").write_text("x" * 1000001)
    (repo_dir / "ignore.xyz").write_text("binary data")
    return repo_dir


def test_scan_files(mock_repo):
    files = scan_files(mock_repo)
    assert str(mock_repo / "valid.py") in files
    assert str(mock_repo / "large_file.py") not in files
    assert str(mock_repo / "ignore.xyz") not in files


def test_read_file(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    assert read_file(test_file) == "test content"


def test_analyzer_with_findings(mocker):
    mocker.patch('codeanalyzer.deepseek.DeepSeekClient.analyze_code',
                 return_value="SQL injection risk found")

    analyzer = CodeAnalyzer()
    analyzer.analyze_file("dummy_path")

    assert len(analyzer.findings) == 1
    assert "SQL injection" in analyzer.findings[0]['result']


def test_analyzer_no_issues(mocker):
    mocker.patch('codeanalyzer.deepseek.DeepSeekClient.analyze_code',
                 return_value="No issues found")

    analyzer = CodeAnalyzer()
    analyzer.analyze_file("dummy_path")

    assert len(analyzer.findings) == 0


def test_cli_analyze_command(mocker, capsys):
    mocker.patch('codeanalyzer.utils.download_repo', return_value="/fake/path")
    mocker.patch('codeanalyzer.utils.scan_files', return_value=[])
    mocker.patch('codeanalyzer.analyzer.CodeAnalyzer.generate_report',
                 return_value={"summary": "Test summary", "detailed_findings": []})

    class Args:
        github_url = "https://github.com/fake/repo"

    analyze_command(Args())

    captured = capsys.readouterr()
    assert "Test summary" in captured.out


def test_config_loading():
    from codeanalyzer.config import Config
    assert hasattr(Config, 'DEEPSEEK_API_URL')
    assert Config.MAX_FILE_SIZE == 1000000