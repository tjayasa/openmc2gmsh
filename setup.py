from setuptools import setup
setup(
    name = 'OMC2Gmsh',
    version = '0.1.0',
    packages = ['Converter'],
    entry_points = {
        'console_scripts': [
            'OMC2Gmsh = Converter.__main__:main'
        ]
    })