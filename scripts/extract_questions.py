#!/usr/bin/env python3
"""
Script to extract questions from reference questionnaire documents and convert
them to JSON format matching the Question schema.
"""

import json
import re
from pathlib import Path
from typing import Dict, List

# Source directory for questionnaires
SOURCE_DIR = Path(
    "/Users/caroline.sieger/Google Drive/My Drive/Solutions Scoping & Sizing Agent/Dev Work/knowledge base docs/questionnaires"
)
DEST_FILE = Path("scoper_shared/src/scoper_shared/kb_content/master_questionnaire.json")

# Question type inference patterns
SINGLE_SELECT_PATTERNS = [
    r"where",
    r"which",
    r"what.*(?:format|method|type|framework|level|access)",
    r"how many",
    r"how large",
]
BOOL_PATTERNS = [
    r"do you",
    r"are there",
    r"is there",
    r"will.*require",
    r"can you",
    r"does.*require",
]
MULTI_SELECT_PATTERNS = [
    r"what.*(?:all|multiple|list)",
    r"which.*(?:all|multiple|list)",
]


def infer_question_type(text: str) -> str:
    """
    Infer question type from text.
    
    Args:
        text: Question text
        
    Returns:
        Question type: "free_text", "single_select", "multi_select", or "bool"
    """
    text_lower = text.lower()
    
    # Check for boolean patterns
    for pattern in BOOL_PATTERNS:
        if re.search(pattern, text_lower):
            return "bool"
    
    # Check for multi-select patterns
    for pattern in MULTI_SELECT_PATTERNS:
        if re.search(pattern, text_lower):
            return "multi_select"
    
    # Check for single-select patterns
    for pattern in SINGLE_SELECT_PATTERNS:
        if re.search(pattern, text_lower):
            return "single_select"
    
    # Default to free_text
    return "free_text"


def extract_questions_from_markdown(content: str, source_file: str) -> List[Dict]:
    """
    Extract questions from Markdown content.
    
    Args:
        content: Markdown file content
        source_file: Source filename for context
        
    Returns:
        List of question dictionaries
    """
    questions = []
    lines = content.split("\n")
    
    # Pattern to match numbered questions
    question_pattern = re.compile(r"^(\d+\.?\s*)(.+)$")
    # Pattern to match table rows with questions
    table_pattern = re.compile(r"^\|\s*(\d+\.?\s*)?(.+?)\s*\|")
    
    question_id_counter = 1
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("|") and "---" in line:
            continue
        
        # Try table format first
        table_match = table_pattern.match(line)
        if table_match:
            question_text = table_match.group(2).strip()
            if question_text and len(question_text) > 10:  # Filter out headers
                # Clean up markdown formatting
                question_text = re.sub(r"\*([^*]+)\*", r"\1", question_text)  # Remove bold
                question_text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", question_text)  # Remove links
                question_text = question_text.replace("\\", "")
                
                q_type = infer_question_type(question_text)
                q_id = f"q_{source_file.replace('.md', '').replace(' ', '_').lower()}_{question_id_counter}"
                
                questions.append({
                    "id": q_id,
                    "text": question_text,
                    "type": q_type,
                    "options": None if q_type == "free_text" or q_type == "bool" else [],
                    "required": True,
                    "rationale": f"Extracted from {source_file}",
                    "tracks": []  # Will be assigned based on content
                })
                question_id_counter += 1
            continue
        
        # Try numbered list format
        match = question_pattern.match(line)
        if match:
            question_text = match.group(2).strip()
            if question_text and len(question_text) > 10:
                # Clean up markdown formatting
                question_text = re.sub(r"\*([^*]+)\*", r"\1", question_text)
                question_text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", question_text)
                question_text = question_text.replace("\\", "")
                
                q_type = infer_question_type(question_text)
                q_id = f"q_{source_file.replace('.md', '').replace(' ', '_').lower()}_{question_id_counter}"
                
                questions.append({
                    "id": q_id,
                    "text": question_text,
                    "type": q_type,
                    "options": None if q_type == "free_text" or q_type == "bool" else [],
                    "required": True,
                    "rationale": f"Extracted from {source_file}",
                    "tracks": []
                })
                question_id_counter += 1
    
    return questions


