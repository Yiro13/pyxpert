from rulesbased.knowledgeBase.rule import Rule

condition = {"Tos": True, "Fiebre": True, "Dolor de cabeza": True}
rule = Rule(condition=condition, conclusion="Covid-19")

print(rule.getRule())
