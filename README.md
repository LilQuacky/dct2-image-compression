# DCT2 Image Compression

### Image compression using 2d Discrete Cosine Transform

> **University Project – Scientific Computing Methods**
> Authors: *Falbo Andrea*, *Tenderini Ruben*

## Table of Contents

* [Overview](#overview)
* [First Part](#first-part)

  * [Objective](#objective)
  * [Repository Structure](#repository-structure)
  * [Tools and Libraries](#tools-and-libraries)
  * [Methodology](#methodology)
  * [Run](#run)
* [Second Part](#second-part)

  * [Objective](#objective-1)
  * [Software Structure](#software-structure)
  * [Tools and Libraries](#tools-and-libraries-1)
  * [Methodology](#methodology-1)
  * [Run](#run-1)
  * [Example](#example)
  * [Results](#results)
* [Authors](#authors)
* [License](#license)

---

## Overview

This repository contains the code and materials developed for the **Scientific Computing Methods** course at **Università degli Studi Milano-Bicocca**.

The project is divided into two main parts:

* **First Part**: Manual implementation and benchmarking of the 2D Discrete Cosine Transform (DCT2).
* **Second Part**: Development of a block-based image compression tool using DCT2.

Full specifications and analysis are available in [`report.pdf`](./report.pdf) (in Italian).

---

## First Part

### Objective

In this phase, we:

* Implemented the 2D Discrete Cosine Transform (DCT2) from scratch using the separable method.
* Compared its performance with the fast DCT2 provided by SciPy (`scipy.fft.dctn`).
* Verified correctness against reference data.
* Plotted execution time vs matrix size on a semi-logarithmic scale.

Expected theoretical complexities:

* **Custom DCT2**: O(N³)
* **SciPy DCT2**: O(N² log N)

### Repository Structure

```
dct2_performance/
├── main.py                <- Entry point for performance analysis
├── utils/
│   ├── constants.py       <- Test data and config
|   |── CSVLogger.py       <- CSV logging utility     
│   ├── plotter.py         <- Plot generation utility
│   └── runner.py          <- Benchmark runner
├── benchmark/             <- Output CSV results
└── plot_benchmark/        <- Performance plots
```

### Tools and Libraries

* **Python**: 3.11.11
* **Main libraries**:

  * `numpy`
  * `scipy` (version ≥ 1.15.2)
  * `matplotlib`

### Methodology

* The **custom DCT2** was implemented using a 1D DCT formula applied row-wise and column-wise.
* The **fast DCT2** used `scipy.fft.dctn` with `type=2` and `norm='ortho'`.
* Benchmarks were run over square matrices with increasing size, averaged over multiple iterations.
* Results were saved in CSV and visualized as log-scaled performance plots.

See details in [`report.pdf`](./report.pdf), Section 2.

### Run

1. **Clone the repository**

   ```bash
   git clone https://github.com/LilQuacky/dct2-image-compression
   cd dct2-image-compression/dct2_performance
   ```

2. **Install dependencies**

   ```bash
   pip install numpy scipy matplotlib pandas
   ```

3. **Run the performance benchmark**

   ```bash
   python main.py
   ```

### Results

Experimental results (detailed in [`report.pdf`](./report.pdf), Chapter 2):

* The manual DCT2 has a complexity of O(N³) confirmed empirically. For 2048×2048 matrices, execution time exceeded 5 hours, making it impractical to go further.
* The fast DCT2 provided by `scipy.fft.dctn` was tested up to 32768×32768 matrices, showing consistent growth with O(N² log N) complexity.
* A test with sizes up to 65536×65536 and higher powers of 2 was attempted but was blocked by system memory limits (32 GB RAM).


---

## Second Part

### Objective

Build a minimal interactive tool that compresses BMP images by removing high-frequency DCT coefficients within macro-blocks. The user can adjust:

* **Block size `F`** (macro-blocks of F×F)
* **Frequency threshold `d`** (coefficients where `k + l ≥ d` are zeroed out)

The compressed image is displayed alongside the original.

### Software Structure

```
compression_tool/
├── main.py         <- Image processing logic
└── gui.py          <- Tkinter-based user interface
```

### Tools and Libraries

* **Python**: 3.11.11
* **Libraries**:

  * `numpy`, `scipy` (DCT2/IDCT2)
  * `Pillow` (image I/O)
  * `tkinter` (GUI)

### Methodology

1. **Image Input**: User selects a grayscale `.bmp` image.
2. **Block Division**: Image is split into blocks of size `F × F`.
3. **DCT2 Application**: For each block, apply DCT2 using `scipy.fftpack.dctn`.
4. **Frequency Cutoff**: Zero coefficients where `k + l ≥ d`.
5. **IDCT2**: Apply inverse DCT2, round and clip values to \[0, 255].
6. **Rebuild Image**: Assemble modified blocks back into an image.
7. **Visualization**: Original and compressed images are opened for comparison.

### Run

1. **Clone the repository**

   ```bash
   git clone https://github.com/LilQuacky/dct2-image-compression
   cd dct2-image-compression/compression_tool
   ```

2. **Install dependencies**

   ```bash
   pip install numpy scipy tkinter Pillow
   ```

3.  **GUI Mode**

```bash
python gui.py
```

Use the interface to:

* Select a BMP image
* Set block size (F) and threshold (d)
* Choose output folder

4. **CLI Mode**

```bash
python main.py
```

You will be prompted to enter values in the terminal.

### Example

* **F = 8**, **d = 10**: Retains more detail, mild compression
* **F = 32**, **d = 5**: Higher compression, lower image quality

### Results

Experimental results (detailed in [`report.pdf`](./report.pdf), Chapter 3):

* **Images with low-frequency content** (e.g., gradients) are compressed well with minimal quality loss.
* **High-frequency patterns** (e.g., checkerboards) show visible artifacts with small `d`.
* **Real images** (e.g., cathedral) require higher `d` to retain details.

---

## Authors

* [**Falbo Andrea**](https://github.com/LilQuacky)
* [**Tenderini Ruben**](https://github.com/Ruben-2828)

---

## License

This project is licensed under the MIT License – see the [LICENSE](./LICENSE) file for details.
