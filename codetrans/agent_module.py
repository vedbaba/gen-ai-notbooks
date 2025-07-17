import os, re, time, random, traceback
from functools import partial
from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import Tool
from langsmith import traceable

os.environ["GOOGLE_API_KEY"] = "**"
os.environ["LANGSMITH_API_KEY"] = "**"


def retry_with_backoff(func, max_retries=5):
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            wait = (2 ** i) + random.random()
            print(f"Retrying in {wait:.2f} seconds...")
            time.sleep(wait)
            traceback.print_exc()
    raise Exception("Max retries exceeded")

def translate_csharp_to_python(code: str) -> str:
    prompt = (
        "Translate the following C# code to Python without comment and markdown "
        "characters like '```python' or '```'. Code must be executable and include a main method:\n\n"
        + code
    )
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
    return llm.predict(prompt)

translation_tool = Tool(
    name="CSharpToPythonTranslator",
    func=translate_csharp_to_python,
    description="Translates C# code to Python code."
)

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
agent = initialize_agent(
    tools=[translation_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

@traceable(name="CSharpToPythonTranslationAgent")
def run_translation_agent(code: str):
    return agent.run(
        f"Translate the following C# code to Python without comment and markdown characters like '```python' or '```'. Code must be executable and include a main method:\n{code}"
    )