from graph import Graph
from utils import parse_email
import os


def main() -> None:
    # Traversing the dataset
    for root, _, files in os.walk("eron-dataset"):
        for file in files:
            path = os.path.join(root, file)
            sender, receivers = parse_email(path)

            if len(receivers) == 0:
                continue


if __name__ == "__main__":
    main()
