#!/usr/bin/env python3
"""
Script to copy and organize platform guides from Google Drive reference documents
into the scoper_shared KB content directory, organized by domain track.
"""

import shutil
from pathlib import Path
from typing import Dict, List

# Source and destination paths
SOURCE_DIR = Path(
    "/Users/caroline.sieger/Google Drive/My Drive/Solutions Scoping & Sizing Agent/Dev Work/knowledge base docs/platform_guides"
)
DEST_BASE = Path("scoper_shared/src/scoper_shared/kb_content/platform_guides")

# Track categorization rules based on filename patterns
TRACK_RULES: Dict[str, List[str]] = {
    "time_series": [
        "time-index",
        "time-series",
        "timeseries",
        "forecast",
        "temporal",
    ],
    "nlp": [
        "nlp",
        "text",
        "natural-language",
        "language-model",
    ],
    "cv": [
        "image",
        "vision",
        "computer-vision",
        "cv-",
    ],
    "genai_rag": [
        "app-builder",
        "genai",
        "generative",
        "rag",
        "retrieval",
        "agent",
        "chat",
        "llm",
        "openai",
        "notebooks",
    ],
    "classic_ml": [
        "mlops",
        "deployment",
        "modeling",
        "predictions",
        "model",
        "training",
        "eda",
        "feature",
        "data-import",
        "data-transform",
        "governance",
        "monitor",
    ],
    "infrastructure": [
        "pulumi",
        "terraform",
        "iac",
        "kubernetes",
        "aws",
        "cloud",
    ],
    "general": [
        "index",
        "overview",
        "classic-ui",
        "integrations",
    ],
}


def categorize_file(filename: str) -> str:
    """
    Categorize a file into a track based on filename patterns.
    
    Args:
        filename: The filename to categorize
        
    Returns:
        Track name (time_series, nlp, cv, genai_rag, classic_ml, infrastructure, general)
    """
    filename_lower = filename.lower()
    
    # Check each track's keywords
    for track, keywords in TRACK_RULES.items():
        for keyword in keywords:
            if keyword in filename_lower:
                return track
    
    # Default to general if no match
    return "general"


def copy_platform_guides() -> None:
    """Copy and organize all platform guide Markdown files."""
    if not SOURCE_DIR.exists():
        print(f"❌ Source directory not found: {SOURCE_DIR}")
        return
    
    if not DEST_BASE.exists():
        DEST_BASE.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created destination directory: {DEST_BASE}")
    
    # Track statistics
    stats: Dict[str, int] = {track: 0 for track in TRACK_RULES.keys()}
    stats["other"] = 0
    
    # Find all .md files
    md_files = list(SOURCE_DIR.glob("*.md"))
    print(f"📄 Found {len(md_files)} Markdown files to process\n")
    
    for md_file in md_files:
        track = categorize_file(md_file.name)
        dest_dir = DEST_BASE / track
        dest_dir.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
        dest_file = dest_dir / md_file.name
        
        # Copy file
        try:
            shutil.copy2(md_file, dest_file)
            stats[track] += 1
            print(f"  ✓ {md_file.name} → {track}/")
        except Exception as e:
            print(f"  ✗ Error copying {md_file.name}: {e}")
            stats["other"] += 1
    
    # Print summary
    print(f"\n📊 Summary:")
    print(f"  Total files processed: {len(md_files)}")
    for track, count in sorted(stats.items()):
        if count > 0:
            print(f"  {track}: {count} files")
    
    # Handle PDF files (need conversion)
    pdf_files = list(SOURCE_DIR.glob("*.pdf"))
    if pdf_files:
        print(f"\n⚠️  Found {len(pdf_files)} PDF files (need manual conversion to Markdown):")
        for pdf_file in pdf_files:
            print(f"  - {pdf_file.name}")


if __name__ == "__main__":
    print("🚀 Organizing Platform Guides\n")
    copy_platform_guides()
    print("\n✅ Done!")

