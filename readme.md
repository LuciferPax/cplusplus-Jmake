# jmake

jmake is a Python script designed to automate the compilation and linking process for C++ projects using a JSON configuration file.

## Installation

No installation is required for jmake. Simply download the script and ensure you have Python installed on your system.

## Usage

To use jmake, follow these steps:

1. Create a JSON configuration file (`jmake.json`) in your project directory. See the example below for the required structure.
2. Run the jmake script using Python, passing the path to your `jmake.json` file as an argument:

   ```bash
   python jmake.py /path/to/your/jmake.json
   ```

### Example jmake.json

```json
{
  "main_file": "main.cpp",
  "output_dir": "build",
  "include_dirs": ["include"]
}
```

## Configuration Options

- **\*main_file:** The path to the main C++ file of your project.
- **output_dir:** The directory where the compiled binary and object files will be stored.
- **include_dirs:** A list of directories containing header files and source files to be included during compilation.

## Dependencies

- Python 3.x
