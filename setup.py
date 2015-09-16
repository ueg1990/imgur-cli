import re

from setuptools import setup, find_packages

with open('imgur_cli/__init__.py', 'r') as fd:
    meta_data = fd.read()
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        meta_data, re.MULTILINE).group(1)
    if not version:
        raise RuntimeError('Cannot find version information')
    name = re.search(r'^__title__\s*=\s*[\'"]([^\'"]*)[\'"]',
                     meta_data, re.MULTILINE).group(1)
    author = re.search(r'^__author__\s*=\s*[\'"]([^\'"]*)[\'"]',
                       meta_data, re.MULTILINE).group(1)
    email = re.search(r'^__email__\s*=\s*[\'"]([^\'"]*)[\'"]',
                      meta_data, re.MULTILINE).group(1)
    license = re.search(r'^__license__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        meta_data, re.MULTILINE).group(1)
    url = re.search(r'^__url__\s*=\s*[\'"]([^\'"]*)[\'"]',
                    meta_data, re.MULTILINE).group(1)

    print(name, author, email, license, url)

requires = ['imgurpython >= 1.1.6', 'requests >= 2.7.0']
classifiers = [
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stablegit
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3.4',
]

setup(
    name=name,
    version=version,
    description='Imgur CLI',
    author=author,
    license=license,
    classifiers=classifiers,
    keywords="imgur cli imgurpython meme memes",
    author_email=email,
    url=url,
    packages=find_packages(exclude='tests'),
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'imgur = imgur_cli.cli:main'
        ],
    }
)
