"""
Main Pipeline Module

Orchestrates the complete biomechanical analysis pipeline.
"""

from typing import List, Tuple, Optional, Dict, Any
from pathlib import Path

from .data_reader import TSVReader
from .coordinate_processor import CoordinateProcessor
from .segment_analyzer import SegmentAnalyzer
from .mubokap_exporter import MuboKapExporter


class BiomechanicsPipeline:
    """
    Main pipeline class that orchestrates the complete analysis workflow.
    """
    
    def __init__(self):
        self.reader = TSVReader()
        self.processor = CoordinateProcessor()
        self.analyzer = SegmentAnalyzer(self.processor)
        self.exporter = MuboKapExporter()
        
        self.input_file = None
        self.output_file = None
        
    def run_complete_pipeline(
        self,
        input_tsv_path: str,
        output_path: str,
        segment_definitions: List[Tuple[str, str, Optional[str]]] = None,
        metadata: Dict[str, Any] = None
    ) -> bool:
        """
        Run the complete biomechanical analysis pipeline.
        
        Args:
            input_tsv_path: Path to input TSV file
            output_path: Path for output MuboKap file
            segment_definitions: List of segment definitions (marker1, marker2, optional_name)
            metadata: Optional metadata for the output file
            
        Returns:
            True if pipeline completed successfully
        """
        try:
            # Step 1: Read TSV data
            print(f"Reading TSV file: {input_tsv_path}")
            data = self.reader.read_file(input_tsv_path)
            print(f"Loaded data with {len(data)} timesteps and {len(self.reader.markers)} markers")
            
            # Validate data
            is_valid, issues = self.reader.validate_data()
            if not is_valid:
                print("Data validation issues:")
                for issue in issues:
                    print(f"  - {issue}")
                return False
                
            # Step 2: Get 3D coordinates and project to 2D
            print("Processing coordinates (3D to 2D projection)...")
            marker_3d_data = self.reader.get_all_markers_data()
            marker_2d_data = self.processor.process_all_markers(marker_3d_data)
            print(f"Projected {len(marker_2d_data)} markers to 2D coordinates")
            
            # Step 3: Define and analyze segments
            if segment_definitions:
                print("Analyzing segment lengths...")
                self.analyzer.define_multiple_segments(segment_definitions)
                segment_lengths = self.analyzer.calculate_all_segment_lengths()
                average_lengths = self.analyzer.calculate_average_lengths()
                segment_stats = self.analyzer.get_segment_statistics()
                print(f"Calculated lengths for {len(segment_lengths)} segments")
            else:
                # Auto-generate segments between all marker pairs
                print("Auto-generating segments between all marker pairs...")
                marker_names = list(marker_2d_data.keys())
                auto_segments = []
                for i in range(len(marker_names)):
                    for j in range(i + 1, len(marker_names)):
                        auto_segments.append((marker_names[i], marker_names[j], None))
                
                self.analyzer.define_multiple_segments(auto_segments)
                segment_lengths = self.analyzer.calculate_all_segment_lengths()
                average_lengths = self.analyzer.calculate_average_lengths()
                segment_stats = self.analyzer.get_segment_statistics()
                print(f"Auto-generated and calculated {len(segment_lengths)} segments")
            
            # Step 4: Prepare export data
            print("Preparing export data...")
            if metadata:
                self.exporter.set_metadata(**metadata)
            else:
                self.exporter.set_metadata(
                    source_file=Path(input_tsv_path).name,
                    total_markers=len(marker_2d_data),
                    total_segments=len(segment_lengths),
                    timesteps=len(data)
                )
            
            # Add data sections
            self.exporter.add_marker_data(marker_2d_data, 'MARKERS_2D')
            if segment_lengths:
                self.exporter.add_segment_data(average_lengths, 'SEGMENT_AVERAGES')
                self.exporter.add_statistics(segment_stats, 'SEGMENT_STATISTICS')
            
            # Step 5: Export to MuboKap format
            print(f"Exporting to MuboKap file: {output_path}")
            success = self.exporter.export_to_file(output_path)
            
            if success:
                print("Pipeline completed successfully!")
                self._print_summary()
                return True
            else:
                print("Export failed!")
                return False
                
        except Exception as e:
            print(f"Pipeline error: {str(e)}")
            return False
    
    def _print_summary(self) -> None:
        """Print a summary of the pipeline results."""
        print("\n--- Pipeline Summary ---")
        print(f"Input file: {self.reader.data.shape if self.reader.data is not None else 'None'}")
        print(f"Markers processed: {len(self.reader.markers)}")
        print(f"2D projections: {len(self.processor.projected_data)}")
        print(f"Segments analyzed: {len(self.analyzer.segment_lengths)}")
        
        if self.analyzer.average_lengths:
            print(f"Average segment lengths:")
            for segment, length in list(self.analyzer.average_lengths.items())[:5]:  # Show first 5
                print(f"  {segment}: {length:.3f}")
            if len(self.analyzer.average_lengths) > 5:
                print(f"  ... and {len(self.analyzer.average_lengths) - 5} more")
        
        export_summary = self.exporter.get_export_summary()
        print(f"Export sections: {export_summary['data_sections']}")
        print("--- End Summary ---\n")
    
    def get_detailed_results(self) -> Dict[str, Any]:
        """
        Get detailed results from the pipeline.
        
        Returns:
            Dictionary with all pipeline results
        """
        return {
            'markers': self.reader.markers,
            'timesteps': self.reader.timesteps,
            'marker_2d_data': self.processor.projected_data,
            'projection_summary': self.processor.get_projection_summary(),
            'segment_definitions': self.analyzer.segment_definitions,
            'segment_lengths': self.analyzer.segment_lengths,
            'average_lengths': self.analyzer.average_lengths,
            'segment_statistics': self.analyzer.get_segment_statistics(),
            'segment_variability': self.analyzer.get_segment_variability(),
            'export_summary': self.exporter.get_export_summary()
        }
    
    def save_intermediate_results(self, output_dir: str) -> bool:
        """
        Save intermediate results to separate files.
        
        Args:
            output_dir: Directory to save intermediate files
            
        Returns:
            True if successful
        """
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Save 2D coordinates
            coord_exporter = MuboKapExporter()
            coord_exporter.add_marker_data(self.processor.projected_data, 'COORDINATES_2D')
            coord_exporter.export_to_file(output_path / "coordinates_2d.txt")
            
            # Save segment analysis
            if self.analyzer.average_lengths:
                seg_exporter = MuboKapExporter()
                seg_exporter.add_segment_data(self.analyzer.average_lengths, 'SEGMENTS')
                seg_exporter.add_statistics(self.analyzer.get_segment_statistics(), 'STATISTICS')
                seg_exporter.export_to_file(output_path / "segments_analysis.txt")
            
            return True
            
        except Exception as e:
            print(f"Error saving intermediate results: {str(e)}")
            return False