# Awerbuch and Cidon's Wave Traversal Algorithms:

This is a project for the course CENG 532 Distributed Computing Systems at METU. The project is about implementing and
documenting Awerbuch and Cidon's wave traversal algorithms in distributed systems. The project is
using [AHC framework](https://github.com/cengwins/ahc) which is a framework for design and implement component-based ad
hoc and distributed computing models and algorithms.

The project uses distributed algorithm template repository provided by the WINS lab at METU. The template repository
is [here](https://github.com/cengwins/ahc_distalg_template)

## Structure

The project is structured as a library instead of an application. Awerbuch and Cidon's wave traversal algorithms can be
used in different applications with importing the library. Main folders:

- `WaveTraversal`: The main library folder. It contains the implementation of the algorithms in the following files:
    - [AwerbuchsDFS.py](https://github.com/buraksenn/ahc-wave-traversal/blob/main/WaveTraversal/AwerbuchsDFS.py): The
      implementation of Awerbuch's wave traversal algorithm.
    - [CidonsDFS.py](https://github.com/buraksenn/ahc-wave-traversal/blob/main/WaveTraversal/CidonsDFS.py): The
      implementation of Cidon's wave traversal algorithm.


- `tests`: The folder for the tests of the algorithms. It contains the following files:
    - [test_awerbuch.py](https://github.com/buraksenn/ahc-wave-traversal/blob/main/tests/test_awerbuch.py): The test
      file for Awerbuch's wave traversal algorithm. It tests the algorithm with different
      topologies using AHC.
    - [test_cidon.py](https://github.com/buraksenn/ahc-wave-traversal/blob/main/tests/test_cidon.py): The test file for
      Cidon's wave traversal algorithm. It tests the algorithm with different
      topologies using AHC.

- `docs`: The folder for the documentation of the project. It contains all of the required documentation files for the
  project report. It's format is restructured text (.rst) and it is converted to PDF using Sphinx
  library. [wavetraversal.rst](https://github.com/buraksenn/ahc-wave-traversal/blob/main/docs/wavetraversal/wavetraversal.rst)
  file has the main order of the documentation since the format is to import other .rst files to this file such as
  introduction.rst etc.

- `presentation`: The folder for the presentation of the project. It contains the presentation slides of the project. It
  is in latex format and converted to PDF. The main file
  is [talktemplate.tex](https://github.com/buraksenn/ahc-wave-traversal/blob/main/presentation/talktemplate.tex). 