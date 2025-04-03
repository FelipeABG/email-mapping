from collections import defaultdict


class Graph:
    def __init__(self) -> None:
        self.size = 0
        self.order = 0
        # Each key is a node and each value is the list of the node adjacencies
        self.adj_list: dict[str, list[tuple[str, int]]] = defaultdict(list)

    def contains_node(self, label: str) -> bool:
        return label in self.adj_list

    def contains_edge(self, u: str, v: str) -> bool:
        if not self.contains_node(u):
            return False

        for tup in self.adj_list[u]:
            if tup[0] == v:
                return True

        return False

    def add_node(self, label: str) -> None:
        if self.contains_node(label):
            raise Exception("Node already in graph")

        self.adj_list[label] = list()
        self.order += 1

    def remove_node(self, label: str) -> None:
        if not self.contains_node(label):
            return

        self.adj_list.pop(label)
        self.order -= 1

        for node in self.adj_list:
            if self.contains_edge(node, label):
                self.remove_edge(node, label)

    def add_edge(self, u: str, v: str, weight: int) -> None:
        if weight < 0:
            raise Exception("Negative weight is not allowed")

        if not self.contains_node(u):
            self.add_node(u)
        if not self.contains_node(v):
            self.add_node(v)

        for idx, tup in enumerate(self.adj_list[u]):
            if tup[0] == v:
                self.adj_list[u][idx] = (v, weight)
                return

        self.adj_list[u].append((v, weight))
        self.size += 1

    def remove_edge(self, u: str, v: str) -> None:
        if not self.contains_node(u):
            raise Exception("Source node does not exist")

        for tup in self.adj_list[u]:
            if tup[0] == v:
                self.adj_list[u].remove(tup)
                self.size -= 1
                return

    def in_degree(self, label: str) -> int:
        if not self.contains_node(label):
            return 0

        degree = 0
        for node in self.adj_list:
            for tup in self.adj_list[node]:
                if tup[0] == label:
                    degree += 1

        return degree

    def out_degree(self, label: str) -> int:
        if not self.contains_node(label):
            return 0

        return len(self.adj_list[label])

    def degree(self, label: str) -> int:
        return self.in_degree(label) + self.out_degree(label)

    def get_weight(self, u: str, v: str) -> int:
        if not self.contains_edge(u, v):
            raise Exception("Edge between 2 nodes does not exist")

        for tup in self.adj_list[u]:
            if tup[0] == v:
                return tup[1]

        # This is unreacheable
        return 0

    def to_string(self) -> str:
        result = []
        for node, adjacencies in self.adj_list.items():
            adj_str = " -> ".join([f"({v}, {w})" for v, w in adjacencies])
            result.append(f"{node}: {adj_str} ->" if adjacencies else f"{node}:")
        return "\n".join(result)
