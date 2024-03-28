.. include:: substitutions.rst
========
Abstract
========

This paper investigates wave traversal algorithms in distributed systems, focusing on Awerbuch's and Cidon's approaches. The goal is to evaluate their performance in terms of message exchange, fault tolerance, and scalability. Awerbuch's algorithm uses depth-first search to prioritize parallel traversal along back edges, while Cidon's algorithm further minimizes message exchange by optimizing acknowledgment handling. The implementation for both algorithms is done in Python using the AHC framework, and experiments are conducted to evaluate performance metrics such as message count, rounds, and traversal time across various network topologies and sizes.

