#!/usr/bin/env python3
"""
Command-line interface for the Biomechanics Pipeline.

Usage:
    python run_pipeline.py input.tsv output.txt [options]
"""

import argparse
import sys
from pathlib import Path
from typing import List, Tuple, Optional

from biomechanics_pipeline import BiomechanicsPipeline


def parse_segment_definitions(segment_string: str) -> List[Tuple[str, str, Optional[str]]]:
    """
    Parse segment definitions from command line string.
    
    Expected format: "marker1,marker2[,name];marker3,marker4[,name];..."
    
    Args:
        segment_string: String with segment definitions
        
    Returns:
        List of segment tuples
    """
    segments = []
    
    if not segment_string:
        return segments
    
    for segment_def in segment_string.split(';'):
        parts = segment_def.strip().split(',')
        if len(parts) >= 2:
            marker1 = parts[0].strip()
            marker2 = parts[1].strip()
            name = parts[2].strip() if len(parts) > 2 else None
            segments.append((marker1, marker2, name))
    
    return segments


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(
        description="Biomechanical Analysis Pipeline - Process TSV marker data to MuboKap format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage - auto-generate all possible segments
  python run_pipeline.py data/markers.tsv output/result.txt
  
  # With specific segment definitions
  python run_pipeline.py data/markers.tsv output/result.txt \\
    --segments "shoulder,elbow,upper_arm;elbow,wrist,forearm"
  
  # With custom metadata
  python run_pipeline.py data/markers.tsv output/result.txt \\
    --metadata "subject:P001,condition:running,trial:1"
  
  # Save intermediate results
  python run_pipeline.py data/markers.tsv output/result.txt \\
    --save-intermediate output/intermediate/
        """
    )
    
    parser.add_argument(
        'input_file',
        help='Input TSV file containing marker coordinate data'
    )
    
    parser.add_argument(
        'output_file', 
        help='Output file path for MuboKap format (.txt)'
    )
    
    parser.add_argument(
        '--segments',
        help='Segment definitions: "marker1,marker2[,name];marker3,marker4[,name];..."',
        default=None
    )
    
    parser.add_argument(
        '--metadata',
        help='Additional metadata: "key1:value1,key2:value2,..."',
        default=None
    )
    
    parser.add_argument(
        '--save-intermediate',
        help='Directory to save intermediate results',
        default=None
    )
    
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate input file without processing'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not Path(args.input_file).exists():
        print(f"Error: Input file '{args.input_file}' not found.")
        sys.exit(1)
    
    # Parse segments if provided
    segment_definitions = None
    if args.segments:
        segment_definitions = parse_segment_definitions(args.segments)
        if args.verbose:
            print(f"Parsed {len(segment_definitions)} segment definitions:")
            for seg in segment_definitions:
                print(f"  {seg[0]} -> {seg[1]}" + (f" ({seg[2]})" if seg[2] else ""))
    
    # Parse metadata if provided  
    metadata = {}
    if args.metadata:
        for item in args.metadata.split(','):
            if ':' in item:
                key, value = item.split(':', 1)
                metadata[key.strip()] = value.strip()
    
    # Initialize pipeline
    pipeline = BiomechanicsPipeline()
    
    try:
        if args.validate_only:
            # Just validate the input file
            print(f"Validating input file: {args.input_file}")
            data = pipeline.reader.read_file(args.input_file)
            is_valid, issues = pipeline.reader.validate_data()
            
            print(f"File contains {len(data)} timesteps and {len(pipeline.reader.markers)} markers")
            print(f"Markers found: {', '.join(pipeline.reader.markers)}")
            
            if is_valid:
                print("✓ Input file is valid")
                sys.exit(0)
            else:
                print("✗ Input file has issues:")
                for issue in issues:
                    print(f"  - {issue}")
                sys.exit(1)
        
        else:
            # Run the complete pipeline
            success = pipeline.run_complete_pipeline(
                input_tsv_path=args.input_file,
                output_path=args.output_file,
                segment_definitions=segment_definitions,
                metadata=metadata
            )
            
            if success:
                print(f"✓ Pipeline completed successfully!")
                print(f"Output file: {args.output_file}")
                
                # Save intermediate results if requested
                if args.save_intermediate:
                    print(f"Saving intermediate results to: {args.save_intermediate}")
                    pipeline.save_intermediate_results(args.save_intermediate)
                
                # Show detailed results if verbose
                if args.verbose:
                    results = pipeline.get_detailed_results()
                    print(f"\nDetailed Results:")
                    print(f"  Markers: {len(results['markers'])}")
                    print(f"  Timesteps: {results['timesteps']}")
                    print(f"  Segments: {len(results['average_lengths'])}")
                    
                    if results['average_lengths']:
                        print(f"  Top 5 segment lengths:")
                        sorted_segments = sorted(results['average_lengths'].items(), 
                                                key=lambda x: x[1], reverse=True)
                        for name, length in sorted_segments[:5]:
                            print(f"    {name}: {length:.3f}")
                
                sys.exit(0)
            else:
                print("✗ Pipeline failed!")
                sys.exit(1)
                
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()