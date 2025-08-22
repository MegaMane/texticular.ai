# https://github.com/JonathanMurray/dialog-tree-py
from typing import List, Optional, Dict

class DialogueChoice:
    def __init__(self, text: str, leads_to_id: str):
        self.text = text
        self.leads_to_id = leads_to_id

class DialogueNode:
    def __init__(self, node_id: str, text: str, choices: List[DialogueChoice]):
        if not node_id:
            raise ValueError("Invalid node config (missing ID)")
        self.node_id = node_id
        self.text = text
        self.choices = choices

class DialogueGraph:
    """
    A graph representation of a dialog

    This class is very central. One instance represents a full dialog. It keeps track of where you are as you progress
    through a dialog.
    """
    def __init__(self, root_node_id: str, nodes: List[DialogueNode], title: Optional[str] = None):
        self.title = title
        self._nodes_by_id: Dict[str, DialogueNode] = {}
        self._active_node_id = root_node_id
        for node in nodes:
            node_id = node.node_id
            if node_id in self._nodes_by_id:
                raise ValueError(f"Duplicate node ID found: {node_id}")
            self._nodes_by_id[node_id] = node

        for node in nodes:
            for choice in node.choices:
                if choice.leads_to_id not in self._nodes_by_id:
                    raise ValueError(
                        f"Dialog choice leading to missing node: {choice.leads_to_id}")

        if root_node_id not in self._nodes_by_id:
            raise ValueError(f"No node found with ID: {root_node_id}")

    def current_node(self) -> DialogueNode:
        return self._nodes_by_id[self._active_node_id]

    def make_choice(self, choice_index: int):
        node = self._nodes_by_id[self._active_node_id]
        self._active_node_id = node.choices[choice_index].leads_to_id

    def nodes(self) -> List[DialogueNode]:
        """ Return the nodes of this graph as a list. Should not needed for normal usage,
         but is used when visualizing the graph with graphviz. """
        return list(self._nodes_by_id.values())

    def __repr__(self):
        return str(self.__dict__)



