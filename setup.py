from distutils.core import setup
import py2exe

setup(
    console=[
        {
            "script": "main.py",
            "icon_resources": [(1, "icon.ico")],
            "dest_base" : "xing-collect"
        }
    ],
    options={
        "py2exe": {
            "optimize" : 2,
            # "excludes": ["win32com.gen_py", ],
            "includes": ["win32com.client", "win32com.server.util"],
            # "includes": ["win32api", "win32com", "win32com.client", "win32com.client.gencache"],
            # "dll_excludes": ["MSVCP90.dll", "w9xpopen.exe"]
        }
    }
)
