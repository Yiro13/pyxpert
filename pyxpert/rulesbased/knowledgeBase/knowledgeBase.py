from rulesbased.knowledgeBase.rule import Rule


class KnowledgeBase:
    def __init__(self) -> None:
        self.rules = []

    def addRule(self, rule: Rule) -> None:
        self.rules.append(rule)

    def getKnowledgeBase(self) -> str:
        knowledgeBase = "\n-------Knowledge Base------- \n\n"
        if not self.rules:
            knowledgeBase += "Empty Knowledge Base"
            return knowledgeBase

        for rule in self.rules:
            knowledgeBase += "Rule: " + rule.getRule() + "\n"

        return knowledgeBase
