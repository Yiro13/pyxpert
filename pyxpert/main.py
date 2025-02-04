from rulesbased.knowledgeBase.rule import Rule
from rulesbased.knowledgeBase.knowledgeBase import KnowledgeBase
from rulesbased.inferenceEngine.inferenceEngine import InferenceEngine

condition = {"A": True, "B": True}
rule = Rule(fact=condition, conclusion="C")

condition1 = {"D": True, "E": True, "F": True}
rule1 = Rule(fact=condition1, conclusion="G")

condition2 = {"H": True, "I": True}
rule2 = Rule(fact=condition2, conclusion="J")

condition3 = {"C": True, "G": True}
rule3 = Rule(fact=condition3, conclusion="K")

condition4 = {"J": True, "G": True}
rule4 = Rule(fact=condition4, conclusion="L")

condition5 = {"K": True, "L": True}
rule5 = Rule(fact=condition5, conclusion="M")

kb = KnowledgeBase()

kb.addRule(rule=rule)
kb.addRule(rule=rule1)
kb.addRule(rule=rule2)
kb.addRule(rule=rule3)
kb.addRule(rule=rule4)
kb.addRule(rule=rule5)

ie = InferenceEngine(knowledgeBase=kb)

ie.forwardChain()
