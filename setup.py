from setuptools import setup, find_packages

# Read the README.md file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='civitai-downloader',
    version='1.1.4',
    packages=find_packages(),
    install_requires=[
        'gradio',  # Include other dependencies here if needed
    ],
    entry_points={
        'console_scripts': [
            'civitai-downloader=civitai_downloader.app:main',  # Adjust entry point to match your file structure
        ],
    },
    author='Ryouko-Yamanda65777',
    author_email='',  # Optional, but recommended for contact
    description='A downloader for CivitAI models',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Ryouko-Yamanda65777/civitai-downloader',  # Add your GitHub repo URL
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='CivitAI downloader gradio',
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        '': ['*.md'],  # Include markdown files in the package
    },
    project_urls={  # Optional additional URLs
        'Bug Tracker': 'https://github.com/Ryouko-Yamanda65777/civitai-downloader/issues',
        'Source Code': 'https://github.com/Ryouko-Yamanda65777/civitai-downloader',
    },
)
