package ui;

import domain.DirectedGraph;
import domain.Edge;
import service.GraphIO;
import service.RandomGraphMaker;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.stream.Collectors;

public class ConsoleMenu {
    private final Scanner scanner;
    private DirectedGraph graph;
    private DirectedGraph backup;
    private boolean hasBackup;

    public ConsoleMenu(DirectedGraph graph) {
        this.graph = graph;
        this.backup = new DirectedGraph(0);
        this.hasBackup = false;
        this.scanner = new Scanner(System.in);
    }

    public void run() {
        while (true) {
            printMenu();
            String option = readString("Choose an option: ");

            if ("0".equals(option)) {
                System.out.println("Exiting application.");
                return;
            }

            try {
                handleOption(option);
            } catch (Exception error) {
                System.out.println("Error: " + error.getMessage());
            }

            System.out.println();
        }
    }

    private void printMenu() {
        System.out.println("Directed Graph Console");
        System.out.println("1. Load graph from file");
        System.out.println("2. Save graph to file");
        System.out.println("3. Generate random graph");
        System.out.println("4. Show graph summary");
        System.out.println("5. List all vertices");
        System.out.println("6. Inspect a vertex");
        System.out.println("7. Check whether an edge exists");
        System.out.println("8. View an edge cost");
        System.out.println("9. Update an edge cost");
        System.out.println("10. Add a vertex");
        System.out.println("11. Remove a vertex");
        System.out.println("12. Add an edge");
        System.out.println("13. Remove an edge");
        System.out.println("14. Copy current graph to backup");
        System.out.println("15. Restore graph from backup copy");
        System.out.println("16. Print all edges");
        System.out.println("0. Exit");
    }

    private void handleOption(String option) throws IOException {
        switch (option) {
            case "1" -> loadGraph();
            case "2" -> saveGraph();
            case "3" -> generateRandomGraph();
            case "4" -> showSummary();
            case "5" -> listVertices();
            case "6" -> inspectVertex();
            case "7" -> checkEdge();
            case "8" -> showEdgeCost();
            case "9" -> updateEdgeCost();
            case "10" -> addVertex();
            case "11" -> removeVertex();
            case "12" -> addEdge();
            case "13" -> removeEdge();
            case "14" -> backupGraph();
            case "15" -> restoreGraph();
            case "16" -> printEdges();
            default -> throw new IllegalArgumentException("Unknown menu option");
        }
    }

    private void loadGraph() throws IOException {
        String fileName = readString("File name: ");
        graph = GraphIO.readGraph(fileName);
        System.out.println("Loaded graph from " + fileName + ".");
    }

    private void saveGraph() throws IOException {
        String fileName = readString("File name: ");
        GraphIO.writeGraph(fileName, graph);
        System.out.println("Saved graph to " + fileName + ".");
    }

    private void generateRandomGraph() {
        int vertices = readInt("Number of vertices: ");
        int edges = readInt("Number of edges: ");
        int minCost = readInt("Minimum edge cost: ");
        int maxCost = readInt("Maximum edge cost: ");

        graph = RandomGraphMaker.makeRandomGraph(vertices, edges, minCost, maxCost);
        System.out.println("Random graph generated.");
    }

    private void showSummary() {
        System.out.println("Vertices: " + graph.getVertices());
        System.out.println("Edges: " + graph.getEdges());
    }

    private void listVertices() {
        List<Integer> vertices = graph.parseVertices();
        if (vertices.isEmpty()) {
            System.out.println("The graph has no vertices.");
            return;
        }

        System.out.println("Vertices: " + formatCollection(vertices));
    }

    private void inspectVertex() {
        int vertex = readInt("Vertex: ");
        List<Integer> inbound = graph.parseInboundNeighbors(vertex);
        List<Integer> outbound = graph.parseOutboundNeighbors(vertex);

        System.out.println("In-degree: " + graph.getInDegree(vertex));
        System.out.println("Out-degree: " + graph.getOutDegree(vertex));
        System.out.println("Inbound neighbors: " + formatCollection(inbound));
        System.out.println("Outbound neighbors: " + formatCollection(outbound));
    }

    private void checkEdge() {
        Edge edge = readEdge();
        boolean exists = graph.isEdge(edge.getStart(), edge.getEnd());
        System.out.println(
                "Edge " + edge.getStart() + " -> " + edge.getEnd() + " exists: " + (exists ? "yes" : "no")
        );
    }

    private void showEdgeCost() {
        Edge edge = readEdge();
        System.out.println(
                "Cost of " + edge.getStart() + " -> " + edge.getEnd() + ": "
                        + graph.getEdgeCost(edge.getStart(), edge.getEnd())
        );
    }

    private void updateEdgeCost() {
        Edge edge = readEdge();
        int cost = readInt("New cost: ");
        graph.setEdgeCost(edge.getStart(), edge.getEnd(), cost);
        System.out.println("Edge cost updated.");
    }

    private void addVertex() {
        int vertex = graph.addVertex();
        System.out.println("Added vertex " + vertex + ".");
    }

    private void removeVertex() {
        int vertex = readInt("Vertex to remove: ");
        graph.removeVertex(vertex);
        System.out.println("Removed vertex " + vertex + ".");
    }

    private void addEdge() {
        Edge edge = readEdge();
        int cost = readInt("Cost: ");
        graph.addEdge(edge.getStart(), edge.getEnd(), cost);
        System.out.println("Added edge " + edge.getStart() + " -> " + edge.getEnd() + ".");
    }

    private void removeEdge() {
        Edge edge = readEdge();
        graph.removeEdge(edge.getStart(), edge.getEnd());
        System.out.println("Removed edge " + edge.getStart() + " -> " + edge.getEnd() + ".");
    }

    private void backupGraph() {
        backup = graph.copyGraph();
        hasBackup = true;
        System.out.println("Backup copy created.");
    }

    private void restoreGraph() {
        if (!hasBackup) {
            throw new IllegalStateException("No backup graph is available");
        }

        graph = backup.copyGraph();
        System.out.println("Graph restored from backup.");
    }

    private void printEdges() {
        Map<Edge, Integer> costs = graph.getCosts();
        if (costs.isEmpty()) {
            System.out.println("The graph has no edges.");
            return;
        }

        for (Map.Entry<Edge, Integer> entry : costs.entrySet()) {
            Edge edge = entry.getKey();
            System.out.println(edge.getStart() + " -> " + edge.getEnd() + " (cost = " + entry.getValue() + ")");
        }
    }

    private int readInt(String prompt) {
        System.out.print(prompt);

        if (!scanner.hasNext()) {
            throw new IllegalStateException("No more input available");
        }

        String value = scanner.next();
        try {
            return Integer.parseInt(value);
        } catch (NumberFormatException error) {
            throw new IllegalArgumentException("Invalid integer input", error);
        }
    }

    private String readString(String prompt) {
        System.out.print(prompt);

        if (!scanner.hasNext()) {
            throw new IllegalStateException("No more input available");
        }

        return scanner.next();
    }

    private Edge readEdge() {
        int u = readInt("Start vertex: ");
        int v = readInt("End vertex: ");
        return new Edge(u, v);
    }

    private String formatCollection(List<Integer> values) {
        if (values.isEmpty()) {
            return "none";
        }

        return values.stream()
                .map(String::valueOf)
                .collect(Collectors.joining(" "));
    }
}
