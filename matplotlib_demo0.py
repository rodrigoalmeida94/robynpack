"""
Matplotlib binpack demo
"""
from typing import List
from random import randint
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Patch
import matplotlib.pyplot as plt
import itertools

import greedypacker as g


def get_vertices(i: g.Item, margin: int = 0.0) -> List[int]:
    if hasattr(i,'top_clear'):
        corners = [(i.x, i.y),
                (i.x+i.width, i.y),
                (i.x+i.width, i.y+i.height),
                (i.x, i.y+i.height)]
        if margin:
            scalar = margin
            corners = [(i.x + scalar, i.y + scalar),
                       (i.x + i.width - scalar, i.y + scalar),
                       (i.x + i.width - scalar, i.y + i.height - scalar),
                       (i.x + scalar, i.y + i.height - scalar)]
    else:
        corners = [(i.x, i.y),
                (i.x+i.width, i.y),
                (i.x+i.width, i.y+i.height),
                (i.x, i.y+i.height)]
        if margin:
            scalar = margin
            corners = [(i.x + scalar, i.y + scalar),
                       (i.x + i.width - scalar, i.y + scalar),
                       (i.x + i.width - scalar, i.y + i.height - scalar),
                       (i.x + scalar, i.y + i.height - scalar)]
    return corners

def generate_path(i: g.Item, margin: float = 0.0) -> Path:
    vertices = []
    codes = []
    codes += [Path.MOVETO] + [Path.LINETO]*3 + [Path.CLOSEPOLY]
    vertices += get_vertices(i, margin) + [(0, 0)]

    vertices = np.array(vertices, float)
    return Path(vertices, codes)

#def generate_path(items: List[g.Item], margin: bool = False) -> Path:
#    vertices = []
#    codes = []
#    for i in items:
#        codes += [Path.MOVETO] + [Path.LINETO]*3 + [Path.CLOSEPOLY]
#        vertices += get_vertices(i, margin) + [(0, 0)]
#
#    vertices = np.array(vertices, float)
#    return Path(vertices, codes)

def draw_wastemap(binpack: g.BinManager) -> None:
    path = generate_path(binpack.bins[0].wastemap.freerects)
    return PathPatch(path, lw=2.0, fc='white', edgecolor='orange', hatch='/',  label='wastemap')


def render_bin(binpack: g.BinManager, save: bool = False) -> None:
    fig, ax = plt.subplots()
    for item in binpack.items:
        path = generate_path(item)
        packed_item = PathPatch(path, facecolor='blue', edgecolor='green', label='packed items')
        ax.add_patch(packed_item)
    handles = [packed_item]

    if binpack.pack_algo == 'shelf':
        vertices = []
        codes = []
        for shelf in binpack.bins[0].shelves:
            codes += [Path.MOVETO] + [Path.LINETO] + [Path.CLOSEPOLY]
            vertices += [(0, shelf.vertical_offset), (shelf.x, shelf.vertical_offset), (0, 0)]
        vertices = np.array(vertices, int)
        path = Path(vertices, codes)
        shelf_border = PathPatch(path, lw=2.0, fc='red', edgecolor='red', label='shelf')
        handles.append(shelf_border)
        ax.add_patch(shelf_border)

    if binpack.pack_algo == 'skyline':
        vertices = []
        codes = []
        for seg in binpack.bins[0].skyline:
            codes += [Path.MOVETO] + [Path.LINETO] + [Path.CLOSEPOLY]
            vertices += [(seg.x, seg.y), (seg.x+seg.width, seg.y), (0, 0)]
        vertices = np.array(vertices, int)
        path = Path(vertices, codes)
        skyline = PathPatch(path, lw=2.0, fc='red', edgecolor='red', label='skyline')
        ax.add_patch(skyline)
        handles.append(skyline)

        wastemap = draw_wastemap(binpack)
        handles.append(wastemap)
        ax.add_patch(wastemap)

    if binpack.pack_algo == 'guillotine':
        path = generate_path(binpack.bins[0].freerects, True)
        freerects = PathPatch(path, fc='none', edgecolor='red', hatch='/', lw=1, label='freeRectangles')
        ax.add_patch(freerects)
        handles.append(freerects)

    if binpack.pack_algo == 'maximal_rectangle':
        margin = 0
        for rect in binpack.bins[0].freerects:
            path = generate_path(rect, margin=margin)
            freerects = PathPatch(path, fc='none', ec='red', lw=1, label='freeRectangles')
            ax.add_patch(freerects)
            margin += .0
        handles.append(freerects)

    ax.set_title('%s Algorithm - %r Heuristic' % (M.pack_algo, M.heuristic))
    ax.set_xlim(0, M.bin_width)
    ax.set_ylim(0, M.bin_height)

    plt.legend(handles=handles, bbox_to_anchor=(1.04,1), loc="upper left")


    if save:
        plt.savefig('%s Algorithm - %r Heuristic' % (M.pack_algo, M.heuristic), bbox_inches="tight", dpi=150)
    else:
        plt.show()
    return


