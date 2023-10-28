from setuptools import setup

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(
    name='Dashboard & Tk Application',
    version='1.0',
    author='Romain BOYRIE',
    author_email='romain@boyrie.email',
    description='Data viz',
    url="https://github.com/sha-cmd/Tk_dashboard",
    license='GNU V3 License',
    long_description=long_description,
    packages=['src'],
    install_requires=['ttkbootstrap', 'matplotlib'],
    python_requires='>=3.11',
    #package_data={'src.lang.images': ['*.png']},
    entry_points={
        'console_scripts': [
            'prg = main'
        ]
    }
)
