from fastapi import FastAPI
from pydantic import BaseModel
import AICore

title, sum, chunks = AICore.doc_summary("E:\\Users\\nqdhocai\PyCharmProjects\\test\soulcode_coreAI\\assets\Mamba.pdf")
tag = AICore.get_tags(sum)

print(title)
print(sum)
print(tag)
