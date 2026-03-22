from src.service.GraphIO import readGraph
from src.UI.menu import ConsoleMenu


def main():
    graph = readGraph("graph.txt")
    menu = ConsoleMenu(graph)
    menu.run()


if __name__ == "__main__":
    main()
