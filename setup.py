from setuptools import setup, find_packages

with open('README.md') as fh:
    long_description = fh.read()


setup(
    name='low-disk-check-johnivore',
    author='John Begenisich',
    author_email='john.begenisich@outlook.com',
    description='Print alert if disk space is low.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/johnivore/low-disk-check',
    python_requires='>=3.5',
    license='GPLv3',
    classifiers=[
        'Intended Audience :: System Administrators',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'psutil',
    ],
    entry_points="""
        [console_scripts]
        low-disk-check=low_disk_check:main
    """,
)
