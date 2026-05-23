from importlib.resources import files
from matplotlib import font_manager as fm

_fonts_loaded = False

_FONT_NAMES = [
    'Shentox-Bold.otf',
    'Shentox-Light.otf',
    'Shentox-Medium.otf',
    'Shentox-Regular.otf',
    'Shentox-SemiBold.otf',
    'Shentox-SemiBoldItalic.otf',
    'Shentox-UltraLight.otf',
]


def load_shentox_fonts() -> None:
    global _fonts_loaded
    if _fonts_loaded:
        return
    resource_dir = files('skillcornerviz') / 'resources' / 'Shentox'
    for name in _FONT_NAMES:
        fm.fontManager.addfont(str(resource_dir / name))
    _fonts_loaded = True
