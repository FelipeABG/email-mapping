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
            sender, receivers = parse_email(path)  # Get those involved in the email

            if len(receivers) == 0:
                continue  # Skips if the email has no receivers

            for receiver in receivers:  # Adds the nodes and the edges of the email
                previous_weigth = graph.get_weight(sender, receiver)
                graph.add_edge(sender, receiver, previous_weigth + 1)

    open("output.txt", "w").write(graph.to_string())  # Saves the graph in a txt file
    print(graph.get_order())
    print(graph.get_size())


if __name__ == "__main__":
    main()
