
from client import avg, count, count0, _pretty_print
from dp import dp_histogram

# This function estimates the original query results
# by averaging 200 differentially private outputs.
def expose(query_func):
    headers, many_results = None, []

    print("Making 200 queries with noise...")
    for i in range(200):
        headers, results = query_func()
        many_results.append(results)

    exposed_result = []
    num_iterations = len(many_results)
    rows = len(many_results[0])

    # Estimate each row's original value by averaging
    # the noisy values from all 200 queries.
    for r in range(rows):
        value = sum(
            result[r][-1] for result in many_results
        ) / num_iterations

        labels = tuple(many_results[0][r][:-1])
        exposed_result.append(labels + (value,))

    return headers, exposed_result


if __name__ == "__main__":

    # Part 1: Test the composition attack on our DP histogram.
    print("TESTING: The two histograms should be almost equal.\n")

    print("Non-noised histogram:")
    headers, result = count(["age", "music"], False)
    _pretty_print(headers, result)

    print("\nExposing histogram:")
    headers, result = expose(lambda: dp_histogram(0.5))
    _pretty_print(headers, result)

    # Question 9: Recover average age by programming experience.
    print("\nExposing average:")
    headers, result = expose(
        lambda: avg(["programming"], "age", True)
    )
    _pretty_print(headers, result)

    # Question 10: Recover counts by age group and programming level.
    print("\nExposing count:")
    headers, result = expose(
        lambda: count0(["agegroup", "programming"], True)
    )
    _pretty_print(headers, result)
