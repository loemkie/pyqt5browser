# -*- mode: python -*-

block_cipher = None


a = Analysis(['p2-uat.py'],
             pathex=['C:\\Users\\chenqiwang\\AppData\\Local\\Programs\\Python\\Python35/Lib/site-packages/PyQt5/Qt/bin', 'D:\\mydocument\\myprojects\\python\\mylike\\pyqt5'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          name='p2-uat',
          debug=False,
          strip=False,
          upx=True,
          console=True )
