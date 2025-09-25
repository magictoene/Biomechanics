"""
Coordinate Processor Module

Handles 3D to 2D projection by removing the y-component of coordinates.
"""

import numpy as np
from typing import Dict, Tuple


class CoordinateProcessor:
    """
    Processor for converting 3D marker coordinates to 2D by removing y-component.
    """
    
    def __init__(self):
        self.projected_data = {}
        
    def project_to_2d(self, coordinates_3d: np.ndarray) -> np.ndarray:
        """
        Project 3D coordinates to 2D by removing the y-component.
        
        Args:
            coordinates_3d: Array of shape (timesteps, 3) with x, y, z coordinates
            
        Returns:
            Array of shape (timesteps, 2) with x, z coordinates
        """
        if coordinates_3d.shape[1] != 3:
            raise ValueError("Input coordinates must have 3 dimensions (x, y, z)")
            
        # Extract x and z coordinates (remove y)
        return np.column_stack([coordinates_3d[:, 0], coordinates_3d[:, 2]])
    
    def process_all_markers(self, marker_data: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """
        Process all markers from 3D to 2D coordinates.
        
        Args:
            marker_data: Dictionary mapping marker names to 3D coordinate arrays
            
        Returns:
            Dictionary mapping marker names to 2D coordinate arrays
        """
        self.projected_data = {}
        
        for marker_name, coords_3d in marker_data.items():
            try:
                coords_2d = self.project_to_2d(coords_3d)
                self.projected_data[marker_name] = coords_2d
            except Exception as e:
                print(f"Warning: Could not process marker {marker_name}: {str(e)}")
                
        return self.projected_data
    
    def get_marker_2d_coordinates(self, marker_name: str) -> np.ndarray:
        """
        Get 2D coordinates for a specific marker.
        
        Args:
            marker_name: Name of the marker
            
        Returns:
            Array of shape (timesteps, 2) with x, z coordinates
        """
        return self.projected_data.get(marker_name, np.array([]))
    
    def calculate_distances_2d(self, coords1: np.ndarray, coords2: np.ndarray) -> np.ndarray:
        """
        Calculate Euclidean distances between two sets of 2D coordinates.
        
        Args:
            coords1: First set of 2D coordinates (timesteps, 2)
            coords2: Second set of 2D coordinates (timesteps, 2)
            
        Returns:
            Array of distances for each timestep
        """
        if coords1.shape != coords2.shape:
            raise ValueError("Coordinate arrays must have the same shape")
            
        # Calculate Euclidean distance for each timestep
        return np.sqrt(np.sum((coords1 - coords2) ** 2, axis=1))
    
    def get_projection_summary(self) -> Dict[str, Dict[str, float]]:
        """
        Get summary statistics of the projection process.
        
        Returns:
            Dictionary with statistics for each marker
        """
        summary = {}
        
        for marker_name, coords_2d in self.projected_data.items():
            if len(coords_2d) > 0:
                summary[marker_name] = {
                    'timesteps': len(coords_2d),
                    'x_range': float(np.ptp(coords_2d[:, 0])),
                    'z_range': float(np.ptp(coords_2d[:, 1])),
                    'x_mean': float(np.mean(coords_2d[:, 0])),
                    'z_mean': float(np.mean(coords_2d[:, 1])),
                    'x_std': float(np.std(coords_2d[:, 0])),
                    'z_std': float(np.std(coords_2d[:, 1]))
                }
        
        return summary