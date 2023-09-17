import variables as vars

test1 = "Hi, this is a test"
test2 = "Hi, this is also a test"

print(len(vars.llm.tokenize(test1)))
print(len(vars.llm.tokenize(test2)))