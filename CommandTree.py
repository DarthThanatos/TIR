# [floor];[room];[device];[ID];[operation]
from pprint import PrettyPrinter
from time import time

p_print = PrettyPrinter().pprint

class State(object):
    def __init__(self):
        self.state = 0
        self.auto_turned_on = False
        self.timestamp = 0
        self.state = 0

    def isAutoActivated(self):
        if time() - self.timestamp > 5:
            self.auto_turned_on = False
        return self.auto_turned_on

    def setAutoState(self):
        self.state = 1
        self.timestamp = time()
        self.auto_turned_on = True


class Command(object):
    pass

class Add(Command):
    def __init__(self, val, state):
        self.val = val
        self.state = state

    def execute(self, aggregate_val):
        if self.state.isAutoActivated(): print "Could not write, auto_turn_on set"
        else:
            print "Device wrote:",self.val + aggregate_val
            self.state.state = self.val


class Change(Command):
    def __init__(self, state):
        self.state = state

    def execute(self, aggregate_val):
        if self.state.isAutoActivated(): print "Could not write, auto_turn_on set"
        else:
            self.state.state = 0 if self.state.state == 1 else 1
            print "Device changed state to:",self.state.state + aggregate_val

class AdaptToMotion(Command):
    def __init__(self, state):
        self.state = state

    def execute(self, aggregate_val):
        self.state.setAutoState()
        print "Device set autoset:",self.state.state + aggregate_val



class CommandTree:
    def __init__(self):

        state = State()
        addZero = Add(0, state)
        addOne = Add(1, state)
        change = Change(state)
        adaptToMotion = AdaptToMotion(state)

        devices = ["lamp", "shutter"]
        devices_vals = {"lamp": 32, "shutter": 1000}
        IDs = [ "1", "2"]
        IDs_vals = {"1":0, "2":32}
        operations = ["on", "off", "change", "motion"]
        operations_vals = { "on" : addOne, "off" : addZero, "change": change, "motion" : adaptToMotion}

        root_settings = [(devices,devices_vals), (IDs, IDs_vals), (operations,operations_vals)]
        self.root = self.tree_recursion_level(root_settings)

    def tree_recursion_level(self, lvl_settings):
        # lvl_settings: [(names, names_vals_dict), ...] e.g. [(devices, devices_vals), ...]
        # val - current Node val e.g. = 0
        if lvl_settings.__len__() > 0:
            names, names_vals_dict = lvl_settings[0]
            res = {}
            for name in names:
                node = Node(names_vals_dict[name], name)
                children_dict = self.tree_recursion_level(lvl_settings[1:] if lvl_settings.__len__() > 1 else [])
                node.children = children_dict
                res[name] = node
            asterix_node = AsterixNode(names_vals_dict)
            asterix_node.children = dict(res)
            res["*"] = asterix_node
            return res
        else: return {}

    def execute_command(self, cmd):
        cmd_parts = cmd.split(";")
        if cmd_parts.__len__() != 3:
            print "Incorrect syntax"
            return
        if cmd_parts[2] == "*":
            print "Incorrect syntax"
            return
        try:
            self.root[cmd_parts[0]].execute(cmd, 0)
        except Exception:
            print "Incorrect syntax"

class AbstractNode(object):

    def __init__(self, val = None, name = None):
        self.val = val
        self.name = name
        self.children = {}

class Node(AbstractNode):
    def __init__(self, val=0, name=None):
        super(Node, self).__init__(val,name)

    def execute(self, cmd, val):
        cmd_parts = cmd.split(";")
        #print "\n" + cmd
        #print "children of me:", self.children.keys()
        if self.name == cmd_parts[0]:
            if self.children != {}:
                child = self.children[cmd_parts[1]]
                child.execute(";".join(cmd_parts[1:]), val+ self.val)
            else:
                self.val.execute(val)

class AsterixNode(AbstractNode):
    def __init__(self, vals):
        super(AsterixNode,self).__init__(name = "*")
        self.name = "*"
        self.vals = vals


    def execute(self, cmd,val):
        #print "\n*:",cmd
        #print "children of *:", self.children.keys()
        #print self.vals
        cmd_parts = cmd.split(";")
        if not self.children == {}:
            for name, name_val in self.vals.items():
                self.children[name].execute(name + ";" + ";".join(cmd_parts[1:]), val)
        else:
            raise Exception