import numpy as np

class CheckLoops:
    def __init__(self, valve_drop_extend, n, joints) -> None:
        self.valve_drop_extend = valve_drop_extend
        self.connected_units = []
        self.no_connected = []
        self.n = n
        self.joints = joints

    def get_units(self):
        connected_units = []
        for vde in self.valve_drop_extend:
            units = tuple()
            for v in vde:
                units += v
            connected_units.append(set(units))
        self.connected_units = connected_units

    def get_no_connected_units(self):
        self.get_units()
        no_connected = []
        for u in self.connected_units:
            unit = [a for a in u if a not in self.joints]
            no_connected.append(len(unit))
        
        self.no_connected = no_connected

    def issatisfied(self):
        return all(np.array(self.no_connected)<=self.n)