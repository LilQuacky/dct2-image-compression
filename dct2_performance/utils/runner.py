from typing import Collection, Callable

import numpy as np
import time

from dct2_performance.utils.CSVLogger import CSVLogger
from dct2_performance.utils.constants import ITERATIONS


class DCTRunner:
    """
    Class to easily run benchmarks on dct2 functions.
    """
    def __init__(self, functions: Collection[Callable], benchmark_sizes: Collection[int], logs_path: str = ".\\"):
        """
        DCTRunner constructor
        :param functions: list of callables to test
        :param benchmark_sizes: sizes to run the benchmark on
        :param logs_path: path to save the logs to
        """
        self.functions = functions
        self.benchmark_sizes = benchmark_sizes
        self.logger = CSVLogger("benchmark", logs_path)

    def run(self) -> str:
        """
        Method to start the benchmark procedure
        :return: path to the logs file
        """
        print("Starting benchmark...")

        results = {}
        for N in self.benchmark_sizes:
            results["size"] = N
            for func in self.functions:
                results[func.__name__] = self._run_single(func, N)

            self.logger.write_row(results)

        print("Benchmark completed.")

        return self.logger.log_file

    def _run_single(self, func: Callable, N: int) -> float:
        """
        Method to test a single function with a specified size
        :param func: callable to test
        :param N: size to test
        :return: total test time
        """
        print(f"Running function: {func.__name__} with size {N}")

        matrix = np.random.rand(N, N) * 255
        tot_time = 0

        for _ in range(ITERATIONS):
            start = time.perf_counter()
            func(matrix)
            end = time.perf_counter()

            tot_time += end - start

        return tot_time / ITERATIONS