def assign_tracks(question: Dict) -> None:
    """
    Assign domain tracks to a question based on its content.
    
    Args:
        question: Question dictionary to update
    """
    text_lower = question["text"].lower()
    tracks = set()
    
    # Time series keywords
    if any(kw in text_lower for kw in ["forecast", "time series", "temporal", "sequence", "time-based"]):
        tracks.add("time_series")
    
    # NLP keywords
    if any(kw in text_lower for kw in ["text", "nlp", "language", "document", "chatbot", "llm", "generative"]):
        tracks.add("nlp")
        tracks.add("genai_rag")
    
    # CV keywords
    if any(kw in text_lower for kw in ["image", "vision", "computer vision", "cv", "photo", "picture"]):
        tracks.add("cv")
    
    # GenAI/RAG keywords
    if any(kw in text_lower for kw in ["rag", "retrieval", "agent", "generative ai", "genai", "chatbot", "llm"]):
        tracks.add("genai_rag")
    
    # Infrastructure keywords
    if any(kw in text_lower for kw in ["deployment", "infrastructure", "cloud", "on-premise", "environment", "api", "database"]):
        tracks.add("infrastructure")
    
    # If no specific tracks, add classic_ml as default
    if not tracks:
        tracks.add("classic_ml")
    
    question["tracks"] = list(tracks)


def extract_from_markdown_files() -> List[Dict]:
    """Extract questions from all Markdown files."""
    all_questions = []
    
    md_files = list(SOURCE_DIR.glob("*.md"))
    print(f"📄 Processing {len(md_files)} Markdown files\n")
    
    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8")
            questions = extract_questions_from_markdown(content, md_file.name)
            for q in questions:
                assign_tracks(q)
            all_questions.extend(questions)
            print(f"  ✓ {md_file.name}: {len(questions)} questions extracted")
        except Exception as e:
            print(f"  ✗ Error processing {md_file.name}: {e}")
    
    return all_questions


def main() -> None:
    """Main extraction function."""
    print("🚀 Extracting Questions from Reference Documents\n")
    
    # Extract from Markdown files
    questions = extract_from_markdown_files()
    
    # Load existing questions if file exists
    existing_questions = []
    if DEST_FILE.exists():
        try:
            with open(DEST_FILE, "r", encoding="utf-8") as f:
                existing_questions = json.load(f)
            print(f"\n📋 Found {len(existing_questions)} existing questions in master_questionnaire.json")
        except Exception as e:
            print(f"\n⚠️  Could not load existing questions: {e}")
    
    # Merge questions (avoid duplicates by ID)
    existing_ids = {q["id"] for q in existing_questions}
    new_questions = [q for q in questions if q["id"] not in existing_ids]
    
    # Combine and save
    all_questions = existing_questions + new_questions
    
    # Ensure unique IDs
    seen_ids = set()
    unique_questions = []
    for q in all_questions:
        if q["id"] not in seen_ids:
            unique_questions.append(q)
            seen_ids.add(q["id"])
    
    # Save to file
    DEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DEST_FILE, "w", encoding="utf-8") as f:
        json.dump(unique_questions, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Summary:")
    print(f"  Total questions: {len(unique_questions)}")
    print(f"  Existing questions: {len(existing_questions)}")
    print(f"  New questions extracted: {len(new_questions)}")
    print(f"  Saved to: {DEST_FILE}")
    
    # Track distribution
    track_counts = {}
    for q in unique_questions:
        for track in q.get("tracks", []):
            track_counts[track] = track_counts.get(track, 0) + 1
    
    print(f"\n📈 Questions by track:")
    for track, count in sorted(track_counts.items()):
        print(f"  {track}: {count} questions")
    
    print(f"\n⚠️  Note: PDF files need manual extraction or PDF parsing:")
    pdf_files = list(SOURCE_DIR.glob("*.pdf"))
    for pdf_file in pdf_files:
        print(f"  - {pdf_file.name}")


if __name__ == "__main__":
    main()

