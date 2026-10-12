# Super Investing — AI Research Agent

## Overview

This project is an AI-powered research agent that analyzes a company's research documents and generates a concise, structured Markdown research brief.

The project was developed for the Super Investing AI Innovator Assignment. It uses Sarvottam Cables Ltd (NSE: SRVCABLE) as the test company and assumes the current date is 23 September 2026.

The agent uses only the documents supplied in the research pack and does not search the web for additional company information.

## Features

- Reads company research documents from a local folder.
- Generates a research brief with five sections:
  - Snapshot
  - Bull Case
  - Bear Case
  - Open Questions
  - Sources
- Includes source IDs to help trace factual claims to their supporting documents.
- Highlights conflicting financial figures and missing information.
- Generates multiple outputs to compare different prompt designs.

## Technology Stack

- **Language:** Python
- **LLM:** Google Gemini API
- **Libraries:** `google-genai`, `python-dotenv`, `pypdf`, `python-docx`

## Project Structure

```text
super-investing-agent/
├── research_pack/          # Supplied company research documents
├── outputs/                # Generated research briefs
│   ├── run1_baseline.md
│   ├── run2_citations.md
│   └── run3_conflicts.md
├── agent.py                # Main agent implementation
├── system_prompt.md        # Agent instructions
├── test_log.md             # Experiments and observations
├── requirements.txt        # Python dependencies
├── .env                    # API key; not committed
└── .gitignore              # Excluded files
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd super-investing-agent
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
```

Replace the placeholder with your own Gemini API key. Do not commit the `.env` file to GitHub.

### 5. Run the agent

```powershell
python agent.py
```

The generated research briefs are saved in the `outputs/` directory.

## Design Decisions

1. **Local document processing:** The agent reads the supplied research pack instead of searching the internet. This keeps the analysis grounded in the assignment's documents.
2. **Separate system prompt:** Instructions are maintained in `system_prompt.md`, making the agent's behaviour easier to inspect and improve.
3. **Source references:** Documents are assigned source IDs so that claims can be traced back to their source files.
4. **Iterative testing:** Three prompt variations were tested to improve citation quality, conflict handling, and the relevance of the final brief.

## Testing

The agent was evaluated through three runs:

- **Run 1 — Baseline:** Generated the initial research brief.
- **Run 2 — Citation-first:** Emphasized claim-level source references.
- **Run 3 — Conflict-aware:** Emphasized conflicting figures, missing evidence, and uncertainty.

Detailed observations and improvements are documented in `test_log.md`.

## Limitations

- The agent relies on the supplied documents and does not independently verify claims using external sources.
- Source references indicate where claims should be checked, but they do not guarantee that a claim is accurate.
- Conflicting figures may remain unresolved when the available documents do not provide sufficient evidence.
- The output may contain repetitive or unsupported statements and should be reviewed against the original documents before being used for financial decisions.

## Security

API credentials must be stored locally in `.env`. The `.env` file and virtual environment should be excluded from version control using `.gitignore`.

## Disclaimer

This project is an experimental research-assistance tool created for an assignment. It is not investment advice and does not provide buy or sell recommendations.