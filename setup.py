from setuptools import setup, find_packages

setup(
    name='Surveysgen',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'gql',
        'aiohttp'
    ],
    entry_points={
        'console_scripts': [
            'import-data = Surveysgen.gql_endpoint',
            'generate-data = Surveysgen.generator_old',
        ]
    }
)