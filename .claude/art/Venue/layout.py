"""Suggested prop placement. x, y = the prop's BASE point in map units
(x right, y DOWN, origin = top-left corner of the map).
mark = what the ground painter draws underneath that spot.
"""
W, H = 80, 64
CHUNK = 16          # units per ground chunk (2048 px @ 128 PPU)
PPU = 128

PROPS = [
    # --- eucalyptus trees (central gravel court, each inside a flower island)
    ('tree_eucalyptus_a', 27.5, 33.8, 'bed'),
    ('tree_eucalyptus_b', 52.8, 33.6, 'bed'),
    ('tree_eucalyptus_b', 30.4, 43.6, 'bed'),
    ('tree_eucalyptus_a', 56.2, 44.4, 'bed'),
    ('tree_eucalyptus_a', 16.2, 9.4, 'mulch'),
    # --- palms (south entrance court + desert garden)
    ('tree_palm', 26.4, 54.6, 'mulch'),
    ('tree_palm', 31.8, 58.2, 'mulch'),
    ('tree_palm', 36.6, 53.4, 'mulch'),
    ('tree_palm', 52.8, 53.6, 'mulch'),
    ('tree_palm', 62.0, 59.4, 'sand'),
    ('tree_palm', 72.6, 59.2, 'sand'),
    # --- olives
    ('tree_olive', 64.0, 36.5, 'deck'),
    ('tree_olive', 71.5, 48.5, 'deck'),
    ('tree_olive', 71.0, 23.6, 'ring'),
    ('tree_olive', 6.6, 23.2, 'mulch'),
    # --- citrus (north-west orchard)
    ('tree_citrus', 6.2, 8.4, 'mulch'),
    ('tree_citrus', 10.9, 6.8, 'mulch'),
    ('tree_citrus', 20.0, 7.4, 'mulch'),
    ('tree_citrus', 19.6, 21.4, 'mulch'),
    # --- cypress rows
    ('tree_cypress', 5.2, 37.0, 'mulch'),
    ('tree_cypress', 5.2, 42.5, 'mulch'),
    ('tree_cypress', 5.2, 48.0, 'mulch'),
    ('tree_cypress', 5.2, 53.5, 'mulch'),
    ('tree_cypress', 75.9, 9.6, 'ring'),
    ('tree_cypress', 75.9, 14.6, 'ring'),
    ('tree_cypress', 75.9, 19.6, 'ring'),
    # --- hall front pillars (stand on the stone plinths of the sill)
    ('pillar_wood', 29.0, 25.05, 'plinth'),
    ('pillar_wood', 35.0, 25.05, 'plinth'),
    ('pillar_wood', 41.0, 25.05, 'plinth'),
    ('pillar_wood', 47.0, 25.05, 'plinth'),
    ('pillar_wood', 53.0, 25.05, 'plinth'),
    ('pillar_wood', 59.0, 25.05, 'plinth'),
    # --- planter boxes between the pillars
    ('planter_long', 32.0, 25.3, None),
    ('planter_long', 56.0, 25.3, None),
    # --- entrance arches + bollard lights
    ('arch_metal', 44.0, 49.2, 'arch'),
    ('arch_metal', 44.0, 53.2, 'arch'),
    ('arch_metal', 44.0, 57.2, 'arch'),
    ('bollard_light', 40.85, 47.2, None), ('bollard_light', 47.15, 47.2, None),
    ('bollard_light', 40.85, 51.2, None), ('bollard_light', 47.15, 51.2, None),
    ('bollard_light', 40.85, 55.2, None), ('bollard_light', 47.15, 55.2, None),
    ('bollard_light', 40.85, 59.2, None), ('bollard_light', 47.15, 59.2, None),
    # --- lamp posts
    ('lamp_post', 21.8, 29.1, 'foot'), ('lamp_post', 66.2, 29.1, 'foot'),
    ('lamp_post', 37.9, 36.0, 'foot'), ('lamp_post', 50.1, 36.0, 'foot'),
    ('lamp_post', 37.9, 43.2, 'foot'), ('lamp_post', 50.1, 43.2, 'foot'),
    ('lamp_post', 20.2, 45.6, 'foot'), ('lamp_post', 8.6, 28.4, 'foot'),
    ('lamp_post', 11.4, 22.0, 'foot'), ('lamp_post', 21.0, 13.4, 'foot'),
    ('lamp_post', 67.2, 18.0, 'foot'), ('lamp_post', 59.9, 31.0, 'foot'),
    ('lamp_post', 59.9, 55.2, 'foot'),
    # --- string lights (two poles + garland, 8 units wide)
    ('string_lights', 33.0, 29.45, 'poles'), ('string_lights', 55.0, 29.45, 'poles'),
    ('string_lights', 30.6, 36.9, 'poles'), ('string_lights', 31.0, 52.4, 'poles'),
    ('string_lights', 68.2, 33.6, 'poles'), ('string_lights', 68.2, 53.0, 'poles'),
    ('string_lights', 12.0, 58.4, 'poles'),
    # --- greenery chandeliers hanging in the hall (pivot = floor point below them)
    ('chandelier_green', 31.0, 16.0, None),
    ('chandelier_green', 44.0, 17.0, None),
    ('chandelier_green', 57.0, 16.0, None),
    # --- potted plants
    ('pot_fiddle', 24.7, 23.6, None), ('pot_fiddle', 63.3, 23.6, None),
    ('pot_fiddle', 24.7, 9.2, None), ('pot_fiddle', 63.3, 9.2, None),
    ('pot_fiddle', 35.6, 8.2, None), ('pot_fiddle', 52.4, 8.2, None),
    ('pot_urn', 22.2, 26.2, None), ('pot_urn', 65.8, 26.2, None),
    ('pot_urn', 41.6, 29.2, None), ('pot_urn', 46.4, 29.2, None),
    ('pot_urn', 66.4, 5.4, None),
    ('planter_small', 62.0, 31.0, None), ('planter_small', 74.0, 31.0, None),
    ('planter_small', 60.4, 43.5, None), ('planter_small', 62.0, 55.6, None),
    ('planter_small', 74.0, 55.6, None),
    # --- bushes
    ('bush_round', 22.0, 32.6, None), ('bush_round', 9.0, 14.0, None),
    ('bush_round', 17.8, 25.2, None), ('bush_round', 24.4, 59.6, None),
    ('bush_round', 58.2, 30.6, None), ('bush_round', 68.4, 27.8, None),
    ('bush_flower', 4.6, 12.2, None), ('bush_flower', 21.6, 5.6, None),
    ('bush_flower', 5.0, 30.6, None), ('bush_flower', 19.4, 58.6, None),
    ('bush_flower', 37.2, 59.7, None), ('bush_flower', 57.0, 55.8, None),
    ('bush_flower', 75.6, 26.6, None),
    ('bush_lavender', 14.6, 27.4, None), ('bush_lavender', 4.8, 18.6, None),
    ('bush_lavender', 23.0, 49.8, None), ('bush_lavender', 49.6, 49.6, None),
    ('bush_lavender', 66.0, 14.4, None), ('bush_lavender', 57.6, 36.6, None),
    ('grass_pampas', 4.6, 26.8, None), ('grass_pampas', 22.0, 23.6, None),
    ('grass_pampas', 60.6, 58.6, None), ('grass_pampas', 76.2, 30.2, None),
    ('grass_pampas', 17.2, 14.4, None), ('grass_pampas', 39.6, 45.4, None),
    ('grass_pampas', 48.4, 45.4, None),
]


def unity_xy(x, y):
    """Map units (y down, origin top-left) -> Unity world position (map centred on 0,0)."""
    return (round(x - W / 2, 2), round(H / 2 - y, 2))
