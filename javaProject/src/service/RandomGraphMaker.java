package service;

import domain.DirectedGraph;

import java.util.concurrent.ThreadLocalRandom;

public final class RandomGraphMaker {
    private RandomGraphMaker() {
    }

    public static DirectedGraph makeRandomGraph(int vertices, int edges, int minCost, int maxCost) {
        if (vertices < 0) {
            throw new IllegalArgumentException("The number of vertices cannot be negative");
        }
        if (edges < 0) {
            throw new IllegalArgumentException("The number of edges cannot be negative");
        }
        if (minCost > maxCost) {
            throw new IllegalArgumentException("Invalid cost interval");
        }

        long maxEdges = (long) vertices * vertices;
        if (edges > maxEdges) {
            throw new IllegalArgumentException("Too many edges for the given number of vertices");
        }

        DirectedGraph graph = new DirectedGraph(vertices);
        if (vertices == 0) {
            return graph;
        }

        ThreadLocalRandom random = ThreadLocalRandom.current();
        while (graph.getEdges() < edges) {
            int u = random.nextInt(vertices);
            int v = random.nextInt(vertices);

            if (graph.isEdge(u, v)) {
                continue;
            }

            int cost = (int) random.nextLong(minCost, (long) maxCost + 1);
            graph.addEdge(u, v, cost);
        }

        return graph;
    }
}
