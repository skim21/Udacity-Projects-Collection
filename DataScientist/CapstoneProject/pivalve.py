from loopOps import Loops
from checkLoops import CheckLoops
import numpy as np
from pprint import pprint

class PIValve(Loops):
    def __init__(self, loops) -> None:
        super().__init__(loops)
        self.ve = self.get_valve_id()
        self.n = 3

    def get_valve_id(self):
        for v in self.valves:
            yield v

    def is_done(self, v_tag):
        return v_tag == list(self.valves.keys())[-1]

    def step(self, a):
        v_tag = next(self.ve)
        if a == 0:
            self.drop_valve(v_tag)
            
            if valve_checkup(self,  self.n):
                reward = 1
            else:
                self.restore_valve(v_tag)
                reward = 0
        else:
            reward = 0        

        done = self.is_done(v_tag)
        return np.fromiter(self.valves.values(), dtype=float), reward, done

    def get_no_valves(self):
        return sum(self.valves.values()), len(self.valves)

    def reset(self):
        self.initiate_valves()
        self.ve = self.get_valve_id()
        return np.fromiter(self.valves.values(), dtype=float)

    def close(self):
        #print(self.valves)
        no_valves, total = self.get_no_valves()
        print("Total number of valves:\n  {} in {}".format(no_valves, total) )
        #print(self.valve_drop_extend)

def valve_checkup(object, n, verbose=False):
    get_valve_drop_extend(object)
    
    check = CheckLoops(object.valve_drop_extend, n, object.joints)
    check.get_no_connected_units()

    if check.issatisfied():
        return True
    else:
        return False

    if verbose:
        if check.issatisfied():
            print("Check completed... Valves located fine!")
        else:
            print('*'*25)
            print("No Good! Check Valve Locations")
            print('*'*25)

def get_valve_drop_extend(object):
    valve_drops = object.get_valve_drop_location()
    visited = set()
    valve_drop_extend = []
    buffer = set()
    for vd in valve_drops:
        vde = set()
        if vd in visited:
            pass
        else:
            visited.add(vd)
            vde.add(vd)
            buffer.add(vd)
            while len(buffer)>0:
                b = buffer.pop()
                for u in b:
                    one_step_extend = object.get_one_step_extend(u, b)
                    for ose in one_step_extend:
                        if (len(one_step_extend)>0)&(ose not in visited):
                            vde.add(ose)
                            visited.add(ose)
                            buffer.add(ose)
        if len(vde)>0:
            valve_drop_extend.append(vde)
    object.valve_drop_extend = valve_drop_extend