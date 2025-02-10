from setuptools import setup, find_packages

setup(
    name="seppy",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'rich>=10.0.0',
        'tqdm>=4.62.0',
        'psutil>=5.8.0',
        'memory-profiler>=0.58.0',
        'typing-extensions>=4.0.0',
        'PyYAML>=6.0.0',
        'Jinja2>=3.0.0'
    ],
    entry_points={
        'console_scripts': [
            'seppy=seppy.__main__:main',
        ],
    },
    author="Your Name",
    description="A tool for splitting Python scripts into modules",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
) 