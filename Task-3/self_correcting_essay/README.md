# Self-Correcting Essay Writer

## Overview

The **Self-Correcting Essay Writer** is an AI-powered system that automatically generates, evaluates, and improves essays through iterative feedback. It uses LangGraph to create a workflow where an AI writer creates essays and an AI critic provides feedback until the essay reaches an acceptable quality score.

## Features

- **AI-Powered Essay Generation**: Uses Google's Gemini AI to write essays on any topic
- **Automated Feedback Loop**: Critic node evaluates essays and provides constructive feedback
- **Iterative Improvement**: Continues refining essays based on critic feedback
- **Quality Control**: Stops when essay score reaches 7/10 or max 5 iterations reached
- **Detailed Logging**: Saves all iterations and final essay to timestamped log files

## Architecture

### Workflow Components

1. **Writer Node**: Generates essay drafts based on topic and feedback
2. **Critic Node**: Evaluates essays on multiple criteria (clarity, structure, grammar, depth, conclusion)
3. **State Management**: Tracks essay content, scores, feedback, and iteration count
4. **Conditional Logic**: Routes workflow based on quality score and iteration limits

### File Structure

```
self_correcting_essay/
├── app.py                    # Main application entry point
├── requirements.txt          # Project dependencies
├── README.md                 # This file
├── graph/
│   ├── workflow.py          # LangGraph workflow definition
│   ├── state.py             # EssayState TypedDict
│   └── node.py              # Writer and Critic node functions
├── prompts/
│   ├── writer_prompt.py     # Essay writing instructions
│   └── critic_prompt.py     # Critique and scoring instructions
├── utils/
│   └── logger.py            # Logging utilities
├── logs/                    # Output directory for essay logs
└── data/                    # Input data (if needed)
```

## Installation

### Prerequisites
- Python 3.8+
- Google Generative AI API key

### Setup

1. **Clone/Navigate to the project:**
   ```bash
   cd self_correcting_essay
   ```

2. **Create virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Usage

### Run the Application

```bash
python app.py
```

### Workflow
1. Enter an essay topic when prompted
2. The writer generates an initial draft
3. The critic evaluates the essay and provides a score (1-10)
4. If score < 7 and iterations < 5, the writer improves based on feedback
5. Process repeats until essay is accepted or max iterations reached
6. Final essay and logs are saved

### Example Output
```
Current Score: 6
Current Iteration: 1
Essay Needs Improvement...

Current Score: 8
Current Iteration: 2
Essay Accepted!

======================================================================
FINAL ESSAY
======================================================================
[Final polished essay content...]

FINAL SCORE: 8

Logs saved to: logs/2026-06-05_12-30-45.txt
```

## Configuration

### Adjustment Points

- **Quality Threshold**: Change line in `workflow.py` `if score >= 7:` to adjust accepted score
- **Max Iterations**: Modify `if iteration >= 5:` to change iteration limit
- **LLM Model**: Update `model="gemini-3-flash-preview"` in `node.py` for different Gemini versions
- **Temperature**: Adjust `temperature=0.7` in `node.py` for more/less creative output

## Dependencies

- **langchain**: LLM orchestration framework
- **langgraph**: Stateful graph-based workflow management
- **langchain-google-genai**: Google Gemini AI integration
- **python-dotenv**: Environment variable management

## How It Works

### State Management
The `EssayState` tracks:
- `topic`: Essay subject
- `essay`: Current essay draft
- `score`: Quality score from critic
- `feedback`: Improvement suggestions
- `iteration`: Current iteration count
- `logs`: Accumulated iteration logs

### Conditional Routing
The `should_continue()` function decides workflow direction:
- Returns `END` if score ≥ 7 (essay accepted)
- Returns `END` if iteration ≥ 5 (max iterations reached)
- Returns `"writer"` to continue improving

## Output

Essays and their evaluation logs are saved to the `logs/` directory with timestamped filenames:
- Format: `YYYY-MM-DD_HH-MM-SS.txt`
- Contains: Topic, all iteration logs, final score, and final essay

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `GOOGLE_API_KEY not found` | Ensure `.env` file exists with valid API key |
| `AttributeError: 'StateGraph' object...` | Check langgraph version compatibility |
| No logs directory error | Utility creates it automatically on first run |
| Low essay quality | Increase max iterations or adjust quality threshold |

## Future Enhancements

- Multiple essay generation strategies
- Configurable evaluation criteria
- Support for different AI models (OpenAI, Anthropic, etc.)
- Web interface for easier interaction
- Batch essay processing
- Custom prompt templates

## License

Project completed as part of AI/Agentic Systems internship program.

## Support

For issues or questions, refer to the LangGraph documentation:
- [LangGraph Documentation](https://python.langchain.com/docs/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
