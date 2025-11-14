#!/usr/bin/env python3
"""
Test script for all 4 agents in the Agentic Professional Services Scoper.

This script tests:
1. Requirement Analyzer Agent - extracts facts from use case input
2. Questionnaire Agent - generates questionnaire from facts
3. Clarifier Agent - asks clarification questions
4. Architecture Agent - generates architecture plan

Usage:
    python test_all_agents.py
    # Or with environment variables:
    INFRA_ENABLE_LLM=gateway_direct.py python test_all_agents.py
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Set environment variable if not already set
if "INFRA_ENABLE_LLM" not in os.environ:
    os.environ["INFRA_ENABLE_LLM"] = "gateway_direct.py"

# Change to requirement_analyzer_agent directory for imports to work correctly
# (since agents use relative imports like "from config import Config")
original_cwd = os.getcwd()
os.chdir(root_dir / "requirement_analyzer_agent")
sys.path.insert(0, str(root_dir / "requirement_analyzer_agent" / "custom_model"))

try:
    from requirement_analyzer_agent.custom_model.agent import RequirementAnalyzerAgent
    from questionnaire_agent.custom_model.agent import QuestionnaireAgent
    from clarifier_agent.custom_model.agent import ClarifierAgent
    from architecture_agent.custom_model.agent import ArchitectureAgent
    from scoper_shared.schemas import (
        UseCaseInput,
        FactExtractionModel,
        QuestionnaireDraft,
        QuestionnaireFinal,
    )
finally:
    os.chdir(original_cwd)


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_result(title: str, data: any, max_length: int = 500) -> None:
    """Print a formatted result."""
    print(f"\n{title}:")
    print("-" * 70)
    if isinstance(data, (dict, list)):
        json_str = json.dumps(data, indent=2, default=str)
        if len(json_str) > max_length:
            print(json_str[:max_length] + "...\n[truncated]")
        else:
            print(json_str)
    else:
        str_data = str(data)
        if len(str_data) > max_length:
            print(str_data[:max_length] + "...\n[truncated]")
        else:
            print(str_data)


async def test_requirement_analyzer() -> FactExtractionModel | None:
    """Test Requirement Analyzer Agent (Agent 1)."""
    print_section("Test 1: Requirement Analyzer Agent")
    
    agent = RequirementAnalyzerAgent()
    
    input_data = UseCaseInput(
        paragraph=(
            "We need to build a predictive maintenance system for industrial equipment. "
            "The system should analyze sensor data from machines (temperature, vibration, pressure) "
            "to predict failures before they occur. We have historical data from the past 2 years "
            "stored in a SQL database. The goal is to reduce unplanned downtime by 30%."
        ),
        use_case_title="Predictive Maintenance System",
        transcript=None,
    )
    
    print_result("📥 Input", {
        "use_case_title": input_data.use_case_title,
        "paragraph": input_data.paragraph[:200] + "...",
    })
    
    try:
        print("\n🔄 Running agent...")
        result = await agent.run(input_data)
        
        print_result("✅ Output", {
            "use_case_title": result.use_case_title,
            "technical_confidence_score": result.technical_confidence_score,
            "key_extracted_requirements": result.key_extracted_requirements,
            "domain_keywords": result.domain_keywords,
            "identified_gaps": result.identified_gaps,
        })
        
        return result
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_questionnaire_agent(facts: FactExtractionModel) -> QuestionnaireDraft | None:
    """Test Questionnaire Agent (Agent 2)."""
    print_section("Test 2: Questionnaire Agent")
    
    agent = QuestionnaireAgent()
    
    print_result("📥 Input (Facts)", {
        "use_case_title": facts.use_case_title,
        "technical_confidence_score": facts.technical_confidence_score,
        "domain_keywords": facts.domain_keywords,
        "identified_gaps": facts.identified_gaps,
    })
    
    try:
        print("\n🔄 Running agent...")
        result = await agent.run(facts)
        
        print_result("✅ Output", {
            "questions_count": len(result.questions),
            "selected_from_master_ids": result.selected_from_master_ids[:5] if result.selected_from_master_ids else [],
            "delta_questions_count": len(result.delta_questions),
            "coverage_estimate": result.coverage_estimate,
            "sample_questions": [
                {
                    "id": q.id,
                    "text": q.text[:100] + "..." if len(q.text) > 100 else q.text,
                    "type": q.type,
                }
                for q in result.questions[:3]
            ],
        })
        
        return result
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_clarifier_agent(draft: QuestionnaireDraft) -> QuestionnaireFinal | None:
    """Test Clarifier Agent (Agent 3)."""
    print_section("Test 3: Clarifier Agent")
    
    agent = ClarifierAgent(max_questions=3)  # Limit to 3 questions for testing
    
    print_result("📥 Input (Questionnaire Draft)", {
        "questions_count": len(draft.questions),
        "coverage_estimate": draft.coverage_estimate,
    })
    
    try:
        print("\n🔄 Running clarification loop...")
        current_answers: list[dict[str, any]] = []
        
        # Ask up to 3 questions
        for i in range(1, 4):
            question, status = await agent.ask_question(draft, current_answers, i)
            
            if question is None:
                print(f"\n✅ No more questions to ask (status: {status})")
                break
            
            print(f"\n❓ Question {i}: {question.text}")
            if question.options:
                print(f"   Options: {question.options}")
            
            # Simulate user answer (for testing, use first option or "yes")
            if question.type == "boolean":
                answer = "yes"
            elif question.options:
                answer = question.options[0]
            else:
                answer = "Database"
            
            print(f"   💬 Simulated Answer: {answer}")
            current_answers.append({"question_id": question.id, "answer": answer})
        
        # Finalize
        print("\n🔄 Finalizing questionnaire...")
        result = await agent.finalize(draft, current_answers)
        
        print_result("✅ Output", {
            "qas_count": len(result.qas),
            "answered_pct": result.answered_pct,
            "gaps": result.gaps,
            "sample_qas": [
                {"id": qa["id"], "answer": qa["answer"]}
                for qa in result.qas[:3]
            ],
        })
        
        return result
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_architecture_agent(questionnaire_final: QuestionnaireFinal) -> tuple | None:
    """Test Architecture Agent (Agent 4)."""
    print_section("Test 4: Architecture Agent")
    
    agent = ArchitectureAgent()
    
    print_result("📥 Input (Questionnaire Final)", {
        "qas_count": len(questionnaire_final.qas),
        "answered_pct": questionnaire_final.answered_pct,
        "gaps": questionnaire_final.gaps,
    })
    
    try:
        print("\n🔄 Running agent...")
        # For testing, we'll use None for RAG context (since RAG system isn't implemented yet)
        result, markdown = await agent.run(questionnaire_final, rag_context=None)
        
        print_result("✅ Output (Architecture Plan)", {
            "steps_count": len(result.steps),
            "assumptions_count": len(result.assumptions),
            "risks_count": len(result.risks),
            "notes_count": len(result.notes),
            "sample_steps": [
                {
                    "id": step.id,
                    "name": step.name,
                    "purpose": step.purpose[:100] + "..." if len(step.purpose) > 100 else step.purpose,
                }
                for step in result.steps[:3]
            ],
        })
        
        print_result("📄 Markdown Output", markdown[:500] + "..." if len(markdown) > 500 else markdown)
        
        return (result, markdown)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


async def main() -> None:
    """Run all agent tests in sequence."""
    print("\n" + "=" * 70)
    print("  🧪 Testing All 4 Agents - Agentic Professional Services Scoper")
    print("=" * 70)
    print(f"\n📋 Configuration:")
    print(f"   INFRA_ENABLE_LLM: {os.getenv('INFRA_ENABLE_LLM', 'not set')}")
    print(f"   USE_DATAROBOT_LLM_GATEWAY: {os.getenv('USE_DATAROBOT_LLM_GATEWAY', 'not set')}")
    print(f"   DATAROBOT_API_TOKEN: {'set' if os.getenv('DATAROBOT_API_TOKEN') else 'not set'}")
    print(f"   DATAROBOT_ENDPOINT: {os.getenv('DATAROBOT_ENDPOINT', 'not set')}")
    
    # Check if DataRobot credentials are available
    if os.getenv("INFRA_ENABLE_LLM") == "gateway_direct.py":
        if not os.getenv("DATAROBOT_API_TOKEN") or not os.getenv("DATAROBOT_ENDPOINT"):
            print("\n⚠️  WARNING: DataRobot LLM Gateway is enabled but credentials are missing!")
            print("   Please set DATAROBOT_API_TOKEN and DATAROBOT_ENDPOINT environment variables.")
            print("   Or set INFRA_ENABLE_LLM to a different value to use direct OpenAI.")
            print("\n   Example:")
            print("   export DATAROBOT_API_TOKEN='your-token'")
            print("   export DATAROBOT_ENDPOINT='https://app.datarobot.com/api/v2'")
            print("\n   Or to test with direct OpenAI instead:")
            print("   unset INFRA_ENABLE_LLM")
            print("   export OPENAI_API_KEY='your-key'")
            response = input("\n   Continue anyway? (y/n): ")
            if response.lower() != 'y':
                print("   Exiting...")
                return
    
    results = {}
    
    # Test 1: Requirement Analyzer
    facts = await test_requirement_analyzer()
    results["requirement_analyzer"] = facts is not None
    
    if not facts:
        print("\n❌ Requirement Analyzer failed. Cannot continue with other tests.")
        return
    
    # Test 2: Questionnaire Agent
    draft = await test_questionnaire_agent(facts)
    results["questionnaire"] = draft is not None
    
    if not draft:
        print("\n❌ Questionnaire Agent failed. Cannot continue with other tests.")
        return
    
    # Test 3: Clarifier Agent
    questionnaire_final = await test_clarifier_agent(draft)
    results["clarifier"] = questionnaire_final is not None
    
    if not questionnaire_final:
        print("\n❌ Clarifier Agent failed. Cannot continue with Architecture Agent test.")
        return
    
    # Test 4: Architecture Agent
    arch_result = await test_architecture_agent(questionnaire_final)
    results["architecture"] = arch_result is not None
    
    # Summary
    print_section("📊 Test Summary")
    print("\nResults:")
    for agent_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {agent_name:25} {status}")
    
    all_passed = all(results.values())
    print("\n" + "=" * 70)
    if all_passed:
        print("  ✅ All tests passed!")
    else:
        print("  ⚠️  Some tests failed. Check output above for details.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

