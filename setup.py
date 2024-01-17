
from setuptools import setup, find_packages

setup(
    name='FileMetadataExtractor',
    version='0.1',
    packages=find_packages(),
    description='A Python utility for extracting file metadata',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='MasterCard007',
    author_email='',
    url='[Your URL]',
    install_requires=[
        'tqdm',  # Assuming tqdm is a dependency, as it was used in the script
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'filemetadataextractor=model_res:main'  # Assuming 'model_res.py' contains a main function
        ]
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
