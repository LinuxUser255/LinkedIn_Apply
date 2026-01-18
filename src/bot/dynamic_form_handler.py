"""
Dynamic form handler for LinkedIn application questions with wildcard pattern matching.
Handles edge cases and unknown question types intelligently.
"""
import json
import os
import time
import logging
from typing import Dict, List, Optional, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class DynamicFormHandler:
    """Handles dynamic LinkedIn application forms with pattern-based question recognition."""
    
    def __init__(self, driver: webdriver.Chrome, config_path: str = None, credentials_path: str = None):
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        
        # Load dynamic questions config
        if not config_path:
            config_path = os.path.expanduser("~/.config/LinkedIn_Apply_Profile/dynamic_questions.json")
        
        if not credentials_path:
            credentials_path = os.path.expanduser("~/.config/LinkedIn_Apply_Profile/credentials.json")
            
        self.config = self._load_json_config(config_path)
        self.credentials = self._load_json_config(credentials_path)
        
        # Cache for recognized patterns
        self._pattern_cache = {}
        
    def _load_json_config(self, file_path: str) -> Dict:
        """Load JSON configuration file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.warning(f"Could not load config from {file_path}: {e}")
            return {}
    
    def _extract_question_text(self, element) -> str:
        """Extract question text from various element types."""
        question_text = ""
        
        # Try different attributes and nearby elements
        sources = [
            element.get_attribute('aria-label'),
            element.get_attribute('name'), 
            element.get_attribute('placeholder'),
            element.get_attribute('id')
        ]
        
        # Get text from nearby labels/spans/divs
        try:
            container = element.find_element(By.XPATH, "ancestor::*[self::div or self::section or self::form][1]")
            nearby_elements = container.find_elements(By.XPATH, ".//label | .//span | .//p | .//div")
            for elem in nearby_elements[:5]:  # Limit to first 5 elements
                text = elem.get_attribute('textContent') or elem.text
                if text and len(text.strip()) > 5:  # Skip very short text
                    sources.append(text.strip())
        except:
            pass
        
        question_text = " ".join(filter(None, sources)).lower()
        return question_text
    
    def _match_question_pattern(self, question_text: str) -> Optional[Dict]:
        """Match question text against configured patterns."""
        if not self.config.get('question_patterns'):
            return None
            
        # Check cache first
        if question_text in self._pattern_cache:
            return self._pattern_cache[question_text]
        
        best_match = None
        best_score = 0
        
        for pattern_name, pattern_config in self.config['question_patterns'].items():
            keywords = pattern_config.get('keywords', [])
            score = sum(1 for keyword in keywords if keyword.lower() in question_text)
            
            if score > best_score:
                best_score = score
                best_match = pattern_config
                
        # Cache the result
        if best_match:
            self._pattern_cache[question_text] = best_match
            
        return best_match if best_score > 0 else None
    
    def _get_answer_value(self, pattern_config: Dict) -> str:
        """Get the answer value from pattern configuration."""
        if 'answer_from_config' in pattern_config:
            config_key = pattern_config['answer_from_config']
            return str(self.credentials.get(config_key, ''))
        elif 'answer_logic' in pattern_config:
            return self._execute_answer_logic(pattern_config['answer_logic'])
        else:
            return str(pattern_config.get('answer', ''))
    
    def _execute_answer_logic(self, logic_name: str) -> str:
        """Execute custom answer logic."""
        if logic_name == 'check_certifications':
            # Check if user has certifications in credentials
            certs = self.credentials.get('CERTIFICATIONS', 'None').lower()
            if certs in ['none', '', 'n/a']:
                return 'No'
            else:
                return 'Yes'
        return 'No'  # Default fallback
    
    def handle_yes_no_question(self, modal, question_text: str, answer: str) -> bool:
        """Handle yes/no radio button questions."""
        try:
            # Try fieldset + legend approach first
            for keyword in question_text.split()[:5]:  # Use first 5 words
                try:
                    fieldset = modal.find_element(By.XPATH,
                        f".//fieldset[.//legend[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{keyword}')]]")
                    label = fieldset.find_element(By.XPATH, f".//label[normalize-space()='{answer}']")
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label)
                    label.click()
                    return True
                except:
                    continue
            
            # Try generic container approach
            containers = modal.find_elements(By.XPATH, ".//div | .//section | .//form")
            for container in containers:
                container_text = (container.get_attribute('textContent') or '').lower()
                if any(word in container_text for word in question_text.split()[:3]):
                    try:
                        labels = container.find_elements(By.XPATH, f".//label[normalize-space()='{answer}']")
                        for label in labels:
                            try:
                                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label)
                                label.click()
                                return True
                            except:
                                continue
                    except:
                        continue
            return False
        except Exception as e:
            self.logger.debug(f"Error handling yes/no question: {e}")
            return False
    
    def handle_dropdown_question(self, modal, question_text: str, pattern_config: Dict) -> bool:
        """Handle dropdown/select questions."""
        try:
            answer = self._get_answer_value(pattern_config)
            dropdown_values = pattern_config.get('dropdown_values', [answer])
            
            # Find dropdown elements
            selects = modal.find_elements(By.TAG_NAME, 'select')
            for select_elem in selects:
                try:
                    select_context = self._extract_question_text(select_elem)
                    if any(word in select_context for word in question_text.split()[:3]):
                        select_obj = Select(select_elem)
                        
                        # Try each possible dropdown value
                        for value in dropdown_values:
                            for option in select_obj.options:
                                option_text = (option.text or '').strip()
                                if value.lower() in option_text.lower():
                                    try:
                                        select_obj.select_by_visible_text(option_text)
                                        return True
                                    except:
                                        try:
                                            select_obj.select_by_value(option.get_attribute('value'))
                                            return True
                                        except:
                                            continue
                except Exception as e:
                    self.logger.debug(f"Error with select element: {e}")
                    continue
            
            # Handle artdeco dropdowns
            return self._handle_artdeco_dropdown(modal, question_text, dropdown_values)
            
        except Exception as e:
            self.logger.debug(f"Error handling dropdown question: {e}")
            return False
    
    def _handle_artdeco_dropdown(self, modal, question_text: str, values: List[str]) -> bool:
        """Handle LinkedIn's custom artdeco dropdown elements."""
        try:
            # Find dropdown trigger buttons
            triggers = modal.find_elements(By.XPATH, 
                ".//button[contains(@class,'artdeco-dropdown__trigger') or @aria-haspopup='listbox'] | .//*[@role='combobox']")
            
            for trigger in triggers:
                try:
                    # Check if this dropdown is related to our question
                    trigger_context = self._extract_question_text(trigger)
                    if any(word in trigger_context for word in question_text.split()[:3]):
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trigger)
                        trigger.click()
                        time.sleep(0.5)
                        
                        # Try to find and click the right option
                        for value in values:
                            try:
                                option = modal.find_element(By.XPATH,
                                    f".//*[@role='listbox']//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{value.lower()}')]")
                                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
                                option.click()
                                return True
                            except:
                                continue
                except Exception as e:
                    self.logger.debug(f"Error with artdeco dropdown: {e}")
                    continue
            return False
        except Exception as e:
            self.logger.debug(f"Error handling artdeco dropdown: {e}")
            return False
    
    def handle_text_question(self, modal, question_text: str, answer: str) -> bool:
        """Handle text input questions."""
        try:
            # Find text inputs
            inputs = modal.find_elements(By.CSS_SELECTOR, 
                "input[type='text'], input[type='number'], input:not([type]), textarea")
            
            for input_elem in inputs:
                try:
                    input_context = self._extract_question_text(input_elem)
                    if any(word in input_context for word in question_text.split()[:3]):
                        # Clear and fill the input
                        input_elem.clear()
                        input_elem.send_keys(answer)
                        return True
                except Exception as e:
                    self.logger.debug(f"Error with input element: {e}")
                    continue
            return False
        except Exception as e:
            self.logger.debug(f"Error handling text question: {e}")
            return False
    
    def handle_checkbox_question(self, modal, question_text: str, pattern_config: Dict) -> bool:
        """Handle checkbox questions (like follow company)."""
        try:
            answer = self._get_answer_value(pattern_config)
            should_check = answer.lower() in ['true', 'yes', '1']
            
            # Special handling for follow company - respect default if no config answer
            if 'follow' in question_text and not answer:
                should_check = pattern_config.get('default_answer', 'No').lower() in ['true', 'yes', '1']
            
            # Find checkbox inputs
            checkboxes = modal.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
            
            for checkbox in checkboxes:
                try:
                    checkbox_context = self._extract_question_text(checkbox)
                    if any(word in checkbox_context for word in question_text.split()[:3]):
                        current_state = checkbox.is_selected()
                        
                        if should_check and not current_state:
                            # Need to check the checkbox
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                            checkbox.click()
                            return True
                        elif not should_check and current_state:
                            # Need to uncheck the checkbox
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                            checkbox.click()
                            return True
                        else:
                            # Already in desired state
                            return True
                except Exception as e:
                    self.logger.debug(f"Error with checkbox element: {e}")
                    continue
                    
            return False
        except Exception as e:
            self.logger.debug(f"Error handling checkbox question: {e}")
            return False
    
    def apply_fallback_strategy(self, modal, element) -> bool:
        """Apply fallback strategy for unrecognized questions."""
        try:
            fallback_config = self.config.get('fallback_strategies', {})
            
            # Try to determine element type
            tag_name = element.tag_name.lower()
            element_type = element.get_attribute('type') or ''
            
            if tag_name == 'select':
                return self._fallback_dropdown(element, fallback_config)
            elif 'radio' in element_type or 'checkbox' in element_type:
                return self._fallback_yes_no(modal, element, fallback_config)
            elif tag_name in ['input', 'textarea']:
                return self._fallback_text(element, fallback_config)
            
            return False
        except Exception as e:
            self.logger.debug(f"Error in fallback strategy: {e}")
            return False
    
    def _fallback_dropdown(self, select_element, fallback_config: Dict) -> bool:
        """Fallback strategy for dropdown elements."""
        try:
            dropdown_config = fallback_config.get('dropdown_questions', {})
            if dropdown_config.get('skip_if_unsure', True):
                return False  # Skip unknown dropdowns
                
            # Select first reasonable option
            select_obj = Select(select_element)
            if len(select_obj.options) > 1:  # Skip if only placeholder
                select_obj.select_by_index(1)  # Skip first (usually placeholder)
                return True
            return False
        except:
            return False
    
    def _fallback_yes_no(self, modal, element, fallback_config: Dict) -> bool:
        """Fallback strategy for yes/no questions."""
        try:
            yes_no_config = fallback_config.get('yes_no_questions', {})
            element_context = self._extract_question_text(element).lower()
            
            # Check for negative keywords
            negative_keywords = yes_no_config.get('negative_keywords', [])
            if any(keyword in element_context for keyword in negative_keywords):
                answer = 'No'
            else:
                answer = yes_no_config.get('default_answer', 'Yes')
            
            # Try to click the appropriate label
            container = element.find_element(By.XPATH, "ancestor::*[self::div or self::section or self::form][1]")
            labels = container.find_elements(By.XPATH, f".//label[normalize-space()='{answer}']")
            if labels:
                labels[0].click()
                return True
            return False
        except:
            return False
    
    def _fallback_text(self, element, fallback_config: Dict) -> bool:
        """Fallback strategy for text inputs."""
        try:
            text_config = fallback_config.get('text_questions', {})
            element_context = self._extract_question_text(element).lower()
            
            if 'year' in element_context or 'experience' in element_context:
                element.send_keys(text_config.get('default_years', '5'))
            else:
                element.send_keys(text_config.get('default_text', 'N/A'))
            return True
        except:
            return False
    
    def process_dynamic_form(self, modal) -> Dict[str, bool]:
        """Process all dynamic form elements in the modal."""
        results = {'handled': [], 'skipped': [], 'errors': []}
        
        try:
            # Find all interactive elements
            elements = modal.find_elements(By.CSS_SELECTOR, 
                "input, select, textarea, button[aria-haspopup='listbox']")
            
            for element in elements:
                try:
                    # Skip if already filled
                    if element.tag_name.lower() in ['input', 'textarea']:
                        value = element.get_attribute('value') or ''
                        if value.strip():
                            continue
                    
                    # Extract question context
                    question_text = self._extract_question_text(element)
                    if not question_text or len(question_text.strip()) < 3:
                        continue
                    
                    # Try to match against patterns
                    pattern_match = self._match_question_pattern(question_text)
                    
                    success = False
                    if pattern_match:
                        question_type = pattern_match.get('type', 'text')
                        answer = self._get_answer_value(pattern_match)
                        
                        if question_type == 'yes_no':
                            success = self.handle_yes_no_question(modal, question_text, answer)
                        elif question_type == 'dropdown':
                            success = self.handle_dropdown_question(modal, question_text, pattern_match)
                        elif question_type == 'text':
                            success = self.handle_text_question(modal, question_text, answer)
                        elif question_type == 'checkbox':
                            success = self.handle_checkbox_question(modal, question_text, pattern_match)
                    else:
                        # Apply fallback strategy
                        success = self.apply_fallback_strategy(modal, element)
                    
                    if success:
                        results['handled'].append(question_text[:50])
                        self.logger.info(f"Successfully handled: {question_text[:50]}")
                    else:
                        results['skipped'].append(question_text[:50])
                        self.logger.debug(f"Skipped: {question_text[:50]}")
                        
                except Exception as e:
                    error_msg = f"Error processing element: {str(e)[:50]}"
                    results['errors'].append(error_msg)
                    self.logger.error(error_msg)
                    
        except Exception as e:
            self.logger.error(f"Error processing dynamic form: {e}")
            
        return results