.. include:: substitutions.rst

|DistAlgTopic|
=========================================

Wave traversal algorithms are fundamental tools in distributed systems, enabling the dissemination of information across a network of processes. These algorithms operate by propagating messages through the processes/nodes, with each process forwarding the message to its neighbors similar to a wave propagating through a medium. They are used in various distributed applications, such as broadcasting, flooding, and etc. 

In this section, we delve into wave traversal algorithms, focusing on Awerbuch's algorithm and Cidon's algorithm. We discuss their underlying principles, implementation details, and analyze their complexity. 

**Awerbuch's Wave Traversal Algorithm:**

The Awerbuch depth-first search algorithm is proposed by Baruch Awerbuch. The main difference Awerbuch's algorithm has with the traditional depth-first search algorithm is that it does traversals along back edges in parallel instead of serial. This reduces time complexity without increasing other complexities such as communication. 

Awerbuch's algorithm efficiently executes distributed depth-first search in networks. Initiated by a DISCOVER message, a node marks itself visited and notifies all neighbors except the sender (its parent) with a VISITED message, pausing the search. Neighbors send back ACK messages, and upon receipt of all ACKs, the node resumes the search. If there are unvisited neighbors, it sends them a DISCOVER message; otherwise, it returns to its parent with a RETURN message. This process prevents backtracking, utilizing DISCOVER and RETURN messages for direct paths and VISITED messages with ACKs for indirect paths. The communication complexity is tied to the edge count, O(E), while the time complexity is linked to the node count, O(V), with minimal delays at highly connected nodes. Awerbuch's method ensures minimal communication and efficient search continuation, optimizing network traversal.


The implementation has a main class implementing the Awerbuch's DFS algorithm. It inherits from GenericModel. The class has several methods to handle different events and states in the DFS algorithm.

The methods are:

1. **on_init**: This method is called when the node is initialized. It sets the initial state of the node and sends a discover message if the node is the source node.

2. **on_message_from_bottom**: This method is called when a message is received from a lower layer. It creates an event based on the message type and sends the event to itself for further processing.

3. **on_discover**: This method is called when a discover event is received. It traverses the neighbors of the node and sends a VISITED message to the neighbors that are not visited yet. It also handles the edge case when there are only two nodes in the network.

4. **on_return**: This method is called when a return event is received. If node is visited before, it sends RETURN message to its parent. If node is not visited before, it picks a random destination from the neighbors and sends a DISCOVER message to that neighbor.

5. **on_visited**: This method is called when a visited event is received. It removes the neighbor from the list of neighbors to visit and sends a ACK message to the neighbor.

6. **on_ack**: This method is called when an acknowledgement event is received. It sets the state of the node to VISITED and sends a RETURN message to itself.

**Correctness:**

*Termination (liveness)*: Awerbuch's algorithm terminates reliably because it systematically visits each node exactly once, ensuring no node is left unexplored or revisited, and thus covering the entire network. Each node signals completion by sending a RETURN message to its parent only after all neighbors have been either visited or acknowledged as visited, ensuring all paths are fully explored. This methodical progression through the network, coupled with the guaranteed response from all neighbors, ensures the algorithm reaches a definitive end when the starting node receives the final RETURN message, confirming network-wide traversal.

*Correctness*: Awerbuch's algorithm ensures each node and edge is explored exactly once by establishing a clear parent-child relationship, preventing cycles. It minimizes communication through VISITED and ACK messages, ensuring all neighbors are synchronized before resuming search, which eliminates unnecessary explorations and loops. The algorithm's design for message efficiency and controlled exploration guarantees completeness and efficient network traversal, optimizing time and communication complexity.

**Complexity:**

1. **Time Complexity**  The Awerbuch's Wave Traversal Algorithm has a time complexity of O(4*N-2).
2. **Message Complexity:** The Awerebuch's Wave Traversal Algorithm has a message complexity of O(4*E).


**Cidon's Wave Traversal Algorithm:**

Cidon's algorithm is proposed by Isreal Cidon and is a wave traversal algorithm that is based on Awerbuch's algorithm. It improves on Awerbuch's algorithm by reducing the number of messages sent in the network. The main idea behind Cidon's algorithm is to reduce the number of messages sent in the network by using a different approach to handle the ACK messages.

In Cidon's algorithm, when a node receives a VISITED message from a neighbor, it sends an ACK message to the neighbor. The neighbor then sends a RETURN message to the node. This way, the node does not have to send a RETURN message to the neighbor. This reduces the number of messages sent in the network. The algorithm ensures that each node is visited exactly once and that the network is traversed efficiently.

In the implementation there is a child class that inherits from GenericModel class. The class has several methods to handle different events and states in the DFS algorithm.

The class has the following methods:

1. **on_init**: This method is called when the node is initialized. It sets the initial state of the node and sends a start message if the node is the source node.

2. **on_message_from_bottom**: This method is called when a message is received from a lower layer. It sends the message to itself for further processing.

3. **on_start**: This method is called when a start event is received. If the node is idle, it starts visiting its neighbors.

4. **visit_neighbors**: This method is used when a node starts visiting its neighbors. It changes the state of the node to DISCOVERED and then calls the search method. After that, it iterates over all the neighbors of the node. For each neighbor, if the mark of the neighbor is VISITED or UNVISITED, it sends a VISITED message to that neighbor. This is done by creating a new ApplicationLayerMessageHeader with the VISITED message type, the instance number of the current node, and the instance number of the neighbor. This message is then sent to the lower layer. The number of messages sent by the node is also incremented.

5. **on_token**: This method is called when a token event is received. If node is idle it visits its neighbors. If node is not idle, it sets itself VISITED or continues visiting its neighbors if message comes from child.

6. **on_visited**: This method is called when a visited event is received. If the node is unvisited it is set to visited, otherwise it continues visiting its neighbors if message comes from child.

7. **search**: This method is used to search for unvisited neighbors. It iterates over all the neighbors of the node. If it finds a neighbor that is marked as UNVISITED, it sends a TOKEN message to that neighbor and marks it as CHILD. This is done by creating a new ApplicationLayerMessageHeader with the TOKEN message type, the instance number of the current node, and the instance number of the neighbor. This message is then sent to the lower layer. The number of messages sent by the node is also incremented. If it doesn't find any unvisited neighbors and the node is not the source node, it sends a TOKEN message to its parent.


**Correctness:**

*Termination (liveness)*: Cidon's algorithm guarantees termination by ensuring that each node is visited exactly once. The algorithm uses a combination of VISITED, ACK, and RETURN messages to synchronize the traversal of the network. This ensures that all nodes are visited and that the traversal is completed efficiently.

*Correctness*: Cidon's algorithm ensures correctness by maintaining a parent-child relationship between nodes and by using VISITED, ACK, and RETURN messages to synchronize the traversal of the network. The algorithm guarantees that each node is visited exactly once and that the network is traversed efficiently. By reducing the number of messages sent in the network, Cidon's algorithm optimizes the traversal process.

**Complexity:**

1. **Time Complexity**  The Cidon's Wave Traversal Algorithm has a time complexity of O(2*N-2).

2. **Message Complexity:** The Cidon's Wave Traversal Algorithm has a message complexity of O(4*E).