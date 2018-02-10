#!/usr/bin/python3
# -*- coding_ utf-8 -*-

"""
This program implements a parser and data structure for Petri net files.

Original author: Copyright (c) 2015 Thomas Irgang
see MIT license: https://github.com/irgangla/pntools/blob/master/LICENSE

This program implements an XML parser and a python data structure for
Petri nets/PNML.
"""

import sys # argv for test file path
import xml.etree.ElementTree as ET # XML parser
import time # timestamp for id generation
from random import randint # random number for id generation

class PetriNet(object):
    """ This class represents a Petri net.

    This class represents a Petri net. A Petri net consists of
    a set of labelled labelled transitions, labelled places and
    arcs from places to transitions or transitions to places.

    net.edges: List of all edges of this Petri net
    net.transitions: Map of (id, transition) of all transisions of this Petri net
    net.places: Map of (id, place) of all places of this Petri net
    """

    def __init__(self):
        self.edges = [] # List or arcs
        self.transitions = {} # Map of transitions. Key: transition id, Value: event
        self.places = {} # Map of places. Key: place id, Value: place
        self.roles = [] # use roles to model inhibitor arc actors
        self.name = None

    def __str__(self):
        text = '--- Net: ' + self.name + '\nTransitions: '
        for transition in self.transitions.values():
            text += str(transition) + ' '
        text += '\nPlaces: '
        for place in self.places.values():
            text += str(place) + ' '
        text += '\n'
        for edge in self.edges:
            text += str(edge) + '\n'
        text += '---'

        return text

class Transition(object):
    """ This class represents a labelled transition of a Petri net.

    A transition represents an activity.

    transition.id: Unique ID of this transition.
    transition.label: Label of this transition.

    Layout information:
      transition.position: Position to display the transition in graphical representations.
        Usually a transition is drawn as a square. The position is the center of this square.
      transition.offset: Offest of the transition label.
        Usually the label of a transition is printed centered below the square which
        represents the transition in graphical representations. This offset represents
        a vector which defines a translation of the label inscription from its
        usual position.
    """

    def __init__(self):
        self.label = "Transition" # default label of event
        #generate a unique id
        self.id = ("Transition" + str(time.time())) + str(randint(0, 1000))
        self.offset = [0, 0]
        self.position = [0, 0]
        self.net = None

    def __str__(self):
        return self.label


class Place(object):
    """ This class represents a labelled Place of a Petri net.

    A place represents a resource.

    place.id: Unique ID of this place.
    place.label: Label of this place.
    place.marking: Current marking of this place.
      Usually a marking is the count of tokens contained into this place.

    Layout information:
      place.position: Position to display the place in graphical representations.
        Usually a place is drawn as a circle. The position is the center of this circel.
      place.offset: Offest of the place label.
        Usually the label of a place is printed centered below the circle which
        represents the place in graphical representations. This offset represents
        a vector which defines a translation of the label inscription from its
        usual position.
    """

    def __init__(self):
        self.label = "Place" # default label of event
        #generate a unique id
        self.id = ("Place" + str(time.time())) + str(randint(0, 1000))
        self.offset = [0, 0]
        self.position = [0, 0]
        self.marking = 0

    def __str__(self):
        return self.label


class Edge(object):
    """ This class represents an arc of a Petri net.

    An edge represents an relation between a place and a transition or a transition
    and a place.

    edge.id: Unique ID of this edge.
    edge.source: ID of the source (start) node of this edge.
    edge.target: ID of the target (end) node of this edge.
    edge.inscription: Inscription of this edge.
      The inscription is usually an integer which is interpreted as weight of this edge.
    edge.net: The Petri net which contains this edge.
      This reference is used for the label resolution of the source and target events.
      See __str__ method.
    """

    def __init__(self):
        #generate a unique id
        self.id = ("Arc" + str(time.time())) + str(randint(0, 1000))
        self.source = None # id of the source event of this arc
        self.target = None # id of the target event of this arc
        self.inscription = "1" # inscription of this arc
        self.net = None # Reference to net object for label resolution of source an target

        self.inhibitor = False
        self.role = None


    def find_source(self):
        """ find source of txn """
        if self.source in self.net.transitions:
            return self.net.transitions[self.source]

        return self.net.places[self.source]

    def find_target(self):
        """ find txn target """
        if self.target in self.net.transitions:
            return self.net.transitions[self.target]

        return self.net.places[self.target]

    def __str__(self):
        return str(self.find_source()) + "-->" + str(self.find_target())


def parse_pnml_file(filename):
    """ This method parse all Petri nets of the given file.

    This method expects a path to a VipTool pnml file which
    represent a Petri net (.pnml), parse all Petri nets
    from the file and returns the Petri nets as list of PetriNet
    objects.

    XML format:
    <pnml>
      <net id="...">
        (<page>)
        <name>
          <text>name of Petri net</text>
        </name>
        <transition id="...">
          <name>
            <text>label of transition</text>
            <graphics>
              <offset x="0" y="0"/>
            </graphics>
          </name>
          <graphics>
            <position x="73" y="149"/>
          </graphics>
        </transition>
        ...
        <place id="...">
          <name>
            <text>label of transition</text>
            <graphics>
              <offset x="0" y="0"/>
            </graphics>
          </name>
          <graphics>
            <position x="73" y="149"/>
          </graphics>
          <initialMarking>
            <text>1</text>
          </initialMarking>
        </place>
        ...
        <arc id="..." source="id of source event" target="id of target event">
          <inscription>
            <text>1</text>
          </inscription>
        </arc>
        ...
        (</page>)
      </net>
      ...
    </pnml>
    """
    tree = ET.parse(filename) # parse XML with ElementTree
    root = tree.getroot()

    nets = [] # list for parsed PetriNet objects

    for net_node in root.iter('net'):
        # create PetriNet object
        net = PetriNet()
        nets.append(net)
        net.name = net_node.get('id')

        # and parse transitions
        for transition_node in net_node.iter('transition'):
            transition = Transition()
            transition.id = transition_node.get('id')
            transition.label = transition.id
            off_node = transition_node.find('./name/graphics/offset')
            transition.offset = [float(off_node.get('x')), float(off_node.get('y'))]
            position_node = transition_node.find('./graphics/position')
            transition.position = [float(position_node.get('x')), float(position_node.get('y'))]

            net.transitions[transition.id] = transition
            transition.net = net

        # and parse places
        for place_node in net_node.iter('place'):
            place = Place()
            place.id = place_node.get('id')
            place.label = place.id
            off_node = place_node.find('./name/graphics/offset')
            place.offset = [float(off_node.get('x')), float(off_node.get('y'))]
            position_node = place_node.find('./graphics/position')
            place.position = [float(position_node.get('x')), float(position_node.get('y'))]

            marking_str = place_node.find('./initialMarking/value')

            if marking_str.text:
                place.marking = int(marking_str.text.split(',')[1])
            else:
                place.marking = 0

            net.places[place.id] = place

        # and arcs
        for arc_node in net_node.iter('arc'):
            edge = Edge()
            net.edges.append(edge)

            edge.id = arc_node.get('id')
            edge.source = arc_node.get('source')
            edge.target = arc_node.get('target')
            #edge.inscription = float(arc_node.find('./inscription/text').text)
            arc_type = arc_node.find('type').get('value')

            if arc_type == 'inhibitor':
                # TODO use edge.source to determine if this arc expresses a role or
                # if the source yields a token
                # record 'roles' accordingly
                edge.inhibitor = True

            edge.net = net

    return nets

if __name__ == "__main__":

    for pnet in parse_pnml_file(sys.argv[1]):
        print(pnet)
