import networkx as nx
import matplotlib.pyplot as plt
from rulesbased.inferenceEngine.node import Node


class InferenceEngine:
    def __init__(self, knowledgeBase) -> None:
        self.knowledgeBase = knowledgeBase
        self.nodes = []

    def backwardChain(self, evaluate: str) -> None:
        self._genGraph()
        self.printGraph()
        node = self._getNode(evaluate)
        if node is None:
            print(f"No se encontró el nodo con el hecho '{evaluate}'.")
            return
        resultado = self._eval(node)
        print(f"Resultado de la evaluación para '{evaluate}': {resultado}")

    def _eval(self, node):
        if node.status is not None:
            return node.status

        if not node.ant:
            result = input(f"Ingrese el valor para '{node.fact}' (True/False): ")
            node.status = result.strip().lower() in ["true", "1", "sí", "si"]
            return node.status

        results = []
        for ant in node.ant:
            result_ant = self._eval(ant)
            results.append(result_ant)

        node.status = all(results)
        return node.status

    def _nodeExists(self, node: Node) -> bool:
        for nodes in self.nodes:
            if nodes.fact == node.fact:
                return True

        return False

    def _getNode(self, fact: str) -> Node:
        for node in self.nodes:
            if node.fact == fact:
                return node

        return None

    def _genGraph(self) -> None:
        for rule in self.knowledgeBase.rules:
            conc = self._getNode(rule.conclusion)
            if conc is None:
                conc = Node(fact=rule.conclusion)
                self.nodes.append(conc)

            for fact in rule.fact.keys():
                node = self._getNode(fact)
                if node is None:
                    node = Node(fact=fact)
                    self.nodes.append(node)
                conc.ant.append(node)
                node.next = conc

    def printGraph(self) -> None:
        G = nx.DiGraph()

        for node in self.nodes:
            if node.ant:
                for a in node.ant:
                    G.add_edges_from([(a.fact, node.fact)])
        plt.figure(figsize=(5, 5))
        nx.draw(
            G,
            with_labels=True,
            node_color="green",
            edge_color="gray",
            node_size=2000,
            font_size=16,
        )

        plt.show()
