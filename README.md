# Open Prism API (Unofficial)

[![License](https://img.shields.io/badge/License-LGPL%203.0-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0.html)
![Python Version](https://img.shields.io/badge/Python-3.7%2B-purple)
[![Prism Version](https://img.shields.io/badge/Prism-2.0.13-orange)](https://prism-pipeline.com/)

A community-maintained Python API for interacting with Prism pipeline tools in DCC applications like Maya and Houdini.

**Disclaimer:** This is an independent community project not affiliated with Prism Software GmbH.  
Official Prism website: [prism-pipeline.com](https://prism-pipeline.com/)

## Description

The Open Prism API provides a standardized interface to access some Prism pipeline functionality from within Digital Content Creation (DCC) applications. It offers methods to:

- Get project information (name, path, root folder)
- Check and manage Prism plugins (Maya, Houdini)
- Retrieve scene metadata (task, department, shot range)
- Generate export paths for products, media, and playblasts
- Manage versioning (setting master versions)
- Browse and request products

## Features

- **DCC Integration**: Automatic support for Prism inside Maya and Houdini
- **Standalone Mode**: You can set a standalone Prism core module with `set_core()` for partial DCC support
- **Project Management**: Access project names, paths, and configurations
- **Export Path Generation**: Create valid Prism export paths for various asset types
- **Version Control**: Set master versions for products and media
- **Scene Metadata**: Retrieve task, department, and shot information

## Installation

1. Place the `prism.py` file within your plugin directory or Python path (must be loaded by your DCC to be available)
2. Import in your scripts with `import prism`

## Compatibility

- Tested with Prism 2.0.13
- Compatible with Maya and Houdini
- Partial compatibility with other DCCs through `set_core()`

## Basic Usage

```python
import prism

# Check if Prism is available
if prism.is_prism():
    # Get current project info
    project_name = prism.get_project_name()
    project_path = prism.get_project_path()
    
    # Generate export path for a product
    export_path = prism.get_product_export_file_path("model", ".abc")
    
    # Get current scene task
    current_task = prism.get_task()
```

## API Reference

### Core Functions
- `get_core()` - Get the Prism core reference

- `set_core()` - Set a custom Prism core reference

- `is_prism()` - Check if Prism is available

### Project Information
- `get_project_name()` - Get current prism project name

- `get_project_path()` - Get current prism project path

- `get_prism_folder()` - Get Prism root folder

### Scene Information
- `get_curr_scene_file_path()` - Get current scene path

- `is_scene_in_prism()` - Check if scene is in Prism project

- `get_task()` - Get current scene task

- `get_department()` - Get current scene department

- `get_shot_range()` - Get shot start/end frames for the current scene

### Export Path Generation
- `get_product_export_data()` - Generate product export metadata

- `get_product_export_file_path()` - Generate product export path

- `get_media_product_data()` - Generate media export metadata

- `get_media_export_file_path()` - Generate media export path

- `get_playblast_product_data()` - Generate playblast metadata

- `get_playblast_export_file_path()` - Generate playblast export path

### Version Management
- `set_product_master_version()` - Set product master version from file path

- `set_media_master_version()` - Set media master version from file path

- `set_playblast_master_version()` - Set playblast master version from file path

- `set_render_master_version()` - Set render master version from file path

### Location Management
- `get_export_locations()` - Get available prism export locations

- `get_render_locations()` - Get available prism render locations

### UI Integration
- `request_products()` - Open product browser and return selected paths

## Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

Maintainer: [Anna Fratus](https://github.com/annafratus)

## License

Copyright © 2024-2025 [Anna Fratus](https://annafratus.com/)

This library is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This library is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this library. If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.