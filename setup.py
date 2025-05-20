from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai_building_blocks",
    version="0.1.0",
    author="Matthieu Vincke",
    author_email="matthieu.vincke@gmail.com",
    description="Reusable AI/ML components for fast prototyping",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matthieu-vincke/ai_building_blocks",
    packages=find_packages(include=["components", "components.*"]),
    install_requires=[
        "numpy",
        "torch",
        "scikit-learn",
        "pandas",
        "requests",
        "beautifulsoup4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
)
