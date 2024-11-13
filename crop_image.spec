# -*- mode: python ; coding: utf-8 -*-

import cv2
import os
import sys

block_cipher = None

# Get the path to the haarcascade file
cascade_path = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')

a = Analysis(['crop_image.py'],
             pathex=[],
             binaries=[],
             datas=[(cascade_path, 'cv2/data')],  # Modified this line
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='FaceCropper',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True)