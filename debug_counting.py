"""
Debug script for counting task issues.
This will help identify why ground truth accuracy is decreasing.
"""

import pandas as pd
import json
from pl_multidataset import data_prep_json, simple_test, compare_results_with_targets, object_prompt

def debug_counting_task():
    """Debug the counting task to see what's going wrong."""
    
    print("🔍 DEBUGGING COUNTING TASK")
    print("=" * 50)
    
    # Load the counting data
    dataset, train_set, test_set, train_targets, test_targets = data_prep_json("bbh-download/object_counting.json")
    
    print(f"📊 Dataset info:")
    print(f"   Total samples: {len(dataset)}")
    print(f"   Train samples: {len(train_set)}")
    print(f"   Test samples: {len(test_set)}")
    print()
    
    # Look at some examples
    print("📝 Sample data:")
    for i in range(min(5, len(dataset))):
        print(f"   Input: {dataset.iloc[i]['input'][:100]}...")
        print(f"   Target: {dataset.iloc[i]['target']}")
        print()
    
    # Check target distribution
    print("🎯 Target value distribution:")
    target_counts = pd.Series(test_targets).value_counts().sort_index()
    print(target_counts.head(10))
    print()
    
    # Run a simple experiment
    print("🧪 Running counting experiment...")
    results_df = pd.DataFrame(columns=["initial metric", "train", "test", "prompt", "file", "raw"])
    results, results_df = simple_test(train_set, test_set, object_prompt, "evaluator-object", results_df)
    
    # Analyze the results in detail
    print("\n🔍 DETAILED ANALYSIS:")
    
    if 'raw' in results and len(results['raw']) > 0:
        # Compare initial vs final outputs
        initial_outputs = results['raw'][0]['output'] if len(results['raw']) > 0 else None
        final_outputs = results['raw'][-1]['output'] if len(results['raw']) > 1 else initial_outputs
        
        if initial_outputs is not None:
            print("\n📊 Initial vs Final Output Analysis:")
            analyze_counting_outputs(initial_outputs, test_targets, "INITIAL")
            
            if final_outputs is not initial_outputs:
                print()
                analyze_counting_outputs(final_outputs, test_targets, "FINAL")
                
                # Compare differences
                print("\n🔄 Changes from Initial to Final:")
                compare_output_changes(initial_outputs, final_outputs, test_targets)

def analyze_counting_outputs(outputs, targets, label):
    """Analyze counting outputs in detail."""
    print(f"--- {label} OUTPUTS ---")
    
    correct_count = 0
    parse_errors = 0
    value_errors = 0
    
    detailed_results = []
    
    for i, (output, target) in enumerate(zip(outputs, targets)):
        try:
            # Parse JSON
            if isinstance(output, str):
                output_data = json.loads(output)
                predicted_str = output_data.get('result', '')
            else:
                predicted_str = str(output)
            
            # Try numeric comparison
            try:
                pred_num = float(predicted_str)
                target_num = float(target)
                is_correct = pred_num == target_num
                
                detailed_results.append({
                    'index': i,
                    'predicted_str': predicted_str,
                    'predicted_num': pred_num,
                    'target_str': str(target),
                    'target_num': target_num,
                    'correct': is_correct,
                    'error_type': None
                })
                
                if is_correct:
                    correct_count += 1
                    
            except ValueError as e:
                # Fallback to string comparison
                is_correct = predicted_str.lower() == str(target).lower()
                value_errors += 1
                
                detailed_results.append({
                    'index': i,
                    'predicted_str': predicted_str,
                    'predicted_num': 'ERROR',
                    'target_str': str(target),
                    'target_num': float(target),
                    'correct': is_correct,
                    'error_type': 'VALUE_ERROR'
                })
                
                if is_correct:
                    correct_count += 1
                
        except (json.JSONDecodeError, KeyError) as e:
            parse_errors += 1
            detailed_results.append({
                'index': i,
                'predicted_str': 'PARSE_ERROR',
                'predicted_num': 'ERROR',
                'target_str': str(target),
                'target_num': float(target),
                'correct': False,
                'error_type': 'PARSE_ERROR'
            })
    
    accuracy = correct_count / len(outputs)
    
    print(f"✅ Correct: {correct_count}/{len(outputs)} = {accuracy:.3f}")
    print(f"❌ Parse errors: {parse_errors}")
    print(f"⚠️  Value errors: {value_errors}")
    
    # Show some examples
    print(f"\n📋 Sample results:")
    df = pd.DataFrame(detailed_results)
    
    # Show first few correct
    correct_samples = df[df['correct']].head(3)
    if len(correct_samples) > 0:
        print("   ✅ Correct examples:")
        for _, row in correct_samples.iterrows():
            print(f"      Predicted: {row['predicted_str']}, Target: {row['target_str']}")
    
    # Show first few incorrect
    incorrect_samples = df[~df['correct']].head(3)
    if len(incorrect_samples) > 0:
        print("   ❌ Incorrect examples:")
        for _, row in incorrect_samples.iterrows():
            print(f"      Predicted: {row['predicted_str']}, Target: {row['target_str']}, Error: {row['error_type']}")

def compare_output_changes(initial_outputs, final_outputs, targets):
    """Compare changes between initial and final outputs."""
    
    changes = 0
    improved = 0
    worsened = 0
    
    for i, (init_out, final_out, target) in enumerate(zip(initial_outputs, final_outputs, targets)):
        if init_out != final_out:
            changes += 1
            
            # Check if this change was an improvement
            init_correct = check_counting_correctness(init_out, target)
            final_correct = check_counting_correctness(final_out, target)
            
            if not init_correct and final_correct:
                improved += 1
            elif init_correct and not final_correct:
                worsened += 1
                
                # Show examples of worsened cases
                if worsened <= 3:  # Show first 3
                    print(f"   Example {worsened}: {init_out} → {final_out} (target: {target})")
    
    print(f"📈 Changes: {changes}/{len(initial_outputs)}")
    print(f"   ✅ Improved: {improved}")
    print(f"   ❌ Worsened: {worsened}")
    print(f"   🔄 Net change: {improved - worsened}")

def check_counting_correctness(output, target):
    """Check if a single counting output is correct."""
    try:
        if isinstance(output, str):
            output_data = json.loads(output)
            predicted_str = output_data.get('result', '')
        else:
            predicted_str = str(output)
        
        try:
            pred_num = float(predicted_str)
            target_num = float(target)
            return pred_num == target_num
        except ValueError:
            return predicted_str.lower() == str(target).lower()
            
    except (json.JSONDecodeError, KeyError):
        return False

if __name__ == "__main__":
    debug_counting_task() 