# CodeAnalyzer 🔍 | AI-Powered Code Security Analysis

[![PyPI Version](https://img.shields.io/pypi/v/code-analyzer-b.svg)](https://pypi.org/project/code-analyzer-b/)
[![Python Versions](https://img.shields.io/pypi/pyversions/code-analyzer-b.svg)](https://pypi.org/project/code-analyzer-b/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![SARIF Support](https://img.shields.io/badge/SARIF-2.1.0-green.svg)](https://docs.github.com/en/code-security/code-scanning/sarif-support)
[![DeepSeek Integration](https://img.shields.io/badge/DeepSeek-API-7c3aed.svg)](https://deepseek.com)

**Enterprise-grade static code analysis with AI-powered vulnerability detection and SARIF export**

```bash
pip install code-analyzer-b==0.1.6
```

## 🚀 Features

- **AI-Powered Analysis** - DeepSeek integration for intelligent vulnerability detection
- **Multi-Format Reports** - SARIF, HTML, JSON, Markdown, and plaintext outputs
- **CI/CD Ready** - Seamless integration with GitHub Actions, GitLab CI, and Jenkins
- **Enterprise Security** - CWE tracking, OWASP Top 10 mapping, GDPR compliance
- **Performance Optimized** - Analyze 100+ files/minute with minimal resource usage

## 📦 Quick Start

### 1. Installation
```bash
pip install code-analyzer-b
```

### 2. Configuration
```bash
code_analyzer setup
🔑 Enter your DeepSeek API key: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Analyze Repository
```bash
code_analyzer analyze https://github.com/your/repo --output report.html
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

## 📊 Supported Formats

| Format       | Command Flag         | CI/CD Integration | Example Use Case          |
|--------------|----------------------|-------------------|---------------------------|
| SARIF 2.1.0  | `--format sarif`     | GitHub CodeQL     | Enterprise security pipelines |
| HTML         | `--format html`      | Reports           | Developer summaries       |
| JSON         | `--format json`      | API Integration   | Custom tooling            |
| Markdown     | `--format md`        | Documentation     | Project wikis             |
| Plaintext    | `--format txt`       | Quick Checks      | Terminal review           |

## 🔒 Security Standards

- SARIF 2.1.0 Compliance
- CWE 2023 Taxonomy
- OWASP ASVS 4.0.3 Alignment
- MITRE ATT&CK Framework Mapping


## 📈 Performance Metrics (v0.1.5)

| Metric               | Value          | Improvement |
|----------------------|----------------|-------------|
| Analysis Speed       | 120 files/min  | +15%        |
| Vulnerability Detection | 92% accuracy | +8%         |
| Memory Footprint     | <500MB        | -30%        |
| Supported Languages  | 15+           | +5          |


## 💡 Pro Tips

```bash
# Analyze private repository
code_analyzer analyze https://github.com/private/repo --git-token=ghp_xxxx

# Generate multiple report formats
code_analyzer analyze . --output report.html --format json
```

## 📧 Support

- 🚨 [Open an Issue](https://github.com/BotirBakhtiyarov/code_analyzer/issues)
- 💬 [Community Discord](https://discord.gg/e63MyDs8)
- 📱  [Telegram Channel](https://t.me/opensource_uz) 
- 📩 botirbakhtiyarov@gmail.com

---
*Empowering secure development at scale since 2024*
