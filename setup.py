from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
desc = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="format_game",
    version="1.0.2",
    description="A python module that allows you to format various games",
    long_description=desc,
    long_description_content_type="text/markdown",
    author="andrew",
    url="https://github.com/andrewthederp/FormatGame",
    license="Apache",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    include_package_data=True,
    package_data={
        '': [
            'hangman/**',
            'fonts/**',
            'chess/**',
            'chess/8bit/**',
            'chess/blue/**',
            'chess/glass/**',
            'chess/graffiti/**',
            'chess/green/**',
            'chess/light/**',
            'chess/lolz/**',
            'chess/metal/**',
            'chess/neon/**',
            'chess/newspaper/**',
            'chess/tournament/**',
            'chess/wood/**',
            '2048/**'
        ]
    },
    install_requires=["pillow", "colorama"],
    python_requires=">=3.6",
    packages=find_packages(include=["format_game", "format_game.*"]),
)
