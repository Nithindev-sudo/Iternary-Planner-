Ollama connection if locally hosted


# from langchain_groq import ChatGroq

# client = ChatGroq(
# 
#     model="llama3-8b-8192",
#     api_key="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",
# )

# response = client.invoke("Hello, how can I assist you today?")
# print(response.content)



from langchain_ollama import ChatOllama


a = ChatOllama(
    model="llama-3.2-3b-it:latest",
)

response = a.invoke("Hello, how can I assist you today?")
print(response.content)
 
