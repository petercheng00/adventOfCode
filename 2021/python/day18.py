import math
import sys
from typing import Optional, Union

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


class SFNode:
    def __init__(
        self,
        left: Union["SFNode", "SFLeaf"],
        right: Union["SFNode", "SFLeaf"],
        parent: Optional["SFNode"] = None,
    ):
        self.left = left
        self.right = right
        self.parent = parent
        self.left.parent = self
        self.right.parent = self

    def __add__(self, o):
        return SFNode(self, o)

    def __repr__(self):
        return f"[{self.left},{self.right}]"


class SFLeaf:
    def __init__(self, value: int, parent: Optional[SFNode] = None):
        self.value = value
        # Parent gets set when an SFNode is built using this leaf.
        self.parent = parent

    def __repr__(self):
        return str(self.value)


def parse(line: str) -> Union[SFNode, SFLeaf]:
    if line.isdigit():
        return SFLeaf(int(line))
    # The idea is to always find the comma at depth 1, then recursively parse both sides of the string.
    depth = 0
    for i, c in enumerate(line):
        if c == "," and depth == 1:
            return SFNode(left=parse(line[1:i]), right=parse(line[i + 1 : -1]))
        elif c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
    # Shouldn't ever reach here.
    print("Bad Parse!")
    return SFLeaf(-1)


def find_node_to_explode(node: SFNode, nodes_above: int) -> Optional[SFNode]:
    if nodes_above == 4:
        return node
    if isinstance(node.left, SFNode):
        left_result = find_node_to_explode(node.left, nodes_above + 1)
        if left_result:
            return left_result
    if isinstance(node.right, SFNode):
        right_result = find_node_to_explode(node.right, nodes_above + 1)
        if right_result:
            return right_result
    return None


def get_inorder_leaves(node: Union[SFNode, SFLeaf]) -> list[SFLeaf]:
    if isinstance(node, SFLeaf):
        return [node]
    else:
        return get_inorder_leaves(node.left) + get_inorder_leaves(node.right)


def replace_node_with_zero(node: SFNode):
    if node.parent.left == node:
        node.parent.left = SFLeaf(0, node.parent)
    else:
        node.parent.right = SFLeaf(0, node.parent)


def explode_node(root: SFNode, node_to_explode: SFNode) -> None:
    inorder_leaves = get_inorder_leaves(root)

    for i, leaf in enumerate(inorder_leaves):
        if leaf == node_to_explode.left:
            if i > 0:
                inorder_leaves[i - 1].value += node_to_explode.left.value
        elif leaf == node_to_explode.right:
            if i < len(inorder_leaves) - 1:
                inorder_leaves[i + 1].value += node_to_explode.right.value

    replace_node_with_zero(node_to_explode)


def explode_if_possible(root: SFNode) -> bool:
    node_to_explode = find_node_to_explode(root, 0)
    if node_to_explode:
        explode_node(root, node_to_explode)
        return True
    return False


def split_if_possible(root: SFNode) -> bool:
    inorder_leaves = get_inorder_leaves(root)
    for leaf in inorder_leaves:
        if leaf.value >= 10:
            new_l_leaf = SFLeaf(math.floor(leaf.value / 2))
            new_r_leaf = SFLeaf(math.ceil(leaf.value / 2))
            new_node = SFNode(new_l_leaf, new_r_leaf, leaf.parent)
            if leaf.parent.left == leaf:
                leaf.parent.left = new_node
            else:
                leaf.parent.right = new_node
            return True

    return False


def reduce(num: SFNode) -> None:
    while True:
        if explode_if_possible(num):
            continue
        if split_if_possible(num):
            continue
        return


def magnitude(x: Union[SFNode, SFLeaf]) -> int:
    if isinstance(x, SFLeaf):
        return x.value
    return 3 * magnitude(x.left) + 2 * magnitude(x.right)


def part1():
    nums = [parse(line) for line in lines]
    result = nums[0]
    for num in nums[1:]:
        result = result + num
        reduce(result)
    print(magnitude(result))


def part2():
    # We're modifying all sorts of stuff in place, so as a hack, just reparse each time.
    max_magnitude = 0
    for a in lines:
        for b in lines:
            if a == b:
                continue
            sum = parse(a) + parse(b)
            reduce(sum)
            max_magnitude = max(max_magnitude, magnitude(sum))
    print(max_magnitude)


part1()
part2()
