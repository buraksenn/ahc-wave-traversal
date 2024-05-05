from adhoccomputing.GenericModel import GenericModel
from adhoccomputing.Generics import *

sourceInstanceNumber = 0


class ApplicationLayerMessageTypes(Enum):
    """
    Enum for the message types in the CidonsDFS algorithm. The message types are START, TOKEN and VISITED
    which are required for the algorithm to work.
    """
    START = "START"
    TOKEN = "TOKEN"
    VISITED = "VISITED"


class NodeState(Enum):
    """
    Enum for the state of the node in the CidonsDFS algorithm
    """
    IDLE = "IDLE"
    DISCOVERED = "DISCOVERED"


class NodeMark(Enum):
    """
    Enum for the mark of the node in the CidonsDFS algorithm. Nodes are marked as VISITED, UNVISITED,
    PARENT or CHILD based on the flow of the algorithm.
    """
    VISITED = "VISITED"
    UNVISITED = "UNVISITED"
    PARENT = "PARENT"
    CHILD = "CHILD"


class ApplicationLayerMessageHeader(GenericMessageHeader):
    """
    Header for the messages in the CidonsDFS algorithm. The header contains the message type, the message from
    and the destination of the message.
    """
    pass


class ApplicationLayerMessagePayload(GenericMessagePayload):
    """
    Payload for the messages in the CidonsDFS algorithm. The payload contains the data that is to be sent
    in the message.
    """
    pass


class CidonsDFS(GenericModel):
    """
    CidonsDFS class is the implementation of the CidonsDFS algorithm. The algorithm is used to traverse a graph
    in a depth first search manner. The algorithm is used to find the minimum spanning tree of a graph. It is a
    subclass of the GenericModel class to use it with the AdHocComputing framework.
    """

    def __init__(self, component_name, component_instance_number, topology=None):
        """
        Constructor for the CidonsDFS class. It registers the event handlers for the messages in the algorithm and
        sets the initial values for the variables used in the algorithm.
        """
        super().__init__(component_name, component_instance_number)
        self.numberOfMessages = None
        self.mark = None
        self.state = None
        self.neighbours = None
        self.eventhandlers[ApplicationLayerMessageTypes.START] = self.on_start
        self.eventhandlers[ApplicationLayerMessageTypes.TOKEN] = self.on_token
        self.eventhandlers[ApplicationLayerMessageTypes.VISITED] = self.on_visited
        self.topology = topology

    def on_init(self, eventobj: Event):
        """
        Method to initialize the node with the required values. It sets the neighbours of the node, the state of the
        node and the mark of the node. It also sends the START message to the source node to start the algorithm.
        """
        self.neighbours = self.topology.get_neighbors(self.componentinstancenumber)
        self.state = NodeState.IDLE
        self.numberOfMessages = 0
        self.mark = [NodeMark.UNVISITED] * len(self.neighbours)

        if self.componentinstancenumber == sourceInstanceNumber:
            destination = self.componentinstancenumber
            new_header = ApplicationLayerMessageHeader(ApplicationLayerMessageTypes.START, self.componentinstancenumber,
                                                       destination)
            self.send_self(
                Event(self, ApplicationLayerMessageTypes.START, GenericMessage(new_header, get_dummy_payload())))
        else:
            pass

    def on_message_from_bottom(self, eventobj: Event):
        """
        Method to handle the messages received from the bottom layer.
        """
        try:
            message = eventobj.eventcontent
            self.send_self(Event(self, message.header.messagetype, message))

        except AttributeError:
            logger.critical("Attribute Error")

    def on_start(self, eventobj: Event):
        """
        Method to handle the START message. If node is in IDLE state, it calls visit_neighbors method to start the
        algorithm.
        """
        if self.state == NodeState.IDLE:
            self.visit_neighbors()

    def visit_neighbors(self):
        """
        Method to visit the neighbours of the node. It sets the state of the node to DISCOVERED and calls the search
        method to start the algorithm. Then visits the neighbours of the node and sends the VISITED message to the
        neighbours.
        """
        self.state = NodeState.DISCOVERED
        self.search()
        for i in self.neighbours:
            if self.mark[i] == NodeMark.VISITED or self.mark[i] == NodeMark.UNVISITED:
                new_header = ApplicationLayerMessageHeader(ApplicationLayerMessageTypes.VISITED,
                                                           self.componentinstancenumber,
                                                           i)
                proposal_message = GenericMessage(new_header, get_dummy_payload())
                self.send_down(Event(self, EventTypes.MFRT, proposal_message))
                self.numberOfMessages += 1

    def on_token(self, eventobj: Event):
        """
        Method to handle the TOKEN message. If the node is in IDLE state, it marks the message from the sender as
        PARENT and calls the visit_neighbors method. If the node is in DISCOVERED state, it marks the message from
        the sender as VISITED and calls the search method.
        """
        message_from = eventobj.eventcontent.header.messagefrom
        if self.state == NodeState.IDLE:
            self.mark[message_from] = NodeMark.PARENT
            self.visit_neighbors()
        else:
            if self.mark[message_from] == NodeMark.UNVISITED:
                self.mark[message_from] = NodeMark.VISITED
            elif self.mark[message_from] == NodeMark.CHILD:
                self.search()

    def on_visited(self, eventobj: Event):
        """
        Method to handle the VISITED message. If the node is in DISCOVERED state, it marks the message from the sender
        as VISITED and calls the search method. If the node is in IDLE state, it marks the message from the sender as
        VISITED.
        """
        message_from = eventobj.eventcontent.header.messagefrom
        if self.mark[message_from] == NodeMark.UNVISITED:
            self.mark[message_from] = NodeMark.VISITED
            return

        if self.mark[message_from] == NodeMark.CHILD:
            self.mark[message_from] = NodeMark.VISITED
            self.search()

    def search(self):
        """
        Method to search for the next node to send the TOKEN message. It sends the TOKEN message to the next node
        based on the mark of the neighbours of the node. If the node is the source node, it sends the TOKEN message
        to the next node based on the mark of the neighbours of the node.
        """
        for i in self.neighbours:
            if self.mark[i] == NodeMark.UNVISITED:
                new_header = ApplicationLayerMessageHeader(ApplicationLayerMessageTypes.TOKEN,
                                                           self.componentinstancenumber,
                                                           i)
                self.send_down(Event(self, EventTypes.MFRT, GenericMessage(new_header, get_dummy_payload())))
                self.numberOfMessages += 1
                self.mark[i] = NodeMark.CHILD
                return
            else:
                pass
        if self.componentinstancenumber == sourceInstanceNumber:
            pass
        else:
            for i in self.neighbours:
                if self.mark[i] == NodeMark.PARENT:
                    new_header = ApplicationLayerMessageHeader(ApplicationLayerMessageTypes.TOKEN,
                                                               self.componentinstancenumber, i)
                    self.send_down(Event(self, EventTypes.MFRT, GenericMessage(new_header, get_dummy_payload())))
                    self.numberOfMessages += 1

                    return


def get_dummy_payload():
    """
    Function to get the dummy payload for the messages in the algorithm.
    """
    return ApplicationLayerMessagePayload("dummy")
