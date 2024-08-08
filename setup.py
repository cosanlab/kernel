from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

version = {}
with open("feat/version.py") as f:
    exec(f.read(), version)

extra_setuptools_args = dict(tests_require=["pytest"])

setup(
    name="kernel",
    version="0.1.0",
    description="Code for working with data collected from Kernel Flow2 System",
    author="Luke Chang",
    author_email="luke.j.chang@dartmouth.edu",
    url="https://github.com/cosanlab/kernel",
    license="MIT license",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    test_suite="kernel/tests",
)
