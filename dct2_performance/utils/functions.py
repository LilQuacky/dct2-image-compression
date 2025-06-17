import numpy as np

from scipy.fft import dctn
from dct2_performance.utils import constants


def dct1d_custom(signal: np.ndarray) -> np.ndarray:
    """
    Custom implementation of the 1D Discrete Cosine Transform (DCT Type II).
    :param signal: Input signal (1D array)
    :return: Transformed signal (1D array)
    """
    N = len(signal)
    result = np.zeros(N)

    def alpha(u): return 1 / np.sqrt(2) if u == 0 else 1

    for u in range(N):
        sum_val = sum(signal[x] * np.cos((2 * x + 1) * u * np.pi / (2 * N)) for x in range(N))
        result[u] = np.sqrt(2 / N) * alpha(u) * sum_val
    return result


def dct2_separable(image: np.ndarray) -> np.ndarray:
    """
    Custom implementation of the 2D Discrete Cosine Transform (DCT Type II) using separable DCT.
    :param image: Input image (2D array)
    :return: Transformed image (2D array)
    """
    rows_dct = np.apply_along_axis(dct1d_custom, axis=1, arr=image)
    return np.apply_along_axis(dct1d_custom, axis=0, arr=rows_dct)


def dct2_scipy(image: np.ndarray) -> np.ndarray:
    """
    Wrapper for the scipy's dctn function to compute the 2D DCT Type II.
    :param image: Input image (2D array)
    :return: Transformed image (2D array)
    """
    return dctn(image, type=2, norm='ortho')


def test_correctness_scipy() -> None:
    """
    Test to verify the correctness of the DCT2 implementation against scipy's dctn.
    """
    scipy_result = dct2_scipy(constants.TEST_BLOCK.astype(float))
    print("Testing correctness of scipy's dctn for DCT Type II...\n")

    print("Expected values:")
    print(constants.EXPECTED_DCT2)
    print("\nActual values:")
    print(scipy_result)

    max_err_dct2 = np.max(np.abs(scipy_result - constants.EXPECTED_DCT2))
    assert max_err_dct2 < constants.TOLERANCE, f"DCT2 max error {max_err_dct2:.2f} exceeds tolerance"

    row_result = dctn(constants.TEST_BLOCK[0, :].astype(float), type=2, norm='ortho')

    print("\nExpected values:")
    print(constants.EXPECTED_DCT1D)
    print("\nActual values:")
    print(row_result)

    max_err_dct1 = np.max(np.abs(row_result - constants.EXPECTED_DCT1D))
    assert max_err_dct1 < constants.TOLERANCE, f"DCT1D max error {max_err_dct1:.2f} exceeds tolerance"
    print("\nCorrectness test passed for scipy's dctn DCT Type II implementation.\n")
