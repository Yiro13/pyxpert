class Rule:
    def __init__(self, condition: dict, conclusion: str) -> None:
        self.condition = condition
        self.conclusion = conclusion

    def getRule(self) -> str:
        rule = "if "
        for x, y in self.condition.items():
            rule += x + " -> " + str(y) + ", "

        rule += "then " + self.conclusion

        return rule
