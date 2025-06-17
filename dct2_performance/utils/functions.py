import numpy as np

from scipy.fft import dctn
from dct2_performance.utils import constants


def dct1d_custom(signal: np.ndarray) -> np.ndarray:
    N = len(signal)
    result = np.zeros(N)

    def alpha(u): return 1 / np.sqrt(2) if u == 0 else 1

    for u in range(N):
        sum_val = sum(signal[x] * np.cos((2 * x + 1) * u * np.pi / (2 * N)) for x in range(N))
        result[u] = np.sqrt(2 / N) * alpha(u) * sum_val
    return result


def dct2_separable(image: np.ndarray) -> np.ndarray:
    rows_dct = np.apply_along_axis(dct1d_custom, axis=1, arr=image)
    return np.apply_along_axis(dct1d_custom, axis=0, arr=rows_dct)


def dct2_scipy(image: np.ndarray) -> np.ndarray:
    return dctn(image, type=2, norm='ortho')


def test_correctness_scipy() -> None:
    scipy_result = dct2_scipy(constants.TEST_BLOCK.astype(float))
    max_err_dct2 = np.max(np.abs(scipy_result - constants.EXPECTED_DCT2))
    assert max_err_dct2 < constants.TOLERANCE, f"DCT2 max error {max_err_dct2:.2f} exceeds tolerance"

    row_result = dctn(constants.TEST_BLOCK[0, :].astype(float), type=2, norm='ortho')
    max_err_dct1 = np.max(np.abs(row_result - constants.EXPECTED_DCT1D))
    assert max_err_dct1 < constants.TOLERANCE, f"DCT1D max error {max_err_dct1:.2f} exceeds tolerance"