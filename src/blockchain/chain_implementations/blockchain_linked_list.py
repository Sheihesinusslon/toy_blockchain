from typing import List

from pydantic.dataclasses import dataclass

from blockchain.models import Block


@dataclass
class Node:
    block: Block
    next_node: Block | None = None


class LinkedList:
    def __init__(self):
        self.root: Node | None = None
        self.current_node: Node | None = None


class LinkedListChain:
    def __init__(self):
        self.chain = LinkedList()

    def add_block(self, block: Block) -> None:
        if not self.chain.root:
            root_node = Node(block=block)
            self.chain.root = root_node
            self.chain.current_node = self.chain.root
        else:
            new_node = Node(block=block)
            prev_node = self.chain.current_node
            self.chain.current_node = new_node
            prev_node.next_node = new_node

    @property
    def chain_serializable(self) -> List:
        """Convert the linked list chain into a list of block dictionaries."""
        chain_list = []
        current_node = self.chain.root
        while current_node:
            chain_list.append(current_node.block.model_dump())
            current_node = current_node.next_node
        return chain_list

    @property
    def last_block(self) -> Block:
        return self.chain.current_node.block

    def get_block_by_index(self, index: int) -> Block:
        cur_node, cur_idx = self.chain.root, self.chain.root.block.index - 1
        while cur_idx != index:
            cur_node = cur_node.next_node
            cur_idx = cur_node.block.index - 1

        return cur_node.block

    def __repr__(self):
        return f"LinkedListChain(chain={self.chain})"

    def __len__(self):
        return self.chain.current_node.block.index if self.chain.current_node else 0
