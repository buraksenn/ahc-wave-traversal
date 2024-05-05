import random

from adhoccomputing.GenericModel import GenericModel
from adhoccomputing.Generics import *


class ApplicationLayerMessageTypes(Enum):
    """
    Enum class for Application Layer Message Types in AwerbuchsDFS which are used to identify the type of message and conduct the appropriate action.
    ACK: Acknowledgement message is used to acknowledge the receipt of a message in AwerbuchsDFS.
    DISCOVER: Discover message is used to discover the neighbours of a node in AwerbuchsDFS.
    RETURN: Return message is used to return to the parent node in AwerbuchsDFS.
    VISITED: Visited message is used to mark the node as visited in AwerbuchsDFS.
    """
    ACK = "ACK"
    DISCOVER = "DISCOVER"
    RETURN = "RETURN"
    VISITED = "VISITED"


class ApplicationLayerMessageHeader(GenericMessageHeader):
    """
    Class for Application Layer Message Header in AwerbuchsDFS which is used to store the header information of the
    message. It is the same as the GenericMessageHeader class.
    """
    pass


class ApplicationLayerMessagePayload(GenericMessagePayload):
    """
    Class for Application Layer Message Payload in AwerbuchsDFS which is used to store the payload information of the
    message. It is the same as the GenericMessagePayload class.
    """
    pass


class AwerbuchsDFS(GenericModel):
    """
    Class for AwerbuchsDFS which is used to implement the AwerbuchsDFS algorithm. It is a subclass of the GenericModel to use with AdHocComputing framework.
    """

    def __init__(self, component_name, component_instance_number, topology=None):
        """
        Constructor for AwerbuchsDFS class which initializes the component name, component instance number, number of
        messages, parent, unvisited, neighbours, flag, event handlers and topology. It mostly initializes the variables
        for their empty values and call the super class constructor.
        """
        super().__init__(component_name, component_instance_number)
        self.numberOfMessages = None
        self.parent = None
        self.unvisited = None
        self.neighbours = None
        self.flag = None
        self.eventhandlers[ApplicationLayerMessageTypes.DISCOVER] = self.on_discover
        self.eventhandlers[ApplicationLayerMessageTypes.RETURN] = self.on_return
        self.eventhandlers[ApplicationLayerMessageTypes.VISITED] = self.on_visited
        self.eventhandlers[ApplicationLayerMessageTypes.ACK] = self.on_ack
        self.topology = topology

    def on_init(self, eventobj: Event):
        """
        Method to initialize the AwerbuchsDFS algorithm. It gets the neighbours of the node from the topology and
        initializes the parent, unvisited, neighbours, flag and sends the DISCOVER message to the neighbours.
        """
        neighbour_list = self.topology.get_neighbors(self.componentinstancenumber)
        self.neighbours = neighbour_list
        self.unvisited = neighbour_list.copy()
        self.parent = self.componentinstancenumber
        self.flag = [0] * len(neighbour_list)

        if self.componentinstancenumber == 0:
            destination = self.componentinstancenumber
            new_header = ApplicationLayerMessageHeader(ApplicationLayerMessageTypes.DISCOVER,
                                                       self.componentinstancenumber,
                                                       destination)
            proposal_message = GenericMessage(new_header, get_dummy_payload())
            self.send_self(Event(self, ApplicationLayerMessageTypes.DISCOVER, proposal_message))
        else:
            pass

    def on_message_from_bottom(self, eventobj: Event):
        """
        Method to handle the message from the bottom layer. It gets the message from the event object and sends the
        message to the itself.
        """
        try:
            message = eventobj.eventcontent
            self.send_self(Event(self, message.header.messagetype, message))

        except AttributeError:
            logger.error("Attribute Error")

    def on_discover(self, eventobj: Event):
        """
        Method to handle the DISCOVER message. It gets the message from the event object and sends the VISITED message
        to the neighbours except the parent. If the node has only one neighbour, and it is the parent, it sends
        the RETURN message to the parent.
        """
        self.parent = eventobj.eventcontent.header.messagefrom
        for i in self.neighbours:
            if i != self.parent:
                self.flag[i] = 1
                new_header = ApplicationLayerMessageHeader(ApplicationLayerMessageTypes.VISITED,
                                                           self.componentinstancenumber, i)
                proposal_message = GenericMessage(new_header, get_dummy_payload())
                self.send_down(Event(self, EventTypes.MFRT, proposal_message))
                self.numberOfMessages += 1
            else:
                pass

        if len(self.neighbours) == 1 and self.neighbours[0] == self.parent:
            new_header = ApplicationLayerMessageHeader(ApplicationLayerMessageTypes.RETURN,
                                                       self.componentinstancenumber,
                                                       self.neighbours[0])
            proposal_message = GenericMessage(new_header, get_dummy_payload())
            self.send_down(Event(self, EventTypes.MFRT, proposal_message))
            self.numberOfMessages += 1

    def on_return(self, eventobj: Event):
        """
        Method to handle the RETURN message. It gets the message from the event object and sends the RETURN message to
        the parent if the node has no unvisited neighbours. Otherwise, it sends the DISCOVER message to the unvisited
        neighbours.
        """
        if not self.unvisited:
            if self.parent != self.componentinstancenumber:
                new_header = ApplicationLayerMessageHeader(ApplicationLayerMessageTypes.RETURN,
                                                           self.componentinstancenumber,
                                                           self.parent)
                proposal_message = GenericMessage(new_header, get_dummy_payload())
                self.send_down(Event(self, EventTypes.MFRT, proposal_message))
                self.numberOfMessages += 1
        else:
            destination = random.choice(self.unvisited)
            new_header = ApplicationLayerMessageHeader(ApplicationLayerMessageTypes.DISCOVER,
                                                       self.componentinstancenumber,
                                                       destination)
            self.send_down(Event(self, EventTypes.MFRT, GenericMessage(new_header, get_dummy_payload())))
            self.numberOfMessages += 1
            self.unvisited.remove(destination)

    def on_visited(self, eventobj: Event):
        """
        Method to handle the VISITED message. It gets the message from the event object and removes the node from the
        unvisited list. It sends the ACK message to the sender of the VISITED message.
        """
        message_from = eventobj.eventcontent.message.header.messageform
        self.unvisited.remove(message_from)
        new_header = ApplicationLayerMessageHeader(ApplicationLayerMessageTypes.ACK, self.componentinstancenumber,
                                                   message_from)
        self.send_down(Event(self, EventTypes.MFRT, GenericMessage(new_header, get_dummy_payload())))
        self.numberOfMessages += 1

    def on_ack(self, eventobj: Event):
        """
        Method to handle the ACK message. It gets the message from the event object and decrements the flag of the
        sender of the ACK message. If the sum of all the flags is 0, it sends the RETURN message to the parent.
        """
        message = eventobj.eventcontent
        self.flag[message.header.messagefrom] = 0

        sum_of_all = sum(self.flag)
        if sum_of_all != 0:
            return

        self.send_self(Event(self, ApplicationLayerMessageTypes.RETURN, message))


def get_dummy_payload():
    """
    Method to get the dummy payload. It returns the ApplicationLayerMessagePayload with the dummy value.
    """
    return ApplicationLayerMessagePayload("dummy")
