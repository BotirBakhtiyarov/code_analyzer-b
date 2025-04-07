import argparse
import sys
import os
import shutil
from .utils import download_repo, scan_files, write_report, get_translation
from .analyzer import CodeAnalyzer
from . import __version__

def analyze_command(args):
    # If --no-stream is used, require an output file
    if args.no_stream and not args.output:
        print("Error: --no-stream requires an output file to be specified with -o or --output.")
        sys.exit(1)

    # Only print if not in no-stream mode
    if not args.no_stream:
        print(f"\n🔍 Starting analysis of {args.github_url}")

    repo_path = None
    try:
        repo_path = download_repo(args.github_url, git_token=args.git_token)
        files = scan_files(repo_path)
        if not args.no_stream:
            print(f"📁 Found {len(files)} files to analyze")

        # Pass the no_stream flag to the analyzer
        analyzer = CodeAnalyzer(lang=args.lang, verbose=args.verbose, no_details=args.no_details, no_stream=args.no_stream)
        analyzer.analyze_project(files)
        report = analyzer.generate_report()

        # Save the report to the output file if specified
        if args.output:
            write_report(report, args.output, args.format, lang=args.lang)
            if not args.no_stream:
                print(f"\n✅ Report saved to {args.output}")
        # If no output file and not in no-stream mode, print to console
        elif not args.no_stream:
            print(f"\n📝 {get_translation(args.lang, 'summary_title')}:")
            print("=" * 80)
            print(report['summary'])
            if not args.no_details and report['detailed_findings']:
                print(f"\n🔍 {get_translation(args.lang, 'detailed_findings')}:")
                for finding in report['detailed_findings']:
                    print(f"\n{get_translation(args.lang, 'file')}: {finding['file']}")
                    print("-" * 80)
                    print(finding['result'])

    except Exception as e:
        # Always print errors, even in no-stream mode
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
    finally:
        if repo_path and os.path.exists(os.path.dirname(repo_path)):
            shutil.rmtree(os.path.dirname(repo_path))

def main():
    parser = argparse.ArgumentParser(prog="code_analyzer")
    subparsers = parser.add_subparsers()

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a repository')
    analyze_parser.add_argument('github_url', help='GitHub repository URL')
    analyze_parser.add_argument('--git-token', help='GitHub access token for private repositories')
    analyze_parser.add_argument('-o', '--output', help='Output file path for report (e.g., report.txt)')
    analyze_parser.add_argument('-f', '--format', choices=['txt', 'md', 'html', 'json', 'sarif'], default='txt', help='Output format')
    analyze_parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    analyze_parser.add_argument('--no-details', action='store_true', help='Exclude detailed findings')
    analyze_parser.add_argument('--lang', default='en', choices=['en', 'uz', 'zh', 'ru'], help='Report language')
    analyze_parser.add_argument('--no-stream', action='store_true', help='Suppress console output and save to output file')

    analyze_parser.set_defaults(func=analyze_command)
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()