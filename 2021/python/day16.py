from __future__ import annotations
from dataclasses import dataclass, field
import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()


def hex2bin(hex_str: str) -> str:
    bin_str = ""
    for hex_char in hex_str:
        value = int(hex_char, 16)
        bin_str += f"{bin(value)[2:]:0>4}"
    return bin_str


@dataclass
class Packet:
    version: int
    type: int
    is_literal: bool
    literal_value: int = -1
    subpackets: list[Packet] = field(default_factory=list)


# We always just pass around the full string.
# Each function takes the start index, and returns the end index. because we don't know how long each packet goes.
# We can return other data besides the end index.
# At that point though, should we just construct packet objects?


def parse_literal_packet(bin_str: str, start_index: int) -> tuple[Packet, int]:
    packet_version = int(bin_str[start_index : start_index + 3], 2)
    packet_type = int(bin_str[start_index + 3 : start_index + 6], 2)

    index = start_index + 6
    value_bin_str = ""
    parsed_last_group = False
    while not parsed_last_group:
        group = bin_str[index : index + 5]
        parsed_last_group = group[0] == "0"
        value_bin_str += group[1:]
        index += 5
    value = int(value_bin_str, 2)

    return (
        Packet(
            version=packet_version,
            type=packet_type,
            is_literal=True,
            literal_value=value,
        ),
        index,
    )


def parse_operator_packet(bin_str: str, start_index: int) -> tuple[Packet, int]:
    packet_version = int(bin_str[start_index : start_index + 3], 2)
    packet_type = int(bin_str[start_index + 3 : start_index + 6], 2)
    length_type_id = bin_str[start_index + 6]
    assert length_type_id == "0" or length_type_id == "1"
    subpackets = []
    if length_type_id == "0":
        # Next 15 bits represent the total length in bits of the subpackets.
        subpackets_bits = int(bin_str[start_index + 7 : start_index + 7 + 15], 2)
        subpackets_start_index = start_index + 7 + 15
        index = subpackets_start_index
        while index < subpackets_start_index + subpackets_bits:
            subpacket, index = parse_packet(bin_str, index)
            subpackets.append(subpacket)
    else:
        # Next 11 bits represent the number of sub packets.
        num_subpackets = int(bin_str[start_index + 7 : start_index + 7 + 11], 2)
        index = start_index + 7 + 11
        for _ in range(num_subpackets):
            subpacket, index = parse_packet(bin_str, index)
            subpackets.append(subpacket)

    return (
        Packet(
            version=packet_version,
            type=packet_type,
            is_literal=False,
            subpackets=subpackets,
        ),
        index,
    )


def parse_packet(bin_str: str, start_index: int) -> tuple[Packet, int]:
    # Parse a packet starting at start index. Return the packet, and the index past the final consumed binary digit.
    packet_type = int(bin_str[start_index + 3 : start_index + 6], 2)
    if packet_type == 4:
        # Literal packet.
        return parse_literal_packet(bin_str, start_index)
    else:
        # Operator packet.
        return parse_operator_packet(bin_str, start_index)


def sum_all_versions(packet: Packet) -> int:
    version = packet.version
    for p in packet.subpackets:
        version += sum_all_versions(p)
    return version


def part1():
    bin_str = hex2bin(lines[0])
    root_packet, _ = parse_packet(bin_str, 0)

    print(sum_all_versions(root_packet))


def eval_packets(packet: Packet) -> int:
    if packet.type == 0:
        return sum(eval_packets(x) for x in packet.subpackets)
    elif packet.type == 1:
        product = 1
        for p in packet.subpackets:
            product *= eval_packets(p)
        return product
    elif packet.type == 2:
        return min(eval_packets(x) for x in packet.subpackets)
    elif packet.type == 3:
        return max(eval_packets(x) for x in packet.subpackets)
    elif packet.type == 4:
        return packet.literal_value
    elif packet.type == 5:
        return (
            1
            if eval_packets(packet.subpackets[0]) > eval_packets(packet.subpackets[1])
            else 0
        )
    elif packet.type == 6:
        return (
            1
            if eval_packets(packet.subpackets[0]) < eval_packets(packet.subpackets[1])
            else 0
        )
    elif packet.type == 7:
        return (
            1
            if eval_packets(packet.subpackets[0]) == eval_packets(packet.subpackets[1])
            else 0
        )
    print("Encountered illegal packet type!")
    return 0


def part2():
    bin_str = hex2bin(lines[0])
    root_packet, _ = parse_packet(bin_str, 0)

    print(eval_packets(root_packet))


part1()
part2()
