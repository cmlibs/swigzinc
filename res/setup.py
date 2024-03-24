""" Zinc: A library for visualisation of FE models.

"""

classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Intended Audience :: Education
Intended Audience :: Science/Research
License :: OSI Approved :: Apache Software License
Programming Language :: Python
Operating System :: Microsoft :: Windows
Operating System :: Unix
Operating System :: MacOS :: MacOS X
Topic :: Software Development :: Libraries :: Python Modules
"""

import os
import platform

from pathlib import Path
from skbuild import setup


here = Path(os.path.dirname(__file__))


cmake_args = [f"-DZinc_DIR={here.parent}/build-nonpython/ZincLibrary/src/build_zinc-build"] # ["-DUNIT_TESTS=OFF", "-DCOVERAGE=OFF", "-DMEMCHECK=OFF", "-DLLVM_COVERAGE=OFF", "-DCLANG_TIDY=OFF"]

if platform.system() == "Windows":
    cmake_args.append("-DLibXml2_DIR=C:/Program Files (x86)/libxml2/libxml2-2.9.10/CMake/")

doclines = __doc__.split("\n")

tag = "v0.0.1"
env_variables_file = os.path.join(here.parent, "env_variables.txt")
if os.path.isfile(env_variables_file):
    with open(env_variables_file) as f:
        content = f.read()

    for line in content.split("\n"):
        version_line = line.strip()
        if version_line.startswith("v"):
            tag = version_line.strip()
else:
    tag = os.environ.get("ZINC_VERSION_TAG", "v0.0.0")


setup(
    name="cmlibs.zinc",
    version=tag[1:],
    description=doclines[0],
    author="Zinc contributors",
    url="https://cmlibs.org",
    license="Apache 2.0",
    packages=["cmlibs", "cmlibs.zinc"],
    package_data={
        'cmlibs.zinc': ['libzinc*.dylib', 'libzinc*.so', '_*.so'],
    },
    classifiers=[cl for cl in classifiers.split('\n') if cl],
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    include_package_data=True,
    cmake_source_dir="../",
    cmake_install_target="install-python-bindings",
    cmake_args=cmake_args,
    cmake_install_dir="./",
    exclude_package_data={"": ["bin/*", "cmake/*", "include/*", "lib/*"]},
)

