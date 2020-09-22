# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['epidemic.py'],
             pathex=['/Users/tz/Files/Docs/Code/Python/Epidemic'],
             binaries=[],
             datas=[('data/cards.yml', 'data'), ('img/pandemic-logo.png', 'img')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Epidemic',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='icon.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Epidemic')
app = BUNDLE(coll,
             name='Epidemic.app',
             icon='icon.icns',
             bundle_identifier='com.talzana.epidemic',
             info_plist={
                  'NSHighResolutionCapable': 'True'
                })
