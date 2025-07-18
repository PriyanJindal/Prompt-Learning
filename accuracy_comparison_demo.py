import pandas as pd
import json

# Your ground truth targets (from the data you provided)
ground_truth = pd.Series({
    6: False, 97: False, 60: False, 197: False, 9: True, 67: True, 15: True, 247: True,
    19: False, 68: True, 176: False, 120: False, 141: True, 18: True, 196: True, 180: True,
    96: False, 185: True, 146: False, 173: False, 132: False, 225: True, 238: False, 136: False,
    217: True, 154: False, 168: False, 229: True, 233: False, 156: True, 84: True, 125: False,
    109: False, 172: True, 158: True, 237: True, 82: True, 79: True, 86: True, 186: False,
    170: False, 140: True, 124: True, 148: False, 12: True, 35: True, 42: True, 93: False,
    212: False, 101: True
}, name='target')

# Example model outputs (simulated - would come from your model)
# Format: {"result": "True"} or {"result": "False"}
model_outputs_json = [
    '{"result": "False"}',  # ID 6: False - CORRECT ✅
    '{"result": "True"}',   # ID 97: False - WRONG ❌  
    '{"result": "False"}',  # ID 60: False - CORRECT ✅
    '{"result": "False"}',  # ID 197: False - CORRECT ✅
    '{"result": "True"}',   # ID 9: True - CORRECT ✅
    '{"result": "True"}',   # ID 67: True - CORRECT ✅
    '{"result": "False"}',  # ID 15: True - WRONG ❌
    '{"result": "True"}',   # ID 247: True - CORRECT ✅
    '{"result": "False"}',  # ID 19: False - CORRECT ✅
    '{"result": "True"}',   # ID 68: True - CORRECT ✅
    # ... continuing for all 50 samples
]

# Complete the model outputs for all samples (for demonstration)
# Let's simulate some realistic outputs with ~80% accuracy
import random
random.seed(42)  # For reproducible demo

model_outputs_json = []
for idx, true_value in ground_truth.items():
    # Simulate 80% accuracy
    if random.random() < 0.8:  # 80% chance of correct answer
        predicted = "True" if true_value else "False"
    else:  # 20% chance of wrong answer
        predicted = "False" if true_value else "True"
    
    model_outputs_json.append(f'{{"result": "{predicted}"}}')

print("🎯 BOOLEAN EXPRESSIONS ACCURACY CALCULATION")
print("=" * 50)
print(f"Ground truth shape: {ground_truth.shape}")
print(f"Model outputs count: {len(model_outputs_json)}")
print(f"Task type: 'boolean'")
print()

# Manual calculation step by step
def calculate_boolean_accuracy_detailed(model_outputs, ground_truth):
    """Calculate accuracy with detailed step-by-step breakdown"""
    
    correct_count = 0
    total_count = len(ground_truth)
    detailed_results = []
    
    print("📊 STEP-BY-STEP COMPARISON:")
    print("ID   | Target | Model Output JSON        | Extracted | Match | Status")
    print("-" * 75)
    
    for i, (idx, true_target) in enumerate(ground_truth.items()):
        try:
            # Parse JSON output
            output_json = model_outputs[i]
            output_data = json.loads(output_json)
            predicted_str = output_data.get('result', '')
            
            # Convert target to string for comparison
            target_str = str(true_target)
            
            # Boolean task: case-insensitive comparison
            is_correct = predicted_str.lower() == target_str.lower()
            
            if is_correct:
                correct_count += 1
                status = "✅ CORRECT"
            else:
                status = "❌ WRONG"
            
            # Show first 10 and last 5 for brevity
            if i < 10 or i >= total_count - 5:
                print(f"{idx:3d}  | {target_str:6s} | {output_json:23s} | {predicted_str:9s} | {is_correct:5s} | {status}")
            elif i == 10:
                print("...  | ...    | ...                     | ...       | ...   | ...")
            
            detailed_results.append({
                'id': idx,
                'target': true_target,
                'predicted': predicted_str,
                'correct': is_correct
            })
            
        except (json.JSONDecodeError, KeyError) as e:
            status = "❌ PARSE ERROR"
            if i < 10 or i >= total_count - 5:
                print(f"{idx:3d}  | {target_str:6s} | {output_json:23s} | ERROR     | False | {status}")
            detailed_results.append({
                'id': idx,
                'target': true_target,
                'predicted': 'ERROR',
                'correct': False
            })
    
    accuracy = correct_count / total_count
    
    print()
    print("📈 CALCULATION SUMMARY:")
    print(f"Correct predictions: {correct_count}")
    print(f"Total predictions: {total_count}")
    print(f"Accuracy = {correct_count} / {total_count} = {accuracy:.4f} = {accuracy*100:.2f}%")
    
    return accuracy, detailed_results

# Calculate accuracy
accuracy, details = calculate_boolean_accuracy_detailed(model_outputs_json, ground_truth)

print()
print("🔍 BREAKDOWN BY RESULT:")
correct_details = [d for d in details if d['correct']]
wrong_details = [d for d in details if not d['correct']]

print(f"✅ Correct predictions: {len(correct_details)}")
for detail in correct_details[:5]:  # Show first 5
    print(f"   ID {detail['id']}: Target={detail['target']} → Predicted={detail['predicted']}")
if len(correct_details) > 5:
    print(f"   ... and {len(correct_details)-5} more")

print(f"❌ Wrong predictions: {len(wrong_details)}")
for detail in wrong_details[:5]:  # Show first 5
    print(f"   ID {detail['id']}: Target={detail['target']} → Predicted={detail['predicted']}")
if len(wrong_details) > 5:
    print(f"   ... and {len(wrong_details)-5} more")

print()
print("🔬 VALIDATION USING pl_multidataset.py FUNCTION:")

# Now test with the actual function from pl_multidataset
import sys
sys.path.append('.')  # Add current directory to path

try:
    from pl_multidataset import compare_with_targets
    
    # Convert ground truth to list (same order as model outputs)
    targets_list = [str(val) for val in ground_truth.values]
    
    # Calculate using the function
    function_accuracy = compare_with_targets(model_outputs_json, targets_list, task_type="boolean")
    
    print(f"Manual calculation: {accuracy:.4f}")
    print(f"Function calculation: {function_accuracy:.4f}")
    print(f"Match: {'✅' if abs(accuracy - function_accuracy) < 0.001 else '❌'}")
    
except ImportError:
    print("Could not import compare_with_targets function")

print()
print("🎯 KEY POINTS:")
print("1. Boolean task uses case-insensitive comparison ('True' == 'true')")
print("2. Each prediction must exactly match the target after case normalization")
print("3. JSON parsing errors count as incorrect predictions")
print("4. Accuracy = (Correct Predictions) / (Total Predictions)") 