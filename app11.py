from langchain.tools import PubmedQueryRun

tool = PubmedQueryRun()

answer = tool.run("Creatine and effects on muscle growth")

print(answer)