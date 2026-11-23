#!/usr/bin/env python3
"""Picture tools for the end-of-week update. Needs Pillow.

  media.py sheet OUT.png FILE...            numbered contact sheet, to look at many images at once
  media.py pair BEFORE AFTER -o OUT.png     one labelled before / after image
  media.py row A B C -o OUT.png --labels .. the versions of a test, or the steps of a flow, in one image
  media.py crop IN -o OUT --top 90          cut a tab bar or an internal label off an edge
"""

import argparse
import pathlib
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("media: Pillow is missing (pip install pillow)")

INK = (24, 27, 31)
MUTED = (104, 112, 122)
PAPER = (255, 255, 255)
RULE = (226, 229, 233)
BEFORE_CHIP = (104, 112, 122)
AFTER_CHIP = (22, 128, 78)
FONTS = (
    "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "C:/Windows/Fonts/arialbd.ttf",
    "DejaVuSans-Bold.ttf",
)


def font(size):
    for name in FONTS:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


def load(path):
    image = Image.open(path)
    if getattr(image, "is_animated", False):
        image.seek(0)
    image = image.convert("RGBA")
    flat = Image.new("RGB", image.size, PAPER)
    flat.paste(image, mask=image.split()[3])
    return flat


def fit(image, width=None, height=None):
    if width:
        ratio = width / image.width
    else:
        ratio = height / image.height
    size = (max(1, round(image.width * ratio)), max(1, round(image.height * ratio)))
    return image.resize(size, Image.LANCZOS)


def chip(draw, xy, text, fill, size):
    face = font(size)
    box = draw.textbbox((0, 0), text, font=face)
    pad_x, pad_y = round(size * 0.7), round(size * 0.38)
    width, height = box[2] - box[0] + 2 * pad_x, size + 2 * pad_y
    draw.rounded_rectangle((xy[0], xy[1], xy[0] + width, xy[1] + height), radius=height // 2, fill=fill)
    draw.text((xy[0] + pad_x, xy[1] + height / 2), text, font=face, fill=PAPER, anchor="lm")
    return height


def compose(images, labels, fills, args):
    """Lay labelled pictures out as one image: side by side, or stacked when they are wide."""
    layout = args.layout
    if layout == "auto":
        wide = min(image.width / image.height for image in images) >= 1.25
        layout = "stack" if wide else "side"

    pad, gap = 40, 32
    if layout == "side":
        height = min(max(image.height for image in images), 1500)
        images = [fit(image, height=height) for image in images]
        total = sum(image.width for image in images)
        limit = args.max_width - 2 * pad - gap * (len(images) - 1)
        if total > limit:
            height = round(height * limit / total)
            images = [fit(image, height=height) for image in images]
    else:
        width = min(max(image.width for image in images), args.max_width - 2 * pad)
        images = [fit(image, width=width) for image in images]

    span = sum(i.width for i in images) + gap * (len(images) - 1) if layout == "side" else images[0].width
    unit = min(44, max(20, round(span / 52)))
    chip_h = unit + 2 * round(unit * 0.38)
    title_h = round(unit * 2.3) if args.title else 0
    note_h = round(unit * 1.5) if args.note else 0
    head = chip_h + round(unit * 0.7)

    spots, x, y = [], pad, pad + title_h
    for image in images:
        spots.append((x, y))
        if layout == "side":
            x += image.width + gap
        else:
            y += head + image.height + gap
    if layout == "side":
        canvas_w = x - gap + pad
        canvas_h = 2 * pad + title_h + head + max(image.height for image in images) + note_h
    else:
        canvas_w = 2 * pad + images[0].width
        canvas_h = y - gap + pad + note_h

    canvas = Image.new("RGB", (canvas_w, canvas_h), PAPER)
    draw = ImageDraw.Draw(canvas)
    if args.title:
        draw.text((pad, pad - round(unit * 0.2)), args.title, font=font(round(unit * 1.25)), fill=INK)
    for (x, y), image, label, fill in zip(spots, images, labels, fills):
        chip(draw, (x, y), label.upper(), fill, unit)
        canvas.paste(image, (x, y + head))
        draw.rectangle((x - 1, y + head - 1, x + image.width, y + head + image.height), outline=RULE)
    if args.note:
        draw.text((pad, canvas_h - pad - round(unit * 0.1)), args.note, font=font(round(unit * 0.8)),
                  fill=MUTED, anchor="ls")

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, optimize=True)
    print(f"{out} {canvas_w}x{canvas_h} ({layout})")


