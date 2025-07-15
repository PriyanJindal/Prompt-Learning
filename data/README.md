# Data Directory

This directory contains datasets used for meta-prompt optimization research.

## Dataset Structure

### queries.csv

**Description**: Sample dataset for webpage generation optimization experiments.

**Columns**:
- `input`: User descriptions of desired webpages
- `output`: Generated JSON webpage outputs (to be populated)
- `feedback`: Evaluation feedback (to be populated)

**Usage**:
```python
import pandas as pd
dataset = pd.read_csv("data/queries.csv")
```

## Dataset Formats

### 1. CSV Format (Recommended)

**Structure**:
```csv
input,output,feedback
"What is AI?","AI is artificial intelligence","too brief"
"How does ML work?","ML uses algorithms","needs more detail"
```

**Advantages**:
- Human readable
- Easy to edit manually
- Compatible with pandas
- Version control friendly

### 2. JSON Format

**Structure**:
```json
{
  "data": [
    {
      "input": "What is AI?",
      "output": "AI is artificial intelligence",
      "feedback": "too brief"
    }
  ]
}
```

**Usage**:
```python
import json
with open("data/dataset.json", "r") as f:
    data = json.load(f)
dataset = pd.DataFrame(data["data"])
```

## Dataset Requirements

### Required Columns

1. **Input Column**: Contains the user queries/tasks
   - Name: `input`, `query`, `question`, or `task`
   - Type: String
   - Purpose: What the LLM should respond to

2. **Output Column**: Contains LLM-generated responses
   - Name: `output`, `response`, `answer`, or `result`
   - Type: String
   - Purpose: What the LLM actually produced

3. **Feedback Columns**: Contain evaluation feedback
   - Names: `feedback`, `score`, `quality`, etc.
   - Type: String or numeric
   - Purpose: How to improve the prompt

### Optional Columns

1. **Metadata**: Additional context
   - `category`: Task category
   - `difficulty`: Task difficulty level
   - `timestamp`: When the example was created

2. **Template Variables**: For template prompts
   - `{variable_name}`: Template placeholders
   - Should match prompt template variables

## Dataset Preparation Guidelines

### 1. Data Quality

- **Diversity**: Include various input types and difficulty levels
- **Representativeness**: Cover real-world use cases
- **Consistency**: Use consistent formatting and standards
- **Validation**: Check for missing values and errors

### 2. Feedback Quality

- **Specific**: Feedback should be actionable
- **Consistent**: Use consistent evaluation criteria
- **Comprehensive**: Cover different aspects of quality
- **Objective**: Minimize subjective bias

### 3. Size Considerations

- **Minimum**: 10-20 examples for basic testing
- **Recommended**: 50-100 examples for reliable optimization
- **Large Scale**: 1000+ examples for production systems

## Dataset Validation

### Automated Checks

```python
def validate_dataset(dataset):
    """Validate dataset meets requirements"""
    
    # Check required columns
    required_cols = ['input', 'output']
    missing_cols = [col for col in required_cols if col not in dataset.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Check for empty values
    for col in required_cols:
        if dataset[col].isnull().any():
            raise ValueError(f"Empty values found in column: {col}")
    
    # Check data types
    for col in required_cols:
        if not dataset[col].dtype == 'object':
            raise ValueError(f"Column {col} should be string type")
    
    print("Dataset validation passed!")
    return True
```

### Manual Review

1. **Sample Review**: Check random samples for quality
2. **Edge Cases**: Test with unusual inputs
3. **Feedback Consistency**: Review feedback for bias
4. **Template Variables**: Verify variable consistency

## Dataset Versioning

### Naming Convention

```
dataset_name_v{version}_{date}.csv
```

**Examples**:
- `queries_v1_2024-01-15.csv`
- `webpage_generation_v2_2024-01-20.csv`

### Version Control

- Track dataset changes in git
- Document changes in commit messages
- Use tags for major versions
- Keep backup copies of important datasets

## Dataset Sharing

### Export Formats

1. **CSV**: For general use and editing
2. **JSON**: For programmatic access
3. **Parquet**: For large datasets
4. **HDF5**: For complex data structures

### Documentation

Each dataset should include:
- `README.md`: Description and usage instructions
- `schema.json`: Column definitions and types
- `sample.csv`: Small sample for quick review
- `metadata.json`: Dataset statistics and provenance

## Best Practices

### 1. Data Privacy

- Anonymize sensitive data
- Remove personally identifiable information
- Use synthetic data when possible
- Follow data protection regulations

### 2. Data Consistency

- Use consistent naming conventions
- Standardize data formats
- Validate data types
- Handle missing values consistently

### 3. Documentation

- Document data sources
- Explain column meanings
- Provide usage examples
- Track data lineage

### 4. Quality Assurance

- Regular data validation
- Automated quality checks
- Manual review processes
- Feedback incorporation

## Contributing Datasets

1. **Create Dataset**: Prepare data in required format
2. **Validate**: Run validation checks
3. **Document**: Add README and metadata
4. **Test**: Verify with optimization pipeline
5. **Submit**: Add to repository with proper documentation 