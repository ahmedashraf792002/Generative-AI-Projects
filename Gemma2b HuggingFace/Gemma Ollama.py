'''import ollama

response = ollama.chat(
    model="gemma:2b",
    messages=[{"role": "user", "content": "What is AI?"}]
)

# Extracting only the message content
message_content = response['message']['content']
print(message_content)'''

'''from langchain_ollama import OllamaLLM

# Initialize the Ollama model
llm = OllamaLLM(model="gemma:2b")

# Call the model with your prompt
response = llm.invoke("What is ML?")

# Extract the message content

print(response)'''

from langchain_community.llms import Ollama

# Initialize the Ollama model
llm = Ollama(model="gemma:2b", temperature=0)

# Call the model with your prompt
response = llm.invoke("What is Deep Learning?")
print(response)




