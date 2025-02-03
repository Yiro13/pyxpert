from rulesbased.knowledgeBase.rule import Rule
from rulesbased.knowledgeBase.knowledgeBase import KnowledgeBase

condition = {"Tos": True, "Fiebre": True, "Dolor de cabeza": True}
rule = Rule(fact=condition, conclusion="Covid-19")

condition1 = {"Covid-19": True, "Fiebre": False}
rule1 = Rule(fact=condition1, conclusion="Influenza")

kb = KnowledgeBase()

kb.addRule(rule=rule)
kb.addRule(rule=rule1)
print(kb.getKnowledgeBase())
