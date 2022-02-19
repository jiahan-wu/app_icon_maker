import argparse
import json
import os

from PIL import Image

formats = [
    ("iPhone Notification iOS 7 - 14 20pt_2x", (40, 40), 'iphone', '2x', '20x20'),
    ("iPhone Notification iOS 7 - 14 20pt_3x", (60, 60), 'iphone', '3x', '20x20'),

    ("iPhone Settings iOS 7 - 14 29pt_2x", (58, 58), 'iphone', '2x', '29x29'),
    ("iPhone Settings iOS 7 - 14 29pt_3x", (87, 87), 'iphone', '3x', '29x29'),

    ("iPhone Spotlight iOS 7 - 14 40pt_2x", (80, 80), 'iphone', '2x', '40x40'),
    ("iPhone Spotlight iOS 7 - 14 40pt_3x", (120, 120), 'iphone', '3x', '40x40'),

    ("iPhone App iOS 7 - 14 60pt_2x", (120, 120), 'iphone', '2x', '60x60'),
    ("iPhone App iOS 7 - 14 60pt_3x", (180, 180), 'iphone', '3x', '60x60'),

    ("iPad Notification iOS 7 - 14 20pt_1x", (20, 20), 'ipad', '1x', '20x20'),
    ("iPad Notification iOS 7 - 14 20pt_2x", (40, 40), 'ipad', '2x', '20x20'),

    ("iPad Settings iOS 7 - 14 29pt_1x", (29, 29), 'ipad', '1x', '29x29'),
    ("iPad Settings iOS 7 - 14 29pt_2x", (58, 58), 'ipad', '2x', '29x29'),

    ("iPad Spotlight iOS 7 - 14 40pt_1x", (40, 40), 'ipad', '1x', '40x40'),
    ("iPad Spotlight iOS 7 - 14 40pt_2x", (80, 80), 'ipad', '2x', '40x40'),

    ("iPad App iOS 7 - 14 76pt_1x", (76, 76), 'ipad', '1x', '76x76'),
    ("iPad App iOS 7 - 14 76pt_2x", (152, 152), 'ipad', '2x', '76x76'),

    ("iPad (12.9-inch) App iOS 9 - 14 83.5pt_2x", (167, 167), 'ipad', '2x', '83.5x83.5'),

    ("App Store iOS 1024pt_1x", (1024, 1024), 'ios-marketing', '1x', '1024x1024')
]


def make(input, output):
    with Image.open(input) as image:
        if image.size != (1024, 1024):
            raise Exception("The image size must be 1024x1024.")

        metadata_bus = []

        for name, size, idiom, scale, size_class in formats:
            duplication = image.copy()

            duplication.thumbnail(size)

            file_name = f'{name}.' + f'{image.format}'.lower()
            file_path = os.path.join(output, file_name)
            duplication.save(file_path, image.format)

            metadata_bus.append({'filename': file_name, 'idiom': idiom, 'scale': scale, 'size': size_class})

        contents_json_data = {
            'images': metadata_bus,
            'info': {
                'author': 'xcode',
                'version': 1
            }
        }

        contents_json_file = os.path.join(output, 'Contents.json')
        with open(contents_json_file, 'w', encoding='utf-8') as file:
            json.dump(contents_json_data, file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='aim',
        usage='App Icon Maker will generate all required app icon sizes for iOS projects.')
    parser.add_argument('input')
    parser.add_argument('-o', '--output', default='./')

    args = parser.parse_args()
    
    make(args.input, args.output)
