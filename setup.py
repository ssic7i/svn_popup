from distutils.core import setup
import py2exe

setup(windows=['svn_popup.py'], options={"py2exe" : {"includes" : ["sip"], 'bundle_files': 2, 'compressed': False}})
