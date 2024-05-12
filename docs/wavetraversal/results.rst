.. include:: substitutions.rst

Implementation, Results and Discussion
======================================

Implementation and Methodology
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this section, the implementation of the proposed method is discussed. The proposed method is a combination of implementing Awerbuch's  and Cidon's algorithms. The implementation is done using the Python programming language and using Ad Hoc Computing (AHC) Framework. AHC is a event-driven framework that allows user to simulate distributed systems with different topologies. Awerbuch's and Cidon's algorithms' were published in 1985 and 1989 respectively as papers. Both algorithms had pseudocode implementations and explanations in detail within the papers. These pseudocode implementations and explanations were used to implement the algorithms in Python. The implementation of the algorithms were done in a way that they can be used in AHC framework.

**Awerbuch's Algorithm**

The algorithm implementation was heavily based on the pseudocode provided in the paper. [Awerbuch1985]_. Steps:

- Initialization: The initiator process sends a start message to its neighboring processes to begin traversal.

- Traversal Logic: Each process selects an unvisited neighbor to visit next and sends it a visit message.

- Acknowledgment: Upon receiving a return message from a child process, a process sends an acknowledgment message back to the parent process.

- Termination: The initiator process waits for acknowledgment messages from all neighboring processes to conclude the traversal.

**Cidon's Algorithm**

The algorithm implementation was heavily based on the pseudocode provided in the paper. [Cidon1988]_ Steps:

- Initialization: The initiator process sends a start message to its neighboring processes to initiate traversal.

- Traversal Logic: Each process selects an unvisited neighbor to visit next and sends it a visit message, omitting the wait for acknowledgment messages.

- Acknowledgment: Cidon's algorithm abolishes the acknowledgment messages, thus eliminating the need for acknowledgment handling.


.. [Awerbuch1985] Baruch Awerbuch. A new distributed depth-first search algorithm.  `Online <https://groups.csail.mit.edu/tds/papers/Awerbuch/Info-Process-Letters85.pdf>`_.

.. [Cidon1988] I. Cidon Yet another distributed depth-first-search algorithm.  `Online <https://www.sciencedirect.com/science/article/abs/pii/0020019088901871>`_.


Results
~~~~~~~~

Performance of Awerbuch's Algorithm:

- The algorithm was not tested but considering its message and time complexity it is expected to have a linear increase in the number of messages and time taken as the number of nodes increase.

Performance of Cidon's Algorithm:

- The algorithm was not tested but considering its message and time complexity it is also expected to have a linear increase in the number of messages and time taken as the number of nodes increase.

In addition, It is expected that Cidon's algorithm will perform better than Awerbuch's algorithm as it eliminates the need for acknowledgment messages, thus reducing the algorithm's execution time. This is also reflected in the message complexity of the algorithms, where Cidon's algorithm has a lower time complexity than Awerbuch's algorithm even if they are both linear.