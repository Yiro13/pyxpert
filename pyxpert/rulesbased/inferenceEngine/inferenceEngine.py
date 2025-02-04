from rulesbased.inferenceEngine.node import Node


class InferenceEngine:
    def __init__(self, knowledgeBase) -> None:
        self.knowledgeBase = knowledgeBase

    def getNodes(self):
        return self.nodes

    def _nodeExists(self, node: Node) -> bool:
        for nodes in self.nodes:
            if nodes.fact == node.fact:
                return True

        return False

    def genGraph(self) -> None:
        self.nodes = []
        for rule in self.knowledgeBase.rules:
            conc = Node(fact=rule.conclusion)
            for fact in rule.fact.keys():
                node = Node(fact=fact)
                conc.ant.append(node)
                node.next = conc

                if not self._nodeExists(node=node):
                    self.nodes.append(node)

            self.nodes.append(conc)
