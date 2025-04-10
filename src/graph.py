from collections import defaultdict
import heapq


class Graph:
    def __init__(self) -> None:
        self.size = 0
        self.order = 0
        # Each key is a node and each value is the list of the node adj
        self.adj_list: dict[str, list[tuple[str, int]]] = defaultdict(list)

    def get_size(self) -> int:
        return self.size

    def get_order(self) -> int:
        return self.order

    def contains_node(self, name: str) -> bool:
        return name in self.adj_list

    def contains_edge(self, u: str, v: str) -> bool:
        if not self.contains_node(u):
            return False

        for tup in self.adj_list[u]:
            if tup[0] == v:
                return True

        return False

    def add_node(self, name: str) -> None:
        if self.contains_node(name):
            raise Exception("Node already in graph")

        self.adj_list[name] = list()
        self.order += 1

    def remove_node(self, name: str) -> None:
        if not self.contains_node(name):
            return

        self.adj_list.pop(name)
        self.order -= 1

        for node in self.adj_list:
            if self.contains_edge(node, name):
                self.remove_edge(node, name)

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

    def in_degree(self, name: str) -> int:
        if not self.contains_node(name):
            return 0

        degree = 0
        for node in self.adj_list:
            for tup in self.adj_list[node]:
                if tup[0] == name:
                    degree += 1

        return degree

    def out_degree(self, name: str) -> int:
        if not self.contains_node(name):
            return 0

        return len(self.adj_list[name])

    def degree(self, name: str) -> int:
        return self.in_degree(name) + self.out_degree(name)

    def get_weight(self, u: str, v: str) -> int:
        if not self.contains_edge(u, v):
            return 0

        for tup in self.adj_list[u]:
            if tup[0] == v:
                return tup[1]

        # This is unreacheable
        return 0

    def to_string(self) -> str:
        result = []
        for node, adj in self.adj_list.items():
            adj_str = " -> ".join([f"({v}, {w})" for v, w in adj])
            result.append(f"{node}: {adj_str} ->" if adj else f"{node}:")
        return "\n\n".join(result)

    def top_degrees(self) -> tuple[list[tuple[str, int]], list[tuple[str, int]]]:

        # Get the outdegree and indegree of all nodes in the graph
        in_degrees = [(node, self.in_degree(node)) for node in self.adj_list]
        out_degrees = [(node, self.out_degree(node)) for node in self.adj_list]

        # Sort them descending by degree
        in_degrees.sort(key=lambda x: x[1], reverse=True)
        out_degrees.sort(key=lambda x: x[1], reverse=True)

        return in_degrees[:20], out_degrees[:20]

    def dfs(self, start_node: str) -> list[str]:
        if not self.contains_node(start_node):
            raise Exception("Node does not exist in graph")

        # Step 1: add the starting node the the stack
        stack = [start_node]
        visited = []

        while len(stack) != 0:
            # Step 2: Removes a node from the stack
            current = stack.pop()

            # Step 3: Add node to visited list if not there
            if current not in visited:
                visited.append(current)

                # Sorting by alphabetic order
                adjacents = sorted(self.adj_list[current], key=lambda x: x[0])

                # Step 4: add non-visited neighbors to the stack
                for node, _ in adjacents:
                    if node not in visited:
                        stack.append(node)

        return visited

    def is_eulerian(self) -> tuple[bool, str]:
        error_msg = ""

        # Check if the indegree and outdegree is the same for all nodes
        for node in self.adj_list:
            indegree = self.in_degree(node)
            outdegree = self.out_degree(node)
            if indegree != outdegree:
                error_msg += "- At least one node where: indegree != outdegree\n"
                break

        # Check if the graph is strongly connected by `dfsing` all nodes
        for node in self.adj_list:
            if self.order != len(self.dfs(node)):
                error_msg += "- The graph is not strongly conected\n"
                break

        if error_msg == "":
            return (True, error_msg)

        return (False, error_msg)

    def dijkstra(self, start: str) -> dict[str, tuple[float, str]]:
        if not self.contains_node(start):
            raise Exception("Node does not exist in graph")

        # Step 1: adds pair of `inf : -` to all nodes
        paths = {node: (float("inf"), "-") for node in self.adj_list}
        paths[start] = (0, "-")

        # Priority queue (will always pop the node with the least cost)
        queue = [(0, start)]

        while len(queue) != 0:
            current_dist, current_node = heapq.heappop(queue)

            # Step 2: for each non-visited neighbor:
            for neighbor, weight in self.adj_list[current_node]:
                # Calculate the new cost
                new_dist = current_dist + weight
                # Change if the new cost < the current cost
                if new_dist < paths[neighbor][0]:
                    paths[neighbor] = (new_dist, current_node)
                    # Adds the node to the queue
                    heapq.heappush(queue, (new_dist, neighbor))

        return paths

    def nodes_in_distance(self, start: str, distance: int) -> list[str]:
        result = []

        # Calculate cost to all nodes from the start node
        paths = self.dijkstra(start)

        # If the cost is less or equal to the given distance
        # Adds it to the result
        for node, pair in paths.items():
            if node != start and pair[0] <= distance:
                result.append(node)

        return result
