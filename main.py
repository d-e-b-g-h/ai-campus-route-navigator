from campus_map import CampusGraph
from search import SearchEngine
from agents import Pathfinder, Orbit
from experiment import ExperimentRunner


BANNER = """

========================================================
              AI CAMPUS ROUTE NAVIGATOR
========================================================

PATHFINDER  -> Greedy Best-First Search
ORBIT       -> A* Search

========================================================
"""


def display_result(
    agent,
    result
):

    print(
        f"\n{agent.name}"
    )

    if not result.path:

        print(
            "Route: NO VALID ROUTE"
        )

        print(
            f"Nodes explored: "
            f"{result.nodes_explored}"
        )

        print(
            f"Time: "
            f"{result.time:.6f} s"
        )

        return

    print(
        "Route:"
    )

    print(
        " -> ".join(
            result.path
        )
    )

    print(
        f"Cost: "
        f"{result.cost:.2f} m"
    )

    print(
        f"Nodes explored: "
        f"{result.nodes_explored}"
    )

    print(
        f"Time: "
        f"{result.time:.6f} s"
    )


def choose_location(
    graph,
    prompt
):

    while True:

        value = input(
            prompt
        ).strip()

        if value in graph.nodes:

            return value

        print(
            "\nInvalid location."
        )

        print(
            "\nAvailable locations:"
        )

        for location in graph.nodes:

            print(
                f" - {location}"
            )


def main():

    print(BANNER)

    graph = CampusGraph.from_json(
        "campus.json"
    )

    engine = SearchEngine(
        graph
    )

    pathfinder = Pathfinder(
        engine
    )

    orbit = Orbit(
        engine
    )

    print(
        "1. Run predefined experiments"
    )

    print(
        "2. Enter custom source and destination"
    )

    choice = input(
        "\nChoose option: "
    ).strip()

    # --------------------------------------------------
    # EXPERIMENT MODE
    # --------------------------------------------------

    if choice == "1":

        experiment = ExperimentRunner(
            pathfinder,
            orbit
        )

        experiment.run_default_experiments()

        experiment.print_results()

        experiment.summary()

        experiment.save_csv(
            "results.csv"
        )

        print(
            "\nResults saved to results.csv"
        )

    # --------------------------------------------------
    # CUSTOM ROUTE MODE
    # --------------------------------------------------

    elif choice == "2":

        start = choose_location(
            graph,
            "\nEnter starting location: "
        )

        destination = choose_location(
            graph,
            "Enter destination: "
        )

        if start == destination:

            print(
                "\nSource and destination "
                "cannot be the same."
            )

            return

        print(
            "\n"
            "============================================"
        )

        print(
            f"\nRoute: "
            f"{start} -> {destination}"
        )

        print(
            "\n============================================"
        )

        pathfinder_result = (
            pathfinder.find_route(
                start,
                destination
            )
        )

        orbit_result = (
            orbit.find_route(
                start,
                destination
            )
        )

        display_result(
            pathfinder,
            pathfinder_result
        )

        display_result(
            orbit,
            orbit_result
        )

    else:

        print(
            "\nInvalid option."
        )


if __name__ == "__main__":
    main()