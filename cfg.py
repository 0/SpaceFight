# These values depend on the border images.
DEFAULT_WIDTH               = 800
DEFAULT_HEIGHT              = 600
DEFAULT_BORDER_THICKNESS    = 100
DEFAULT_BOUNDS              = {'left': 80, 'top': 50, 'right': 80, 'bottom': 65}
DEFAULT_SCANLINE_COLOR      = (24,30,24)
DEFAULT_SCANLINE_SKIP       = 6
DEFAULT_SCANLINE_SPEED      = 2
DEFAULT_FRAMERATE           = 60

width                       = DEFAULT_WIDTH
height                      = DEFAULT_HEIGHT
border_thickness            = None # Calculated value.
fullscreen                  = False
scanlineColor               = DEFAULT_SCANLINE_COLOR
scanlineSkip                = DEFAULT_SCANLINE_SKIP
scanlineSpeed               = DEFAULT_SCANLINE_SPEED

# Defaults for asset fallbacks
FALLBACK_BACKGROUND_COLOR   = (24,30,24,32)
FALLBACK_FOREGROUND_COLOR   = (1,1,1)
FALLBACK_ICON_COLOR         = (1,1,1)
