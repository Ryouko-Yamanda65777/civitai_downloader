from setuptools import setup, find_packages

setup(
    name='civitai-downloader',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'civitai-downloader=civitai_downloader.downloader:main',
        ],
    },
    author=' Ryouko-Yamanda65777',
    description='A downloader for CivitAI models',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
