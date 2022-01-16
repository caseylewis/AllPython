# -*- mode: python -*-

block_cipher = None


a = Analysis(['ParkingLoginApp.py'],
             pathex=['C:\\Users\\casey\\Dropbox\\Code\\PyCharm Projects\\AllPython\\App_3500ParkingLogin'],
             binaries=None,
             datas=None,
             hiddenimports=['App_3500ParkingLogin'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='ParkingLoginApp_v2.0.0.1',
          debug=False,
          strip=False,
          upx=True,
          console=False )
