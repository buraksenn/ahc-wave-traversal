from adhoccomputing.GenericModel import GenericModel
from adhoccomputing.Generics import *

sourceInstanceNumber = 0


class ApplicationLayerMessageTypes(Enum):
    START = "START"
    TOKEN = "TOKEN"
    VISITED = "VISITED"


class NodeState(Enum):
    IDLE = "IDLE"
    DISCOVERED = "DISCOVERED"


class NodeMark(Enum):
    VISITED = "VISITED"
    UNVISITED = "UNVISITED"
    PARENT = "PARENT"
    CHILD = "CHILD"


class ApplicationLayerMessageHeader(GenericMessageHeader):
    pass


class ApplicationLayerMessagePayload(GenericMessagePayload):
    pass


class CidonDFS(GenericModel):
    def __init__(self, component_name, component_instance_number, topology=None):
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
        try:
            message = eventobj.eventcontent
            self.send_self(Event(self, message.header.messagetype, message))

        except AttributeError:
            logger.critical("Attribute Error")

    def on_start(self, eventobj: Event):
        if self.state == NodeState.IDLE:
            self.visit_neighbors()

    def visit_neighbors(self):
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
        message_from = eventobj.eventcontent.header.messagefrom
        if self.mark[message_from] == NodeMark.UNVISITED:
            self.mark[message_from] = NodeMark.VISITED
            return

        if self.mark[message_from] == NodeMark.CHILD:
            self.mark[message_from] = NodeMark.VISITED
            self.search()

    def search(self):
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
    return ApplicationLayerMessagePayload("dummy")
