.. include:: substitutions.rst

Introduction
============

A distributed system is an interconnected collection of autonomous processes. A traversal algorithm is a distributed algorithm that visits all the processes in a distributed system and returns to the initiator process. This traversal can be used to collect information about the system, to perform a computation, or to perform a task. The traversal algorithm is a fundamental building block in distributed systems.

Traversal algorithm should be efficient, fault-tolerant, and scalable in the context of distributed systems. Otherwise, the traversal algorithm may not be able to complete the traversal or may not be able to return the result to the initiator process. Thus, requested information may not be collected, computation may not be performed, or task may not be completed.

Negative consequences of inefficient wave traversal in distributed systems include:

- Task Incompletion: Wave traversal might also be utilized for task execution across the distributed system, where each process contributes to completing a larger task. If the traversal is not done properly, some processes may not receive the necessary instructions or data to complete their part of the task. As a result, the overall task might remain incomplete or produce incorrect outcomes.

- Increased Latency and Overhead: Inefficient wave traversal can result in increased latency and overhead in the system. Processes might spend more time waiting for traversal messages or processing unnecessary information, leading to slower response times and reduced system throughput. This can impair the system's responsiveness and scalability, particularly in real-time or high-throughput applications.

- Resource Imbalance: Inefficient wave traversal can lead to resource imbalances among processes in the system. Some processes might be overloaded with tasks or data, while others remain underutilized. This imbalance can degrade the overall performance and scalability of the distributed system, as it fails to effectively utilize all available resources.

It becomes evident that ensuring an efficient and stable traversal algorithm is of paramount importance in distributed systems. By leveraging traversal algorithms like Awerbuch's or Cidon's, which optimize message passing and eliminate unnecessary waiting times, distributed systems can better manage resource allocation, mitigate imbalances, and enhance overall system performance and resilience. Thus, investing in the development and optimization of traversal algorithms is crucial for building robust and scalable distributed systems capable of meeting the demands of modern applications and services.

- Awerbuch's traversal algorithm is based on depth-first search and acknowledgment messages between the initiator process and the neighbor processes. [Awerbuch1985]_

- Cidon's traversal algorithm further improves the Awerbuch's traversal algorithm by abolishing the wait for acknowledgment messages from the neighbors. [Cidon1988]_

Our primary contributions consist of the following:

- Implementations of the Awerbuch's and Cidon's traversal algorithms in Python using AHC framework.

- Experiments to evaluate the performance of the Awerbuch's and Cidon's traversal algorithms in terms of the number of messages exchanged, the number of rounds, and the time taken to complete the traversal.

- Comparison of the performance of the Awerbuch's and Cidon's traversal algorithms in different network topologies and different network sizes.

- Comprehensive analysis and discussion of possible improvements to the Awerbuch's and Cidon's traversal algorithms.
