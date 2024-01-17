import os
import shutil
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Function to get metadata of files
def get_metadata(file_paths):
    try:
        # Set the LANG environment variable to ensure UTF-8 output
        os.environ['LANG'] = 'en_US.UTF-8'

        # Ensure full paths are passed to exiftool
        full_file_paths = [os.path.abspath(file_path) for file_path in file_paths]

        command = ['exiftool', '-json'] + full_file_paths
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        
        # Check if the command was successful
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"Error running 'exiftool': {result.stderr}")
            return [None] * len(file_paths)
    except UnicodeDecodeError as e:
        print(f"Error decoding output: {e}")
        return [None] * len(file_paths)
    except Exception as e:
        print(f"Error reading metadata: {e}")
        return [None] * len(file_paths)

# Function to process a single file
# Function to process a single file
def process_file(png_file, hi_folder_path):
    try:
        print(f"Processing file: {png_file}")  # Debugging statement
        metadatas = get_metadata([png_file])
        metadata = metadatas[0]

        if metadata:
            # Parsing the model name from the metadata
            parameters = metadata.get("Parameters", None)
            if parameters:
                params_list = parameters.split(',')
                model_name = next((param.split("Model: ")[1].strip() for param in params_list if "Model: " in param), "Unknown")

                # Create subfolder paths
                model_path = os.path.join(hi_folder_path, model_name)
                dimensions = metadata.get("ImageSize", "").split("x")
                shortest_dimension = min(dimensions, key=int) if dimensions else "Unknown"
                dimension_path = os.path.join(model_path, shortest_dimension + "x")

                # Create directories if they don't exist
                os.makedirs(dimension_path, exist_ok=True)

                # Move the file
                shutil.move(png_file, os.path.join(dimension_path, os.path.basename(png_file)))
                print(f"File {png_file} moved to {dimension_path}")  # Debugging statement
            else:
                print(f"No 'Parameters' found in metadata for file {png_file}")  # Debugging statement
        else:
            print(f"No metadata found for file {png_file}")  # Debugging statement
    except Exception as e:
        print(f"Error processing file {png_file}: {e}")  # Debugging statement


# Function to find PNG files recursively
def find_png_files(root_dir, hi_folder_path):
    png_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude 'Hi' folder and its subdirectories
        if hi_folder_path in dirpath:
            continue
        for file in filenames:
            if file.endswith('.png'):
                full_path = os.path.join(dirpath, file)
                png_files.append(full_path)
    return png_files

# Main function to orchestrate the script
def main():
    try:
        # Root directory where the script is running
        root_dir = os.getcwd()
        print(f"Current working directory: {root_dir}")

        # Path for 'Hi' folder
        hi_folder_path = os.path.join(root_dir, "Hi")
        print(f"'Hi' folder path: {hi_folder_path}")

        # Create 'Hi' folder if it doesn't exist
        os.makedirs(hi_folder_path, exist_ok=True)

        # Recursively find PNG files in the root directory and subdirectories, excluding 'Hi'
        png_files = find_png_files(root_dir, hi_folder_path)

        # Debugging statement to check if PNG files are detected
        print(f"Found PNG files: {png_files}")

        # Use half of the available CPU threads
        num_threads = max(1, os.cpu_count() // 2)

        # Process files in parallel
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(process_file, png_file, hi_folder_path) for png_file in png_files]
            for future in tqdm(as_completed(futures), total=len(png_files), desc="Processing files"):
                future.result()  # Wait for each future to complete
    except Exception as e:
        print(f"Error in main function: {e}")  # Debugging statement

if __name__ == "__main__":
    main()
