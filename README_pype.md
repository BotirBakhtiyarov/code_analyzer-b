# Code Analyzer

**Code Analyzer** is a powerful command-line tool for analyzing code repositories for security vulnerabilities and bugs. It leverages the DeepSeek API to provide AI-powered insights into your codebase, helping you identify and address potential issues efficiently.

**Version**: 0.2.0

---

## Installation

To install Code Analyzer version 0.2.1, use pip:

```bash
pip install code-analyzer==0.2.1
```

After installation, set up your DeepSeek API key:

```bash
code_analyzer setup
```

Follow the prompts to enter your API key. You can obtain a key from [DeepSeek](https://www.deepseek.com/).

---

## Usage

### Analyzing a GitHub Repository

To analyze a public GitHub repository:

```bash
code_analyzer analyze https://github.com/user/repo
```

For private repositories, use the `--git-token` option with a GitHub access token:

```bash
code_analyzer analyze https://github.com/user/private-repo --git-token YOUR_TOKEN
```

### Analyzing a Local Directory

To analyze a local directory:

```bash
code_analyzer analyze /path/to/local/repo
```

Or, to analyze the current directory:

```bash
code_analyzer analyze .
```

### Options

- `-o, --output FILE`: Save the report to a file (supports `.txt`, `.md`, `.html`, `.json`, `.sarif`).
- `-f, --format FORMAT`: Specify the output format (`txt`, `md`, `html`, `json`, `sarif`).
- `--verbose`: Enable detailed output for debugging.
- `--no-details`: Exclude detailed findings from the report.
- `--lang LANG`: Set the report language (`en`, `uz`, `zh`, `ru`).
- `--no-stream`: Suppress console output and save directly to the output file.

Example with options:

```bash
code_analyzer analyze . --output report.sarif --format sarif --no-stream --lang uz
```

---

## Features

- **AI-Powered Analysis**: Utilizes DeepSeek's API for intelligent code analysis.
- **Multi-Language Support**: Reports available in English, Uzbek, Chinese, and Russian.
- **CI/CD Integration**: Easily integrates with GitHub Actions for automated code scanning.
- **Flexible Output**: Supports multiple report formats, including SARIF for GitHub code scanning.
- **Local and Remote Analysis**: Analyze both local directories and remote GitHub repositories.

---

For more information, visit the [GitHub repository](https://github.com/BotirBakhtiyarov/code_analyzer-b).

