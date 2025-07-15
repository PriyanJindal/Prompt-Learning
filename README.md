# Meta-Prompt Optimization Research

This repository contains research on meta-prompt optimization techniques for improving Large Language Model (LLM) prompts using feedback-driven iterative refinement.

## Research Overview

### Problem Statement
Traditional prompt engineering relies on manual iteration and intuition. This research explores automated prompt optimization using meta-prompt techniques, where an LLM analyzes feedback from previous outputs to iteratively improve the original prompt.

### Key Contributions
- **Meta-Prompt Framework**: Automated prompt optimization using LLM-generated feedback
- **Smart Batching**: Token-aware dataset splitting to handle large-scale optimization
- **Template Preservation**: Maintains prompt template variables during optimization
- **Multi-Evaluator Support**: Flexible evaluation framework for diverse feedback types

## Repository Structure

```
prompt-opt-sdk/
├── research/
│   ├── notebooks/           # Jupyter notebooks for experiments
│   ├── experiments/         # Experimental configurations and results
│   └── papers/             # Research papers and documentation
├── src/                    # Core implementation (will be moved to separate package)
├── data/                   # Datasets and evaluation data
├── prompts/                # Prompt templates and examples
└── docs/                   # Documentation and guides
```

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Environment Setup

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Basic Usage

```python
import pandas as pd
from meta_prompt_optimizer import MetaPromptOptimizer

# Create dataset with feedback
dataset = pd.DataFrame({
    'query': ["What is AI?", "How does ML work?"],
    'output': ["AI is artificial intelligence", "ML uses algorithms"],
    'feedback': ["too brief", "needs more detail"]
})

# Initialize optimizer
optimizer = MetaPromptOptimizer(
    prompt="You are helpful. Answer: {query}",
    model_choice="gpt-4"
)

# Optimize the prompt
optimized_prompt = optimizer.optimize(
    dataset=dataset,
    output_column='output',
    feedback_columns=['feedback']
)

print("Original:", "You are helpful. Answer: {query}")
print("Optimized:", optimized_prompt)
```

## Research Methodology

### Meta-Prompt Optimization Process

1. **Dataset Preparation**: Collect examples with inputs, outputs, and feedback
2. **Feedback Generation**: Use evaluators to generate structured feedback
3. **Batch Processing**: Split dataset based on token limits
4. **Meta-Prompt Analysis**: LLM analyzes feedback to suggest prompt improvements
5. **Iterative Refinement**: Apply improvements and repeat

### Key Components

- **MetaPromptOptimizer**: Main optimization engine
- **TiktokenSplitter**: Token-aware dataset batching
- **Evaluator Framework**: Custom feedback generation functions
- **Template Variable Detection**: Automatic preservation of prompt placeholders

## Experiments

### Current Experiments

- **Webpage Generation**: JSON webpage creation with rule-based evaluation
- **Multi-Evaluator Testing**: Comparing different feedback sources
- **Context Window Optimization**: Testing different batch sizes

### Running Experiments

```bash
# Run the main research notebook
jupyter notebook research/notebooks/prompt_learning_cookbook_AX.ipynb
```

## API Reference

### MetaPromptOptimizer

```python
MetaPromptOptimizer(
    prompt: Union[PromptVersion, str, List[Dict[str, str]]],
    model_choice: str = "gpt-4",
    openai_api_key: Optional[str] = None
)
```

#### Methods

- `optimize()`: Main optimization method
- `run_evaluators()`: Execute custom evaluators on dataset

### Evaluator Interface

```python
def evaluator(dataset: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """
    Process dataset and return feedback columns.
    
    Returns:
        (updated_dataframe, feedback_column_names)
    """
    # Your evaluation logic here
    return dataset, ['feedback_column']
```

## Research Papers

- [Meta-Prompt Optimization for LLM Performance](research/papers/meta_prompt_optimization.pdf) (In Progress)

## Contributing

This is a research repository. For contributions:

1. Create a new branch for your experiment
2. Document your methodology in `research/notebooks/`
3. Update this README with findings
4. Submit a pull request

## License

[Add your license here]

## Citation

If you use this research in your work, please cite:

```bibtex
@misc{meta_prompt_optimization_2024,
  title={Meta-Prompt Optimization Research},
  author={[Your Name]},
  year={2024},
  url={https://github.com/[username]/prompt-opt-sdk}
}
```


