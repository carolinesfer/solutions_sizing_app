# Knowledge Base Content

This directory contains the Knowledge Base (KB) content used by the Agentic Professional Services Scoper system.

## Directory Structure

```
kb_content/
├── master_questionnaire.json          # Master questionnaire with all questions
└── platform_guides/                   # Platform guides organized by domain track
    ├── time_series/                   # Time series forecasting guides
    ├── nlp/                           # Natural Language Processing guides
    ├── cv/                            # Computer Vision guides
    ├── genai_rag/                     # GenAI and RAG guides
    ├── classic_ml/                    # Classic ML and MLOps guides
    ├── infrastructure/                 # Infrastructure and deployment guides
    └── general/                       # General/overview guides
```

## Master Questionnaire

**File:** `master_questionnaire.json`

Contains all questions that can be asked during the scoping process. Each question follows the `Question` schema:

```json
{
  "id": "q_genai_chatbot_1",
  "text": "What is the primary data source for this project?",
  "type": "single_select",
  "options": ["Database", "API", "File upload", "Streaming data"],
  "required": true,
  "rationale": "Understanding the data source helps determine ingestion requirements",
  "tracks": ["classic_ml", "time_series"]
}
```

### Question Types

- `free_text`: Open-ended text response
- `single_select`: Choose one option from a list
- `multi_select`: Choose multiple options from a list
- `bool`: Yes/No or True/False question

### Tracks

Questions are tagged with domain tracks to enable filtering:
- `classic_ml`: Traditional machine learning use cases
- `time_series`: Time series forecasting and temporal analysis
- `nlp`: Natural Language Processing
- `cv`: Computer Vision
- `genai_rag`: Generative AI and Retrieval-Augmented Generation
- `infrastructure`: Deployment and infrastructure concerns

## Platform Guides

**Directory:** `platform_guides/`

Contains Markdown documentation files organized by domain track. The KB Retriever loads guides based on selected tracks and concatenates multiple files within each track subdirectory.

### Source Documents

Platform guides are sourced from:
- **DataRobot Documentation**: `docs.datarobot.com-*.md` files
- **Pulumi Documentation**: `www.pulumi.com-*.md` files
- **GitHub Community Examples**: `github.com-datarobot-community-*.md` files

### Organization Rules

- **Time Series**: Files containing "time-index", "time-series", "forecast", "temporal"
- **NLP**: Files containing "nlp", "text", "natural-language", "language-model"
- **CV**: Files containing "image", "vision", "computer-vision"
- **GenAI/RAG**: Files containing "app-builder", "genai", "generative", "rag", "agent", "chat", "llm", "notebooks"
- **Classic ML**: Files containing "mlops", "deployment", "modeling", "predictions", "model", "training", "eda", "feature"
- **Infrastructure**: Files containing "pulumi", "terraform", "iac", "kubernetes", "aws", "cloud"
- **General**: Files containing "index", "overview", "classic-ui", "integrations"

## Source Reference Documents

### Master Questionnaires

**Location:** `/Users/caroline.sieger/Google Drive/My Drive/Solutions Scoping & Sizing Agent/Dev Work/knowledge base docs/questionnaires/`

**Files:**
- `SCOPING MASTER SHEET.pdf` - Main scoping questionnaire (PDF, needs extraction)
- `APP QUESTIONNAIRES.pdf` - Application-specific questions (PDF, needs extraction)
- `AI Analyst - Use Case Questionnaire TEMPLATE v02.docx.md` - ✅ Extracted
- `Custom Application - Use Case Questionnaire TEMPLATE v01.docx.md` - ✅ Extracted
- `Execution Project Questions to Ask.md` - ✅ Extracted
- `Use Case Deep Dive Workshop (Production).pdf` - Workshop questions (PDF, needs extraction)
- `Complexity Questionnaire for Predictive AI TEMPLATE.pdf` - Specialized questionnaire (PDF, needs extraction)
- `Catalyst Build Phase Scoping TEMPLATE.pdf` - Catalyst-specific questions (PDF, needs extraction)

### Platform Guides

**Location:** `/Users/caroline.sieger/Google Drive/My Drive/Solutions Scoping & Sizing Agent/Dev Work/knowledge base docs/platform_guides/`

**Files:**
- 184 Markdown files (DataRobot docs, Pulumi docs, GitHub examples) - ✅ Copied and organized
- `DataRobot Time Series II - Current.pdf` - Time series guide (PDF, needs conversion to Markdown)

## Updating KB Content

### Adding New Questions

1. Extract questions from source documents (PDFs may require manual extraction or PDF parsing tools)
2. Convert to JSON format matching the `Question` schema
3. Assign appropriate `tracks` based on question content
4. Add to `master_questionnaire.json` with unique IDs following convention: `q_<category>_<number>`

### Adding New Platform Guides

1. Copy Markdown files to the appropriate track subdirectory in `platform_guides/`
2. Ensure files are in Markdown format (`.md` extension)
3. For PDFs, convert to Markdown first using appropriate tools
4. Files are automatically loaded by `KBRetriever.get_platform_guides()` based on track selection

### Question Extraction Process

1. **From Markdown files**: Use `scripts/extract_questions.py` to automatically extract questions
2. **From PDF files**: 
   - Option 1: Manual extraction and conversion to JSON
   - Option 2: Use PDF parsing tools (e.g., `pypdf`, `pdfplumber`) to extract text, then parse questions
   - Option 3: Use LLM to extract structured questions from PDF text

### Platform Guide Organization

Use `scripts/organize_platform_guides.py` to automatically categorize and copy platform guides by track based on filename patterns.

## Current Status

- ✅ **Master Questionnaire**: 43 questions extracted from Markdown files
- ⚠️ **PDF Question Extraction**: 5 PDF files need manual extraction or PDF parsing
- ✅ **Platform Guides**: 184 Markdown files copied and organized by track
- ⚠️ **PDF Platform Guide**: 1 PDF file (`DataRobot Time Series II - Current.pdf`) needs conversion to Markdown

## Notes

- Questions extracted from PDFs will need to be manually reviewed and added to `master_questionnaire.json`
- The `DataRobot Time Series II - Current.pdf` should be converted to Markdown and placed in `platform_guides/time_series/`
- Question IDs should be unique and follow a consistent naming convention
- Track assignments may need manual review to ensure accuracy

