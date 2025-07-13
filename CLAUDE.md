# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
CompLOINC (Computational LOINC in OWL) is a Python-based project that creates an OWL formalization of LOINC (Logical Observation Identifiers Names and Codes) with SNOMED CT integration. It builds ontologies from multiple medical coding systems using a sophisticated pipeline.

## Key Technologies
- Python 3.11+ with Poetry for dependency management
- LinkML for schema definition
- NetworkX for graph operations
- ROBOT (Java tool) for OWL manipulation and reasoning
- Typer CLI framework
- Dash/Plotly for visualization

## Essential Commands

### Development Setup
```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install --no-interaction

# Download ROBOT tool
wget https://github.com/ontodev/robot/releases/latest/download/robot.jar
```

### Building the Ontology
```bash
# Full build (rebuilds everything)
make all -B

# Standard build (respects timestamps)
make all

# Fast build for testing
comploinc --fast-run build
```

### Running Tests
```bash
# Run all tests
poetry run python -m unittest discover

# Or without poetry prefix
python -m unittest discover
```

### Code Formatting
```bash
# Format code with Black (line length: 88)
poetry run black src/
poetry run black test/
```

### Analysis Web App
```bash
# Start in debug mode
make start-app-debug

# Start in production mode
make start-app
```

## Architecture Overview

### Core Components

1. **loinclib** (`src/loinclib/`): Creates NetworkX graphs from source data
   - Loads LOINC releases, LOINC Tree hierarchies, SNOMED data, and mappings
   - Key file: `graph.py` - Core graph operations

2. **comp_loinc** (`src/comp_loinc/`): Generates OWL modules from graphs
   - `loinc_builder_steps.py` - LOINC-specific build logic
   - `snomed_builder_steps.py` - SNOMED-specific build logic
   - `module.py` - Module instantiation and processing
   - `runtime.py` - Manages shared state between modules

### Build Pipeline

The makefile orchestrates a complex pipeline:
1. **Module Generation**: Creates individual OWL modules for different aspects
2. **Grouping**: Builds grouping classes (components, systems)
3. **Analysis**: Generates statistics and dangling term analysis
4. **Merge & Reason**: Combines modules and runs reasoners
5. **Documentation**: Generates stats and documentation

Key makefile targets:
- `modules` - Build core OWL modules
- `grouping` - Build grouping classes
- `dangling` - Analyze dangling terms
- `merge-reason` - Merge and reason over ontology
- `stats` - Generate statistics

### Output Modules
- `loinc-term-primary-def.owl` - Primary term definitions
- `loinc-term-supplementary-def.owl` - Supplementary definitions
- `loinc-part-hierarchy-all.owl` - Part hierarchies
- `loinc-snomed-equiv.owl` - LOINC-SNOMED equivalences
- `group_*.owl` - Grouping classes
- `snomed-parts.owl` - SNOMED part definitions

## Configuration
Main configuration file: `comploinc_config.yaml`
- Defines paths to LOINC, SNOMED, and mapping releases
- Sets thresholds for NLP matching
- Configures logging

## Data Sources
Input data is organized in these directories:
- `loinc_release/` - LOINC release files
- `loinc_trees/` - LOINC hierarchy exports from web app
- `loinc_snomed_release/` - LOINC-SNOMED ontology and mappings
- `snomed_release/` - SNOMED CT releases
- `curation/` - Curator feedback files (e.g., NLP matches)

## Testing Considerations
- Tests require ROBOT tool to be available
- Use `comploinc --fast-run build` to populate test data
- Tests use Python's unittest framework
- Test files in `/test/` directory include SPARQL queries

## Important Notes
- The project uses Poetry's lock file - always use `poetry install` for consistent dependencies
- ROBOT is required for SPARQL queries and OWL operations
- The makefile is the primary orchestration tool - understand it before making build changes
- Fast-run mode creates limited output suitable for testing
- Curator feedback in `/curation/nlp-matches.sssom.tsv` affects build output