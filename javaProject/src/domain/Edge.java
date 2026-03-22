package domain;

import java.util.Objects;

public final class Edge implements Comparable<Edge> {
    private final int start;
    private final int end;

    public Edge(int start, int end) {
        this.start = start;
        this.end = end;
    }

    public int getStart() {
        return start;
    }

    public int getEnd() {
        return end;
    }

    @Override
    public int compareTo(Edge other) {
        int startComparison = Integer.compare(start, other.start);
        if (startComparison != 0) {
            return startComparison;
        }

        return Integer.compare(end, other.end);
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (!(other instanceof Edge edge)) {
            return false;
        }
        return start == edge.start && end == edge.end;
    }

    @Override
    public int hashCode() {
        return Objects.hash(start, end);
    }
}
