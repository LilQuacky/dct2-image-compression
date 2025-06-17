from dct2_performance.utils.functions import dct2_separable, dct2_scipy, test_correctness_scipy
from dct2_performance.utils.plotter import PerformancePlotter
from dct2_performance.utils.runner import DCTRunner


def main():
    """
    Main function to run the DCT2 performance benchmark.
    """
    #test_correctness_scipy()

    runner = DCTRunner(
        [dct2_separable, dct2_scipy],
        [8, 16, 32, 64, 128, 256, 512],
        "benchmark/"
    )
    log_file = runner.run()
    plotter = PerformancePlotter(log_file)
    plotter.save_performance_plot(dct2_scipy.__name__)


if __name__ == "__main__":
    main()
