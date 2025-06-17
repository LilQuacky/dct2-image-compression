from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

from dct2_performance.utils.constants import PLOT_PATH


class PerformancePlotter:
    """
    Class to plot the performance of DCT2 functions based on logged data.
    """
    def __init__(self, log_file: str, save_path: str = PLOT_PATH) -> None:
        """
        PerformancePlotter constructor.
        :param log_file: Path to the log file containing benchmark data
        :param save_path: Path to save the performance plot
        """
        self.log_file = log_file
        self.save_path = save_path

    def save_performance_plot(self, func_to_norm: Optional[str] = None):
        """
        Method to save the performance plot based on the logged data.
        :param func_to_norm: Function name to normalize the complexity curves against. If None, uses the first function.
        """
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)

        df = pd.read_csv(self.log_file)
        sizes = df['size'].values
        df.drop(columns=['size'], inplace=True)

        if not func_to_norm:
            func_to_norm = df.columns[0]

        n = sizes.astype(np.float64)
        n1 = n
        nlogn = n * np.log2(n)
        n2 = n ** 2
        n2logn = n ** 2 * np.log2(n)
        n3 = n ** 3

        # Normalize the complexity curves to the first value to match the scale of the plot
        n1_norm = n1 * (df[func_to_norm][0] / n1[0])
        nlogn_norm = nlogn * (df[func_to_norm][0] / nlogn[0])
        n2_norm = n2 * (df[func_to_norm][0] / n2[0])
        n2logn_norm = n2logn * (df[func_to_norm][0] / n2logn[0])
        n3_norm = n3 * (df[func_to_norm][0] / n3[0])
        
        """
        # Hardcoded section to normalize the first 5 functions based on scipy and the last one based on the custom function
        n1_norm = n1 * (df["dct2_scipy"][0] / n1[0])
        nlogn_norm = nlogn * (df["dct2_scipy"][0] / nlogn[0])
        n2_norm = n2 * (df["dct2_scipy"][0] / n2[0])
        n2logn_norm = n2logn * (df["dct2_scipy"][0] / n2logn[0])
        n3_norm = n3 * (df["dct2_separable"][0] / n3[0])
        """

        plt.figure(figsize=(10, 6))

        for func, time in df.items():
            plt.semilogy(sizes, time, label=func, linewidth=2, markersize=6)

        plt.semilogy(sizes, n1_norm, '--', color='gray', label=r'$\mathcal{O}(n)$')
        plt.semilogy(sizes, nlogn_norm, '--c', label=r'$\mathcal{O}(n \log n)$')
        plt.semilogy(sizes, n2_norm, '--', color='orange', label=r'$\mathcal{O}(n^2)$')
        plt.semilogy(sizes, n2logn_norm, '--m', label=r'$\mathcal{O}(n^2 \log n)$')
        plt.semilogy(sizes, n3_norm, '--r', label=r'$\mathcal{O}(n^3)$')

        plt.xlabel('Matrix Size (N×N)')
        plt.ylabel('Execution Time [s]')
        plt.title('DCT2 Performance Comparison')
        plt.legend()
        plt.grid(True, which='both', linestyle='--', alpha=0.5)
        plt.tight_layout()

        file_name = "plot_" + os.path.basename(self.log_file)[:-4] + ".png"
        full_path = os.path.join(self.save_path, file_name)
        plt.savefig(full_path, dpi=300)
        print(f"Plot saved at: {os.path.abspath(full_path)}")

        plt.close()
