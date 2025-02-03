class Rule:
    def __init__(self, fact: dict, conclusion: str) -> None:
        self.fact = fact
        self.conclusion = conclusion

    def getRule(self) -> str:
        rule = "If "
        for x, y in self.fact.items():
            rule += x + " -> " + str(y) + ", "

        rule += "Then " + self.conclusion

        return rule
