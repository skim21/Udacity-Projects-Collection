from collections import deque
import itertools
import numpy as np
from pprint import pprint

class Loops:
    def __init__(self, loops):
        self.loops = loops
        self.joints = {}
        self.valves = dict()
        self.valve_drop_extend = []

        self.get_joints()
        #print('Joints are:\n', self.joints)

        self.initiate_valves()
        #print('Initiate valves...')

    def checkConecutive(self, d):
        sorted_d = sorted(d)
        if sorted_d == list(range(min(d), max(d)+1)):
            return sorted_d[0], sorted_d[-1]
        else:
            return None

    def get_joints(self):
        joints = set()
        for element in itertools.combinations(self.loops, 2):
            intersects = np.intersect1d(*element)
            if len(intersects)>0:
                for e in element:
                    ints_index = [e.index(a) for a in intersects if a in e]
                    if self.checkConecutive(ints_index):
                        a,b = self.checkConecutive(ints_index)
                        joints.add(e[a])
                        joints.add(e[b]) 
        self.joints = joints

    def initiate_valves(self):
        valves = dict()
        for l in self.loops:
            le = l+[l[0]]
            for a, b in zip(le[:-1], le[1:]):
                key = tuple(sorted((a,b)))
                valves[key] = 1

        self.valves = valves

    def get_valve_drop_location(self):
        return [k for k,v in self.valves.items() if v==0]

    def drop_valve(self, v):
        self.valves[tuple(sorted(v))] = 0        

    def drop_valves(self, remove_valve_list):
        for i in remove_valve_list:
            self.drop_valve(i)

    def restore_valve(self, v_tag):
        self.valves[v_tag] = 1

    def get_one_step_extend(self, u, vde):
        return set(k for k,v in self.valves.items() if (u in k)&(v==0)&(vde!=k))
                

    
