import setuptools
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
readme_text = (this_directory / "README.md").read_text()

setuptools.setup(
    include_package_data=True,
    name="gen_readme",
    version="0.1",
    description="python utility for interactive README file generation",
    author="BM",
    author_email="hammermolotok@gmail.com",
    packages=setuptools.find_packages(),
    install_requires=[
        # required packages with versions go here
    ],
    entry_points={
        "console_scripts": [
            "gen_readme = src.makeReadMe:gen_readme",
        ]
    },
    long_description=readme_text,  # Provide entire contents of README to long_description
    long_description_content_type="text/markdown",
)