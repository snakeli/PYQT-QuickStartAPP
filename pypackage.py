import  os
if __name__ == '__main__':
    from PyInstaller.__main__ import run
    opts = ['AppQuickStart.py', '-w', '--icon=Icon.ico']
    run(opts)
