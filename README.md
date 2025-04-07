# CodeAnalyzer🔍 | AI-Powered Code Security Analysis

[![PyPI Version](https://img.shields.io/pypi/v/code-analyzer-b.svg)](https://pypi.org/project/code-analyzer-b/)
[![Python Versions](https://img.shields.io/pypi/pyversions/code-analyzer-b.svg)](https://pypi.org/project/code-analyzer-b/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![SARIF Support](https://img.shields.io/badge/SARIF-2.1.0-green.svg)](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning)
[![DeepSeek Integration](https://img.shields.io/badge/DeepSeek-API-7c3aed.svg)](https://deepseek.com)

**CodeAnalyzer** is an AI-enhanced static analysis tool that identifies security vulnerabilities, code smells, and compliance issues in software repositories. Powered by DeepSeek's AI and compatible with GitHub Code Scanning.

## ✨ Key Features

- **AI-Powered Analysis** - Context-aware vulnerability detection
- **Multi-Language Support** - Python, JS/TS, Java, C/C++, Go, Rust
- **SARIF Export** - GitHub Code Scanning integration
- **CI/CD Ready** - GitHub Actions, GitLab CI, Jenkins support
- **Security Compliance** - OWASP Top 10, CWE/SANS Top 25
- **Smart Reporting** - HTML, Markdown, JSON, SARIF formats

![Alt Text](diagram.png)

## 🚀 Quick Start

### Installation
```bash
pip install code-analyzer-b
```

### Basic Usage
```bash
# Initialize configuration
code_analyzer setup

# Analyze repository
code_analyzer analyze https://github.com/yourusername/repo --output report.html
```

### Sample Output
```text
✅ Configuration saved to ~/.code_analyzer/config.ini
🔍 Analyzing: https://github.com/yourusername/repo
📦 Repository cloned (142 files, 2.8MB)
🛡️ Found 3 critical issues, 7 warnings
📊 Generated HTML report: report.html
```

## 🛠️ Advanced Usage

### GitHub Integration
```bash
code_analyzer analyze . \
  --format sarif \
  --git-token $GITHUB_TOKEN \
  --output results.sarif
```

### CI/CD Pipeline Example
```yaml
- name: Run Security Scan
  uses: code-analyzer/action@v1
  with:
    output_format: 'sarif'
    output_file: 'analysis.sarif'
    
- name: Upload Results
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: analysis.sarif
```

### Custom Analysis
```bash
# Output formats
code_analyzer analyze https://github.com/repo --output report.md --format markdown
```

## 🌐 Supported Languages

| Language       | Extensions           | Common Checks               |
|----------------|----------------------|-----------------------------|
| Python         | `.py`                | SQLi, XSS, Dependency Risks |
| JavaScript/TS  | `.js`, `.ts`         | XSS, Prototype Pollution    |
| Java           | `.java`              | Insecure Deserialization    |
| C/C++          | `.c`, `.cpp`         | Buffer Overflows            |
| Go             | `.go`                | Race Conditions             |
| Rust           | `.rs`                | Unsafe Code Patterns        |

## 💡 Pro Tips

```bash
# Analyze private repository
code_analyzer analyze https://github.com/private/repo --git-token=ghp_xxxx

# Generate multiple report formats
code_analyzer analyze . --output report.html --format json
```

## 🤝 Contributing

We welcome contributions! Please see our [Contribution Guidelines](CONTRIBUTING.md) for:
- Feature requests
- Bug reports
- Documentation improvements
- Code contributions

## 📜 License

MIT Licensed - See [LICENSE](LICENSE) for full text

---

**Disclaimer:** This project is not affiliated with DeepSeek. Use of AI services requires separate API access.

[GitHub Repository](https://github.com/BotirBakhtiyarov/code_analyzer) | 
[PyPI Package](https://pypi.org/project/code-analyzer-b/) | 
[Telegram Channel](https://t.me/opensource_uz)
