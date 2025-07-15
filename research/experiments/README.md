# Experiments

This directory contains experimental configurations and results for meta-prompt optimization research.

## Experiment Structure

Each experiment should be organized as follows:

```
experiments/
├── experiment_name/
│   ├── config.yaml          # Experiment configuration
│   ├── results/             # Experimental results
│   ├── notebooks/           # Analysis notebooks
│   └── README.md           # Experiment documentation
```

## Current Experiments

### 1. Webpage Generation Optimization

**Location**: `webpage_generation/`

**Objective**: Optimize prompts for JSON webpage generation using rule-based evaluation.

**Key Components**:
- Rule-based evaluator for JSON compliance
- Template variable preservation testing
- Context window optimization

**Results**: [Link to results when available]

### 2. Multi-Evaluator Comparison

**Location**: `multi_evaluator/`

**Objective**: Compare different evaluator types and their impact on prompt optimization.

**Evaluators Tested**:
- Rule-based evaluators
- LLM-based evaluators
- Hybrid approaches

### 3. Context Window Optimization

**Location**: `context_optimization/`

**Objective**: Test different context window sizes and their impact on optimization quality.

**Parameters Tested**:
- Context sizes: 8k, 16k, 32k, 64k tokens
- Batch processing strategies
- Token counting accuracy

## Running Experiments

1. **Setup Environment**:
   ```bash
   export OPENAI_API_KEY="your-key"
   pip install -r requirements.txt
   ```

2. **Run Experiment**:
   ```bash
   python research/experiments/run_experiment.py --config experiment_name/config.yaml
   ```

3. **Analyze Results**:
   ```bash
   jupyter notebook research/experiments/experiment_name/notebooks/analysis.ipynb
   ```

## Experiment Configuration

Each experiment should include a `config.yaml` file with:

```yaml
experiment:
  name: "experiment_name"
  description: "Brief description"
  
data:
  dataset_path: "data/queries.csv"
  output_column: "output"
  feedback_columns: ["feedback"]
  
optimization:
  model_choice: "gpt-4"
  context_size_k: 8
  max_iterations: 5
  
evaluators:
  - name: "rule_checker"
    type: "custom"
    config:
      rules: ["rule1", "rule2"]
  
results:
  output_dir: "results/"
  save_intermediate: true
```

## Contributing New Experiments

1. Create a new directory for your experiment
2. Add a `config.yaml` file
3. Document your methodology in `README.md`
4. Include analysis notebooks
5. Update this README with experiment summary

## Results Format

All experiments should produce results in the following format:

- **Metrics**: JSON files with quantitative results
- **Visualizations**: PNG/PDF files for charts and graphs
- **Optimized Prompts**: Text files with final optimized prompts
- **Analysis**: Jupyter notebooks with detailed analysis

## Best Practices

1. **Reproducibility**: Use fixed random seeds and document all parameters
2. **Versioning**: Track code versions and dependency versions
3. **Documentation**: Document all assumptions and methodology
4. **Validation**: Include validation steps and sanity checks
5. **Backup**: Keep backups of important results and configurations 