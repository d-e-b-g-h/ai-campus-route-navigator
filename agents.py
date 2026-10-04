from search import SearchEngine


class RoutingAgent:

    def __init__(
        self,
        name,
        algorithm,
        engine
    ):

        self.name = name
        self.algorithm = algorithm
        self.engine = engine

    def find_route(
        self,
        start,
        destination
    ):

        if self.algorithm == "greedy":

            return self.engine.greedy_best_first(
                start,
                destination
            )

        if self.algorithm == "astar":

            return self.engine.a_star(
                start,
                destination
            )

        raise ValueError(
            f"Unknown algorithm: {self.algorithm}"
        )


class Pathfinder(RoutingAgent):

    def __init__(self, engine):

        super().__init__(
            name="PATHFINDER",
            algorithm="greedy",
            engine=engine
        )


class Orbit(RoutingAgent):

    def __init__(self, engine):

        super().__init__(
            name="ORBIT",
            algorithm="astar",
            engine=engine
        )