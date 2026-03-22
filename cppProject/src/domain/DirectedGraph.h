#ifndef CPPPROJECT_DIRECTEDGRAPH_H
#define CPPPROJECT_DIRECTEDGRAPH_H
#include <map>
#include <vector>
using namespace std;

class DirectedGraph
{
    map<int, vector<int>> inbound;
    map<int, vector<int>> outbound;
    map<pair<int, int>, int> costs;
    int vertices;
    int edges;

    void checkVertex(int vertex) const;
    void checkEdge(int u, int v) const;

public:

    DirectedGraph(int vertices);
    DirectedGraph(const DirectedGraph& other);
    bool isEdge(int u, int v) const;
    void addEdge(int u, int v, int cost);
    void removeEdge(int u, int v);

    int addVertex();

    void removeVertex(int vertex);

    void setEdgeCost(int u, int v, int cost);

    int getEdgeCost(int u, int v);
    int getVertices() const;
    int getEdges() const;
    map<pair<int, int>, int> getCosts() const;
    vector<int> parseVertices() const;
    vector<int> parseOutboundNeighbors(int vertex) const;
    vector<int> parseInboundNeighbors(int vertex) const;
    int getOutDegree(int vertex) const;
    int getInDegree(int vertex) const;
};


#endif //CPPPROJECT_DIRECTEDGRAPH_H
