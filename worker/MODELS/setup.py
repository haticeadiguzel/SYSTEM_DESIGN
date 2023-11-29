from setuptools import setup, find_packages

setup(
    name='models',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'Flask-SQLAlchemy',
    ],
    python_requires='>=3.6',
)
