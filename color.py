def hsl_to_rgb(h):
    r = int(max(0, min(255, 255 * abs(h * 6 - 3) - 1)))
    g = int(max(0, min(255, 255 * (2 - abs(h * 6 - 2)) - 1)))
    b = int(max(0, min(255, 255 * (2 - abs(h * 6 - 4)) - 1)))
    return r, g, b