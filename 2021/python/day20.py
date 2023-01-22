import sys

import numpy as np

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


def enhance(
    image: np.ndarray, background_value: int, lookup: list[int]
) -> tuple[np.ndarray, int]:
    # Output image will be larger than input image by 1 on all sides, since kernel is 3x3.
    output_image = np.zeros((image.shape[0] + 2, image.shape[1] + 2), image.dtype)

    # We will need to access the input image up to 2 past its bounds, so create a padded input for convenience.
    image_padded = np.pad(image, 2, mode="constant", constant_values=background_value)

    for row in range(output_image.shape[0]):
        for col in range(output_image.shape[1]):
            input_region = image_padded[row : row + 3, col : col + 3]
            input_flat = input_region.flatten()
            binary_str = "".join(str(x) for x in input_flat)
            int_value = int(binary_str, 2)
            output_image[row, col] = lookup[int_value]

    output_background_value = lookup[int(str(background_value) * 9, 2)]

    return output_image, output_background_value


def part1_and_2():
    # Load data, but convert ./# to 0/1.
    lookup = lines[0]
    lookup = [0 if x == "." else 1 for x in lookup]

    image = []
    for line in lines[2:]:
        image.append([0 if x == "." else 1 for x in line])
    image = np.array(image)
    background_value = 0

    image, background_value = enhance(image, background_value, lookup)
    image, background_value = enhance(image, background_value, lookup)

    print(np.count_nonzero(image))

    for _ in range(48):
        image, background_value = enhance(image, background_value, lookup)

    print(np.count_nonzero(image))


part1_and_2()
