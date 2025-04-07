import argparse
import sys
import os
import shutil
from .utils import download_repo, scan_files, write_report, get_translation, is_local_path
from .analyzer import CodeAnalyzer
from . import __version__

def setup_command(args):
    print("Initializing code analyzer setup...")
    api_key = input("Please enter your DeepSeek API key: ").strip()
    if not api_key:
        print("Error: API key cannot be empty.")
        sys.exit(1)

    config_dir = os.path.expanduser("~/.code_analyzer")
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, "config.ini")

    config = configparser.ConfigParser()
    config["DEEPSEEK"] = {"API_KEY": api_key}

    with open(config_path, "w") as f:
        config.write(f)

    print(f"Setup complete. API key saved to {config_path}")

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
        # Check if the input is a local path or a GitHub URL
        if is_local_path(args.github_url):
            repo_path = os.path.abspath(args.github_url)
            if not args.no_stream:
                print(f"📁 Analyzing local directory: {repo_path}")
        else:
            repo_path = download_repo(args.github_url, git_token=args.git_token)
            if not args.no_stream:
                print(f"📁 Downloaded repository to: {repo_path}")

        files = scan_files(repo_path)
        if not args.no_stream:
            print(f"📁 Found {len(files)} files to analyze")

        analyzer = CodeAnalyzer(lang=args.lang, verbose=args.verbose, no_details=args.no_details, no_stream=args.no_stream)
        analyzer.analyze_project(files)
        report = analyzer.generate_report()

        if args.output:
            write_report(report, args.output, args.format, lang=args.lang)
            if not args.no_stream:
                print(f"\n✅ Report saved to {args.output}")
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
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
    finally:
        # Only clean up if we downloaded a repo (not for local paths)
        if repo_path and not is_local_path(args.github_url) and os.path.exists(os.path.dirname(repo_path)):
            shutil.rmtree(os.path.dirname(repo_path))

def main():
    parser = argparse.ArgumentParser(prog="code_analyzer")
    subparsers = parser.add_subparsers()

    # Setup command (unchanged)
    setup_parser = subparsers.add_parser('setup', help='Initial setup')
    setup_parser.set_defaults(func=setup_command)

    # Analyze command
    analyze_parser = subparsers.add_parser(
        'analyze',
        help='Analyze a repository or local directory',
        formatter_class=argparse.RawTextHelpFormatter,
        description="Analyze a GitHub repository or local directory for security vulnerabilities"
    )
    analyze_parser.add_argument(
        'github_url',
        help='GitHub repository URL (e.g., https://github.com/user/repo) or local path (e.g., .)'
    )
    analyze_parser.add_argument(
        '--git-token',
        help='GitHub access token for private repositories\n'
             '(create at: https://github.com/settings/tokens)'
    )
    analyze_parser.add_argument(
        '-o', '--output',
        help='Output file path for report\n'
             '(supports .txt, .md, .html, .json, .sarif)'
    )
    analyze_parser.add_argument(
        '-f', '--format',
        choices=['txt', 'md', 'html', 'json', 'sarif'],
        default='txt',
        help='Output format for the report\n'
             '(default: autodetect from output file extension)'
    )
    analyze_parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output for debugging'
    )
    analyze_parser.add_argument(
        '--no-details',
        action='store_true',
        help='Exclude detailed findings from the report'
    )
    analyze_parser.add_argument(
        '--lang',
        default='en',
        choices=['en', 'uz', 'zh', 'ru'],
        help='Language for the report (en, uz, zh, ru)'
    )
    analyze_parser.add_argument(
        '--no-stream',
        action='store_true',
        help='Suppress console output and save to output file'
    )

    # Version and main help
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    analyze_parser.set_defaults(func=analyze_command)
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()