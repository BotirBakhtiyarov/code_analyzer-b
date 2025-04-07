from setuptools import setup, find_packages

with open("README_pype.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="code-analyzer-b",
    version="0.2.1",
    author="Botir Bakhtiyarov",
    author_email="botirbakhtiyarovb@gmail.com",
    description="A tool to analyze code repositories for security vulnerabilities using DeepSeek AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BotirBakhtiyarov/code_analyzer-b",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "code_analyzer = codeanalyzer.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.6",
)