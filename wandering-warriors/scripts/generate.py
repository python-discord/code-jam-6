from pathlib import Path
from PIL import Image

IMAGE_DIR = Path('.') / 'assets' / 'graphics'
GENERATED_DIR = IMAGE_DIR / 'cuneiform'

ONE = Image.open(IMAGE_DIR / 'cuneiform_one.png')
TEN = Image.open(IMAGE_DIR / 'cuneiform_ten.png')


# quick helper
def blank_image_gen():
    return Image.new('RGBA', (300, 300), (255, 255, 255, 0))

# now finally start generating


# blank
blank_image_gen().save(GENERATED_DIR / 'c0.png')

# one
out = blank_image_gen()
out.paste(ONE, (100, 100), mask=ONE)
out.save(GENERATED_DIR / 'c1.png')

# two
out = blank_image_gen()
[out.paste(ONE, (50 + 100 * i, 100), mask=ONE) for i in range(2)]
out.save(GENERATED_DIR / 'c2.png')

# three
out = blank_image_gen()
[out.paste(ONE, (100 * i, 100), mask=ONE) for i in range(3)]
out.save(GENERATED_DIR / 'c3.png')

# four
out = blank_image_gen()
[out.paste(ONE, (100 * i, 50), mask=ONE) for i in range(3)]
out.paste(ONE, (100, 150), mask=ONE)
out.save(GENERATED_DIR / 'c4.png')

# five
out = blank_image_gen()
[out.paste(ONE, (100 * i, 50), mask=ONE) for i in range(3)]
[out.paste(ONE, (50 + 100 * i, 150), mask=ONE) for i in range(2)]
out.save(GENERATED_DIR / 'c5.png')

# six
out = blank_image_gen()
for i in range(3):
    for j in range(2):
        out.paste(ONE, (100 * i, 100 * j + 50), mask=ONE)
out.save(GENERATED_DIR / 'c6.png')

# seven
out = blank_image_gen()
for i in range(3):
    for j in range(3):
        out.paste(ONE, (100 * i, 100 * j), mask=ONE)
out.paste(ONE, (100, 200), mask=ONE)
out.save(GENERATED_DIR / 'c7.png')

# eight
out = blank_image_gen()
for i in range(3):
    for j in range(3):
        out.paste(ONE, (100 * i, 100 * j), mask=ONE)
[out.paste(ONE, (50 + 100 * i, 200)) for i in range(2)]
out.save(GENERATED_DIR / 'c8.png')

# nine
out = blank_image_gen()
for i in range(3):
    for j in range(3):
        out.paste(ONE, (100 * i, 100 * j), mask=ONE)
out.save(GENERATED_DIR / 'c9.png')

# ten
out = blank_image_gen()
out.paste(TEN, (100, 100), mask=TEN)
out.save(GENERATED_DIR / 'c10.png')

# twenty
out = blank_image_gen()
out.paste(TEN, (25, 100), mask=TEN)
out.paste(TEN, (150, 0), mask=TEN)
out.save(GENERATED_DIR / 'c20.png')

# thirty
out = blank_image_gen()
out.paste(TEN, (25, 100), mask=TEN)
out.paste(TEN, (150, 0), mask=TEN)
out.paste(TEN, (150, 200), mask=TEN)
out.save(GENERATED_DIR / 'c30.png')

# forty
out = blank_image_gen()
out.paste(TEN, (25, 100), mask=TEN)
out.paste(TEN, (100, 50), mask=TEN)
out.paste(TEN, (100, 150), mask=TEN)
out.paste(TEN, (200, 0), mask=TEN)
out.save(GENERATED_DIR / 'c40.png')

# fifty
out = blank_image_gen()
out.paste(TEN, (25, 100), mask=TEN)
out.paste(TEN, (100, 50), mask=TEN)
out.paste(TEN, (100, 150), mask=TEN)
out.paste(TEN, (200, 0), mask=TEN)
out.paste(TEN, (200, 100), mask=TEN)
out.save(GENERATED_DIR / 'c50.png')
