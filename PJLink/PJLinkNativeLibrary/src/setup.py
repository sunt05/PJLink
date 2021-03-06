# -*- coding: utf-8 -*-

from distutils.core import setup, Extension
import shutil, os, platform, sys
from PJLink.MathLinkEnvironment import MathLinkEnvironment as Env

setup_orig_dir = os.getcwd()
lib_dir = os.path.dirname(__file__)
os.chdir(lib_dir)

# argv1 = sys.argv
# argv2 = [ "build_ext", "--inplace" ]

mathlink_base = os.path.join(Env.get_Mathematica_root(), "SystemFiles", "Links", "MathLink", "DeveloperKit")

plat = platform.system()
if plat == "Darwin":
    sys_name = "MacOSX"
elif plat == "Linux":
    sys_name = "Linux"
elif plat == "Windows":
    sys_name = "Windows"
else:
    raise ValueError("Don't know how to find the MathLink library on system {}".format(plat))

mathlink_dir = os.path.join(mathlink_base, sys_name + "-x86-64", "CompilerAdditions")
if not os.path.exists(mathlink_dir):
    mathlink_dir = os.path.join(mathlink_base, sys_name, "CompilerAdditions")

module1 = Extension(
    'PJLinkNativeLibrary',
    sources = ['PJLinkNativeLibrary.cpp'],
    library_dirs = [ mathlink_dir ],
    libraries = [ "MLi4" ]
)

setup (name = 'PJLinkNativeLibrary',
       version = '1.0',
       description = 'Implementation of JLinkNativeLibrary for python',
       ext_modules = [module1]
       )

ext = ""
target = os.path.join(os.path.dirname(lib_dir), "PJLinkNativeLibrary")
src = None

for f in os.listdir(lib_dir):
    if f.endswith(".so"):
        ext = ".so"
        src = os.path.join(lib_dir, f)
        target += ext
    elif f.endswith(".pyd"):
        ext = ".pyd"
        src = os.path.join(lib_dir, f)
        target += ext

if src is not None:
    try:
        os.remove(target)
    except:
        pass
    os.rename(src, target)

failed = not os.path.isfile(target)