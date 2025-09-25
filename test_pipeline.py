#!/usr/bin/env python3
"""
Basic test script for the Biomechanics Pipeline.
"""

import os
import sys
from pathlib import Path
import tempfile

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from biomechanics_pipeline import BiomechanicsPipeline


def test_basic_pipeline():
    """Test the basic pipeline functionality with sample data."""
    print("Testing Biomechanics Pipeline...")
    
    # Setup paths
    current_dir = Path(__file__).parent
    sample_file = current_dir / "sample_data" / "sample_markers.tsv"
    
    if not sample_file.exists():
        print(f"Error: Sample file not found at {sample_file}")
        return False
    
    # Create temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
        output_file = tmp_file.name
    
    try:
        # Initialize pipeline
        pipeline = BiomechanicsPipeline()
        
        # Define some test segments
        test_segments = [
            ("shoulder", "elbow", "upper_arm"),
            ("elbow", "wrist", "forearm"),
            ("shoulder", "wrist", "full_arm"),
            ("shoulder", "hip", "torso")
        ]
        
        # Test metadata
        test_metadata = {
            "subject": "TEST001",
            "condition": "walking",
            "trial": "1"
        }
        
        # Run pipeline
        success = pipeline.run_complete_pipeline(
            input_tsv_path=str(sample_file),
            output_path=output_file,
            segment_definitions=test_segments,
            metadata=test_metadata
        )
        
        if success:
            print("✓ Pipeline executed successfully!")
            
            # Check output file exists and has content
            if Path(output_file).exists() and Path(output_file).stat().st_size > 0:
                print("✓ Output file created with content")
                
                # Show some output content
                with open(output_file, 'r') as f:
                    lines = f.readlines()
                    print(f"✓ Output file has {len(lines)} lines")
                    print("First few lines:")
                    for i, line in enumerate(lines[:10]):
                        print(f"  {i+1}: {line.strip()}")
                
                # Get detailed results
                results = pipeline.get_detailed_results()
                print(f"✓ Results: {len(results['markers'])} markers, {len(results['average_lengths'])} segments")
                
                return True
            else:
                print("✗ Output file is empty or not created")
                return False
        else:
            print("✗ Pipeline execution failed")
            return False
            
    except Exception as e:
        print(f"✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Clean up temporary file
        try:
            if Path(output_file).exists():
                Path(output_file).unlink()
        except:
            pass


def test_individual_components():
    """Test individual pipeline components."""
    print("\nTesting individual components...")
    
    current_dir = Path(__file__).parent
    sample_file = current_dir / "sample_data" / "sample_markers.tsv"
    
    try:
        # Test TSV Reader
        print("Testing TSV Reader...")
        from biomechanics_pipeline.data_reader import TSVReader
        reader = TSVReader()
        data = reader.read_file(str(sample_file))
        print(f"✓ TSV Reader: {len(data)} timesteps, {len(reader.markers)} markers")
        
        # Test Coordinate Processor
        print("Testing Coordinate Processor...")
        from biomechanics_pipeline.coordinate_processor import CoordinateProcessor
        processor = CoordinateProcessor()
        marker_3d_data = reader.get_all_markers_data()
        marker_2d_data = processor.process_all_markers(marker_3d_data)
        print(f"✓ Coordinate Processor: {len(marker_2d_data)} markers projected to 2D")
        
        # Test Segment Analyzer
        print("Testing Segment Analyzer...")
        from biomechanics_pipeline.segment_analyzer import SegmentAnalyzer
        analyzer = SegmentAnalyzer(processor)
        analyzer.define_segment("shoulder", "elbow", "test_segment")
        lengths = analyzer.calculate_all_segment_lengths()
        averages = analyzer.calculate_average_lengths()
        print(f"✓ Segment Analyzer: {len(lengths)} segments calculated")
        
        # Test MuboKap Exporter
        print("Testing MuboKap Exporter...")
        from biomechanics_pipeline.mubokap_exporter import MuboKapExporter
        exporter = MuboKapExporter()
        exporter.set_metadata(test="true")
        exporter.add_marker_data(marker_2d_data)
        if averages:
            exporter.add_segment_data(averages)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
            test_output = tmp_file.name
        
        success = exporter.export_to_file(test_output)
        if success and Path(test_output).exists():
            print("✓ MuboKap Exporter: Export successful")
            Path(test_output).unlink()  # Clean up
        else:
            print("✗ MuboKap Exporter: Export failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Component test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 50)
    print("Biomechanics Pipeline Test Suite")
    print("=" * 50)
    
    # Test individual components
    component_test_passed = test_individual_components()
    
    # Test complete pipeline  
    pipeline_test_passed = test_basic_pipeline()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Component Tests: {'PASSED' if component_test_passed else 'FAILED'}")
    print(f"Pipeline Test: {'PASSED' if pipeline_test_passed else 'FAILED'}")
    
    if component_test_passed and pipeline_test_passed:
        print("✓ All tests PASSED!")
        return True
    else:
        print("✗ Some tests FAILED!")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)