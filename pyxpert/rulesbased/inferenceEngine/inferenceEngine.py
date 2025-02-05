from rulesbased.inferenceEngine.node import Node
from PyQt5.QtWidgets import QMessageBox


class InferenceEngine:
    def __init__(self, knowledgeBase, graph_view, main_window) -> None:
        self.knowledgeBase = knowledgeBase
        self.nodes = []
        self.graph_view = graph_view
        self.main_window = main_window
        self.layout_positions = {}

    def ask_user(self, fact: str) -> bool:
        value = self.main_window.get_node_input(fact)
        return value.strip().lower() in ["true", "1", "sí", "si"]

    def backwardChain(self, evaluate: str) -> None:
        self._genGraph()
        self._compute_layout()
        self.graph_view.update_scene(self.nodes, self.layout_positions)
        node = self._getNode(evaluate)
        if node is None:
            QMessageBox.warning(
                self.graph_view,
                "Error",
                f"No se encontró el nodo con el hecho '{evaluate}'.",
            )
            return
        resultado = self._eval(node)
        QMessageBox.information(
            self.graph_view,
            "Resultado",
            f"Resultado de la evaluación para '{evaluate}': {resultado}",
        )
        self.graph_view.update_scene(self.nodes, self.layout_positions)

    def _eval(self, node: Node) -> bool:
        if node.status is not None:
            return node.status

        if not node.ant:
            node.status = self.ask_user(node.fact)
            self.graph_view.update_scene(self.nodes, self.layout_positions)
            return node.status

        results = []
        for ant in node.ant:
            results.append(self._eval(ant))
        node.status = all(results)
        return node.status

    def _nodeExists(self, fact: str) -> bool:
        return any(n.fact == fact for n in self.nodes)

    def _getNode(self, fact: str) -> Node:
        for node in self.nodes:
            if node.fact == fact:
                return node
        return None

    def _genGraph(self) -> None:
        self.nodes = []
        for rule in self.knowledgeBase.rules:
            conc = self._getNode(rule.conclusion)
            if conc is None:
                conc = Node(rule.conclusion)
                self.nodes.append(conc)
            for fact in rule.fact.keys():
                node = self._getNode(fact)
                if node is None:
                    node = Node(fact)
                    self.nodes.append(node)
                if node not in conc.ant:
                    conc.ant.append(node)
                if conc not in node.next:
                    node.next.append(conc)

    def _compute_layout(self) -> None:
        niveles = {}

        def get_level(node: Node):
            if not node.ant:
                return 0
            return max(get_level(ant) for ant in node.ant) + 1

        for node in self.nodes:
            niveles[node.fact] = get_level(node)

        niveles_dict = {}
        for fact, nivel in niveles.items():
            niveles_dict.setdefault(nivel, []).append(fact)

        pos = {}
        ancho_scene = 600
        alto_nivel = 100
        for nivel, facts in niveles_dict.items():
            count = len(facts)
            separacion = ancho_scene / (count + 1)
            for i, fact in enumerate(sorted(facts)):
                x = (i + 1) * separacion
                y = nivel * alto_nivel + 50
                pos[fact] = (x, y)
        self.layout_positions = pos

    def forwardChain(self) -> None:
        hechos = {}
        hechos_basicos = set()
        conclusiones = set(rule.conclusion for rule in self.knowledgeBase.rules)
        for rule in self.knowledgeBase.rules:
            for fact in rule.fact.keys():
                if fact not in conclusiones:
                    hechos_basicos.add(fact)
        for hecho in hechos_basicos:
            val = self.ask_user(hecho)
            hechos[hecho] = val

        inferidos = True
        while inferidos:
            inferidos = False
            for rule in self.knowledgeBase.rules:
                if rule.conclusion in hechos:
                    continue
                condiciones = rule.fact
                if all(hechos.get(cond, False) for cond in condiciones):
                    hechos[rule.conclusion] = True
                    inferidos = True
                elif any(
                    cond in hechos and hechos[cond] is False for cond in condiciones
                ):
                    hechos[rule.conclusion] = False
                    inferidos = True

        self._genGraph()
        for node in self.nodes:
            if node.fact in hechos:
                node.status = hechos[node.fact]
        self._compute_layout()
        self.graph_view.update_scene(self.nodes, self.layout_positions)
        resultado = "\n".join(f"{h}: {v}" for h, v in hechos.items())
        QMessageBox.information(self.graph_view, "Forward Chaining", resultado)

    def reset_tree(self) -> None:
        self._genGraph()
        for node in self.nodes:
            node.status = None
        self._compute_layout()
        self.graph_view.update_scene(self.nodes, self.layout_positions)
