import csv


DEFAULT_PAIRS = [
    (
        "Reception of Calcutta University",
        "Library"
    ),
    (
        "Canteen, CU Technology Campus",
        "New Building 2 (Workshop Building)"
    ),
    (
        "Entry Gate 1",
        "CSE Laboratory"
    ),
    (
        "Auditorium Hall",
        "CSE_AKC Seminar Hall"
    ),
    (
        "Library",
        "Canteen, CU Technology Campus"
    )
]


class ExperimentRunner:

    def __init__(
        self,
        pathfinder,
        orbit
    ):

        self.pathfinder = pathfinder
        self.orbit = orbit
        self.results = []

    def run_pair(
        self,
        pair_number,
        start,
        destination
    ):

        agents = [
            self.pathfinder,
            self.orbit
        ]

        for agent in agents:

            result = agent.find_route(
                start,
                destination
            )

            if result.path:

                path = " -> ".join(
                    result.path
                )

                cost = round(
                    result.cost,
                    2
                )

            else:

                path = "NO VALID ROUTE"
                cost = "NO ROUTE"

            self.results.append(
                {
                    "pair": pair_number,
                    "agent": agent.name,
                    "source": start,
                    "destination": destination,
                    "path": path,
                    "cost": cost,
                    "nodes_explored": result.nodes_explored,
                    "time": round(
                        result.time,
                        6
                    )
                }
            )

    def run_default_experiments(self):

        self.results.clear()

        for index, (
            start,
            destination
        ) in enumerate(
            DEFAULT_PAIRS,
            start=1
        ):

            self.run_pair(
                index,
                start,
                destination
            )

        return self.results

    def save_csv(
        self,
        filename="results.csv"
    ):

        fields = [
            "pair",
            "agent",
            "source",
            "destination",
            "path",
            "cost",
            "nodes_explored",
            "time"
        ]

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fields
            )

            writer.writeheader()
            writer.writerows(
                self.results
            )

    def print_results(self):

        print(
            "\n"
            "============================================\n"
            "           ROUTE EXPERIMENT RESULTS\n"
            "============================================"
        )

        current_pair = None

        for row in self.results:

            if row["pair"] != current_pair:

                current_pair = row["pair"]

                print(
                    f"\nPair {current_pair}: "
                    f"{row['source']} -> "
                    f"{row['destination']}"
                )

            print(
                f"\n{row['agent']}"
            )

            print(
                f"Route: {row['path']}"
            )

            print(
                f"Cost: {row['cost']} m"
            )

            print(
                f"Nodes explored: "
                f"{row['nodes_explored']}"
            )

            print(
                f"Time: "
                f"{row['time']} s"
            )

    def summary(self):

        print(
            "\n"
            "============================================\n"
            "                 SUMMARY\n"
            "============================================"
        )

        for pair in range(
            1,
            len(DEFAULT_PAIRS) + 1
        ):

            rows = [
                row
                for row in self.results
                if row["pair"] == pair
            ]

            if len(rows) != 2:
                continue

            pathfinder = next(
                row
                for row in rows
                if row["agent"] == "PATHFINDER"
            )

            orbit = next(
                row
                for row in rows
                if row["agent"] == "ORBIT"
            )

            print(
                f"\nPair {pair}: "
                f"{pathfinder['source']} -> "
                f"{pathfinder['destination']}"
            )

            print(
                f"PATHFINDER cost: "
                f"{pathfinder['cost']}"
            )

            print(
                f"ORBIT cost: "
                f"{orbit['cost']}"
            )

            if (
                pathfinder["path"]
                != orbit["path"]
            ):

                print(
                    "Routes different: YES"
                )

            else:

                print(
                    "Routes different: NO"
                )