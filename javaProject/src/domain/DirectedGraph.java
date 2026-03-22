package domain;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.NavigableMap;
import java.util.SortedSet;
import java.util.TreeMap;
import java.util.TreeSet;

public class DirectedGraph {
    private final NavigableMap<Integer, SortedSet<Integer>> inbound;
    private final NavigableMap<Integer, SortedSet<Integer>> outbound;
    private final NavigableMap<Edge, Integer> costs;
    private int vertices;
    private int edges;

    public DirectedGraph(int vertices) {
        if (vertices < 0) {
            throw new IllegalArgumentException("The number of vertices cannot be negative");
        }

        this.inbound = new TreeMap<>();
        this.outbound = new TreeMap<>();
        this.costs = new TreeMap<>();
        this.vertices = vertices;
        this.edges = 0;

        for (int vertex = 0; vertex < vertices; vertex++) {
            outbound.put(vertex, new TreeSet<>());
            inbound.put(vertex, new TreeSet<>());
        }
    }

    public DirectedGraph(DirectedGraph other) {
        this.inbound = new TreeMap<>();
        this.outbound = new TreeMap<>();
        this.costs = new TreeMap<>(other.costs);
        this.vertices = other.vertices;
        this.edges = other.edges;

        for (Map.Entry<Integer, SortedSet<Integer>> entry : other.outbound.entrySet()) {
            outbound.put(entry.getKey(), new TreeSet<>(entry.getValue()));
        }

        for (Map.Entry<Integer, SortedSet<Integer>> entry : other.inbound.entrySet()) {
            inbound.put(entry.getKey(), new TreeSet<>(entry.getValue()));
        }
    }

    private void checkVertex(int vertex) {
        if (!outbound.containsKey(vertex)) {
            throw new IllegalArgumentException("Vertex " + vertex + " not found");
        }
    }

    private void checkEdge(int u, int v) {
        checkVertex(u);
        checkVertex(v);

        if (!outbound.get(u).contains(v)) {
            throw new IllegalArgumentException("Edge " + u + " -> " + v + " not found");
        }
    }

    public boolean isEdge(int u, int v) {
        checkVertex(u);
        checkVertex(v);
        return outbound.get(u).contains(v);
    }

    public void addEdge(int u, int v, int cost) {
        checkVertex(u);
        checkVertex(v);

        if (outbound.get(u).contains(v)) {
            throw new IllegalArgumentException("Edge " + u + " -> " + v + " already exists");
        }

        outbound.get(u).add(v);
        inbound.get(v).add(u);
        costs.put(new Edge(u, v), cost);
        edges++;
    }

    public void removeEdge(int u, int v) {
        checkEdge(u, v);
        outbound.get(u).remove(v);
        inbound.get(v).remove(u);
        costs.remove(new Edge(u, v));
        edges--;
    }

    public int addVertex() {
        int newVertex = outbound.isEmpty() ? 0 : outbound.lastKey() + 1;
        outbound.put(newVertex, new TreeSet<>());
        inbound.put(newVertex, new TreeSet<>());
        vertices++;
        return newVertex;
    }

    public void removeVertex(int vertex) {
        checkVertex(vertex);

        List<Integer> outboundNeighbors = new ArrayList<>(outbound.get(vertex));
        for (int neighbor : outboundNeighbors) {
            removeEdge(vertex, neighbor);
        }

        List<Integer> inboundNeighbors = new ArrayList<>(inbound.get(vertex));
        for (int neighbor : inboundNeighbors) {
            if (outbound.containsKey(neighbor) && outbound.get(neighbor).contains(vertex)) {
                removeEdge(neighbor, vertex);
            }
        }

        outbound.remove(vertex);
        inbound.remove(vertex);
        vertices--;
    }

    public void setEdgeCost(int u, int v, int cost) {
        checkEdge(u, v);
        costs.put(new Edge(u, v), cost);
    }

    public int getEdgeCost(int u, int v) {
        checkEdge(u, v);
        return costs.get(new Edge(u, v));
    }

    public int getVertices() {
        return vertices;
    }

    public int getEdges() {
        return edges;
    }

    public NavigableMap<Edge, Integer> getCosts() {
        return new TreeMap<>(costs);
    }

    public List<Integer> parseVertices() {
        return new ArrayList<>(outbound.navigableKeySet());
    }

    public List<Integer> parseOutboundNeighbors(int vertex) {
        checkVertex(vertex);
        return new ArrayList<>(outbound.get(vertex));
    }

    public List<Integer> parseInboundNeighbors(int vertex) {
        checkVertex(vertex);
        return new ArrayList<>(inbound.get(vertex));
    }

    public int getOutDegree(int vertex) {
        checkVertex(vertex);
        return outbound.get(vertex).size();
    }

    public int getInDegree(int vertex) {
        checkVertex(vertex);
        return inbound.get(vertex).size();
    }

    public DirectedGraph copyGraph() {
        return new DirectedGraph(this);
    }
}
