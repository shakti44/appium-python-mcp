from setuptools import setup, find_packages

setup(
    name='your-package-name',  # Update with your package name
    version='0.1.0',  # Update with your package version
    author='Your Name',  # Update with your name
    author_email='your.email@example.com',  # Update with your email
    description='A brief description of your package',  # Update with your description
    long_description=open('README.md').read(),  # Assuming you have a README.md
    long_description_content_type='text/markdown',
    url='https://github.com/shakti44/appium-python-mcp',  # Update with your repository URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Update with your license
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'somepackage',  # List your package dependencies here
    ],
    entry_points={
        'console_scripts': [
            'your_command=your_module:main_function',  # Update with your command
        ],
    },
    python_requires='>=3.6',  # Update with your required Python version
) 
