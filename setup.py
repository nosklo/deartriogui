from setuptools import setup, find_packages

exec(open("deartriogui/_version.py", encoding="utf-8").read())

LONG_DESC = open("README.rst", encoding="utf-8").read()

setup(
    name="deartriogui",
    version=__version__,
    description="Async DearPyGui support using trio guest mode eventloop",
    url="Project URL (for setup.py metadata)",
    long_description=LONG_DESC,
    author="Clovis Fabricio Costa",
    author_email="python.nosklo@0sg.net",
    license="MIT -or- Apache License 2.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["trio", "dearpygui"],
    keywords=[
        "async", "io", "gui",
    ],
    python_requires=">=3.7",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "Framework :: Trio",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
