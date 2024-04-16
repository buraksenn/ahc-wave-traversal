import random

from adhoccomputing.GenericModel import GenericModel
from adhoccomputing.Generics import *


class ApplicationLayerMessageTypes(Enum):
    ACK = "ACK"
    DISCOVER = "DISCOVER"
    RETURN = "RETURN"
    VISITED = "VISITED"


class ApplicationLayerMessageHeader(GenericMessageHeader):
    pass


class ApplicationLayerMessagePayload(GenericMessagePayload):
    pass


class AwerbuchsDFS(GenericModel):
    def __init__(self, component_name, component_instance_number, topology=None):
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
        try:
            message = eventobj.eventcontent
            self.send_self(Event(self, message.header.messagetype, message))

        except AttributeError:
            logger.error("Attribute Error")

    def on_discover(self, eventobj: Event):
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
        message_from = eventobj.eventcontent.message.header.messageform
        self.unvisited.remove(message_from)
        new_header = ApplicationLayerMessageHeader(ApplicationLayerMessageTypes.ACK, self.componentinstancenumber,
                                                   message_from)
        self.send_down(Event(self, EventTypes.MFRT, GenericMessage(new_header, get_dummy_payload())))
        self.numberOfMessages += 1

    def on_ack(self, eventobj: Event):
        message = eventobj.eventcontent
        self.flag[message.header.messagefrom] = 0

        sum_of_all = sum(self.flag)
        if sum_of_all != 0:
            return

        self.send_self(Event(self, ApplicationLayerMessageTypes.RETURN, message))


def get_dummy_payload():
    return ApplicationLayerMessagePayload("dummy")
