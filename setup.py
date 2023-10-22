with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(
    name='Mon Programme',
    version='1.0',
    author='Romain BOYRIE',
    author_email='romain@boyrie.email',
    description='Financial Data Analysis',
    url="http://github.example.com",
    license='GNU V3 License',
    long_description=long_description,
    packages=['mon_programme'],
    install_requires=['psycopg3', 'ttkbootstrap', 'matplotlib'],
    python_requires='>=3.11',
    package_data={'src.lang.images': ['*.png']},
    entry_points={
        'console_scripts': [
            'prg = main'
        ]
    }
)
