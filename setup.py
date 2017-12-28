from cx_Freeze import setup, Executable

includes = ['ply', 'lambdastack']
excludes = []
packages = []

executables = [
    Executable('main.py')
]

setup(name='lambdastack',
      version='1.0',
      description='Stack-based, lambda-calculus language',
      options = {'build_exe': {'excludes':excludes,'packages':packages,'includes':includes}},
      executables=executables
      )