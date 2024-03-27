.. include:: substitutions.rst

|DistAlgTopic|
=========================================

Wave traversal algorithms are fundamental tools in distributed systems, enabling the dissemination of information across a network of processes. These algorithms operate by propagating messages through the processes/nodes, with each process forwarding the message to its neighbors similar to a wave propagating through a medium. They are used in various distributed applications, such as broadcasting, flooding, and etc. 

In this section, we delve into wave traversal algorithms, focusing on Awerbuch's algorithm and Cidon's algorithm. We discuss their underlying principles, implementation details, and analyze their complexity. 

**Awerbuch's Wave Traversal Algorithm:**

The Awerbuch depth-first search algorithm is proposed by Baruch Awerbuch. The main difference Awerbuch's algorithm has with the traditional depth-first search algorithm is that it does traversals along back edges in parallel instead of serial. This reduces time complexity without increasing other complexities such as communication. 

Awerbuch's algorithm efficiently executes distributed depth-first search in networks. Initiated by a DISCOVER message, a node marks itself visited and notifies all neighbors except the sender (its parent) with a VISITED message, pausing the search. Neighbors send back ACK messages, and upon receipt of all ACKs, the node resumes the search. If there are unvisited neighbors, it sends them a DISCOVER message; otherwise, it returns to its parent with a RETURN message. This process prevents backtracking, utilizing DISCOVER and RETURN messages for direct paths and VISITED messages with ACKs for indirect paths. The communication complexity is tied to the edge count, O(E), while the time complexity is linked to the node count, O(V), with minimal delays at highly connected nodes. Awerbuch's method ensures minimal communication and efficient search continuation, optimizing network traversal.


*Implementation details will be added soon with pseudocode and examples.*

**Correctness:**

*Termination (liveness)*: Awerbuch's algorithm terminates reliably because it systematically visits each node exactly once, ensuring no node is left unexplored or revisited, and thus covering the entire network. Each node signals completion by sending a RETURN message to its parent only after all neighbors have been either visited or acknowledged as visited, ensuring all paths are fully explored. This methodical progression through the network, coupled with the guaranteed response from all neighbors, ensures the algorithm reaches a definitive end when the starting node receives the final RETURN message, confirming network-wide traversal.

*Correctness*: Awerbuch's algorithm ensures each node and edge is explored exactly once by establishing a clear parent-child relationship, preventing cycles. It minimizes communication through VISITED and ACK messages, ensuring all neighbors are synchronized before resuming search, which eliminates unnecessary explorations and loops. The algorithm's design for message efficiency and controlled exploration guarantees completeness and efficient network traversal, optimizing time and communication complexity.

**Complexity:**

1. **Time Complexity**  The Awerbuch's Wave Traversal Algorithm has a time complexity of O(4*N-2).
2. **Message Complexity:** The Awerebuch's Wave Traversal Algorithm has a message complexity of O(4*E).


**Cidon's Wave Traversal Algorithm:**

Cidon's algorithm is proposed by Isreal Cidon and is a wave traversal algorithm that is based on Awerbuch's algorithm. It improves on Awerbuch's algorithm by reducing the number of messages sent in the network. The main idea behind Cidon's algorithm is to reduce the number of messages sent in the network by using a different approach to handle the ACK messages.

In Cidon's algorithm, when a node receives a VISITED message from a neighbor, it sends an ACK message to the neighbor. The neighbor then sends a RETURN message to the node. This way, the node does not have to send a RETURN message to the neighbor. This reduces the number of messages sent in the network. The algorithm ensures that each node is visited exactly once and that the network is traversed efficiently.

*Implementation details will be added soon with pseudocode and examples.*

**Correctness:**

*Termination (liveness)*: Cidon's algorithm guarantees termination by ensuring that each node is visited exactly once. The algorithm uses a combination of VISITED, ACK, and RETURN messages to synchronize the traversal of the network. This ensures that all nodes are visited and that the traversal is completed efficiently.

*Correctness*: Cidon's algorithm ensures correctness by maintaining a parent-child relationship between nodes and by using VISITED, ACK, and RETURN messages to synchronize the traversal of the network. The algorithm guarantees that each node is visited exactly once and that the network is traversed efficiently. By reducing the number of messages sent in the network, Cidon's algorithm optimizes the traversal process.

**Complexity:**

1. **Time Complexity**  The Cidon's Wave Traversal Algorithm has a time complexity of O(2*N-2).

2. **Message Complexity:** The Cidon's Wave Traversal Algorithm has a message complexity of O(4*E).