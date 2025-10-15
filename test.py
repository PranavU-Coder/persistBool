import persistBool as pb
from langchain.output_parsers import BooleanOutputParser

counter = pb.booleanPersistence()

text = "I absolutely disagree, definitely not!"
result = counter.process_text(text)

parser = BooleanOutputParser()

try:
    langchain_result = parser.parse(text)
    print(f"→ Result: {langchain_result}")

except Exception as e:
    print(f"Error: {e}")

final_answer = counter.parse()

print(f"{final_answer}")