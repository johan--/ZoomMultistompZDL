"""Generic capture covers, drawn at the pedal's native resolution."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src/airwindows/common'))
from screen_image import Canvas, encode_zoom_rle
from stock_style_covers import fill, line, round_shape, FONT
from pack_covers import word

def draw(kind):
    c = Canvas()
    c.rect(2, 1, 125, 63)
    fill(c, 5, 3, 122, 33)
    if kind == 'NAM':
        # Neural lattice: three columns of physically round nodes.
        nodes = [[(14, 12), (14, 25)], [(28, 8), (28, 18), (28, 28)], [(42, 12), (42, 25)]]
        for left, right in zip(nodes, nodes[1:]):
            for a in left:
                for b in right: line(c, a, b, 0)
        for column in nodes:
            for x, y in column:
                round_shape(c, x, y, 4, 0)
                round_shape(c, x, y, 2, 1)
        letters = dict(FONT, N=['10001','11001','11001','10101','10011','10011','10001'])
        for n, ch in enumerate('NAM'):
            for y, row in enumerate(letters[ch]):
                for x, bit in enumerate(row):
                    if bit == '1': fill(c,52+n*24+x*4,6+y*3,55+n*24+x*4,8+y*3,0)
        for x in range(57, 119, 5): c.px(x, 30, 0)
        labels = ['INPUT', 'OUTPUT', 'MIX']
    elif kind == 'IR':
        word(c, 'IR', 12, 7, sx=7, sy=4, v=0)
        c.hline(65, 117, 26, 0)
        # One strong impulse, followed by an irregular decaying response.
        for x, h in [(68,20),(72,12),(77,16),(82,11),(87,8),(92,10),(97,6),(102,4),(107,5),(112,2)]:
            c.vline(x, 26-h, 26, 0)
        line(c, (62, 5), (119, 5), 0)
        line(c, (114, 3), (119, 5), 0)
        line(c, (114, 7), (119, 5), 0)
        labels = ['CAB', 'MIX', 'LEVEL']      # CabIR 0.20 page 1
    else: raise ValueError(kind)
    for x, label in zip((24,65,106), labels):
        c.draw_text(label, x-(len(label)*4-1)//2, 37)
        round_shape(c,x,53,7)
        round_shape(c,x,53,5,0)
        c.vline(x,49,53)
    return c

def picture(kind):
    return encode_zoom_rle(draw(kind))
