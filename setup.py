from setuptools import setup

setup(name='pyHRAExplorer',
      version='1.0',
      description='Tools for HRV and HRA analysis',
      url='https://github.com/jaropis/pyHRAExplorer',
      author='Jarosław Piskorski, Maria Guzik',
      author_email='jaropis@zg.home.pl, myguzik@gmail.com',
      license='GPLv3',
      packages=['signal_properties'],
      install_requires = [
            'numpy',
            'scipy',
            'matplotlib'
      ]
)