if __name__ == '__main__':
    maximal = [
    g.Item(300, 150, 0, 45, 0, 45),
    g.Item(300, 150, 45, 0, 45, 0),
    g.Item(300, 150, 45, 0, 0, 45),
    g.Item(300, 150, 0, 45, 45, 0)
    ]
    """
    g.Item(270, 150, 0, 45, 0, 45),
    g.Item(270, 150, 45, 0, 45, 0),
    g.Item(270, 150, 45, 0, 0, 45),
    g.Item(270, 150, 0, 45, 45, 0),
    g.Item(250, 150, 0, 45, 0, 45),
    g.Item(250, 150, 45, 0, 45, 0),
    g.Item(250, 150, 45, 0, 0, 45),
    g.Item(250, 150, 0, 45, 45, 0)
    """

    result = []
    #['best_area', 'best_shortside', 'best_longside', 'worst_area', 'worst_shortside', 'worst_longside', 'bottom_left', 'contact_point']
    for heur in ['bottom_left']:
        for c in itertools.permutations(maximal):
            M = g.BinManager(700, 500, pack_algo='maximal_rectangle', heuristic=heur, rotation=False, sorting=False, wastemap=False)
            M.add_items(*list(c))
            M.execute()
            print(M.bins[0].bin_stats()['free_area'])
            #render_bin(M)
            result += [(M.bins[0].bin_stats(), M)]

    # select M with more efficiency
    best_bin = max(result, key=lambda x: x[0]['efficiency'])
    render_bin(best_bin[1], save=True)

    """
    g.Item(300, 150, 0, 90, 0, 90), g.Item(270, 150, 0, 90, 0, 90), g.Item(250, 150, 0, 90, 0, 90),
    g.Item(300, 150, 90, 0, 90, 0), g.Item(270, 150, 90, 0, 90, 0), g.Item(250, 150, 90, 0, 90, 0),
    g.Item(150, 300, 0, 90, 0, 90), g.Item(150, 270, 0, 90, 0, 90), g.Item(150, 250, 0, 90, 0, 90),
    g.Item(150, 300, 90, 0, 90, 0), g.Item(150, 270, 90, 0, 90, 0), g.Item(150, 250, 90, 0, 90, 0),

    g.Item(300, 150, 0, 90, 0, 90), g.Item(270, 150, 0, 90, 0, 90), g.Item(250, 150, 0, 90, 0, 90),
    g.Item(300, 150, 90, 0, 90, 0), g.Item(270, 150, 90, 0, 90, 0), g.Item(250, 150, 90, 0, 90, 0),
    g.Item(150, 300, 0, 90, 0, 90), g.Item(150, 270, 0, 90, 0, 90), g.Item(150, 250, 0, 90, 0, 90),
    g.Item(150, 300, 90, 0, 90, 0), g.Item(150, 270, 90, 0, 90, 0), g.Item(150, 250, 90, 0, 90, 0),
    g.Item(300, 150, 0, 90, 0, 90), g.Item(270, 150, 0, 90, 0, 90), g.Item(250, 150, 0, 90, 0, 90),
    g.Item(300, 150, 90, 0, 90, 0), g.Item(270, 150, 90, 0, 90, 0), g.Item(250, 150, 90, 0, 90, 0),
    g.Item(150, 300, 0, 90, 0, 90), g.Item(150, 270, 0, 90, 0, 90), g.Item(150, 250, 0, 90, 0, 90),
    g.Item(150, 300, 90, 0, 90, 0), g.Item(150, 270, 90, 0, 90, 0), g.Item(150, 250, 90, 0, 90, 0),


    #g.Item(300, 150, 0, 90, 0, 90), g.Item(270, 150, 0, 90, 0, 90), g.Item(250, 150, 0, 90, 0, 90),
    #g.Item(300, 150, 0, 90, 0, 90), g.Item(270, 150, 0, 90, 0, 90), g.Item(250, 150, 0, 90, 0, 90),
    #g.Item(300, 150, 0, 90, 0, 90), g.Item(270, 150, 0, 90, 0, 90), g.Item(250, 150, 0, 90, 0, 90),
    #g.Item(300, 150, 0, 90, 0, 90), g.Item(270, 150, 0, 90, 0, 90), g.Item(250, 150, 0, 90, 0, 90),
    #g.Item(300, 150, 0, 90, 0, 90), g.Item(270, 150, 0, 90, 0, 90), g.Item(250, 150, 0, 90, 0, 90),
    """
