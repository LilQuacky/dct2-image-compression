import os
import platform
import subprocess
import numpy as np

from scipy.fftpack import dctn, idctn
from tkinter import filedialog, Tk
from PIL import Image


def dct2(block):
    """
    Wrapper of scipy dctn function.
    """
    return dctn(block, type=2, norm='ortho')


def idct2(block):
    """
    Wrapper of scipy idctn function.
    """
    return idctn(block, type=2, norm='ortho')


def select_image():
    """
    Function to select an image.
    :return: path to the selected image
    """
    root = Tk()
    root.withdraw()
    return filedialog.askopenfilename(filetypes=[("Bitmap files", "*.bmp")])


def compress_image(img_array, F, d):
    """
    Function to compress an image using dct2.
    :param img_array: image to be compressed, in array format
    :param F: block dimension
    :param d: frequency cutoff threshold
    :return: compressed image in array format
    """
    h, w, c = img_array.shape
    h_blocks = h // F
    w_blocks = w // F

    compressed = np.zeros((h_blocks * F, w_blocks * F, c))

    for ch in range(c):
        for i in range(h_blocks):
            for j in range(w_blocks):
                block = img_array[i * F:(i + 1) * F, j * F:(j + 1) * F, ch]
                coeffs = dct2(block)

                for k in range(F):
                    for l in range(F):
                        if k + l >= d:
                            coeffs[k, l] = 0

                restored = idct2(coeffs)
                restored = np.round(restored)
                restored = np.clip(restored, 0, 255)
                compressed[i * F:(i + 1) * F, j * F:(j + 1) * F, ch] = restored

    return compressed.astype(np.uint8)


def save_compressed_image(compressed_img, out_path):
    """
    Function to save compressed image.
    :param compressed_img: compressed image in array format
    :param out_path: output path
    :return: abs path to the saved image
    """
    output_abs_path = os.path.abspath(out_path)

    Image.fromarray(compressed_img).save(output_abs_path)
    print(f"Image saved at: {output_abs_path}")

    return output_abs_path


def open_image(path):
    """
    Function to open an image.
    :param path: path to the image to open
    """
    try:
        # macOS
        if platform.system() == "Darwin":
            subprocess.run(["open", path])
        # Windows
        elif platform.system() == "Windows":
            os.startfile(path)
        # Linux
        else:
            subprocess.run(["xdg-open", path])
    except Exception as e:
        print(f"Error opening the image: {e}")


def dct2_compress(input_file, F, d, output_dir, show_img=True):
    """
    Function to start the compression process
    :param input_file: path to the input image
    :param F: block dimension
    :param d: frequency cutoff threshold
    :param output_dir: folder to save the plot_benchmark to
    :param show_img: to show an image comparison at the end of the script
    """
    img = Image.open(input_file)
    img_array = np.array(img)

    if len(img_array.shape) == 2:
        # Grayscale
        #img_array = img_array.astype(np.uint8)
        compressed_img = compress_image(np.expand_dims(img_array, axis=2), F, d)
        compressed_img = compressed_img[:, :, 0]
    else:
        # Color
        compressed_img = compress_image(img_array, F, d)

    img_name = os.path.splitext(os.path.basename(input_file))[0]
    compressed_img_name = f"{img_name}_compressed_F{F}_d{d}.bmp"

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, compressed_img_name)
    output_file = save_compressed_image(compressed_img, output_path)

    if show_img:
        open_image(input_file)
        open_image(output_file)


if __name__ == "__main__":
    print("Select a .BMP image")
    input_file = select_image()

    if not input_file:
        print("No image selected.")
        exit()

    F = int(input("Insert block dimension F: "))
    d = int(input(f"Insert frequency cutoff threshold d (0 <= d < {2 * F - 1}): "))

    dct2_compress(input_file, F, d, "output/")
