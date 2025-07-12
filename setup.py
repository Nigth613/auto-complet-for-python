from setuptools import setup, find_packages

setup(
    name='autocomplete',
    version='0.1.0',
    description='Auto-complete widget for Python using Tkinter and Jedi',
    author='Night',
    author_email='nightgg904@gmail.com',
    url='https://github.com/Nigth613/auto-complet-for-python',  # se for usar GitHub
    packages=find_packages(),
    install_requires=[
        'jedi',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
