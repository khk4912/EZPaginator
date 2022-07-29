from setuptools import setup, find_packages
from EZPaginator import __version__

setup(
    name="EZPaginator",
    license="MIT",
    version=__version__,
    description="Python library for discord.py pagination.",
    author="khk4912",
    author_email="khk49121@gmail.com",
    url="https://github.com/khk4912/EZPaginator",
    packages=find_packages(),
    keywords=["discord.py", "pagination"],
    python_requires=">=3.9",
    install_requires=["discord.py"],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
