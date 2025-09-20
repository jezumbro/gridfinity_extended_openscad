# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Testing
- Run tests: `pytest`
- Run tests with coverage: `pytest --cov=model --cov-report=html`

### Linting and Formatting
- Format code: `ruff format`
- Check linting: `ruff check`
- Auto-fix linting issues: `ruff check --fix`

### Running the Application
- Run main script: `python main.py` (interactive mode with questionary for file selection)
- Run kitchen drawer generator: `python kitchen_drawer.py`
- Generate STL from OpenSCAD: `openscad -o output.stl --export-format binstl input.scad`

### Dependencies
- Install dependencies: `pip install -r requirements.txt`
- Development dependencies: `pip install -r requirements-dev.txt`

## Architecture

This project combines Python-based socket configuration management with OpenSCAD 3D modeling for creating Gridfinity-compatible storage solutions.

### Core Components

**Python Socket Generation System:**
- `model/socket.py`: Defines `Socket` and `MultiLevelSocket` data models using Pydantic
- `model/configuration.py`: Contains `Configuration` and `Tolerance` classes for parametric control
- `model/socket_generator.py`: Core `SocketGenerator` class that converts socket specifications into OpenSCAD code
- `main.py`: Interactive CLI that loads JSON configurations and generates OpenSCAD files, then calls OpenSCAD to produce STL files

**OpenSCAD Templates:**
- Multiple `.scad` files provide pre-built Gridfinity components (cups, baseplates, drawers, etc.)
- `modules/` directory contains reusable OpenSCAD modules
- Generated `main.scad` file is produced by the Python system for custom socket layouts

**Data-Driven Configuration:**
- `data/` directory contains JSON files with socket specifications
- JSON files define arrays of socket rows with dimensions, tolerances, and layout parameters
- Supports both simple sockets and multi-level sockets (with diameter transitions)

### Key Workflow

1. User selects a JSON configuration file via questionary interface
2. `DataModel` validates and loads socket specifications from JSON
3. `SocketGenerator` calculates optimal grid layout and spacing
4. OpenSCAD code is generated with precise cylinder cutouts for each socket
5. OpenSCAD executable converts the generated code to STL format
6. Output STL files are saved to `out/` directory

### Dependencies

- **loguru**: Logging throughout the application
- **pydantic**: Data validation and modeling for configurations
- **questionary**: Interactive CLI prompts
- **more-itertools**: Utility functions for list processing
- **cqgridfinity**: CadQuery-based Gridfinity components (used in kitchen_drawer.py)

### Testing

- Uses pytest with parametrized tests
- Test fixtures defined in `conftest.py`
- Tests focus on spacing calculations and socket generation logic
