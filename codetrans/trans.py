import os , re
from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import Tool
from langsmith import traceable
import time
import random, traceback
from functools import partial


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

os.environ["GOOGLE_API_KEY"] = "*****"
os.environ["LANGSMITH_API_KEY"] = "****"


# Define the translation function
def translate_csharp_to_python(code: str) -> str:
    prompt = f"Translate the following C# code to Python without comment and markdown charactors like '```python' or '```' , code can be executable by copy and pasting in python file directly and code must have main mehtod:\n\n{code}"
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
    return llm.predict(prompt)

# Wrap the tool for LangChain
translation_tool = Tool(
    name="CSharpToPythonTranslator",
    func=translate_csharp_to_python,
    description="Translates C# code to Python code."
)

# Initialize the agent
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
agent = initialize_agent(
    tools=[translation_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Traceable function for LangSmith observability
@traceable(name="CSharpToPythonTranslationAgent")
def run_translation_agent(code: str):
    return agent.run(f"Translate the following C# code to Python without comment and markdown charactors like '```python' or '```' , code can be executable by copy and pasting in python file directly and code must have main mehtod:\n{code}")

# Main function to read C# code from file and write translated Python code to file
def main():
    input_file = r"C:\Users\veyadav\Documents\OneDrive - Capgemini\Documents\INTUDO\python\notebook\codetrans\input_code.cs"
    output_file = r"C:\Users\veyadav\Documents\OneDrive - Capgemini\Documents\INTUDO\python\notebook\codetrans\translated_code.py"

    # Read C# code from file
    with open(input_file, "r", encoding="utf-8") as f:
        csharp_code = f.read()

  
    wrapped_func = partial(run_translation_agent, csharp_code)

    # Translate using the agent
    translated_python_code =  retry_with_backoff(wrapped_func,2)
    
    updated = translated_python_code.replace( "```python","") 
    updated = updated.replace("```","") 

    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"{output_file} has been deleted.")
    else:
        print(f"{output_file} does not exist.")

    # Write the translated Python code to a new file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(updated.strip()) 

    print(f"Translation complete. Python code saved to '{output_file}'.")

if __name__ == "__main__":
    main()
