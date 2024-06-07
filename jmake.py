import json
import subprocess
import os

def jmake(json_file='jmake.json'):
    # Read the JSON file
    include_dirs = []
    linkable_files = []
    compiler_path = 'g++'  # Default compiler path
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)

            main_file = data['main_file']
            output_dir = data['output_dir']
            objects_dir = os.path.join(output_dir, 'objects')

            # Create directories if they don't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            if not os.path.exists(objects_dir):
                os.makedirs(objects_dir)

            # Check if compiler path is specified
            if 'compiler_path' in data:
              compiler_path = data['compiler_path']

            # Dictionary to track dependencies
            dependencies = {}

            for include_dir in data['include_dirs']:
                include_dirs.append('-I' + include_dir)
                for file in os.listdir(include_dir):
                    if file.endswith('.cpp'):
                        file_path = os.path.join(include_dir, file)
                        file_without_extension = os.path.splitext(file)[0]
                        output_file_path = os.path.join(objects_dir, file_without_extension + '.o')

                        # Get dependencies for each source file
                        dependencies[file_path] = set()
                        with open(file_path, 'r') as source_file:
                            for line in source_file:
                                if line.startswith('#include'):
                                    dependency = line.split(' ')[1].strip('"\n')
                                    if dependency.endswith('.h'):
                                        dependencies[file_path].add(dependency)

                        # Compile source file
                        subprocess.run([compiler_path, '-c', file_path, '-o', output_file_path] + include_dirs)
                        linkable_files.append(output_file_path)

            # Compile main file
            main_output_file_path = os.path.join(objects_dir, os.path.splitext(os.path.basename(main_file))[0] + '.o')
            subprocess.run([compiler_path, '-c', main_file, '-o', main_output_file_path] + include_dirs)
            linkable_files.append(main_output_file_path)

            # Link all objects
            subprocess.run([compiler_path, '-o', os.path.join(output_dir, 'main')] + linkable_files)

            print("Dependencies:")
            for source_file, deps in dependencies.items():
                print(source_file, "depends on", deps)
    except FileNotFoundError:
        print("Could not locate jmake file:", json_file)

# main function that takes in an argument
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        jmake(sys.argv[1])
    else:
        jmake()
