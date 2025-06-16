import matplotlib.pyplot as plt
import os
from dct2_performance.utils.constants import PLOT_PATH


class PerformancePlotter:
    def __init__(self, save_path=PLOT_PATH):
        self.save_path = save_path

    def save_performance_plot(self, sizes, times_custom, times_scipy):
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)

        plt.figure(figsize=(10, 6))
        plt.semilogy(sizes, times_custom, 'o-b', label='Custom DCT2', linewidth=2, markersize=6)
        plt.semilogy(sizes, times_scipy, 's-g', label='SciPy DCT2', linewidth=2, markersize=6)

        plt.xlabel('Matrix Size (N×N)')
        plt.ylabel('Execution Time [s]')
        plt.title('DCT2 Performance Comparison')
        plt.legend()
        plt.grid(True, which='both', linestyle='--', alpha=0.5)
        plt.tight_layout()

        plt.savefig(self.save_path, dpi=300)
        plt.close()
