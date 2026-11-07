
from client import count, _pretty_print
from matplotlib import pyplot
import numpy as np
import sys

# Return a random sample from Laplace with mean mu and scale b.
def laplace(mu, b):
    return np.random.laplace(mu, b)

# Return a noised histogram that is epsilon-DP.
def dp_histogram(epsilon):
    if epsilon <= 0:
        raise ValueError("Epsilon must be positive")

    # Each person contributes to exactly one histogram group.
    sensitivity = 1
    mu = 0
    b = sensitivity / epsilon

    # Get the original histogram.
    headers, rows = count(["age", "music"], False)

    noised_rows = []
    for age, music, value in rows:
        noise = laplace(mu, b)
        noised_value = int(round(value + noise))
        noised_rows.append((age, music, noised_value))

    return headers, noised_rows

# Plot the frequency of counts for the first group.
def plot(epsilon):
    ITERATIONS = 150
    d = {}

    for i in range(ITERATIONS):
        headers, rows = dp_histogram(epsilon)
        value = round(rows[0][-1])
        d[value] = d.get(value, 0) + 1

    vmin, vmax = min(d.keys()) - 3, max(d.keys()) + 3
    xs = list(range(vmin, vmax + 1))
    ys = [d.get(x, 0) / ITERATIONS for x in xs]

    pyplot.figure(figsize=(9, 5))
    pyplot.plot(xs, ys, 'o-', drawstyle='steps-mid')
    pyplot.xlabel("Count value")
    pyplot.ylabel("Frequency")
    pyplot.title(f"DP Histogram: epsilon = {epsilon}")
    pyplot.grid(alpha=0.3)
    pyplot.tight_layout()
    pyplot.savefig("dp-plot.png", dpi=200)
    pyplot.close()

if __name__ == "__main__":
    epsilon = 0.5
    if len(sys.argv) > 1:
        epsilon = float(sys.argv[1])

    print("Using epsilon =", epsilon)
    headers, rows = dp_histogram(epsilon)
    _pretty_print(headers, rows)

    print("Plotting...")
    plot(epsilon)
    print("Plot saved at 'dp-plot.png'")
