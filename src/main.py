from graph import Graph
from utils import parse_email
import os


def main() -> None:
    graph = Graph()

    # Traversing the dataset
    for root, _, files in os.walk("eron-dataset"):
        # For each file (email)
        for file in files:
            path = os.path.join(root, file)

            # Get those involved in the email
            sender, receivers = parse_email(path)

            # Skips if the email has no receivers
            if len(receivers) == 0:
                continue

            # Adds the nodes and the edges of the email
            for receiver in receivers:
                previous_weigth = graph.get_weight(sender, receiver)
                graph.add_edge(sender, receiver, previous_weigth + 1)

    # Saves the graph in a txt file
    open("output.txt", "w").write(graph.to_string())

    # Exercise 2
    print(f"Graph order (number of nodes): {graph.get_order()}")
    print(f"Graph size (number of edges): {graph.get_size()}\n")
    top_indegree, top_outdegree = graph.top_degrees()
    print("TOP 20 OUTDEGREE NODES:")
    for outdegree in top_outdegree:
        print(outdegree)
    print("\n-------------------------\n")
    print("TOP 20 INDEGREE NODES:")
    for indegree in top_indegree:
        print(indegree)

    # Exercise 3
    eul, error = graph.is_eulerian()
    print("\nGRAPH IS EULERIAN") if eul else print(f"\nGRAPH ISNT EULERIAN: \n{error}")

    # Exercise 4
    print(f"\nDijkstra: {graph.nodes_in_distance(top_indegree[19][0], 0)}")


if __name__ == "__main__":
    main()
