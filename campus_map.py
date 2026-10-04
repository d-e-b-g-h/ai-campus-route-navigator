import json
import math
from pathlib import Path


class CampusGraph:

    CSE_ZONE = {
        "CSE Laboratory",
        "CSE_AKC Seminar Hall",
        "CSE_Reflxon Room"
    }

    TOWER_ENTRIES = {
        "Tower 2 Front Entry",
        "Tower 2 Rear Entry"
    }

    LIFT = "Lift Area"

    def __init__(self, data):
        self.nodes = data["nodes"]
        self.adjacency = {
            node: []
            for node in self.nodes
        }

        for edge in data["edges"]:
            a, b, weight = edge

            self.adjacency[a].append(
                (b, float(weight))
            )

            self.adjacency[b].append(
                (a, float(weight))
            )

    @classmethod
    def from_json(cls, filename="campus.json"):

        path = Path(filename)

        with path.open(
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        return cls(data)

    def neighbors(self, node):
        return self.adjacency[node]

    def heuristic(self, node, destination):
        """
        Euclidean distance between the stored coordinates.
        """

        x1 = self.nodes[node]["x"]
        y1 = self.nodes[node]["y"]

        x2 = self.nodes[destination]["x"]
        y2 = self.nodes[destination]["y"]

        return math.sqrt(
            (x1 - x2) ** 2 +
            (y1 - y2) ** 2
        )

    def initial_mode(self, start):
        """
        Determine the initial routing mode.

        normal:
            Ordinary campus routing.

        cse:
            Start inside the CSE zone.

        exit:
            Not normally used at the beginning.
        """

        if start in self.CSE_ZONE:
            return "cse"

        return "normal"

    def transition_mode(
        self,
        current,
        neighbor,
        mode
    ):
        """
        Apply the special CSE routing rule.

        normal:
            Normal campus movement.
            CSE can only be entered from Lift Area.

        cse:
            Only CSE locations or Lift Area can be visited.

        exit:
            After leaving the CSE zone through Lift Area,
            the route must go through Tower 2 Front/Rear
            Entry before reaching other campus locations.
        """

        # --------------------------------------------------
        # MODE: CSE
        # --------------------------------------------------

        if mode == "cse":

            # Movement inside CSE is allowed.
            if neighbor in self.CSE_ZONE:
                return "cse"

            # CSE -> Lift is the only exit.
            if neighbor == self.LIFT:
                return "exit"

            return None

        # --------------------------------------------------
        # MODE: EXIT
        # --------------------------------------------------

        if mode == "exit":

            # After leaving CSE at Lift,
            # only Tower 2 entries are allowed.
            if (
                current == self.LIFT
                and neighbor in self.TOWER_ENTRIES
            ):
                return "normal"

            return None

        # --------------------------------------------------
        # MODE: NORMAL
        # --------------------------------------------------

        if mode == "normal":

            # CSE can only be entered from Lift Area.
            if neighbor in self.CSE_ZONE:

                if current == self.LIFT:
                    return "cse"

                return None

            return "normal"

        return None

    def valid_neighbors(
        self,
        current,
        mode
    ):
        """
        Return valid neighbors while respecting
        the CSE routing constraint.
        """

        valid = []

        for neighbor, weight in self.neighbors(current):

            next_mode = self.transition_mode(
                current,
                neighbor,
                mode
            )

            if next_mode is not None:
                valid.append(
                    (
                        neighbor,
                        weight,
                        next_mode
                    )
                )

        return valid