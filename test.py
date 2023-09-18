from llama_cpp import Llama

llm = Llama(model_path="D:/models/llm/airoboros-l2-7b-2.2.Q4_K_M/airoboros-l2-7b-2.2.Q4_K_M.gguf")

output = llm("Q: Name the planets in the solar system? A: ", max_tokens=32, stop=["Q:", "\n"], echo=True)

print(output)