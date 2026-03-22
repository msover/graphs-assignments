import domain.DirectedGraph;
import service.GraphIO;
import ui.ConsoleMenu;

public class Main {
    public static void main(String[] args) {
        DirectedGraph graph = new DirectedGraph(0);

        try {
            graph = GraphIO.readGraph("graph.txt");
        } catch (Exception ignored) {
        }

        ConsoleMenu menu = new ConsoleMenu(graph);
        menu.run();
    }
}
