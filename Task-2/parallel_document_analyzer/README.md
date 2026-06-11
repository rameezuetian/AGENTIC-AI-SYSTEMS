# Parallel Document Analyzer

## Overview

The **Parallel Document Analyzer** is an AI-powered system that simultaneously analyzes documents across multiple dimensions. It uses LangGraph to orchestrate a parallel workflow that performs summarization, topic extraction, and sentiment analysis on documents concurrently, then merges the results into a comprehensive analysis report.

## Features

- **Parallel Processing**: Simultaneously runs three analysis tasks for efficiency
- **Document Summarization**: Creates concise 5-sentence summaries
- **Topic Extraction**: Identifies key topics as bullet points
- **Sentiment Analysis**: Determines document sentiment (Positive/Neutral/Negative)
- **Execution Tracing**: Logs all processing steps for transparency
- **Report Generation**: Combines all analyses into formatted report
- **File Logging**: Saves reports with timestamps

## Architecture

### Workflow Components

1. **Load Document Node**: Reads document from `data/document.txt`
2. **Summarize Node** (Parallel): Creates concise summary of document
3. **Extract Topics Node** (Parallel): Identifies key topics/themes
4. **Analyze Sentiment Node** (Parallel): Determines sentiment and reasoning
5. **Merge Results Node**: Combines all analyses into final report

### Parallel Execution Flow

```
START
  ↓
Load Document
  ↓
  ├─→ Summarize (Parallel)
  ├─→ Extract Topics (Parallel)
  └─→ Analyze Sentiment (Parallel)
  ↓
Merge Results
  ↓
END
```

### File Structure

```
parallel_document_analyzer/
├── app.py                       # Main application entry point
├── requirements.txt             # Project dependencies
├── README.md                    # This file
├── graph/
│   ├── workflow.py             # LangGraph workflow definition
│   ├── state.py                # DocumentState TypedDict
│   └── node.py                 # All analysis node functions
├── prompts/
│   ├── summary_prompts.py      # Summarization instructions
│   ├── sentiment_prompts.py    # Sentiment analysis instructions
│   └── topic_prompts.py        # Topic extraction instructions
├── utils/
│   └── logger.py               # Report and logging utilities
├── data/
│   └── document.txt            # Input document to analyze
└── logs/                        # Output directory for reports
```

## Installation

### Prerequisites
- Python 3.8+
- Google Generative AI API key

### Setup

1. **Navigate to the project:**
   ```bash
   cd parallel_document_analyzer
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

5. **Prepare your document:**
   - Place your document in `data/document.txt` or modify the path in `node.py`

## Usage

### Run the Analyzer

```bash
python app.py
```

### Workflow Execution

1. Application initializes empty state
2. Document is loaded from `data/document.txt`
3. Three analysis tasks run in parallel:
   - **Summary**: Condenses document to 5 sentences
   - **Topics**: Extracts key themes as bullet points
   - **Sentiment**: Analyzes tone and provides reasoning
4. Results are merged into formatted report
5. Report and execution trace are saved to `logs/`

### Example Output

```
==================================================
DOCUMENT ANALYSIS REPORT
==================================================

SUMMARY
--------
AI is transforming industries globally. Companies use machine learning to automate tasks and improve decision making. AI adoption enhances efficiency and customer experiences. Organizations invest heavily in AI for future growth. The technology enables better business outcomes.

TOPICS
-------
• Artificial Intelligence transformation
• Machine Learning automation
• Business efficiency improvements
• Customer experience enhancement
• Organizational AI investment strategies

SENTIMENT
---------
Positive

Reason: The document discusses beneficial impacts and growth opportunities from AI adoption with optimistic language.

Log saved to: logs/2026-06-05_14-30-22.txt
```

### Output Files

Analysis reports are saved to `logs/` with structure:
```
=== EXECUTION TRACE ===

Document loaded successfully.
Document summarized successfully.
Topics extracted successfully.
Sentiment analyzed successfully.
Results Merged

=== FINAL REPORT ===

