from setuptools import find_packages, find_namespace_packages, setup
# create setup.py
#step 1 run: in pycharm create new run config "setup.py" param "bdist_wheel"
#step 2 run: in pycharm terminal "pip install -e ."
#setp 2 is what installs the package in the current directory and tells python to find stuff in the "src" dir
#this allows your imports to work without having to fully qualify with "src"
# if you change your setup.py file you should rerun the pip install

#https://setuptools.pypa.io/en/latest/userguide/quickstart.html
#https://www.jetbrains.com/pycharm/guide/tutorials/visual_pytest/hello_test/
setup(
    name='texticular',
    version='0.0.1',
    description='A text adventure in python',
    author='MegaMane',
    extras_require=dict(tests=['pytest']),
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
)