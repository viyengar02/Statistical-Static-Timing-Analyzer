class OP:
    def __init__(self,gate,op,cost,delay):
        self.gate = gate
        self.op = op
        self.cost = cost
        self.a = delay
        self.a0 = delay[0]
        self.a1 = delay[1]
        self.a2 = delay[2]
        self.a3 = delay[3]
    def create_empty_op(gate):
        return OP(gate, 'DFF', 0, [0,0,0,0])
