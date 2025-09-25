# Biomechanics Pipeline

A comprehensive pipeline for processing .tsv files containing marker coordinates for biomechanical analysis and generating MuboKap Input files in MATLAB-compatible format.

## Features

- **TSV Data Reader**: Reads .tsv files containing 3D marker coordinate data
- **3D to 2D Projection**: Projects coordinates from 3D to 2D by removing y-component (stretching)
- **Segment Analysis**: Calculates average segment lengths between marker points across timesteps
- **MuboKap Export**: Generates MATLAB-compatible .txt files with specific layout for MuboKap

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### Command Line Usage

```bash
# Basic usage - auto-generate all possible segments
python run_pipeline.py sample_data/sample_markers.tsv output.txt

# With specific segment definitions
python run_pipeline.py sample_data/sample_markers.tsv output.txt \
  --segments "shoulder,elbow,upper_arm;elbow,wrist,forearm"

# With custom metadata
python run_pipeline.py sample_data/sample_markers.tsv output.txt \
  --metadata "subject:P001,condition:running,trial:1"

# Validate input file only
python run_pipeline.py sample_data/sample_markers.tsv output.txt --validate-only
```

### Python API Usage

```python
from biomechanics_pipeline import BiomechanicsPipeline

# Initialize pipeline
pipeline = BiomechanicsPipeline()

# Define segments (optional)
segments = [
    ("shoulder", "elbow", "upper_arm"),
    ("elbow", "wrist", "forearm"),
    ("shoulder", "wrist", "full_arm")
]

# Run complete pipeline
success = pipeline.run_complete_pipeline(
    input_tsv_path="data/markers.tsv",
    output_path="output/result.txt",
    segment_definitions=segments,
    metadata={"subject": "P001", "condition": "walking"}
)
```

## Input Format

TSV files should contain marker coordinate data with columns formatted as:
```
marker1_x    marker1_y    marker1_z    marker2_x    marker2_y    marker2_z    ...
```

Example:
```
shoulder_x	shoulder_y	shoulder_z	elbow_x	elbow_y	elbow_z	wrist_x	wrist_y	wrist_z
10.5	15.2	8.3	12.1	14.8	6.2	14.3	14.5	4.1
10.6	15.1	8.4	12.2	14.7	6.3	14.4	14.4	4.2
...
```

## Output Format

The pipeline generates MuboKap Input files with the following sections:

1. **Header**: Metadata and file information
2. **MARKERS_2D**: 2D projected coordinates (x, z only)
3. **SEGMENT_AVERAGES**: Average lengths for defined segments
4. **SEGMENT_STATISTICS**: Detailed statistics for each segment

## Testing

Run the test suite to verify installation:

```bash
python test_pipeline.py
```

## Pipeline Components

### TSVReader
- Reads and validates TSV marker data
- Extracts marker names and coordinates
- Validates data completeness

### CoordinateProcessor  
- Projects 3D coordinates to 2D (removes y-component)
- Calculates distances between marker pairs
- Provides projection statistics

### SegmentAnalyzer
- Defines segments between marker pairs
- Calculates segment lengths across timesteps
- Computes average lengths and statistics
- Analyzes segment variability

### MuboKapExporter
- Formats data for MuboKap compatibility
- Exports to MATLAB-readable .txt format
- Includes metadata and structured sections

## Requirements

- Python >= 3.7
- pandas >= 1.3.0
- numpy >= 1.20.0

## License

Code base for the Biomechanics of Movement Course @IST
