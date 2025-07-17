"""
Manual accuracy calculation demo for boolean expressions task.
This shows exactly how the compare_with_targets function works step by step.
"""

import pandas as pd
import json

# Your ground truth targets (from the data you provided)
ground_truth_targets = pd.Series({
    6: False, 97: False, 60: False, 197: False, 9: True, 67: True, 15: True, 247: True,
    19: False, 68: True, 176: False, 120: False, 141: True, 18: True, 196: True, 180: True,
    96: False, 185: True, 146: False, 173: False, 132: False, 225: True, 238: False, 136: False,
    217: True, 154: False, 168: False, 229: True, 233: False, 156: True, 84: True, 125: False,
    109: False, 172: True, 158: True, 237: True, 82: True, 79: True, 86: True, 186: False,
    170: False, 140: True, 124: True, 148: False, 12: True, 35: True, 42: True, 93: False,
    212: False, 101: True
}, name='target')

print("🎯 BOOLEAN EXPRESSIONS ACCURACY CALCULATION DEMO")
print("=" * 60)
print(f"Ground truth shape: {ground_truth_targets.shape}")
print(f"Task type: 'boolean' (case-insensitive True/False comparison)")
print()

# Example model outputs (you would replace this with your actual model outputs)
# Simulating some outputs for demonstration
model_outputs_example = [
    '{"result": "False"}',  # ID 6: Target=False → CORRECT ✅
    '{"result": "False"}',  # ID 97: Target=False → CORRECT ✅  
    '{"result": "True"}',   # ID 60: Target=False → WRONG ❌
    '{"result": "False"}',  # ID 197: Target=False → CORRECT ✅
    '{"result": "True"}',   # ID 9: Target=True → CORRECT ✅
    # ... would continue for all 50 samples
]

# For demo, let's create a complete set with 85% accuracy
import random
random.seed(42)  # For reproducible results

complete_model_outputs = []
targets_list = list(ground_truth_targets.values)

for i, target in enumerate(targets_list):
    # 85% chance of correct answer
    if random.random() < 0.85:
        predicted = "True" if target else "False"
    else:
        predicted = "False" if target else "True"
    complete_model_outputs.append(f'{{"result": "{predicted}"}}')

print("📊 STEP-BY-STEP ACCURACY CALCULATION:")
print()

def manual_boolean_accuracy(model_outputs, ground_truth_values, show_details=True):
    """
    Manual calculation showing exactly how boolean accuracy is computed.
    """
    correct_count = 0
    total_count = len(ground_truth_values)
    
    if show_details:
        print("ID   | Target | Model JSON Output     | Extracted | Match | Status")
        print("-" * 70)
    
    details = []
    
    for i, (target_value, output_json) in enumerate(zip(ground_truth_values, model_outputs)):
        try:
            # Step 1: Parse JSON output
            output_data = json.loads(output_json)
            predicted_value = output_data.get('result', '')
            
            # Step 2: Convert both to strings
            predicted_str = str(predicted_value).strip()
            target_str = str(target_value).strip()
            
            # Step 3: Boolean comparison (case-insensitive)
            is_match = predicted_str.lower() == target_str.lower()
            
            if is_match:
                correct_count += 1
                status = "✅ CORRECT"
            else:
                status = "❌ WRONG"
            
            # Show first 10 rows for demo
            if show_details and i < 10:
                idx = list(ground_truth_targets.index)[i]  # Get original ID
                print(f"{idx:3d}  | {target_str:6s} | {output_json:20s} | {predicted_str:9s} | {str(is_match):5s} | {status}")
            
            details.append({
                'id': list(ground_truth_targets.index)[i],
                'target': target_value,
                'predicted': predicted_str,
                'correct': is_match
            })
            
        except (json.JSONDecodeError, KeyError) as e:
            # Parsing error counts as incorrect
            if show_details and i < 10:
                idx = list(ground_truth_targets.index)[i]
                print(f"{idx:3d}  | {target_str:6s} | {output_json:20s} | ERROR     | False | ❌ PARSE ERROR")
            
            details.append({
                'id': list(ground_truth_targets.index)[i],
                'target': target_value,
                'predicted': 'ERROR',
                'correct': False
            })
    
    if show_details and total_count > 10:
        print("...  | ...    | ...                  | ...       | ...   | ...")
        print(f"[Showing first 10 of {total_count} samples]")
    
    accuracy = correct_count / total_count
    
    print()
    print("📈 CALCULATION BREAKDOWN:")
    print(f"✅ Correct predictions: {correct_count}")
    print(f"❌ Wrong predictions: {total_count - correct_count}")
    print(f"📊 Total predictions: {total_count}")
    print(f"🎯 Accuracy = {correct_count} / {total_count} = {accuracy:.4f} = {accuracy*100:.2f}%")
    
    return accuracy, details

# Calculate accuracy
accuracy, details = manual_boolean_accuracy(complete_model_outputs, targets_list)

print()
print("🔍 VALIDATION WITH pl_multidataset.py:")

# Test with the actual function from pl_multidataset.py
try:
    from pl_multidataset import compare_with_targets
    
    # Convert targets to list of strings (as the function expects)
    targets_str_list = [str(val) for val in targets_list]
    
    # Use the function with task_type="boolean"
    function_accuracy = compare_with_targets(complete_model_outputs, targets_str_list, task_type="boolean")
    
    print(f"Manual calculation:   {accuracy:.4f}")
    print(f"Function calculation: {function_accuracy:.4f}")
    print(f"Match: {'✅ PERFECT MATCH' if abs(accuracy - function_accuracy) < 0.001 else '❌ MISMATCH'}")
    
except ImportError as e:
    print(f"Could not import compare_with_targets: {e}")

print()
print("🎯 KEY POINTS FOR BOOLEAN TASK:")
print("1. JSON format: {'result': 'True'} or {'result': 'False'}")
print("2. Case-insensitive: 'True' == 'true' == 'TRUE'")
print("3. String comparison after extraction from JSON")
print("4. Parse errors count as incorrect")
print("5. Each prediction must match exactly after case normalization")

print()
print("📝 TO USE WITH YOUR ACTUAL DATA:")
print("1. Replace 'complete_model_outputs' with your model's JSON outputs")
print("2. Make sure outputs are in same order as ground_truth_targets")
print("3. Use compare_with_targets(outputs, targets, task_type='boolean')")
print("4. The accuracy will be: (correct_predictions) / (total_predictions)") 