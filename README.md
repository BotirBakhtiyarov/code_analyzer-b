# Code Analyzer
[![PyPI Version](https://img.shields.io/pypi/v/code-analyzer-b.svg)](https://pypi.org/project/code-analyzer-b/)
[![Python Versions](https://img.shields.io/pypi/pyversions/code-analyzer-b.svg)](https://pypi.org/project/code-analyzer-b/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![SARIF Support](https://img.shields.io/badge/SARIF-2.1.0-green.svg)](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning)
[![DeepSeek Integration](https://img.shields.io/badge/DeepSeek-API-7c3aed.svg)](https://deepseek.com)

**Code Analyzer** is an open-source command-line tool designed to help developers and security professionals analyze code repositories for vulnerabilities and bugs. By leveraging the power of AI through the DeepSeek API, it provides detailed insights and recommendations to improve code quality and security.

**Version**: 0.2.0

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [CI/CD Integration](#cicd-integration)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

### Prerequisites

- Python 3.6 or higher
- A DeepSeek API key (obtainable from [DeepSeek](https://www.deepseek.com/))

### Install from PyPI

To install version 0.2.0:

```bash
pip install code-analyzer==0.2.0
```

### Set Up API Key

After installation, run:

```bash
code_analyzer setup
```

Enter your DeepSeek API key when prompted. The key will be saved in `~/.code_analyzer/config.ini`.

---

## Usage

### Analyzing a GitHub Repository

To analyze a public GitHub repository:

```bash
code_analyzer analyze https://github.com/user/repo
```

For private repositories, use a GitHub access token:

```bash
code_analyzer analyze https://github.com/user/private-repo --git-token YOUR_TOKEN
```

### Analyzing a Local Directory

To analyze a local directory:

```bash
code_analyzer analyze /path/to/local/repo
```

Or, for the current directory:

```bash
code_analyzer analyze .
```

### Command-Line Options

- `-o, --output FILE`: Specify the output file for the report.
- `-f, --format FORMAT`: Choose the report format (`txt`, `md`, `html`, `json`, `sarif`).
- `--verbose`: Enable verbose output for debugging.
- `--no-details`: Omit detailed findings from the report.
- `--lang LANG`: Select the report language (`en`, `uz`, `zh`, `ru`).
- `--no-stream`: Suppress console output and save directly to the output file.

Example:

```bash
code_analyzer analyze . --output report.sarif --format sarif --no-stream --lang uz
```

---

## CI/CD Integration

Code Analyzer can be integrated into your CI/CD pipeline, such as GitHub Actions, to automate code analysis on every push or pull request.

### Example GitHub Actions Workflow

```yaml
name: Code Analysis

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  analyze:
    runs-on: ubuntu-latest

    permissions:
      security-events: write
      actions: read
      contents: read

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.x'

    - name: Install code-analyzer
      run: pip install code-analyzer==0.2.0

    - name: Set up DeepSeek API key
      env:
        DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
      run: |
        mkdir -p ~/.code_analyzer
        echo "[DEEPSEEK]" > ~/.code_analyzer/config.ini
        echo "API_KEY = $DEEPSEEK_API_KEY" >> ~/.code_analyzer/config.ini

    - name: Run code analysis
      run: |
        code_analyzer analyze . --output report.sarif --format sarif --no-stream --lang uz

    - name: Upload SARIF file
      uses: github/codeql-action/upload-sarif@v3
      with:
        sarif_file: report.sarif
```

Ensure you add your `DEEPSEEK_API_KEY` as a secret in your GitHub repository settings.

---

## Contributing

We welcome contributions to Code Analyzer! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a clear description of your changes.

### Reporting Issues

If you encounter any issues or have feature requests, please [open an issue](https://github.com/BotirBakhtiyarov/code_analyzer-b/issues) on GitHub.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
