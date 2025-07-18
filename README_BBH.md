# BigBench Hard JSON Data Integration

This document explains how to use the new BigBench Hard JSON data integration functionality in the prompt learning system.

## Overview

The system now supports downloading and using JSON files from the BigBench Hard repository instead of relying on local CSV files. This provides access to a wider variety of benchmark tasks for prompt optimization experiments.

## New Functions

### 1. `download_bbh_json_files(download_dir="bbh-download")`
Downloads all available BigBench Hard JSON files from the repository.

```python
# Download all BigBench Hard JSON files
downloaded_files = download_bbh_json_files("bbh-download")
print(f"Downloaded {len(downloaded_files)} files")
```

### 2. `get_available_bbh_tasks(download_dir="bbh-download")`
Lists all available BigBench Hard tasks from downloaded files.

```python
# Get list of available tasks
available_tasks = get_available_bbh_tasks("bbh-download")
print("Available tasks:", available_tasks)
```

### 3. `load_json_to_dataframe(json_file_path)`
Loads a BigBench Hard JSON file and converts it to a pandas DataFrame.

```python
# Load a specific task
df = load_json_to_dataframe("bbh-download/boolean_expressions.json")
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
```

### 4. `data_prep_json(json_file_path, num_samples=None)`
Prepares training and test datasets from a JSON file (similar to the original `data_prep` function).

```python
# Prepare data for training
dataset, train_set, test_set = data_prep_json("bbh-download/boolean_expressions.json")
```

### 5. `run_bbh_experiments()`
Runs complete experiments on multiple BigBench Hard tasks.

```python
# Run experiments on all configured tasks
results_df = run_bbh_experiments()
```

## Available BigBench Hard Tasks

The system supports the following BigBench Hard tasks:

- `boolean_expressions` - Boolean logic evaluation
- `causal_judgement` - Causal reasoning
- `date_understanding` - Date and time reasoning
- `disambiguation_qa` - Disambiguation questions
- `dyck_languages` - Formal language parsing
- `formal_fallacies` - Logical fallacy detection
- `geometric_shapes` - Geometric reasoning
- `hyperbaton` - Syntax understanding
- `logical_deduction_five_objects` - Logical deduction (5 objects)
- `logical_deduction_seven_objects` - Logical deduction (7 objects)
- `logical_deduction_three_objects` - Logical deduction (3 objects)
- `movie_recommendation` - Recommendation reasoning
- `multistep_arithmetic_two` - Multi-step arithmetic
- `navigate` - Navigation reasoning
- `object_counting` - Object counting
- `penguins_in_a_table` - Table reasoning
- `reasoning_about_colored_objects` - Color reasoning
- `ruin_names` - Name corruption
- `salient_translation_error_detection` - Translation error detection
- `snarks` - Logical puzzles
- `sports_understanding` - Sports reasoning
- `temporal_sequences` - Time sequence reasoning
- `tracking_shuffled_objects_five_objects` - Object tracking (5 objects)
- `tracking_shuffled_objects_seven_objects` - Object tracking (7 objects)
- `tracking_shuffled_objects_three_objects` - Object tracking (3 objects)
- `web_of_lies` - Truth/lie reasoning
- `word_sorting` - Word sorting tasks

## Quick Start Guide

### Step 1: Test Dependencies

```bash
python test_import.py
```

This will verify all required packages are installed correctly.

### Step 2: Test the Download Functionality

```bash
python test_bbh_download.py
```

This will:
- Download all BigBench Hard JSON files
- Test the loading functionality
- Show available tasks and sample data

### Step 3: Use in Your Experiments

```python
# Option 1: Run all configured experiments
from pl_multidataset import run_bbh_experiments
results_df = run_bbh_experiments()

# Option 2: Run a specific task
from pl_multidataset import data_prep_json, simple_test
dataset, train_set, test_set = data_prep_json("bbh-download/boolean_expressions.json")
results, result_df = simple_test(train_set, test_set, bool_prompt, "evaluator-bool", result_df)
```

### Step 4: Customize for Your Tasks

```python
# Define your own task mappings
task_mappings = {
    "boolean_expressions": ("evaluator-bool", bool_prompt),
    "web_of_lies": ("evaluator-lies", wol_prompt),
    # Add more tasks as needed
}

# Run experiments
results_df = pd.DataFrame(columns=["initial metric", "train", "test", "prompt", "file", "raw"])
for task_name, (eval_template, prompt) in task_mappings.items():
    dataset, train_set, test_set = data_prep_json(f"bbh-download/{task_name}.json")
    results, results_df = simple_test(train_set, test_set, prompt, eval_template, results_df)
```

## Data Format

The JSON files are converted to DataFrames with the following structure:

| Column | Description |
|--------|-------------|
| `input` | The input text/question for the model |
| `target` | The expected output/answer |

## Backward Compatibility

The original `data_prep(dataset_name)` function is still available for CSV-based datasets, ensuring backward compatibility with existing code.

## Error Handling

The download function includes error handling and will:
- Try the primary BigBench Hard repository first
- Fall back to the main BIG-bench repository if needed
- Skip files that cannot be downloaded and continue with others
- Provide clear error messages for debugging

## File Structure

```
bbh-download/
├── boolean_expressions.json
├── causal_judgement.json
├── date_understanding.json
├── ...
└── word_sorting.json
```

## Requirements

Make sure you have the following dependencies installed:

```bash
pip install requests pandas
```

## Troubleshooting

1. **Network Issues**: If downloads fail, check your internet connection and try again
2. **File Not Found**: Ensure the `bbh-download` directory exists and contains the JSON files
3. **JSON Format Issues**: The system handles different JSON formats automatically, but custom formats may need manual adjustment
4. **Import Error**: If you get an error about `MetaPromptOptimizer`, this class has been renamed to `PromptLearningOptimizer` in newer versions of arize-toolkit

## Contributing

To add support for new BigBench Hard tasks:

1. Add the task name to the `bbh_tasks` list in `download_bbh_json_files()`
2. Create appropriate evaluator templates
3. Add the task to your experiments configuration

---

For more information, refer to the main documentation or the code comments in `pl_multidataset.py`. 