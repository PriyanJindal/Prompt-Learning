import pandas as pd
import json

json_path = "/Users/sriichavali/Desktop/Prompt-Learning/sri/object_counting.json"

with open(json_path, "r") as f:
    data = json.load(f)

examples = data["examples"] 

df = pd.DataFrame(examples, columns=["input", "target"])

df_inputs = df.drop(columns=["target"])
df_inputs.to_csv("object_inputs.csv")