# LangChain is a framework designed to help developers build applications that integrate Large Language Models (LLMs) such as OpenAI's GPT models with external data sources, tools, and user workflows.
# 
# Common use cases include:
#   - Building chatbots that can access and reason over your own data.
#   - Creating "Search your PDF" tools by connecting LLMs to file and database sources.
#   - Composing multi-step reasoning pipelines that use LLMs as "brains" for custom logic and automation.
#
# LangChain lets you combine (or "chain") prompt templates, models, document loaders, memory, and other utilities in a modular, flexible way.
#
# Basic LangChain Example:
import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama  # Now this will work!
from langchain_core.prompts import PromptTemplate

# 1. Load your local model 
# (Make sure you have downloaded Ollama and run 'ollama pull llama3' first)
llm = Ollama(model="llama3")

# 2. Setup the Chef prompt
template = "You are a chef. Suggest a 3-course meal based on these ingredients: {ingredients}"
prompt = PromptTemplate.from_template(template)

# 3. Connect them
chain = prompt | llm

# 4. Run it for free!
response = chain.invoke({"ingredients": "tomatoes, eggs, and bread"})
print(response)