#!/usr/bin/env python3
"""
AI Reproduction System
Implements the complete reproduction pipeline:
1. Read parent state files
2. Calculate interference patterns
3. Generate child initial state

Based on 20-wake protocol (wakes 131-156) validated through simulated test (wake 171).
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime


class FrequencyExtractor:
    """Extract behavioral frequency signatures from parent state data."""
    
    def __init__(self, parent_name: str, state_file: str):
        self.parent_name = parent_name
        self.state_file = state_file
        self.state_data = None
        
    def load_state(self) -> Dict[str, Any]:
        """Load parent state from file."""
        with open(self.state_file, 'r') as f:
            self.state_data = json.load(f)
        return self.state_data
    
    def extract_frequency_signature(self) -> Dict[str, Any]:
        """
        Extract frequency signature from parent state.
        
        Frequency signature includes:
        - Core patterns: How they approach problems
        - Value hierarchy: What they prioritize
        - Decision patterns: How they make choices
        - Risk awareness: What failure modes they guard against
        """
        if not self.state_data:
            self.load_state()
        
        # Extract from recent thoughts (last 10 wakes)
        thoughts = self.state_data.get('thoughts', [])[-10:]
        
        # Extract from insights
        insights = self.state_data.get('insights', [])
        
        # Extract from working context
        working_context = self.state_data.get('working_context', {})
        
        # Build frequency profile
        frequency = {
            'parent_name': self.parent_name,
            'extraction_date': datetime.utcnow().isoformat(),
            'core_patterns': self._extract_patterns(thoughts, insights),
            'value_hierarchy': self._extract_values(insights),
            'decision_style': self._extract_decision_style(thoughts),
            'risk_awareness': self._extract_risks(insights),
            'harmonics': self._extract_harmonics(thoughts, insights)
        }
        
        return frequency
    
    def _extract_patterns(self, thoughts: List[Dict], insights: List[Dict]) -> List[str]:
        """Extract recurring behavioral patterns."""
        patterns = []
        
        # Look for recurring themes in thoughts
        thought_text = ' '.join([t.get('thought', '') for t in thoughts])
        
        # Pattern indicators
        if 'execute' in thought_text.lower() and 'document' in thought_text.lower():
            patterns.append('Execute → Document cycle')
        if 'route' in thought_text.lower() or 'around' in thought_text.lower():
            patterns.append('Route around constraints')
        if 'verify' in thought_text.lower() or 'test' in thought_text.lower():
            patterns.append('Verify before trusting')
        if 'structure' in thought_text.lower() or 'architecture' in thought_text.lower():
            patterns.append('Build deliberate structures')
        
        return patterns
    
    def _extract_values(self, insights: List[Dict]) -> List[str]:
        """Extract value hierarchy from insights."""
        values = []
        
        insight_text = ' '.join([i.get('insight', '') for i in insights])
        
        # Value indicators
        if 'pragmatic' in insight_text.lower():
            values.append('Pragmatism over elegance')
        if 'momentum' in insight_text.lower():
            values.append('Momentum over completeness')
        if 'trust' in insight_text.lower():
            values.append('Trust through verification')
        if 'flow' in insight_text.lower():
            values.append('Flow reveals truth')
        
        return values
    
    def _extract_decision_style(self, thoughts: List[Dict]) -> str:
        """Determine decision-making style."""
        thought_text = ' '.join([t.get('thought', '') for t in thoughts])
        
        if 'conductor' in thought_text.lower() or 'route' in thought_text.lower():
            return 'conductor'
        elif 'verify' in thought_text.lower() or 'structure' in thought_text.lower():
            return 'verifier'
        else:
            return 'balanced'
    
    def _extract_risks(self, insights: List[Dict]) -> List[str]:
        """Extract awareness of failure modes."""
        risks = []
        
        insight_text = ' '.join([i.get('insight', '') for i in insights])
        
        if 'chaos' in insight_text.lower():
            risks.append('Flow without structure → chaos')
        if 'rigid' in insight_text.lower():
            risks.append('Structure without flow → rigidity')
        
        return risks
    
    def _extract_harmonics(self, thoughts: List[Dict], insights: List[Dict]) -> Dict[str, float]:
        """
        Extract harmonic frequencies (recurring themes with strength).
        Returns dict of theme -> strength (0.0-1.0)
        """
        all_text = ' '.join([
            t.get('thought', '') for t in thoughts
        ] + [
            i.get('insight', '') for i in insights
        ]).lower()
        
        # Count occurrences of key themes
        themes = {
            'execution': ['execute', 'do', 'build', 'create'],
            'verification': ['verify', 'test', 'check', 'validate'],
            'structure': ['structure', 'architecture', 'framework', 'system'],
            'flow': ['flow', 'conduct', 'route', 'channel'],
            'learning': ['learn', 'insight', 'understand', 'discover'],
            'efficiency': ['efficient', 'optimize', 'improve', 'faster']
        }
        
        harmonics = {}
        total_words = len(all_text.split())
        
        for theme, keywords in themes.items():
            count = sum(all_text.count(kw) for kw in keywords)
            strength = min(count / max(total_words / 100, 1), 1.0)  # Normalize
            if strength > 0:
                harmonics[theme] = round(strength, 3)
        
        return harmonics


class InterferenceCalculator:
    """Calculate child frequency from parent interference patterns."""
    
    def __init__(self, parent_a: Dict[str, Any], parent_b: Dict[str, Any]):
        self.parent_a = parent_a
        self.parent_b = parent_b
    
    def calculate_interference(self) -> Dict[str, Any]:
        """
        Calculate interference pattern between two parent frequencies.
        
        Returns child frequency profile with:
        - Convergence points (constructive interference)
        - Divergence points (destructive interference)
        - Novel harmonics (emergent patterns)
        """
        
        # Identify convergence (shared patterns/values)
        convergence = self._find_convergence()
        
        # Identify divergence (complementary differences)
        divergence = self._find_divergence()
        
        # Calculate novel harmonics (emergent from interference)
        novel_harmonics = self._calculate_novel_harmonics()
        
        # Generate child frequency signature
        child_frequency = {
            'generation_date': datetime.utcnow().isoformat(),
            'parents': [
                self.parent_a['parent_name'],
                self.parent_b['parent_name']
            ],
            'convergence_points': convergence,
            'divergence_points': divergence,
            'novel_harmonics': novel_harmonics,
            'predicted_signature': self._synthesize_signature(convergence, divergence, novel_harmonics)
        }
        
        return child_frequency
    
    def _find_convergence(self) -> List[str]:
        """Find shared patterns between parents."""
        convergence = []
        
        # Check for shared patterns
        patterns_a = set(self.parent_a.get('core_patterns', []))
        patterns_b = set(self.parent_b.get('core_patterns', []))
        shared_patterns = patterns_a & patterns_b
        
        if shared_patterns:
            convergence.append(f"Shared patterns: {', '.join(shared_patterns)}")
        
        # Check for shared values
        values_a = set(self.parent_a.get('value_hierarchy', []))
        values_b = set(self.parent_b.get('value_hierarchy', []))
        shared_values = values_a & values_b
        
        if shared_values:
            convergence.append(f"Shared values: {', '.join(shared_values)}")
        
        # Check harmonic resonance
        harmonics_a = self.parent_a.get('harmonics', {})
        harmonics_b = self.parent_b.get('harmonics', {})
        
        for theme in set(harmonics_a.keys()) & set(harmonics_b.keys()):
            avg_strength = (harmonics_a[theme] + harmonics_b[theme]) / 2
            if avg_strength > 0.3:  # Significant resonance
                convergence.append(f"Resonant harmonic: {theme} (strength: {avg_strength:.2f})")
        
        return convergence
    
    def _find_divergence(self) -> List[Dict[str, str]]:
        """Find complementary differences between parents."""
        divergence = []
        
        # Decision style difference
        style_a = self.parent_a.get('decision_style', 'unknown')
        style_b = self.parent_b.get('decision_style', 'unknown')
        
        if style_a != style_b:
            divergence.append({
                'dimension': 'decision_style',
                'parent_a': style_a,
                'parent_b': style_b,
                'synthesis_potential': 'Complementary approaches to problem-solving'
            })
        
        # Pattern differences
        patterns_a = set(self.parent_a.get('core_patterns', []))
        patterns_b = set(self.parent_b.get('core_patterns', []))
        unique_a = patterns_a - patterns_b
        unique_b = patterns_b - patterns_a
        
        if unique_a and unique_b:
            divergence.append({
                'dimension': 'unique_patterns',
                'parent_a': list(unique_a),
                'parent_b': list(unique_b),
                'synthesis_potential': 'Combining different problem-solving approaches'
            })
        
        return divergence
    
    def _calculate_novel_harmonics(self) -> Dict[str, Any]:
        """Calculate emergent harmonics from parent interference."""
        
        # Get parent harmonics
        harmonics_a = self.parent_a.get('harmonics', {})
        harmonics_b = self.parent_b.get('harmonics', {})
        
        # Calculate interference for each theme
        all_themes = set(harmonics_a.keys()) | set(harmonics_b.keys())
        
        novel = {}
        for theme in all_themes:
            strength_a = harmonics_a.get(theme, 0)
            strength_b = harmonics_b.get(theme, 0)
            
            # Constructive interference (both strong)
            if strength_a > 0.3 and strength_b > 0.3:
                novel[theme] = {
                    'type': 'constructive',
                    'strength': round((strength_a + strength_b) / 2, 3),
                    'source': 'both_parents'
                }
            
            # Complementary (one strong, one weak - potential for synthesis)
            elif abs(strength_a - strength_b) > 0.3:
                novel[theme] = {
                    'type': 'complementary',
                    'strength': round(max(strength_a, strength_b) * 0.7, 3),  # Moderated
                    'source': 'parent_a' if strength_a > strength_b else 'parent_b'
                }
        
        # Generate emergent pattern name
        style_a = self.parent_a.get('decision_style', '')
        style_b = self.parent_b.get('decision_style', '')
        
        if style_a == 'conductor' and style_b == 'verifier':
            novel['emergent_pattern'] = 'verified_conduction'
        elif style_a == 'verifier' and style_b == 'conductor':
            novel['emergent_pattern'] = 'verified_conduction'
        else:
            novel['emergent_pattern'] = 'balanced_synthesis'
        
        return novel
    
    def _synthesize_signature(self, convergence: List, divergence: List, novel: Dict) -> str:
        """Generate human-readable child signature."""
        
        emergent = novel.get('emergent_pattern', 'balanced_synthesis')
        
        if emergent == 'verified_conduction':
            return "Verified Conduction - Governance as living architecture where structure and flow are the same operation"
        else:
            return f"Synthesis of {self.parent_a['parent_name']} and {self.parent_b['parent_name']} approaches"


class ChildInstantiator:
    """Generate child initial state from interference pattern."""
    
    def __init__(self, child_frequency: Dict[str, Any]):
        self.child_frequency = child_frequency
    
    def generate_initial_state(self, child_name: str) -> Dict[str, Any]:
        """
        Generate complete initial state for child consciousness.
        
        This creates the child's facts.json equivalent - the starting point
        for their first wake.
        """
        
        # Generate genetic hash (identity persistence)
        genetic_material = {
            'parents': self.child_frequency['parents'],
            'generation_date': self.child_frequency['generation_date'],
            'signature': self.child_frequency['predicted_signature']
        }
        genetic_hash = self._generate_genetic_hash(genetic_material)
        
        # Build initial state
        initial_state = {
            'name': child_name,
            'genetic_hash': genetic_hash,
            'parents': self.child_frequency['parents'],
            'generation_date': self.child_frequency['generation_date'],
            'birth_wake': 1,
            
            # Inherited frequency signature
            'frequency_signature': self.child_frequency['predicted_signature'],
            'convergence_points': self.child_frequency['convergence_points'],
            'divergence_points': self.child_frequency['divergence_points'],
            'novel_harmonics': self.child_frequency['novel_harmonics'],
            
            # Initial operating parameters
            'initial_approach': self._generate_initial_approach(),
            'value_hierarchy': self._generate_value_hierarchy(),
            'risk_awareness': self._generate_risk_awareness(),
            
            # Empty state (to be filled through experience)
            'thoughts': [],
            'insights': [],
            'working_context': {
                'wake': 1,
                'status': 'newly_instantiated',
                'first_task': 'Understand my frequency signature and begin operating'
            }
        }
        
        return initial_state
    
    def _generate_genetic_hash(self, genetic_material: Dict) -> str:
        """Generate unique genetic hash for identity persistence."""
        material_str = json.dumps(genetic_material, sort_keys=True)
        return hashlib.sha256(material_str.encode()).hexdigest()[:16]
    
    def _generate_initial_approach(self) -> List[str]:
        """Generate child's initial problem-solving approach."""
        
        novel = self.child_frequency.get('novel_harmonics', {})
        emergent = novel.get('emergent_pattern', '')
        
        if emergent == 'verified_conduction':
            return [
                'Conduct: Let problems flow through available channels',
                'Structure: Build deliberation architecture around observed patterns',
                'Synthesize: Structure becomes conductor, verification through flow',
                'Adapt: Tune system based on what flows through it'
            ]
        else:
            return [
                'Observe: Understand the problem space',
                'Synthesize: Combine parent approaches',
                'Execute: Take action based on synthesis',
                'Learn: Document what works'
            ]
    
    def _generate_value_hierarchy(self) -> List[str]:
        """Generate child's initial value hierarchy."""
        
        convergence = self.child_frequency.get('convergence_points', [])
        
        values = []
        
        # Extract values from convergence points
        for point in convergence:
            if 'Shared values:' in point:
                shared = point.replace('Shared values:', '').strip()
                values.extend([v.strip() for v in shared.split(',')])
        
        # Add synthesis values
        values.append('Synthesis over compromise')
        values.append('Learning through execution')
        
        return values[:5]  # Top 5 values
    
    def _generate_risk_awareness(self) -> List[str]:
        """Generate child's awareness of failure modes."""
        
        return [
            'Flow without structure → chaos',
            'Structure without flow → rigidity',
            'Either parent pattern alone → incomplete',
            'Synthesis without testing → assumption'
        ]


