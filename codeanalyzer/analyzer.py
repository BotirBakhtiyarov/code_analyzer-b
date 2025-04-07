# codeanalyzer/analyzer.py

from tqdm import tqdm
from .deepseek import DeepSeekClient
from .utils import read_file, get_translation

class CodeAnalyzer:
    def __init__(self, lang='en', verbose=False, no_details=False, no_stream=False):
        self.lang = lang
        self.verbose = verbose
        self.no_details = no_details
        self.no_stream = no_stream
        self.client = DeepSeekClient()
        self.findings = []
        self.stats = {'total_files': 0, 'critical': 0, 'warnings': 0, 'analyzed_files': 0}
        
    def analyze_file(self, file_path):
        try:
            code = read_file(file_path)
            result = self.client.analyze_code(code, self.lang)
            self.stats['total_files'] += 1

            result_lower = result.lower()
            if 'critical' in result_lower:
                self.stats['critical'] += 1
            elif 'warning' in result_lower:
                self.stats['warnings'] += 1

            if "no issues" not in result_lower:
                self.findings.append({"file": file_path, "result": result})
            if self.verbose and not self.no_stream:
                issues_found = "yes" if "no issues" not in result_lower else "no"
                print(f"File: {file_path}, Issues found: {issues_found}")

        except Exception as e:
            if self.verbose and not self.no_stream:
                print(f"Error analyzing {file_path}: {str(e)}")
        finally:
            self.stats['analyzed_files'] += 1

    def analyze_project(self, file_list):
        if self.no_stream:
            # Silent analysis without progress bar
            for file_path in file_list:
                self.analyze_file(file_path)
        else:
            # Show progress bar
            with tqdm(total=len(file_list), desc="Analyzing Files", unit="file") as pbar:
                for file_path in file_list:
                    if self.verbose:
                        print(f"Analyzing {file_path}...")
                    self.analyze_file(file_path)
                    pbar.update(1)

    def generate_report(self):
        stats_summary = self._generate_stats_summary()
        ai_summary = self._generate_ai_summary()
        summary = f"{stats_summary}\n\n{ai_summary}"
        detailed_findings = self.findings if not self.no_details else []

        return {"summary": summary, "detailed_findings": detailed_findings, "stats": self.stats.copy()}

    def _generate_stats_summary(self):
        return (
            f"{get_translation(self.lang, 'summary_title')}:\n"
            f"• {get_translation(self.lang, 'critical_issues')}: {self.stats['critical']}\n"
            f"• {get_translation(self.lang, 'warnings')}: {self.stats['warnings']}\n"
            f"• {get_translation(self.lang, 'files_processed')}: {self.stats['analyzed_files']}/{self.stats['total_files']}"
        )

    def _generate_ai_summary(self):
        if not self.findings:
            return f"{get_translation(self.lang, 'ai_analysis')}: {get_translation(self.lang, 'no_issues')}"

        if not self.no_stream:
            print("\nGenerating AI-powered analysis:")

        findings_text = "\n\n".join(
            f"{get_translation(self.lang, 'file')}: {f['file']}\n{get_translation(self.lang, 'findings')}: {f['result']}"
            for f in self.findings
        )

        full_summary = []
        stream = self.client.generate_summary_streaming(findings_text, self.lang)
        for chunk in stream:
            full_summary.append(chunk)
            if not self.no_stream:
                print(chunk, end='', flush=True)

        return f"{get_translation(self.lang, 'ai_analysis')}:\n" + ''.join(full_summary)