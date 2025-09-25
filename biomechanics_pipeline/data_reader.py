"""
TSV Data Reader Module

Handles reading .tsv files containing marker coordinate data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class TSVReader:
    """
    Reader for TSV files containing marker coordinate data.
    
    Expects TSV format with columns for marker names and their x, y, z coordinates.
    """
    
    def __init__(self):
        self.data = None
        self.markers = []
        self.timesteps = 0
        
    def read_file(self, filepath: str) -> pd.DataFrame:
        """
        Read a TSV file containing marker coordinate data.
        
        Args:
            filepath: Path to the TSV file
            
        Returns:
            DataFrame containing the marker coordinate data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is invalid
        """
        file_path = Path(filepath)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
            
        try:
            # Read TSV file
            self.data = pd.read_csv(filepath, sep='\t')
            
            # Extract marker information
            self._extract_markers()
            self.timesteps = len(self.data)
            
            return self.data
            
        except Exception as e:
            raise ValueError(f"Error reading TSV file: {str(e)}")
    
    def _extract_markers(self) -> None:
        """Extract marker names from column headers."""
        if self.data is None:
            return
            
        # Assume columns are in format: marker1_x, marker1_y, marker1_z, marker2_x, etc.
        marker_set = set()
        for col in self.data.columns:
            if '_' in col:
                marker_name = col.rsplit('_', 1)[0]
                marker_set.add(marker_name)
        
        self.markers = sorted(list(marker_set))
    
    def get_marker_coordinates(self, marker_name: str) -> Optional[np.ndarray]:
        """
        Get 3D coordinates for a specific marker across all timesteps.
        
        Args:
            marker_name: Name of the marker
            
        Returns:
            Array of shape (timesteps, 3) containing x, y, z coordinates
        """
        if self.data is None:
            return None
            
        try:
            x_col = f"{marker_name}_x"
            y_col = f"{marker_name}_y"
            z_col = f"{marker_name}_z"
            
            if all(col in self.data.columns for col in [x_col, y_col, z_col]):
                return np.column_stack([
                    self.data[x_col].values,
                    self.data[y_col].values,
                    self.data[z_col].values
                ])
            else:
                return None
                
        except Exception:
            return None
    
    def get_all_markers_data(self) -> Dict[str, np.ndarray]:
        """
        Get coordinates for all markers.
        
        Returns:
            Dictionary mapping marker names to coordinate arrays
        """
        result = {}
        for marker in self.markers:
            coords = self.get_marker_coordinates(marker)
            if coords is not None:
                result[marker] = coords
        return result
    
    def validate_data(self) -> Tuple[bool, List[str]]:
        """
        Validate the loaded data for completeness and format.
        
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        if self.data is None:
            issues.append("No data loaded")
            return False, issues
        
        if len(self.markers) == 0:
            issues.append("No markers found in data")
        
        # Check for missing coordinate columns
        for marker in self.markers:
            for coord in ['x', 'y', 'z']:
                col_name = f"{marker}_{coord}"
                if col_name not in self.data.columns:
                    issues.append(f"Missing {coord} coordinate for marker {marker}")
        
        # Check for missing values
        for marker in self.markers:
            coords = self.get_marker_coordinates(marker)
            if coords is not None and np.any(np.isnan(coords)):
                issues.append(f"Missing coordinate values for marker {marker}")
        
        return len(issues) == 0, issues