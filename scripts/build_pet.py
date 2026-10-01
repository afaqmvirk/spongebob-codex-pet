"""Rebuild the Spongey Boy v1 atlas from its prepared PNG frames."""

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CELL = (192,208)
SIZE = (1536,1872)
COUNTS = [6,8,8,4,5,8,6,6,6]


def main():
    mapping = json.loads((ROOT/'animation-mapping.json').read_text(encoding='utf-8'))
    assert len(mapping['rows'])==9
    atlas = Image.new('RGBA',SIZE,(0,0,0,0))
    for row in mapping['rows']:
        index = row['row']
        assert len(row['frames'])==COUNTS[index],row['state']
        for frame in row['frames']:
            path = ROOT/frame['frame_file']
            with Image.open(path) as source:
                image = source.convert('RGBA')
            assert image.size==CELL,f'{path}: expected 192 by 208 pixels'
            assert image.getbbox(),f'{path}: frame is empty'
            atlas.alpha_composite(image,(frame['column']*CELL[0],index*CELL[1]))
    # Remove hidden colour beneath fully transparent pixels.
    pixels = atlas.load()
    for y in range(atlas.height):
        for x in range(atlas.width):
            if pixels[x,y][3]==0:
                pixels[x,y]=(0,0,0,0)
    atlas.save(ROOT/'spritesheet.png')
    atlas.save(ROOT/'spritesheet.webp',format='WEBP',lossless=True,quality=100,method=6,exact=True)
    with Image.open(ROOT/'spritesheet.webp') as decoded:
        assert decoded.convert('RGBA').tobytes()==atlas.tobytes(),'WebP round-trip changed pixels'
    print('Built spritesheet.png and spritesheet.webp from 57 prepared frames.')


if __name__=='__main__':
    main()
