import heapq
import time


class SearchResult:

    def __init__(
        self,
        path=None,
        cost=float("inf"),
        nodes_explored=0,
        elapsed=0.0
    ):

        self.path = path or []
        self.cost = cost
        self.nodes_explored = nodes_explored
        self.time = elapsed


class SearchEngine:

    def __init__(self, graph):
        self.graph = graph

    def _reconstruct_path(
        self,
        parent,
        start_state,
        goal_state
    ):

        states = []
        current = goal_state

        while current != start_state:

            states.append(current)
            current = parent[current]

        states.append(start_state)
        states.reverse()

        return [
            state[0]
            for state in states
        ]

    # ======================================================
    # GREEDY BEST-FIRST SEARCH
    # ======================================================

    def greedy_best_first(
        self,
        start,
        destination
    ):

        start_time = time.perf_counter()

        initial_mode = self.graph.initial_mode(start)

        start_state = (
            start,
            initial_mode
        )

        frontier = []

        counter = 0

        heapq.heappush(
            frontier,
            (
                self.graph.heuristic(
                    start,
                    destination
                ),
                counter,
                start_state
            )
        )

        parent = {}

        g_cost = {
            start_state: 0.0
        }

        visited = set()

        nodes_explored = 0

        while frontier:

            _, _, current_state = heapq.heappop(
                frontier
            )

            if current_state in visited:
                continue

            visited.add(current_state)

            current, mode = current_state

            nodes_explored += 1

            # Goal test
            if current == destination:

                path = self._reconstruct_path(
                    parent,
                    start_state,
                    current_state
                )

                elapsed = (
                    time.perf_counter()
                    - start_time
                )

                return SearchResult(
                    path,
                    g_cost[current_state],
                    nodes_explored,
                    elapsed
                )

            for (
                neighbor,
                weight,
                next_mode
            ) in self.graph.valid_neighbors(
                current,
                mode
            ):

                next_state = (
                    neighbor,
                    next_mode
                )

                if next_state in visited:
                    continue

                new_cost = (
                    g_cost[current_state]
                    + weight
                )

                if new_cost < g_cost.get(
                    next_state,
                    float("inf")
                ):

                    g_cost[next_state] = new_cost

                    parent[next_state] = (
                        current_state
                    )

                    counter += 1

                    h = self.graph.heuristic(
                        neighbor,
                        destination
                    )

                    heapq.heappush(
                        frontier,
                        (
                            h,
                            counter,
                            next_state
                        )
                    )

        elapsed = (
            time.perf_counter()
            - start_time
        )

        return SearchResult(
            [],
            float("inf"),
            nodes_explored,
            elapsed
        )

    # ======================================================
    # A* SEARCH
    # ======================================================

    def a_star(
        self,
        start,
        destination
    ):

        start_time = time.perf_counter()

        initial_mode = self.graph.initial_mode(start)

        start_state = (
            start,
            initial_mode
        )

        frontier = []

        counter = 0

        g_cost = {
            start_state: 0.0
        }

        parent = {}

        h = self.graph.heuristic(
            start,
            destination
        )

        heapq.heappush(
            frontier,
            (
                h,
                counter,
                start_state
            )
        )

        visited = set()

        nodes_explored = 0

        while frontier:

            _, _, current_state = heapq.heappop(
                frontier
            )

            if current_state in visited:
                continue

            visited.add(current_state)

            current, mode = current_state

            nodes_explored += 1

            # Goal test
            if current == destination:

                path = self._reconstruct_path(
                    parent,
                    start_state,
                    current_state
                )

                elapsed = (
                    time.perf_counter()
                    - start_time
                )

                return SearchResult(
                    path,
                    g_cost[current_state],
                    nodes_explored,
                    elapsed
                )

            for (
                neighbor,
                weight,
                next_mode
            ) in self.graph.valid_neighbors(
                current,
                mode
            ):

                next_state = (
                    neighbor,
                    next_mode
                )

                if next_state in visited:
                    continue

                tentative_g = (
                    g_cost[current_state]
                    + weight
                )

                if tentative_g < g_cost.get(
                    next_state,
                    float("inf")
                ):

                    g_cost[next_state] = tentative_g

                    parent[next_state] = (
                        current_state
                    )

                    counter += 1

                    h = self.graph.heuristic(
                        neighbor,
                        destination
                    )

                    f = tentative_g + h

                    heapq.heappush(
                        frontier,
                        (
                            f,
                            counter,
                            next_state
                        )
                    )

        elapsed = (
            time.perf_counter()
            - start_time
        )

        return SearchResult(
            [],
            float("inf"),
            nodes_explored,
            elapsed
        )