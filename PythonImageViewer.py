import shutil
import argparse
import cv2
import glob

MODE_HEIGHT = "height"
MODE_STRETCH = "stretch"
MODE_WIDTH = "width"
CHARACTER_SCALE = 2


def main(args):

    paths = []
    for path in args.path:
        paths += glob.glob(path)

    for path in paths[:-1]:
        show(path, args.mode)
        input("")
        print("")
    else:
        show(paths[-1], args.mode)


def show(path: str, mode: str):
    terminal_size = shutil.get_terminal_size()
    columns = terminal_size.columns
    lines = terminal_size.lines - 3

    image = cv2.imread(path)
    if mode == MODE_HEIGHT:
        new_size = (
            int(CHARACTER_SCALE * lines * image.shape[1] / image.shape[0]),
            lines,
        )
    if mode == MODE_STRETCH:
        new_size = (columns, lines)
    if mode == MODE_WIDTH:
        new_size = (
            columns,
            int(columns * image.shape[0] / (CHARACTER_SCALE * image.shape[1])),
        )
    resized = cv2.resize(image, new_size)

    for line in resized:
        for pixel in line:
            print(
                f"\x1b[48;2;{pixel[2]};{pixel[1]};{pixel[0]}m\x1b[38;2;{pixel[2]};{pixel[1]};{pixel[0]}m\u2588\x1b[0m",
                end="",
            )
        print("")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Python Image Viewer")
    parser.add_argument("path", help="Path to image(s) to display", nargs="+")
    parser.add_argument(
        "-m",
        "--mode",
        help="Display Mode",
        choices=[MODE_HEIGHT, MODE_STRETCH, MODE_WIDTH],
        default="height",
    )
    main(parser.parse_args())
