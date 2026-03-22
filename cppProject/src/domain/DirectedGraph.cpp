#include "DirectedGraph.h"

#include <algorithm>
#include <stdexcept>

DirectedGraph::DirectedGraph(const int vertices) {
    this->vertices = vertices;
    this->edges = 0;
    for (int vertex = 0; vertex < vertices; ++vertex) {
        this->outbound[vertex] = {};
        this->inbound[vertex] = {};
    }
}

DirectedGraph::DirectedGraph(const DirectedGraph& other) {
    this->inbound = other.inbound;
    this->outbound = other.outbound;
    this->costs = other.costs;
    this->vertices = other.vertices;
    this->edges = other.edges;
}

void DirectedGraph::checkVertex(int vertex) const {
    for (const auto& entry : this->outbound) {
        if (entry.first == vertex) {
            return;
        }
    }
    throw logic_error("Vertex" + to_string(vertex) + " not found");
}
void DirectedGraph::checkEdge(const int u,const  int v) const {
    checkVertex(u);
    checkVertex(v);
    const auto it = this->outbound.find(u);
    for (const auto& neighbour : it->second) {
        if (neighbour == v) {
            return;
        }
    }
    throw logic_error("Edge " + to_string(u) + " -> " + to_string(v) + " not found");
}

bool DirectedGraph::isEdge(const int u,const  int v) const {
    checkVertex(u);
    checkVertex(v);
    const auto it = this->outbound.find(u);
    for (const auto& neighbour : it->second) {
        if (neighbour == v) {
            return true;
        }
    }
    return false;
}

void DirectedGraph::addEdge(const int u,const  int v, const int cost) {
    checkVertex(u);
    checkVertex(v);
    const auto it = this->outbound.find(u);
    for (const auto& neighbour : it->second) {
        if (neighbour == v) {
            throw logic_error("Edge " + to_string(u) + " -> " + to_string(v) + " already exists");
        }
    }
    this->outbound[u].push_back(v);
    this->inbound[v].push_back(u);
    this->costs[make_pair(u, v)] = cost;
    this->edges++;
}

void DirectedGraph::removeEdge(const int u, const int v) {
    checkEdge(u, v);
    auto& outList = this->outbound[u];

    for (auto it = outList.begin(); it != outList.end(); ++ it) {
        if (*it == v) {
            outList.erase(it);
            break;
        }
    }
    auto& inList = this->inbound[v];
    for (auto it = inList.begin(); it != inList.end(); ++ it) {
        if (*it == u) {
            inList.erase(it);
            break;
        }
    }

    this->costs.erase(make_pair(u, v));
    this->edges --;
}

int DirectedGraph::addVertex() {
    int newVertex = 0;
    if (!this->outbound.empty()) {
        for (const auto& entry : this->outbound) {
            if (entry.first >= newVertex) {
                newVertex = entry.first + 1;
            }
        }
    }
    this->outbound[newVertex] = {};
    this->inbound[newVertex] = {};
    this->vertices ++;
    return newVertex;
}

void DirectedGraph::removeVertex(int vertex) {
    checkVertex(vertex);
    vector<int> outCopy = this->outbound[vertex];
    for (const auto& entry : outCopy) {
        removeEdge(vertex, entry);
    }
    vector<int> inCopy = this->inbound[vertex];
    for (const auto& entry : inCopy) {
        if (this->isEdge(entry, vertex)) {
            removeEdge(entry, vertex);
        }
    }
    this->outbound.erase(vertex);
    this->inbound.erase(vertex);
    this->vertices--;
}

void DirectedGraph::setEdgeCost(int u, int v, int cost) {
    checkEdge(u, v);
    this->costs[make_pair(u, v)] = cost;
}

int DirectedGraph::getEdgeCost(int u, int v) {
    checkEdge(u, v);
    return this->costs[make_pair(u, v)];
}

int DirectedGraph::getVertices() const {
    return this->vertices;
}

int DirectedGraph::getEdges() const {
    return this->edges;
}

map<pair<int, int>, int> DirectedGraph::getCosts() const {
    return this->costs;
}

vector<int> DirectedGraph::parseVertices() const {
    vector<int> verticesList;
    for (const auto& entry : this->outbound) {
        verticesList.push_back(entry.first);
    }
    return verticesList;
}

vector<int> DirectedGraph::parseOutboundNeighbors(int vertex) const {
    checkVertex(vertex);
    vector<int> neighbors = this->outbound.at(vertex);
    sort(neighbors.begin(), neighbors.end());
    return neighbors;
}

vector<int> DirectedGraph::parseInboundNeighbors(int vertex) const {
    checkVertex(vertex);
    vector<int> neighbors = this->inbound.at(vertex);
    sort(neighbors.begin(), neighbors.end());
    return neighbors;
}

int DirectedGraph::getOutDegree(int vertex) const {
    checkVertex(vertex);
    return static_cast<int>(this->outbound.at(vertex).size());
}

int DirectedGraph::getInDegree(int vertex) const {
    checkVertex(vertex);
    return static_cast<int>(this->inbound.at(vertex).size());
}