[Complete formatted analysis report]
```

## State Management

The `DocumentState` tracks:
- `document`: Raw document text
- `summary`: 5-sentence summary
- `topics`: Extracted key topics
- `sentiment`: Sentiment analysis and reasoning
- `report`: Final merged report
- `trace`: Execution steps for logging

## Prompt Templates

### Summary Prompt
Generates 5 concise sentences capturing document essence

### Topic Prompt
Extracts important topics as bullet points

### Sentiment Prompt
Analyzes emotional tone and provides reasoning

## Configuration

### Customization Points

**Change Input Document:**
```python
# In node.py, modify load_document()
with open('path/to/your/document.txt', 'r', encoding='utf-8') as file:
```

**Adjust Summary Length:**
```python
# In prompts/summary_prompts.py
"Summarize in 10 concise sentences"  # Change 5 to desired count
```

**Change LLM Model:**
```python
# In node.py
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
```

**Modify Temperature:**
```python
# In node.py
temperature=0.3  # Lower = more deterministic, Higher = more creative
```

## Dependencies

- **langchain**: LLM orchestration framework
- **langgraph**: Graph-based workflow orchestration
- **langchain-google-genai**: Google Gemini AI integration
- **python-dotenv**: Environment variable management
- **langchain-core**: Core LangChain utilities

## Performance

**Advantages of Parallel Processing:**
- ✅ Three analysis tasks run simultaneously
- ✅ Faster than sequential execution
- ✅ Efficient use of API calls
- ✅ Scalable architecture for additional analyses

**Execution Time:** Typically 10-30 seconds depending on document size and API latency

## Extending the Analyzer

### Add New Analysis Type

1. **Create prompt file** in `prompts/`:
   ```python
   # prompts/new_analysis_prompts.py
   NEW_ANALYSIS_PROMPT = """..."""
   ```

2. **Add node function** in `graph/node.py`:
   ```python
   def new_analysis_node(state):
       prompt = NEW_ANALYSIS_PROMPT.format(document=state['document'])
       response = llm.invoke(prompt)
       return {
           "new_field": response.content,
           "trace": ["New analysis completed."]
       }
   ```

3. **Update state** in `graph/state.py`:
   ```python
   class DocumentState(TypedDict):
       # ... existing fields ...
       new_field: str
   ```

4. **Add to workflow** in `graph/workflow.py`:
   ```python
   builder.add_node("new_analysis", new_analysis_node)
   builder.add_edge("load_document", "new_analysis")
   builder.add_edge("new_analysis", "merge_results")
   ```

5. **Update merge function** in `graph/node.py`:
   ```python
   # Add new_field to report generation
   ```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `GOOGLE_API_KEY not found` | Ensure `.env` file exists with valid API key |
| `FileNotFoundError: document.txt` | Check document path in `load_document()` function |
| Empty analysis results | Verify document contains sufficient content |
| API rate limiting | Add delays or use lower `temperature` values |
| Logs not saving | Ensure `logs/` directory has write permissions |

## Future Enhancements

- Support for multiple document formats (PDF, DOCX, etc.)
- Entity extraction and Named Entity Recognition (NER)
- Keyword frequency analysis
- Document classification
- Comparison of multiple documents
- Web interface for interactive analysis
- Batch processing capabilities
- Custom prompt templates per document type
- Export to multiple formats (JSON, CSV, HTML)

## LangGraph Concepts Used

- **StateGraph**: Defines workflow structure
- **Nodes**: Individual processing units
- **Edges**: Connections between nodes
- **Parallel Execution**: Multiple edges from single node
- **START/END**: Workflow entry and exit points
- **State Management**: Shared data across nodes

## Related Files

- **Task-1**: [langchain_VS_langgraph.md](../Task-1/langchain_VS_langgraph.md) - Framework comparison
- **Task-2**: This directory - Parallel workflow implementation
- **Task-3**: [self_correcting_essay](../Task-3/self_correcting_essay) - Sequential workflow with conditional logic

## License

Project completed as part of AI/Agentic Systems internship program.

## Support

For questions about the implementation:
- [LangGraph Documentation](https://python.langchain.com/docs/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [Google Generative AI Docs](https://ai.google.dev/docs)
