from copy import deepcopy


class Node:
    def __init__(self, id, row, p1, p2, level, hnf):
        self.id = id
        self.row = row
        self.p1 = p1
        self.p2 = p2
        self.level = level
        self.hnf = hnf


class Game_tree:
    def __init__(self):
        self.node_set = []
        self.branch_set = dict()

    def add_node(self, Node):
        self.node_set.append(Node)

    def add_branch(self, beginNode_id, endNode_id):
        self.branch_set[beginNode_id] = self.branch_set.get(beginNode_id, []) + [endNode_id]


def assign_id():
    global node_counter
    id_new = 'N' + str(node_counter)
    node_counter += 1
    return id_new


def check_duplicate(new_node, curr_node, gen_nodes, id_new, row_new, p1_new, p2_new, level_new, hnf_new):
    same_node_check = False
    j = 0
    while (not same_node_check) and (j < len(current_tree.node_set)):
        if (current_tree.node_set[j].row == new_node.row) and (
                current_tree.node_set[j].p1 == new_node.p1) and (
                current_tree.node_set[j].p2 == new_node.p2) and (
                current_tree.node_set[j].level == new_node.level)\
                and (current_tree.node_set[j].hnf == new_node.hnf):
            same_node_check = True
        else:
            j += 1
    if not same_node_check:
        current_tree.add_node(new_node)
        gen_nodes.append(Node(id_new, row_new, p1_new, p2_new, level_new, hnf_new))
        current_tree.add_branch(curr_node.id, id_new)
    else:
        global node_counter
        node_counter -= 1
        current_tree.add_branch(curr_node.id, current_tree.node_set[j].id)


def turn_check(turn_type, gen_nodes, curr_node):
    curr_length = len(curr_node.row)
    if turn_type == 'sum':
        if curr_length > 1:
            iter_length = curr_length
            if curr_length % 2 == 1:
                iter_length -= 1
            for i in range(0, iter_length, 2):
                row_new = deepcopy(curr_node.row)
                number1 = row_new.pop(i + 1)
                number2 = row_new.pop(i)
                sum = number1 + number2
                number_new = sum
                if sum > 6:
                    if sum == 7:
                        number_new = 1
                    elif sum == 8:
                        number_new = 2
                    elif sum == 9:
                        number_new = 3
                    elif sum == 10:
                        number_new = 4
                    elif sum == 11:
                        number_new = 5
                    elif sum == 12:
                        number_new = 6
                row_new.insert(i, number_new)
                plus_points = 1
                if number_new == 4 or number_new == 5 or number_new == 6:
                    plus_points = 2
                f1 = plus_points
                if (curr_node.level % 2) == 0:
                    p1_new = curr_node.p1
                    p2_new = curr_node.p2 + plus_points
                else:
                    p1_new = curr_node.p1 + plus_points
                    p2_new = curr_node.p2
                level_new = curr_node.level + 1
                id_new = assign_id()
                iter_new_row = len(row_new)
                if iter_new_row % 2 == 1:
                    iter_new_row -= 1
                f2 = 1
                for j in range(0, iter_new_row, 2):
                    if (4 <= row_new[j] + row_new[j + 1] <= 6) or row_new[j] + row_new[j + 1] >= 10:
                        f2 = 0
                        break
                hnf_new = f1 + f2
                new_node = Node(id_new, row_new, p1_new, p2_new, level_new, hnf_new)
                check_duplicate(new_node, curr_node, gen_nodes, id_new, row_new, p1_new, p2_new, level_new, hnf_new)

    if turn_type == 'erase':
        if curr_length > 1 and curr_length % 2 == 1:
            row_new = deepcopy(curr_node.row)
            row_new.pop()
            if (curr_node.level % 2) == 0:
                p1_new = curr_node.p1 - 1
                p2_new = curr_node.p2
            else:
                p1_new = curr_node.p1
                p2_new = curr_node.p2 - 1
            level_new = curr_node.level + 1
            id_new = assign_id()
            f1 = 1
            f2 = 1
            for j in range(0, len(row_new), 2):
                if (4 <= row_new[j] + row_new[j + 1] <= 6) or row_new[j] + row_new[j + 1] >= 10:
                    f2 = 0
                    break
            hnf_new = f1 + f2
            new_node = Node(id_new, row_new, p1_new, p2_new, level_new, hnf_new)
            check_duplicate(new_node, curr_node, gen_nodes, id_new, row_new, p1_new, p2_new, level_new, hnf_new)


current_tree = Game_tree()
generated_nodes = []
current_tree.add_node(Node('N1', [6,4,1,2], 0, 0, 1, 0))
generated_nodes.append(Node('N1', [6,4,1,2], 0, 0, 1, 0))
node_counter = 2
while len(generated_nodes) > 0:
    current_node = generated_nodes[0]
    turn_check('sum',generated_nodes,current_node)
    turn_check('erase',generated_nodes,current_node)
    generated_nodes.pop(0)

for node in current_tree.node_set:
    print(node.id, node.row, node.p1, node.p2, node.level, node.hnf)
for node, branches in current_tree.branch_set.items():
    print(node, branches)
