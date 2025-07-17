import os
from functools import partial
from agent_module import run_translation_agent, retry_with_backoff

def main():
    input_file = r"C:\Users\veyadav\Documents\OneDrive - Capgemini\Documents\INTUDO\python\notebook\codetrans\input_code.cs"
    output_file = r"C:\Users\veyadav\Documents\OneDrive - Capgemini\Documents\INTUDO\python\notebook\codetrans\translated_code.py"

    with open(input_file, "r", encoding="utf-8") as f:
        csharp_code = f.read()

    wrapped_func = partial(run_translation_agent, csharp_code)
    translated_python_code = retry_with_backoff(wrapped_func, max_retries=2)

    updated = translated_python_code.replace("```python", "").replace("```", "")
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"{output_file} has been deleted.")
    else:
        print(f"{output_file} does not exist.")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(updated.strip())

    print(f"Translation complete. Python code saved to '{output_file}'.")

if __name__ == "__main__":
    main()