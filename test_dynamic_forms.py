#!/usr/bin/env python3
"""
Test script for dynamic form handler integration.
Run this to validate the configuration and handler are working properly.
"""

import os
import json
from src.bot.dynamic_form_handler import DynamicFormHandler

def test_config_loading():
    """Test that configuration files can be loaded."""
    print("Testing configuration loading...")
    
    # Test dynamic questions config
    config_path = os.path.expanduser("~/.config/LinkedIn_Apply_Profile/dynamic_questions.json")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        print(f"✓ Dynamic questions config loaded: {len(config.get('question_patterns', {}))} patterns")
        
        # Print some examples
        for pattern_name, pattern_config in list(config.get('question_patterns', {}).items())[:3]:
            print(f"  - {pattern_name}: {pattern_config.get('keywords', [])[0] if pattern_config.get('keywords') else 'No keywords'}")
    else:
        print("✗ Dynamic questions config not found")
    
    # Test credentials config
    creds_path = os.path.expanduser("~/.config/LinkedIn_Apply_Profile/credentials.json")
    if os.path.exists(creds_path):
        with open(creds_path, 'r') as f:
            creds = json.load(f)
        print(f"✓ Credentials config loaded: {len(creds)} entries")
    else:
        print("✗ Credentials config not found")

def test_pattern_matching():
    """Test pattern matching logic."""
    print("\nTesting pattern matching...")
    
    # Mock driver for testing (we won't actually use Selenium here)
    class MockDriver:
        pass
    
    try:
        handler = DynamicFormHandler(MockDriver())
        
        # Test some example questions from your screenshot
        test_questions = [
            "Are you willing to take a drug test, in accordance with local law/regulations?",
            "Are you comfortable working in a remote setting?", 
            "Are you a US Citizen?",
            "Are you willing to complete a set of pre-interview questions?",
            "Do you have an OSCP or HackTheBox certification?"
        ]
        
        for question in test_questions:
            match = handler._match_question_pattern(question.lower())
            if match:
                answer = handler._get_answer_value(match)
                print(f"✓ '{question[:50]}...' -> {answer} ({match.get('type')})")
            else:
                print(f"✗ '{question[:50]}...' -> No match found")
                
    except Exception as e:
        print(f"✗ Error testing pattern matching: {e}")

def test_fallback_strategies():
    """Test fallback strategy configuration."""
    print("\nTesting fallback strategies...")
    
    config_path = os.path.expanduser("~/.config/LinkedIn_Apply_Profile/dynamic_questions.json")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        fallback = config.get('fallback_strategies', {})
        if fallback:
            print("✓ Fallback strategies configured:")
            for strategy_type, strategy_config in fallback.items():
                print(f"  - {strategy_type}: {strategy_config}")
        else:
            print("✗ No fallback strategies found")
    else:
        print("✗ Config file not found")

def main():
    """Run all tests."""
    print("=== Dynamic Form Handler Integration Test ===\n")
    
    test_config_loading()
    test_pattern_matching() 
    test_fallback_strategies()
    
    print("\n=== Test Complete ===")
    print("If you see errors above, check that:")
    print("1. ~/.config/LinkedIn_Apply_Profile/dynamic_questions.json exists")
    print("2. ~/.config/LinkedIn_Apply_Profile/credentials.json exists")
    print("3. The JSON files have valid syntax")

if __name__ == "__main__":
    main()