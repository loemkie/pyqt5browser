# -*- mode: python -*-

block_cipher = None


a = Analysis(['standalone.py'],
             pathex=['C:\\Python35-32\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'D:\\mydocument\\myprojects\\python\\mylike\\pyqt5'],
             binaries=[],
             datas=[],
             hiddenimports=['queue'],
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
          exclude_binaries=True,
          name='standalone',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='icon\\m.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='standalone')
