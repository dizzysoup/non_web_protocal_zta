# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['yunagent.py'],
    pathex=['F:\\碩士事物\\資安院計畫\\SSHRDP_ZTA\\PEP\\fido2','.'],
    binaries=[],
    datas=[
      ('F:\\碩士事物\\資安院計畫\\SSHRDP_ZTA\\PEP\\fido2\\public_suffix_list.dat','.\\fido2')
    ],
    hiddenimports=[
        'server.py','cbor.py','webauth.py','pcsc.py','ctap1.py','cose.py','client.py','rpid.py','utils.py','features.py','ctap.py','mds3.py','win_api.py'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='yunagent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='yunagent',
)
