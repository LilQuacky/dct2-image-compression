from dct2_performance.utils.runner import DCTRunner
from dct2_performance.utils.plotter import PerformancePlotter


def main():
    runner = DCTRunner()
    plotter = PerformancePlotter()

    try:
        runner.test_correctness()
        print("DCT correctness test passed.")
    except AssertionError as e:
        print(f"Correctness test failed: {e}")
        return

    results = runner.benchmark_algorithms()
    runner.save_benchmark_csv(results)

    sizes = [r[0] for r in results]
    times_custom = [r[1] for r in results]
    times_scipy = [r[2] for r in results]

    plotter.save_performance_plot(sizes, times_custom, times_scipy)

    print("Benchmark and plot saved successfully.")


if __name__ == "__main__":
    main()
