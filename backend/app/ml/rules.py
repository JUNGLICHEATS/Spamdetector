import re
import string
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class Rule:
    """Represents a spam detection rule"""
    name: str
    pattern: str
    weight: float
    description: str
    rule_type: str

class RulesEngine:
    """Rule-based spam detection engine"""
    
    def __init__(self):
        self.rules = self._initialize_rules()
    
    def _initialize_rules(self) -> List[Rule]:
        """Initialize predefined spam detection rules"""
        rules = [
            # Suspicious phrases
            Rule(
                name="suspicious_phrases",
                pattern=r'(?i)\b(click here|act now|limited time|urgent|congratulations|you have won|free money|make money fast|guaranteed|no risk|100% free|call now|don\'t delete|once in a lifetime)\b',
                weight=0.8,
                description="Common spam phrases",
                rule_type="content"
            ),
            
            # Excessive punctuation
            Rule(
                name="excessive_punctuation",
                pattern=r'[!]{3,}|[?]{3,}|[.]{3,}',
                weight=0.6,
                description="Excessive punctuation marks",
                rule_type="formatting"
            ),
            
            # All caps
            Rule(
                name="all_caps",
                pattern=r'\b[A-Z]{5,}\b',
                weight=0.7,
                description="Words in all capitals",
                rule_type="formatting"
            ),
            
            # Suspicious URLs
            Rule(
                name="suspicious_urls",
                pattern=r'(?i)\b(bit\.ly|tinyurl|goo\.gl|t\.co|short\.link|click\.me)\b',
                weight=0.9,
                description="Suspicious shortened URLs",
                rule_type="content"
            ),
            
            # Multiple dollar signs
            Rule(
                name="money_symbols",
                pattern=r'\$+\d+|\$\$+',
                weight=0.7,
                description="Multiple dollar signs or money amounts",
                rule_type="content"
            ),
            
            # Excessive numbers
            Rule(
                name="excessive_numbers",
                pattern=r'\d{10,}',
                weight=0.6,
                description="Long sequences of numbers",
                rule_type="formatting"
            ),
            
            # Lottery/prize words
            Rule(
                name="lottery_prize",
                pattern=r'(?i)\b(lottery|winner|prize|jackpot|cash|reward|bonus|claim|redeem)\b',
                weight=0.8,
                description="Lottery and prize-related words",
                rule_type="content"
            ),
            
            # Urgent action words
            Rule(
                name="urgent_action",
                pattern=r'(?i)\b(urgent|immediate|expire|deadline|hurry|rush|now|today only|last chance)\b',
                weight=0.7,
                description="Urgent action words",
                rule_type="content"
            ),
            
            # Excessive special characters
            Rule(
                name="special_characters",
                pattern=r'[^\w\s]{5,}',
                weight=0.6,
                description="Excessive special characters",
                rule_type="formatting"
            ),
            
            # Suspicious email patterns
            Rule(
                name="suspicious_emails",
                pattern=r'(?i)\b(noreply|donotreply|support|admin|info)@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
                weight=0.5,
                description="Suspicious generic email addresses",
                rule_type="content"
            )
        ]
        return rules
    
    def analyze_message(self, message: str) -> Dict:
        """Analyze a message against all rules"""
        results = {
            'total_score': 0.0,
            'matched_rules': [],
            'is_spam': False,
            'confidence': 0.0,
            'rule_details': []
        }
        
        # Clean message for analysis
        clean_message = self._clean_message(message)
        
        # Check each rule
        for rule in self.rules:
            matches = self._check_rule(clean_message, rule)
            if matches:
                rule_score = rule.weight * len(matches)
                results['total_score'] += rule_score
                results['matched_rules'].append(rule.name)
                results['rule_details'].append({
                    'rule_name': rule.name,
                    'description': rule.description,
                    'weight': rule.weight,
                    'matches': matches,
                    'score': rule_score
                })
        
        # Calculate final confidence and spam determination
        results['confidence'] = min(results['total_score'], 1.0)
        results['is_spam'] = results['confidence'] >= 0.5
        
        return results
    
    def _clean_message(self, message: str) -> str:
        """Clean message for analysis"""
        # Remove extra whitespace
        message = re.sub(r'\s+', ' ', message.strip())
        return message
    
    def _check_rule(self, message: str, rule: Rule) -> List[str]:
        """Check if a rule matches the message"""
        matches = re.findall(rule.pattern, message)
        return matches if matches else []
    
    def get_rule_by_name(self, name: str) -> Rule:
        """Get a specific rule by name"""
        for rule in self.rules:
            if rule.name == name:
                return rule
        return None
    
    def add_custom_rule(self, name: str, pattern: str, weight: float, description: str, rule_type: str = "custom"):
        """Add a custom rule to the engine"""
        custom_rule = Rule(
            name=name,
            pattern=pattern,
            weight=weight,
            description=description,
            rule_type=rule_type
        )
        self.rules.append(custom_rule)
    
    def remove_rule(self, name: str) -> bool:
        """Remove a rule by name"""
        for i, rule in enumerate(self.rules):
            if rule.name == name:
                del self.rules[i]
                return True
        return False
    
    def get_all_rules(self) -> List[Dict]:
        """Get all rules as dictionaries"""
        return [
            {
                'name': rule.name,
                'pattern': rule.pattern,
                'weight': rule.weight,
                'description': rule.description,
                'rule_type': rule.rule_type
            }
            for rule in self.rules
        ]
    
    def analyze_by_category(self, message: str) -> Dict:
        """Analyze message by rule categories"""
        results = {
            'content_score': 0.0,
            'formatting_score': 0.0,
            'custom_score': 0.0,
            'category_details': {}
        }
        
        # Group rules by type
        rule_categories = {}
        for rule in self.rules:
            if rule.rule_type not in rule_categories:
                rule_categories[rule.rule_type] = []
            rule_categories[rule.rule_type].append(rule)
        
        # Analyze each category
        for category, category_rules in rule_categories.items():
            category_score = 0.0
            category_matches = []
            
            for rule in category_rules:
                matches = self._check_rule(message, rule)
                if matches:
                    rule_score = rule.weight * len(matches)
                    category_score += rule_score
                    category_matches.append({
                        'rule': rule.name,
                        'matches': matches,
                        'score': rule_score
                    })
            
            # Store category results
            if category == 'content':
                results['content_score'] = category_score
            elif category == 'formatting':
                results['formatting_score'] = category_score
            elif category == 'custom':
                results['custom_score'] = category_score
            
            results['category_details'][category] = {
                'score': category_score,
                'matches': category_matches
            }
        
        return results
    
    def get_statistics(self) -> Dict:
        """Get statistics about the rules"""
        stats = {
            'total_rules': len(self.rules),
            'rule_types': {},
            'weight_distribution': {
                'low': 0,  # 0.0 - 0.3
                'medium': 0,  # 0.4 - 0.7
                'high': 0  # 0.8 - 1.0
            }
        }
        
        # Count by rule type
        for rule in self.rules:
            rule_type = rule.rule_type
            if rule_type not in stats['rule_types']:
                stats['rule_types'][rule_type] = 0
            stats['rule_types'][rule_type] += 1
            
            # Weight distribution
            if rule.weight <= 0.3:
                stats['weight_distribution']['low'] += 1
            elif rule.weight <= 0.7:
                stats['weight_distribution']['medium'] += 1
            else:
                stats['weight_distribution']['high'] += 1
        
        return stats

# Example usage
if __name__ == "__main__":
    # Initialize the rules engine
    rules_engine = RulesEngine()
    
    # Test message
    test_message = "CONGRATULATIONS!!! You have WON $1000000!!! Click here NOW to claim your prize! Don't miss this LIMITED TIME offer!!!"
    
    # Analyze the message
    result = rules_engine.analyze_message(test_message)
    
    print("Spam Analysis Results:")
    print(f"Is Spam: {result['is_spam']}")
    print(f"Confidence: {result['confidence']:.2f}")
    print(f"Total Score: {result['total_score']:.2f}")
    print(f"Matched Rules: {result['matched_rules']}")
    
    # Detailed analysis
    print("\nDetailed Rule Analysis:")
    for detail in result['rule_details']:
        print(f"- {detail['rule_name']}: {detail['description']} (Score: {detail['score']:.2f})")