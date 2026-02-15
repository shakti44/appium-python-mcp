from setuptools import setup, find_packages

setup(
    name='appium-python-mcp',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'appium-python-client',
        'fastapi',
        'uvicorn',
        'pydantic',
    ],
    entry_points={
        'console_scripts': [
            'appium-mcp=your_module_name:main',  # Replace your_module_name with the actual module
        ],
    },
)