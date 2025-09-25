"""
Biomechanics Pipeline Package

A pipeline for processing .tsv files containing marker coordinates
for biomechanical analysis and generating MuboKap Input files.
"""

from .data_reader import TSVReader
from .coordinate_processor import CoordinateProcessor
from .segment_analyzer import SegmentAnalyzer
from .mubokap_exporter import MuboKapExporter
from .pipeline import BiomechanicsPipeline

__version__ = "1.0.0"
__all__ = ["TSVReader", "CoordinateProcessor", "SegmentAnalyzer", "MuboKapExporter", "BiomechanicsPipeline"]