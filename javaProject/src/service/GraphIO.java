package service;

import domain.DirectedGraph;
import domain.Edge;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;

public final class GraphIO {
    private GraphIO() {
    }

    public static DirectedGraph readGraph(String fileName) throws IOException {
        Path path = Path.of(fileName);
        if (!Files.exists(path)) {
            throw new FileNotFoundException("Could not open file: " + fileName);
        }

        try (BufferedReader reader = Files.newBufferedReader(path)) {
            String headerLine = reader.readLine();
            if (headerLine == null || headerLine.trim().isEmpty()) {
                throw new IllegalArgumentException("The input file is empty or invalid");
            }

            String[] headerParts = headerLine.trim().split("\\s+");
            if (headerParts.length < 2) {
                throw new IllegalArgumentException("The input file is empty or invalid");
            }

            int vertices = parseInteger(headerParts[0], "The input file is empty or invalid");
            int edges = parseInteger(headerParts[1], "The input file is empty or invalid");

            DirectedGraph graph = new DirectedGraph(vertices);
            for (int index = 0; index < edges; index++) {
                String edgeLine = reader.readLine();
                if (edgeLine == null || edgeLine.trim().isEmpty()) {
                    throw new IllegalArgumentException("The input file ended before all edges were read");
                }

                String[] edgeParts = edgeLine.trim().split("\\s+");
                if (edgeParts.length < 3) {
                    throw new IllegalArgumentException("The input file ended before all edges were read");
                }

                int u = parseInteger(edgeParts[0], "The input file ended before all edges were read");
                int v = parseInteger(edgeParts[1], "The input file ended before all edges were read");
                int cost = parseInteger(edgeParts[2], "The input file ended before all edges were read");
                graph.addEdge(u, v, cost);
            }

            return graph;
        }
    }

    public static void writeGraph(String fileName, DirectedGraph graph) throws IOException {
        Path path = Path.of(fileName);

        try (BufferedWriter writer = Files.newBufferedWriter(path)) {
            writer.write(graph.getVertices() + " " + graph.getEdges());
            writer.newLine();

            for (Map.Entry<Edge, Integer> entry : graph.getCosts().entrySet()) {
                Edge edge = entry.getKey();
                writer.write(edge.getStart() + " " + edge.getEnd() + " " + entry.getValue());
                writer.newLine();
            }
        } catch (IOException error) {
            throw new IOException("Could not open file for writing: " + fileName, error);
        }
    }

    private static int parseInteger(String value, String errorMessage) {
        try {
            return Integer.parseInt(value);
        } catch (NumberFormatException error) {
            throw new IllegalArgumentException(errorMessage, error);
        }
    }
}