def pair(args):
    compose([load(args.before), load(args.after)], args.labels, [BEFORE_CHIP, AFTER_CHIP], args)


def row(args):
    if len(args.labels) != len(args.files):
        sys.exit(f"media: {len(args.files)} pictures need {len(args.files)} labels")
    compose([load(name) for name in args.files], args.labels, [INK] * len(args.files), args)


def crop(args):
    """Cut a strip off an edge: a browser's tab bar, or an internal label on a render."""
    image = load(args.file)
    box = (args.left, args.top, image.width - args.right, image.height - args.bottom)
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    image.crop(box).save(out, optimize=True, quality=92)
    print(f"{out} {box[2] - box[0]}x{box[3] - box[1]}")


def sheet(args):
    cell_w, cell_h, pad, label_h, per_sheet = 560, 400, 16, 44, args.per_sheet
    files = [pathlib.Path(name) for name in args.files]
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    pages = [files[i:i + per_sheet] for i in range(0, len(files), per_sheet)]
    number = args.start
    for page_index, page in enumerate(pages, 1):
        cols = min(args.cols, len(page))
        rows = -(-len(page) // cols)
        canvas = Image.new("RGB", (pad + cols * (cell_w + pad), pad + rows * (cell_h + label_h + pad)),
                           (243, 244, 246))
        draw = ImageDraw.Draw(canvas)
        for index, path in enumerate(page):
            x = pad + (index % cols) * (cell_w + pad)
            y = pad + (index // cols) * (cell_h + label_h + pad)
            draw.rectangle((x, y, x + cell_w, y + cell_h + label_h), fill=PAPER)
            try:
                image = load(path)
                dims = f"{image.width}x{image.height}"
                image.thumbnail((cell_w, cell_h), Image.LANCZOS)
                canvas.paste(image, (x + (cell_w - image.width) // 2, y + (cell_h - image.height) // 2))
            except Exception:
                dims = "not an image"
                draw.text((x + cell_w / 2, y + cell_h / 2), "video or unreadable", font=font(22),
                          fill=MUTED, anchor="mm")
            chip(draw, (x + 8, y + 8), str(number), INK, 22)
            name = path.name if len(path.name) <= 44 else path.name[:20] + "..." + path.name[-21:]
            draw.text((x + 10, y + cell_h + label_h / 2), f"{name}  {dims}", font=font(16), fill=INK,
                      anchor="lm")
            print(f"{number}\t{path}")
            number += 1
        target = out if len(pages) == 1 else out.with_name(f"{out.stem}-{page_index}{out.suffix}")
        canvas.save(target, optimize=True)
        print(f"sheet: {target}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)

    one = commands.add_parser("pair", help="before / after in one image")
    one.add_argument("before")
    one.add_argument("after")
    one.add_argument("-o", "--out", required=True)
    one.add_argument("--labels", nargs=2, default=["Before", "After"])
    one.add_argument("--title", help="one line above the pictures, e.g. 'Collection filters'")
    one.add_argument("--note", help="small grey line under the pictures")
    one.add_argument("--layout", choices=("auto", "side", "stack"), default="auto",
                     help="auto stacks wide desktop shots and sets tall phone shots side by side")
    one.add_argument("--max-width", type=int, default=2400)
    one.set_defaults(run=pair)

    some = commands.add_parser("row", help="two to four labelled pictures in one image")
    some.add_argument("files", nargs="+")
    some.add_argument("-o", "--out", required=True)
    some.add_argument("--labels", nargs="+", required=True, help="one label per picture")
    some.add_argument("--title")
    some.add_argument("--note")
    some.add_argument("--layout", choices=("auto", "side", "stack"), default="auto")
    some.add_argument("--max-width", type=int, default=2400)
    some.set_defaults(run=row)

    cut = commands.add_parser("crop", help="cut pixels off the edges of one picture")
    cut.add_argument("file")
    cut.add_argument("-o", "--out", required=True)
    for edge in ("top", "bottom", "left", "right"):
        cut.add_argument(f"--{edge}", type=int, default=0)
    cut.set_defaults(run=crop)

    many = commands.add_parser("sheet", help="numbered thumbnails of many images")
    many.add_argument("out")
    many.add_argument("files", nargs="+")
    many.add_argument("--cols", type=int, default=4)
    many.add_argument("--per-sheet", type=int, default=16)
    many.add_argument("--start", type=int, default=1)
    many.set_defaults(run=sheet)

    args = parser.parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
