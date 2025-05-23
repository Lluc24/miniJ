class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class GeneralTree():
    def __init__(self, value, evaluation=None, children=[], color=False):
        self.value = value
        self.evaluation = evaluation
        self.depth = 1
        self.children = children
        self.color = color

    def add_child(self, child):
        self.depth = max(self.depth, child.depth + 1)
        self.children.append(child)

    def get_num_children(self):
        return len(self.children)

    def get_depth(self):
        return self.depth

    def get_evaluation(self):
        if self.evaluation is None:
            return int(self.value)
        else:
            return self.evaluation

    def get_tree_view(self):
        tree_str = str(self.value)
        if self.color:
            tree_str += f"{colors.WARNING} " + str(self.evaluation) + f"{colors.ENDC}"
        else:
            tree_str += " " + str(self.evaluation)
        tree_str += "\n"
        num_children = self.get_num_children()
        for i, child in enumerate(self.children):
            child_str = child.get_tree_view()
            for j, line in enumerate(child_str.split("\n")[:-1]):
                if j == 0:
                    tree_str += ("├── " if i < num_children - 1 else "└── ") + line + "\n"
                else:
                    tree_str += ("|   " if i < num_children - 1 else "    ")  + line + "\n"
        return tree_str


    def __str__(self):
        ret = "( " + str(self.value) + " "
        if self.color:
            ret += f"{colors.WARNING}" + str(self.evaluation) + f"{colors.ENDC} "
        for child in self.children:
            ret += str(child) + " "
        ret += ")"
        return ret
