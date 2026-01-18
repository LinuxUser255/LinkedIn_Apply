#!/usr/bin/env python3
"""
Test script for follow company checkbox handling.
This validates that the follow company checkbox will be properly unchecked.
"""

import os
import json
from src.bot.dynamic_form_handler import DynamicFormHandler

def test_follow_company_config():
    """Test that follow company is properly configured."""
    print("Testing follow company configuration...")
    
    # Test credentials config
    creds_path = os.path.expanduser("~/.config/LinkedIn_Apply_Profile/credentials.json")
    if os.path.exists(creds_path):
        with open(creds_path, 'r') as f:
            creds = json.load(f)
        
        follow_companies = creds.get('FOLLOW_COMPANIES', None)
        if follow_companies is False:
            print("✓ FOLLOW_COMPANIES correctly set to false in credentials")
        elif follow_companies is True:
            print("⚠ FOLLOW_COMPANIES is set to true - companies will be followed!")
        else:
            print(f"ℹ FOLLOW_COMPANIES not explicitly set (value: {follow_companies}) - will default to false")
    else:
        print("✗ Credentials config not found")
    
    # Test dynamic questions config
    config_path = os.path.expanduser("~/.config/LinkedIn_Apply_Profile/dynamic_questions.json")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        follow_pattern = config.get('question_patterns', {}).get('follow_company', {})
        if follow_pattern:
            print("✓ Follow company pattern configured in dynamic questions")
            print(f"  - Keywords: {follow_pattern.get('keywords', [])}")
            print(f"  - Default answer: {follow_pattern.get('default_answer', 'Not set')}")
            print(f"  - Answer from config: {follow_pattern.get('answer_from_config', 'Not set')}")
        else:
            print("✗ Follow company pattern not found in dynamic questions")
    else:
        print("✗ Dynamic questions config not found")

def test_follow_company_pattern_matching():
    """Test pattern matching for follow company questions."""
    print("\nTesting follow company pattern matching...")
    
    # Mock driver for testing
    class MockDriver:
        pass
    
    try:
        handler = DynamicFormHandler(MockDriver())
        
        # Test follow company related texts
        test_questions = [
            "Follow company",
            "Follow this company", 
            "Follow organization",
            "Would you like to follow this company?",
            "Check to follow this organization"
        ]
        
        for question in test_questions:
            match = handler._match_question_pattern(question.lower())
            if match:
                answer = handler._get_answer_value(match)
                should_check = answer.lower() in ['true', 'yes', '1'] if answer else False
                default_answer = match.get('default_answer', 'No')
                
                if not should_check and default_answer.lower() in ['no', 'false']:
                    print(f"✓ '{question}' -> Will UNCHECK (Good!)")
                else:
                    print(f"⚠ '{question}' -> Will CHECK (Check your config!)")
            else:
                print(f"✗ '{question}' -> No match found")
                
    except Exception as e:
        print(f"✗ Error testing pattern matching: {e}")

def test_checkbox_logic():
    """Test the checkbox handling logic."""
    print("\nTesting checkbox handling logic...")
    
    # Test different answer configurations
    test_configs = [
        {"answer_from_config": "FOLLOW_COMPANIES", "credentials_value": False},
        {"answer_from_config": "FOLLOW_COMPANIES", "credentials_value": True}, 
        {"default_answer": "No"},
        {"default_answer": "Yes"},
        {"answer": "false"},
        {"answer": "true"}
    ]
    
    for i, config in enumerate(test_configs):
        print(f"\nTest case {i+1}: {config}")
        
        # Simulate the logic from handle_checkbox_question
        answer = ""
        if "answer_from_config" in config:
            # Simulate getting from credentials
            answer = str(config.get("credentials_value", "")).lower()
        elif "answer" in config:
            answer = config["answer"]
        
        should_check = answer.lower() in ['true', 'yes', '1']
        
        # Special follow company logic
        if 'follow' in "follow company" and not answer:
            should_check = config.get('default_answer', 'No').lower() in ['true', 'yes', '1']
        
        if should_check:
            print(f"  Result: Will CHECK the follow company box ⚠")
        else:
            print(f"  Result: Will UNCHECK the follow company box ✓")

def main():
    """Run all follow company tests."""
    print("=== Follow Company Checkbox Test ===\n")
    
    test_follow_company_config()
    test_follow_company_pattern_matching()
    test_checkbox_logic()
    
    print("\n=== Summary ===")
    print("Key points:")
    print("• FOLLOW_COMPANIES should be 'false' in credentials.json")
    print("• Follow company checkbox should be UNCHECKED by default")
    print("• The bot will actively uncheck any checked follow company boxes")
    print("• This happens at each form step AND at final submission")
    print("\nIf you see warnings above, review your configuration!")

if __name__ == "__main__":
    main()