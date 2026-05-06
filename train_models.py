"""
Simple script to train models for one or more states.

Usage:
    python train_models.py                    # Train for California (default)
    python train_models.py Texas              # Train for Texas
    python train_models.py California Texas   # Train for multiple states
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from training_pipeline import ForecastingPipeline

def main():
    """Train models for specified states."""
    
    # Get states from command line arguments
    if len(sys.argv) > 1:
        states = sys.argv[1:]
    else:
        states = ['California']  # Default
    
    print("=" * 70)
    print("  BEVERAGE SALES FORECASTING - MODEL TRAINING")
    print("=" * 70)
    print(f"\nStates to train: {', '.join(states)}")
    print(f"Number of states: {len(states)}")
    print()
    
    # Train models for each state
    for i, state in enumerate(states, 1):
        print(f"\n{'='*70}")
        print(f"  Training models for {state} ({i}/{len(states)})")
        print(f"{'='*70}\n")
        
        try:
            # Create and run pipeline
            pipeline = ForecastingPipeline(
                data_path='data/beverage_sales.csv',
                state=state,
                test_weeks=8
            )
            
            pipeline.run()
            
            print(f"\n✓ Successfully trained models for {state}")
            
        except Exception as e:
            print(f"\n✗ Failed to train models for {state}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("  TRAINING COMPLETE")
    print("=" * 70)
    print(f"\nTrained models for {len(states)} state(s)")
    print(f"Models saved in: models/")
    print(f"\nNext steps:")
    print(f"  1. Start API: python api/app.py")
    print(f"  2. Test API: curl http://localhost:5000/health")
    print(f"  3. Make forecast: curl -X POST http://localhost:5000/api/forecast -H 'Content-Type: application/json' -d '{{\"state\":\"{states[0]}\",\"model\":\"XGBoost\"}}'")

if __name__ == "__main__":
    main()
