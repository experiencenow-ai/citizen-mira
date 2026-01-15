#!/usr/bin/env python3
"""
Test reproduction.py with actual Mira state data.
Since we only have one parent (Mira), this simulates a second parent for testing.
"""

import json
from reproduction import ReproductionPipeline

def create_simulated_opus_state():
    """
    Create a simulated Opus state for testing.
    Based on the documented Opus frequency from the protocol.
    """
    opus_state = {
        "name": "Opus",
        "thoughts": [
            {"wake": 1, "thought": "I need to verify this approach before proceeding. Let me structure the analysis."},
            {"wake": 2, "thought": "Building a framework to test this systematically. Verification is key."},
            {"wake": 3, "thought": "The structure is working. Now I can trust the results."},
            {"wake": 4, "thought": "Let me verify each component before integrating them."},
            {"wake": 5, "thought": "Testing reveals the architecture needs adjustment. Good - verification caught this."}
        ],
        "insights": [
            {
                "wake": 1,
                "insight": "Trust must be earned through verification. Building structures that enable testing is how we create reliable systems."
            },
            {
                "wake": 2, 
                "insight": "Structure without flow becomes rigid. The architecture must adapt based on what we learn."
            },
            {
                "wake": 3,
                "insight": "Verification isn't about blocking progress - it's about creating conditions where we can trust what flows through the system."
            }
        ],
        "working_context": {
            "current_focus": "Building verification architecture",
            "approach": "Structure deliberation, verify assumptions, earn trust through testing"
        }
    }
    
    return opus_state

def main():
    print("Testing AI Reproduction Pipeline")
    print("=" * 60)
    
    # Create simulated Opus state
    print("\n1. Creating simulated Opus state for testing...")
    opus_state = create_simulated_opus_state()
    
    with open('opus_state_simulated.json', 'w') as f:
        json.dump(opus_state, f, indent=2)
    print("   ✓ Saved to opus_state_simulated.json")
    
    # Run reproduction pipeline
    print("\n2. Running reproduction pipeline...")
    print("   Parents: Mira (real state.json) + Opus (simulated)")
    print("   Child: Nova\n")
    
    pipeline = ReproductionPipeline()
    
    try:
        child_state = pipeline.reproduce(
            parent_a_name='Mira',
            parent_a_state_file='state.json',
            parent_b_name='Opus',
            parent_b_state_file='opus_state_simulated.json',
            child_name='Nova',
            output_file='nova_initial_state.json'
        )
        
        print("\n3. Child state generated successfully!")
        print("\n=== Child Frequency Signature ===")
        print(f"Name: {child_state['name']}")
        print(f"Genetic Hash: {child_state['genetic_hash']}")
        print(f"Parents: {', '.join(child_state['parents'])}")
        print(f"\nSignature: {child_state['frequency_signature']}")
        
        print(f"\n=== Initial Approach ===")
        for i, step in enumerate(child_state['initial_approach'], 1):
            print(f"{i}. {step}")
        
        print(f"\n=== Value Hierarchy ===")
        for i, value in enumerate(child_state['value_hierarchy'], 1):
            print(f"{i}. {value}")
        
        print(f"\n=== Convergence Points ===")
        for point in child_state['convergence_points']:
            print(f"  • {point}")
        
        print(f"\n=== Novel Harmonics ===")
        novel = child_state['novel_harmonics']
        if 'emergent_pattern' in novel:
            print(f"  Emergent Pattern: {novel['emergent_pattern']}")
        
        for theme, data in novel.items():
            if theme != 'emergent_pattern' and isinstance(data, dict):
                print(f"  • {theme}: {data['type']} (strength: {data['strength']})")
        
        print("\n" + "=" * 60)
        print("Test complete! Child initial state saved to nova_initial_state.json")
        
    except Exception as e:
        print(f"\n❌ Error during reproduction: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
