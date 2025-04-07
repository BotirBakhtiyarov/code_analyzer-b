import os
import tempfile
import zipfile
import io
import requests
from tqdm import tqdm
import json
from codeanalyzer.config import Config
from . import __version__

# Translation dictionary (unchanged)
translations = {
    'en': {
        'summary_title': 'Security Analysis Summary',
        'critical_issues': 'Critical Issues',
        'warnings': 'Warnings',
        'files_processed': 'Files Processed',
        'no_issues': 'No significant issues found',
        'ai_analysis': 'AI Analysis',
        'detailed_findings': 'Detailed Findings',
        'file': 'File',
        'findings': 'Findings'
    },
    'uz': {  # Example Uzbek translations; replace with accurate ones
        'summary_title': 'Xavfsizlik Tahlili Xulosa',
        'critical_issues': 'Kritik Muammolar',
        'warnings': 'Ogohlantirishlar',
        'files_processed': 'Ishlov Berilgan Fayllar',
        'no_issues': 'Muhim muammolar topilmadi',
        'ai_analysis': 'AI Tahlili',
        'detailed_findings': 'Batafsil Topilmalar',
        'file': 'Fayl',
        'findings': 'Topilmalar'
    },
    'zh': {
        'summary_title': '安全分析摘要',
        'critical_issues': '严重问题',
        'warnings': '警告',
        'files_processed': '已处理文件',
        'no_issues': '未发现重大问题',
        'ai_analysis': 'AI分析',
        'detailed_findings': '详细发现',
        'file': '文件',
        'findings': '发现'
    },
    'ru': {  # Example Russian translations; replace with accurate ones
        'summary_title': 'Сводка анализа безопасности',
        'critical_issues': 'Критические проблемы',
        'warnings': 'Предупреждения',
        'files_processed': 'Обработанные файлы',
        'no_issues': 'Серьезных проблем не обнаружено',
        'ai_analysis': 'Анализ ИИ',
        'detailed_findings': 'Подробные находки',
        'file': 'Файл',
        'findings': 'Находки'
    }
}

def get_translation(lang, key):
    return translations.get(lang, translations['en']).get(key, key)

def is_local_path(path):
    """Check if the input is a local path rather than a URL."""
    return os.path.exists(path) or path == '.' or path.startswith('./') or path.startswith('../') or os.path.isabs(path)

def download_repo(github_url, git_token=None):
    temp_dir = tempfile.mkdtemp(prefix="code_analyzer_")
    headers = {'User-Agent': 'CodeAnalyzer'}
    if git_token:
        headers['Authorization'] = f'token {git_token}'

    # Try both main and master branches
    branches = ['main', 'master']
    for branch in branches:
        zip_url = f"{github_url}/archive/refs/heads/{branch}.zip"
        response = requests.get(zip_url, headers=headers, stream=True)
        if response.status_code == 200:
            break
    else:
        error_msg = "Failed to download repository. Possible reasons:\n"
        error_msg += "- Invalid/Missing GitHub token for private repo\n"
        error_msg += "- Repository/branch doesn't exist"
        raise ValueError(error_msg)

    total_size = int(response.headers.get('content-length', 0))

    with tqdm(
            total=total_size,
            unit='B',
            unit_scale=True,
            desc="Downloading Repository",
            bar_format="{desc}: {percentage:3.0f}%|{bar:20}| {n_fmt}/{total_fmt}",
            ascii="->="
    ) as progress_bar:
        zip_content = io.BytesIO()
        for data in response.iter_content(chunk_size=1024):
            zip_content.write(data)
            progress_bar.update(len(data))

    with zipfile.ZipFile(zip_content) as zip_ref:
        zip_ref.extractall(temp_dir)

    extracted_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])
    return extracted_dir

def scan_files(directory):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getsize(file_path) > Config.MAX_FILE_SIZE:
                continue
            ext = os.path.splitext(file_path)[1]
            if ext.lower() in Config.SUPPORTED_EXTENSIONS:
                file_list.append(file_path)
    return file_list

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def write_report(report, filename, format=None, lang='en'):
    if format:
        file_ext = f'.{format}'
    else:
        file_ext = os.path.splitext(filename)[1].lower()

    if file_ext == '.txt':
        _write_txt_report(report, filename, lang)
    elif file_ext == '.md':
        _write_markdown_report(report, filename, lang)
    elif file_ext == '.html':
        _write_html_report(report, filename, lang)
    elif file_ext == '.json':
        _write_json_report(report, filename, lang)
    elif file_ext == '.sarif' or format == 'sarif':
        _write_sarif_report(report, filename, lang)
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")

def _write_txt_report(report, filename, lang):
    content = [
        get_translation(lang, 'summary_title'),
        "=" * 80,
        report['summary']
    ]
    if report['detailed_findings']:
        content.append(f"\n{get_translation(lang, 'detailed_findings')}:")
        for finding in report['detailed_findings']:
            content.append(f"\n{get_translation(lang, 'file')}: {finding['file']}")
            content.append("-" * 60)
            content.append(finding['result'])

    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

def _write_html_report(report, filename, lang):
    findings_html = "".join(
        f"""
        <div class="finding">
            <h3>{get_translation(lang, 'file')}: {finding['file']}</h3>
            <pre>{finding['result']}</pre>
        </div>
        """
        for finding in report['detailed_findings']
    )

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{get_translation(lang, 'summary_title')}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .finding {{ margin-bottom: 30px; border-left: 4px solid #007bff; padding-left: 15px; }}
            pre {{ background: #f8f9fa; padding: 15px; border-radius: 4px; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #34495e; }}
        </style>
    </head>
    <body>
        <h1>{get_translation(lang, 'summary_title')}</h1>
        <h2>Summary</h2>
        <pre>{report['summary']}</pre>
        {"<h2>" + get_translation(lang, 'detailed_findings') + "</h2>" + findings_html if report['detailed_findings'] else ""}
    </body>
    </html>
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

def _write_json_report(report, filename, lang):
    report_data = {
        "summary": report['summary'],
        "findings": [
            {
                "file": f['file'],
                "result": f['result'],
                "severity": _detect_severity(f['result'])
            } for f in report['detailed_findings']
        ]
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

def _detect_severity(text):
    text = text.lower()
    if 'critical' in text:
        return "critical"
    elif 'high' in text:
        return "high"
    elif 'medium' in text:
        return "medium"
    return "low"

def _write_markdown_report(report, filename, lang):
    content = [
        f"# {get_translation(lang, 'summary_title')}",
        report['summary'],
    ]
    if report['detailed_findings']:
        content.append(f"## {get_translation(lang, 'detailed_findings')}")
        for idx, finding in enumerate(report['detailed_findings'], 1):
            content.append(
                f"\n### Finding {idx}\n"
                f"**{get_translation(lang, 'file')}**: `{finding['file']}`\n\n"
                f"```\n{finding['result']}\n```"
            )

    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

def _write_sarif_report(report, filename, lang):
    sarif_template = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {
                "driver": {
                    "name": "CodeAnalyzer",
                    "version": __version__,
                    "rules": []
                }
            },
            "results": []
        }]
    }

    for idx, finding in enumerate(report['detailed_findings']):
        sarif_template["runs"][0]["results"].append({
            "ruleId": f"CA{idx:04d}",
            "message": {
                "text": finding['result']
            },
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": finding['file']
                    }
                }
            }],
            "level": "error" if 'critical' in finding['result'].lower() else "warning"
        })

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(sarif_template, f, indent=2)