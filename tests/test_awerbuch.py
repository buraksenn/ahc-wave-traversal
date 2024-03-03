#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.getcwd())

from adhoccomputing.Generics import *
from adhoccomputing.Experimentation.Topology import Topology
from adhoccomputing.Networking.LogicalChannels.GenericChannel import GenericChannel


# Wrap Snapshot in a node model!

def main():
    setAHCLogLevel(DEBUG)
    topo = Topology()
    # A larger topology is required for testing
    # Test Awerbuch's DFS here.


if __name__ == "__main__":
    exit(main())