.. include:: substitutions.rst

Introduction
============

A distributed system is an interconnected collection of autonomous processes. A traversal algorithm is a distributed algorithm that visits all the processes in a distributed system and returns to the initiator process. This traversal can be used to collect information about the system, to perform a computation, or to perform a task. The traversal algorithm is a fundamental building block in distributed systems.

Traversal algorithm should be efficient, fault-tolerant, and scalable in the context of distributed systems. Otherwise, the traversal algorithm may not be able to complete the traversal or may not be able to return the result to the initiator process. Thus, requested information may not be collected, computation may not be performed, or task may not be completed.

Awerbuch's traversal algortihm is based on depth-first search and acknowledgment messages between the initiator process and the neighbor processes. Cidon's traversal algorithm further improves the Awerbuch's traversal algorithm by abolishing the wait for acknowledgment messages from the neighbors. 

Our primary contributions consist of the following:

- Implementations of the Awerbuch's and Cidon's traversal algorithms in Python using AHC framework.

- Experiments to evaluate the performance of the Awerbuch's and Cidon's traversal algorithms in terms of the number of messages exchanged, the number of rounds, and the time taken to complete the traversal.

- Comparison of the performance of the Awerbuch's and Cidon's traversal algorithms in different network topologies and different network sizes.

- Comprehensive analysis and discussion of possible improvements to the Awerbuch's and Cidon's traversal algorithms.


