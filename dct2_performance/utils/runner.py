import numpy as np
from scipy.fft import dctn
import time
import os
import csv

from dct2_performance.utils.constants import (
    TEST_BLOCK, EXPECTED_DCT2, EXPECTED_DCT1D, TOLERANCE, BENCHMARK_PATH,
    SCIPY_ITERATIONS, SEPARABLE_ITERATIONS, BENCHMARK_SIZES
)


class DCTRunner:
    def __init__(self):
        pass

    def dct1d_custom(self, signal: np.ndarray) -> np.ndarray:
        N = len(signal)
        result = np.zeros(N)

        def alpha(u): return 1 / np.sqrt(2) if u == 0 else 1

        for u in range(N):
            sum_val = sum(signal[x] * np.cos((2 * x + 1) * u * np.pi / (2 * N)) for x in range(N))
            result[u] = np.sqrt(2 / N) * alpha(u) * sum_val
        return result

    def dct2_separable(self, image: np.ndarray) -> np.ndarray:
        rows_dct = np.apply_along_axis(self.dct1d_custom, axis=1, arr=image)
        return np.apply_along_axis(self.dct1d_custom, axis=0, arr=rows_dct)

    def dct2_scipy(self, image: np.ndarray) -> np.ndarray:
        return dctn(image, type=2, norm='ortho')

    def test_correctness(self):
        scipy_result = self.dct2_scipy(TEST_BLOCK.astype(float))
        max_err_dct2 = np.max(np.abs(scipy_result - EXPECTED_DCT2))
        assert max_err_dct2 < TOLERANCE, f"DCT2 max error {max_err_dct2:.2f} exceeds tolerance"

        row_result = dctn(TEST_BLOCK[0, :].astype(float), type=2, norm='ortho')
        max_err_dct1 = np.max(np.abs(row_result - EXPECTED_DCT1D))
        assert max_err_dct1 < TOLERANCE, f"DCT1D max error {max_err_dct1:.2f} exceeds tolerance"

    def benchmark_algorithms(self):
        print("Starting benchmark...")
        results = []
        for N in BENCHMARK_SIZES:
            matrix = np.random.rand(N, N) * 255

            start = time.time()
            for _ in range(SEPARABLE_ITERATIONS):
                _ = self.dct2_separable(matrix)
            t_custom = (time.time() - start) / SEPARABLE_ITERATIONS

            start = time.time()
            for _ in range(SCIPY_ITERATIONS):
                _ = self.dct2_scipy(matrix)
            t_scipy = (time.time() - start) / SCIPY_ITERATIONS

            results.append((N, t_custom, t_scipy))
        print("Benchmark completed.")
        return results

    def save_benchmark_csv(self, results, path=BENCHMARK_PATH):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Size", "Custom Time (s)", "SciPy Time (s)", "Speedup"])
            for N, t_custom, t_scipy in results:
                writer.writerow([N, t_custom, t_scipy, round(t_custom / t_scipy, 2)])
