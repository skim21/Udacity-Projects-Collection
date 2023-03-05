
class ValveDropExtend:

    def __init__(self, valves):
        self.valves = valves
        self.visited = []
        self.valve_drop_extend = []

    def get_one_step_extend(self, u):
        return [k for k,v in self.valves.items() if (u in k)&(v==0)]

    def get(self, vd):
        temp = []
        for u in vd:
            one_step_extend = self.get_one_step_extend(u)
            if len(one_step_extend)>0:
                valve_drop_extend.extend(one_step_extend)
                temp.append(one_step_extend)
                vd = temp.pop()
        

                        
        return valve_drop_extend
