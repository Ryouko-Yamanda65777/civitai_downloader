from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='civitai-downloader',
    version='1.1.2',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'civitai-downloader=civitai_downloader.downloader:main',
        ],
    },
    author='Ryouko-Yamanda65777',
    description='A downloader for CivitAI models',
    long_description=long_description,  # Include README.md content
    long_description_content_type='text/markdown',  # Specify markdown format
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
