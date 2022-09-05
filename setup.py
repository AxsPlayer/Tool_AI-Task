import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="naiximing",
    version="0.0.2",
    author="kexi",
    author_email="498100059@qq.com",
    description="各种有趣的工具合集.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AxsPlayer/Tool_AI-Task",
    packages=setuptools.find_packages(),
    install_requires=['Pillow'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
