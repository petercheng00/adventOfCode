from __future__ import annotations
from dataclasses import dataclass
import sys
from typing import Optional


def get_linked_list():
    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()
    nums = [int(x) for x in lines]

    # Create a doubly linked list.
    nodes = [Node(x) for x in nums]
    ll_len = len(nodes)
    for i in range(len(nodes)):
        nodes[i].next_node = nodes[(i + 1) % ll_len]
        nodes[(i + 1) % ll_len].prev_node = nodes[i]

    return nodes, ll_len


@dataclass
class Node:
    value: int
    prev_node: Optional[Node] = None
    next_node: Optional[Node] = None


def shift_node_fwd(node: Node, amount: int):
    if amount == 0:
        return
    # Close the gap we create by removing the node.
    node.prev_node.next_node = node.next_node
    node.next_node.prev_node = node.prev_node
    current = node
    for i in range(amount):
        current = current.next_node

    # Drop in the node.
    node.prev_node = current
    node.next_node = current.next_node
    node.prev_node.next_node = node
    node.next_node.prev_node = node


def print_nodes(node: Node):
    print(node.value)
    current = node.next_node
    while current != node:
        print(current.value)
        current = current.next_node


def get_after(node: Node, amount: int):
    """Get the node [amount] spots after node."""
    current = node
    for i in range(amount):
        current = current.next_node
    return current


def part1():
    nodes, ll_len = get_linked_list()

    for node in nodes:
        shift_amount = node.value % (ll_len - 1)
        shift_node_fwd(node, shift_amount)

    # Find the node with value 0
    val0_node = nodes[0]
    while val0_node.value != 0:
        val0_node = val0_node.next_node

    node_1000 = get_after(val0_node, 1000 % ll_len)
    node_2000 = get_after(val0_node, 2000 % ll_len)
    node_3000 = get_after(val0_node, 3000 % ll_len)
    print(node_1000.value + node_2000.value + node_3000.value)


def part2():
    DECRYPTION_KEY = 811589153
    nodes, ll_len = get_linked_list()
    for n in nodes:
        n.value *= DECRYPTION_KEY

    for i in range(10):
        print(f"Pass {i}...")
        for node in nodes:
            shift_amount = node.value % (ll_len - 1)
            shift_node_fwd(node, shift_amount)

    # Find the node with value 0
    val0_node = nodes[0]
    while val0_node.value != 0:
        val0_node = val0_node.next_node

    node_1000 = get_after(val0_node, 1000 % ll_len)
    node_2000 = get_after(val0_node, 2000 % ll_len)
    node_3000 = get_after(val0_node, 3000 % ll_len)
    print(node_1000.value + node_2000.value + node_3000.value)


part1()
part2()
