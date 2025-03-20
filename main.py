from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--task", default="return a list of numbers")
parser.add_argument("--language", default="python")
args = parser.parse_args()
try:
    llm = Ollama(model="llama3")

    code_prompt = PromptTemplate(
        template="Write a very short {language} function that will {task}.",
        input_variables=["language", "task"],
    )

    test_prompt = PromptTemplate(
        template="Write a test function for the following {language} code:\n{code}",
        input_variables=["language", "task"],
    )

    code_chain = LLMChain(llm=llm, prompt=code_prompt, output_key="code")
    test_chain = LLMChain(llm=llm, prompt=test_prompt, output_key="test")

    chain = SequentialChain(
        chains=[code_chain, test_chain],
        input_variables=["task", "language"],
        output_variables=["test", "code"],
    )

    result = chain({"language": args.language, "task": args.task})
    print(">>>>> GENERATED CODE: ")
    print(result["code"])

    print(">>>>> GENERATED TEST: ")
    print(result["test"])

except Exception as e:
    print(f"An error occurred: {e}")
