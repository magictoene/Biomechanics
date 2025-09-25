"""
Segment Analyzer Module

Calculates average segment lengths between marker points across timesteps.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from .coordinate_processor import CoordinateProcessor


class SegmentAnalyzer:
    """
    Analyzer for calculating segment lengths between markers.
    """
    
    def __init__(self, coordinate_processor: CoordinateProcessor):
        self.processor = coordinate_processor
        self.segment_definitions = []
        self.segment_lengths = {}
        self.average_lengths = {}
        
    def define_segment(self, marker1: str, marker2: str, segment_name: Optional[str] = None) -> None:
        """
        Define a segment between two markers.
        
        Args:
            marker1: Name of the first marker
            marker2: Name of the second marker  
            segment_name: Optional custom name for the segment
        """
        if segment_name is None:
            segment_name = f"{marker1}-{marker2}"
            
        segment_def = {
            'name': segment_name,
            'marker1': marker1,
            'marker2': marker2
        }
        
        self.segment_definitions.append(segment_def)
    
    def define_multiple_segments(self, segment_pairs: List[Tuple[str, str, Optional[str]]]) -> None:
        """
        Define multiple segments at once.
        
        Args:
            segment_pairs: List of tuples (marker1, marker2, optional_segment_name)
        """
        for pair in segment_pairs:
            if len(pair) == 2:
                self.define_segment(pair[0], pair[1])
            elif len(pair) == 3:
                self.define_segment(pair[0], pair[1], pair[2])
    
    def calculate_segment_length(self, marker1: str, marker2: str) -> Optional[np.ndarray]:
        """
        Calculate distances between two markers across all timesteps.
        
        Args:
            marker1: Name of the first marker
            marker2: Name of the second marker
            
        Returns:
            Array of distances for each timestep, or None if markers not found
        """
        coords1 = self.processor.get_marker_2d_coordinates(marker1)
        coords2 = self.processor.get_marker_2d_coordinates(marker2)
        
        if len(coords1) == 0 or len(coords2) == 0:
            return None
            
        try:
            return self.processor.calculate_distances_2d(coords1, coords2)
        except Exception as e:
            print(f"Warning: Could not calculate segment length between {marker1} and {marker2}: {str(e)}")
            return None
    
    def calculate_all_segment_lengths(self) -> Dict[str, np.ndarray]:
        """
        Calculate lengths for all defined segments.
        
        Returns:
            Dictionary mapping segment names to distance arrays
        """
        self.segment_lengths = {}
        
        for segment in self.segment_definitions:
            lengths = self.calculate_segment_length(segment['marker1'], segment['marker2'])
            if lengths is not None:
                self.segment_lengths[segment['name']] = lengths
                
        return self.segment_lengths
    
    def calculate_average_lengths(self) -> Dict[str, float]:
        """
        Calculate average lengths for all segments.
        
        Returns:
            Dictionary mapping segment names to average lengths
        """
        self.average_lengths = {}
        
        for segment_name, lengths in self.segment_lengths.items():
            if len(lengths) > 0:
                # Filter out NaN values if any
                valid_lengths = lengths[~np.isnan(lengths)]
                if len(valid_lengths) > 0:
                    self.average_lengths[segment_name] = float(np.mean(valid_lengths))
                
        return self.average_lengths
    
    def get_segment_statistics(self) -> Dict[str, Dict[str, float]]:
        """
        Get comprehensive statistics for all segments.
        
        Returns:
            Dictionary with statistics for each segment
        """
        stats = {}
        
        for segment_name, lengths in self.segment_lengths.items():
            if len(lengths) > 0:
                valid_lengths = lengths[~np.isnan(lengths)]
                if len(valid_lengths) > 0:
                    stats[segment_name] = {
                        'mean': float(np.mean(valid_lengths)),
                        'std': float(np.std(valid_lengths)),
                        'min': float(np.min(valid_lengths)),
                        'max': float(np.max(valid_lengths)),
                        'range': float(np.ptp(valid_lengths)),
                        'count': len(valid_lengths),
                        'total_timesteps': len(lengths)
                    }
                    
        return stats
    
    def get_segment_variability(self) -> Dict[str, float]:
        """
        Calculate coefficient of variation for each segment.
        
        Returns:
            Dictionary mapping segment names to coefficient of variation
        """
        variability = {}
        
        for segment_name, lengths in self.segment_lengths.items():
            if len(lengths) > 0:
                valid_lengths = lengths[~np.isnan(lengths)]
                if len(valid_lengths) > 0:
                    mean_length = np.mean(valid_lengths)
                    std_length = np.std(valid_lengths)
                    if mean_length > 0:
                        variability[segment_name] = float(std_length / mean_length)
                        
        return variability
    
    def filter_segments_by_length(self, min_length: float = 0.0, max_length: float = float('inf')) -> Dict[str, float]:
        """
        Filter segments by average length criteria.
        
        Args:
            min_length: Minimum average length threshold
            max_length: Maximum average length threshold
            
        Returns:
            Dictionary of segments meeting the criteria
        """
        filtered = {}
        
        for segment_name, avg_length in self.average_lengths.items():
            if min_length <= avg_length <= max_length:
                filtered[segment_name] = avg_length
                
        return filtered
    
    def clear_segments(self) -> None:
        """Clear all segment definitions and calculated data."""
        self.segment_definitions = []
        self.segment_lengths = {}
        self.average_lengths = {}