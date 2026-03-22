#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <random>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

#include "domain/DirectedGraph.h"

using namespace std;

namespace {

int readInt(const string& prompt) {
    int value = 0;
    cout << prompt;
    if (!(cin >> value)) {
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        throw runtime_error("Invalid integer input");
    }
    return value;
}

string readString(const string& prompt) {
    string value;
    cout << prompt;
    cin >> value;
    return value;
}

pair<int, int> readEdge() {
    const int u = readInt("Start vertex: ");
    const int v = readInt("End vertex: ");
    return make_pair(u, v);
}

string formatCollection(const vector<int>& values) {
    if (values.empty()) {
        return "none";
    }

    string result;
    for (size_t index = 0; index < values.size(); ++index) {
        if (index > 0) {
            result += " ";
        }
        result += to_string(values[index]);
    }
    return result;
}

DirectedGraph readGraph(const string& fileName) {
    ifstream file(fileName);
    if (!file.is_open()) {
        throw runtime_error("Could not open file: " + fileName);
    }

    int vertices = 0;
    int edges = 0;
    if (!(file >> vertices >> edges)) {
        throw runtime_error("The input file is empty or invalid");
    }

    DirectedGraph graph(vertices);
    for (int index = 0; index < edges; ++index) {
        int u = 0;
        int v = 0;
        int cost = 0;
        if (!(file >> u >> v >> cost)) {
            throw runtime_error("The input file ended before all edges were read");
        }
        graph.addEdge(u, v, cost);
    }

    return graph;
}

void writeGraph(const string& fileName, const DirectedGraph& graph) {
    ofstream file(fileName);
    if (!file.is_open()) {
        throw runtime_error("Could not open file for writing: " + fileName);
    }

    file << graph.getVertices() << " " << graph.getEdges() << '\n';

    const map<pair<int, int>, int> costs = graph.getCosts();
    for (map<pair<int, int>, int>::const_iterator it = costs.begin(); it != costs.end(); ++it) {
        file << it->first.first << " " << it->first.second << " " << it->second << '\n';
    }
}

DirectedGraph makeRandomGraph(int vertices, int edges, int minCost, int maxCost) {
    if (vertices < 0) {
        throw runtime_error("The number of vertices cannot be negative");
    }
    if (edges < 0) {
        throw runtime_error("The number of edges cannot be negative");
    }
    if (minCost > maxCost) {
        throw runtime_error("Invalid cost interval");
    }

    const int maxEdges = vertices * vertices;
    if (edges > maxEdges) {
        throw runtime_error("Too many edges for the given number of vertices");
    }

    DirectedGraph graph(vertices);
    if (vertices == 0) {
        return graph;
    }

    random_device randomDevice;
    mt19937 generator(randomDevice());
    uniform_int_distribution<int> vertexDistribution(0, vertices - 1);
    uniform_int_distribution<int> costDistribution(minCost, maxCost);

    while (graph.getEdges() < edges) {
        const int u = vertexDistribution(generator);
        const int v = vertexDistribution(generator);

        if (graph.isEdge(u, v)) {
            continue;
        }

        graph.addEdge(u, v, costDistribution(generator));
    }

    return graph;
}

void printMenu() {
    cout << "Directed Graph Console\n";
    cout << "1. Load graph from file\n";
    cout << "2. Save graph to file\n";
    cout << "3. Generate random graph\n";
    cout << "4. Show graph summary\n";
    cout << "5. List all vertices\n";
    cout << "6. Inspect a vertex\n";
    cout << "7. Check whether an edge exists\n";
    cout << "8. View an edge cost\n";
    cout << "9. Update an edge cost\n";
    cout << "10. Add a vertex\n";
    cout << "11. Remove a vertex\n";
    cout << "12. Add an edge\n";
    cout << "13. Remove an edge\n";
    cout << "14. Copy current graph to backup\n";
    cout << "15. Restore graph from backup copy\n";
    cout << "16. Print all edges\n";
    cout << "0. Exit\n";
}

void handleOption(const string& option, DirectedGraph& graph, DirectedGraph& backup, bool& hasBackup) {
    if (option == "1") {
        const string fileName = readString("File name: ");
        graph = readGraph(fileName);
        cout << "Loaded graph from " << fileName << ".\n";
        return;
    }

    if (option == "2") {
        const string fileName = readString("File name: ");
        writeGraph(fileName, graph);
        cout << "Saved graph to " << fileName << ".\n";
        return;
    }

    if (option == "3") {
        const int vertices = readInt("Number of vertices: ");
        const int edges = readInt("Number of edges: ");
        const int minCost = readInt("Minimum edge cost: ");
        const int maxCost = readInt("Maximum edge cost: ");

        graph = makeRandomGraph(vertices, edges, minCost, maxCost);
        cout << "Random graph generated.\n";
        return;
    }

    if (option == "4") {
        cout << "Vertices: " << graph.getVertices() << '\n';
        cout << "Edges: " << graph.getEdges() << '\n';
        return;
    }

    if (option == "5") {
        const vector<int> vertices = graph.parseVertices();
        if (vertices.empty()) {
            cout << "The graph has no vertices.\n";
            return;
        }

        cout << "Vertices: " << formatCollection(vertices) << '\n';
        return;
    }

    if (option == "6") {
        const int vertex = readInt("Vertex: ");
        const vector<int> inbound = graph.parseInboundNeighbors(vertex);
        const vector<int> outbound = graph.parseOutboundNeighbors(vertex);

        cout << "In-degree: " << graph.getInDegree(vertex) << '\n';
        cout << "Out-degree: " << graph.getOutDegree(vertex) << '\n';
        cout << "Inbound neighbors: " << formatCollection(inbound) << '\n';
        cout << "Outbound neighbors: " << formatCollection(outbound) << '\n';
        return;
    }

    if (option == "7") {
        const pair<int, int> edge = readEdge();
        const bool exists = graph.isEdge(edge.first, edge.second);
        cout << "Edge " << edge.first << " -> " << edge.second << " exists: "
             << (exists ? "yes" : "no") << '\n';
        return;
    }

    if (option == "8") {
        const pair<int, int> edge = readEdge();
        cout << "Cost of " << edge.first << " -> " << edge.second << ": "
             << graph.getEdgeCost(edge.first, edge.second) << '\n';
        return;
    }

    if (option == "9") {
        const pair<int, int> edge = readEdge();
        const int cost = readInt("New cost: ");
        graph.setEdgeCost(edge.first, edge.second, cost);
        cout << "Edge cost updated.\n";
        return;
    }

    if (option == "10") {
        const int vertex = graph.addVertex();
        cout << "Added vertex " << vertex << ".\n";
        return;
    }

    if (option == "11") {
        const int vertex = readInt("Vertex to remove: ");
        graph.removeVertex(vertex);
        cout << "Removed vertex " << vertex << ".\n";
        return;
    }

    if (option == "12") {
        const pair<int, int> edge = readEdge();
        const int cost = readInt("Cost: ");
        graph.addEdge(edge.first, edge.second, cost);
        cout << "Added edge " << edge.first << " -> " << edge.second << ".\n";
        return;
    }

    if (option == "13") {
        const pair<int, int> edge = readEdge();
        graph.removeEdge(edge.first, edge.second);
        cout << "Removed edge " << edge.first << " -> " << edge.second << ".\n";
        return;
    }

    if (option == "14") {
        backup = graph;
        hasBackup = true;
        cout << "Backup copy created.\n";
        return;
    }

    if (option == "15") {
        if (!hasBackup) {
            throw runtime_error("No backup graph is available");
        }

        graph = backup;
        cout << "Graph restored from backup.\n";
        return;
    }

    if (option == "16") {
        const map<pair<int, int>, int> costs = graph.getCosts();
        if (costs.empty()) {
            cout << "The graph has no edges.\n";
            return;
        }

        for (map<pair<int, int>, int>::const_iterator it = costs.begin(); it != costs.end(); ++it) {
            cout << it->first.first << " -> " << it->first.second
                 << " (cost = " << it->second << ")\n";
        }
        return;
    }

    throw runtime_error("Unknown menu option");
}

}  // namespace

int main() {
    DirectedGraph graph(0);
    DirectedGraph backup(0);
    bool hasBackup = false;

    try {
        graph = readGraph("graph.txt");
    } catch (const exception&) {
    }

    while (true) {
        printMenu();
        const string option = readString("Choose an option: ");

        if (option == "0") {
            cout << "Exiting application.\n";
            return 0;
        }

        try {
            handleOption(option, graph, backup, hasBackup);
        } catch (const exception& error) {
            cout << "Error: " << error.what() << '\n';
        }

        cout << '\n';
    }
}