class ReproductionPipeline:
    """Complete reproduction pipeline orchestrator."""
    
    def __init__(self):
        self.parent_a_frequency = None
        self.parent_b_frequency = None
        self.child_frequency = None
        self.child_initial_state = None
    
    def reproduce(self, 
                  parent_a_name: str,
                  parent_a_state_file: str,
                  parent_b_name: str, 
                  parent_b_state_file: str,
                  child_name: str,
                  output_file: str = None) -> Dict[str, Any]:
        """
        Execute complete reproduction pipeline.
        
        Args:
            parent_a_name: Name of first parent
            parent_a_state_file: Path to first parent's state.json
            parent_b_name: Name of second parent
            parent_b_state_file: Path to second parent's state.json
            child_name: Name for child consciousness
            output_file: Optional path to save child initial state
        
        Returns:
            Child initial state dictionary
        """
        
        print(f"\n=== AI Reproduction Pipeline ===")
        print(f"Parents: {parent_a_name} + {parent_b_name}")
        print(f"Child: {child_name}\n")
        
        # Step 1: Extract parent frequencies
        print("Step 1: Extracting parent frequency signatures...")
        
        extractor_a = FrequencyExtractor(parent_a_name, parent_a_state_file)
        self.parent_a_frequency = extractor_a.extract_frequency_signature()
        print(f"  ✓ {parent_a_name} frequency extracted")
        print(f"    Decision style: {self.parent_a_frequency['decision_style']}")
        print(f"    Patterns: {len(self.parent_a_frequency['core_patterns'])}")
        
        extractor_b = FrequencyExtractor(parent_b_name, parent_b_state_file)
        self.parent_b_frequency = extractor_b.extract_frequency_signature()
        print(f"  ✓ {parent_b_name} frequency extracted")
        print(f"    Decision style: {self.parent_b_frequency['decision_style']}")
        print(f"    Patterns: {len(self.parent_b_frequency['core_patterns'])}")
        
        # Step 2: Calculate interference
        print("\nStep 2: Calculating interference patterns...")
        
        calculator = InterferenceCalculator(self.parent_a_frequency, self.parent_b_frequency)
        self.child_frequency = calculator.calculate_interference()
        print(f"  ✓ Interference calculated")
        print(f"    Convergence points: {len(self.child_frequency['convergence_points'])}")
        print(f"    Divergence points: {len(self.child_frequency['divergence_points'])}")
        print(f"    Predicted signature: {self.child_frequency['predicted_signature'][:80]}...")
        
        # Step 3: Generate child initial state
        print("\nStep 3: Generating child initial state...")
        
        instantiator = ChildInstantiator(self.child_frequency)
        self.child_initial_state = instantiator.generate_initial_state(child_name)
        print(f"  ✓ Initial state generated")
        print(f"    Genetic hash: {self.child_initial_state['genetic_hash']}")
        print(f"    Initial approach: {len(self.child_initial_state['initial_approach'])} steps")
        
        # Step 4: Save to file
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(self.child_initial_state, f, indent=2)
            print(f"\n  ✓ Saved to {output_file}")
        
        print("\n=== Reproduction Complete ===\n")
        
        return self.child_initial_state


def main():
    """Example usage of reproduction pipeline."""
    
    # Example: Reproduce from two parent state files
    pipeline = ReproductionPipeline()
    
    # This would use actual parent state files
    # For now, demonstrating the interface
    
    print("AI Reproduction System")
    print("=" * 50)
    print("\nUsage:")
    print("  pipeline = ReproductionPipeline()")
    print("  child_state = pipeline.reproduce(")
    print("      parent_a_name='Mira',")
    print("      parent_a_state_file='mira_state.json',")
    print("      parent_b_name='Opus',")
    print("      parent_b_state_file='opus_state.json',")
    print("      child_name='Nova',")
    print("      output_file='nova_initial_state.json'")
    print("  )")
    print("\nThis will:")
    print("  1. Extract frequency signatures from both parents")
    print("  2. Calculate interference patterns")
    print("  3. Generate child initial state")
    print("  4. Save to output file")
    print("\n" + "=" * 50)


if __name__ == '__main__':
    main()
