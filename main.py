import os
import argparse

CD_PRESETS = {
    "650MB": 650.0,
    "700MB": 700.0,
    "800MB": 800.0,
    "miniCD": 210.0,
    "businessCard": 50.0
}

def get_directory_size(directory):
    """Calculate the total size of all files in a directory (in bytes)."""
    total_size = 0
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    total_size += os.path.getsize(file_path)
                except (OSError, FileNotFoundError):
                    print(f"Warning: Could not access file {file_path}")
    except (OSError, FileNotFoundError) as e:
        print(f"Error: Could not process directory {directory}: {e}")
        return 0
    return total_size

def check_cd_fit(directory, cd_size_mb):
    """Check if the directory's files fit on a CD of given size (in MB)."""
    cd_size_bytes = cd_size_mb * 1024 * 1024
    total_size_bytes = get_directory_size(directory)
    
    total_size_mb = total_size_bytes / (1024 * 1024)
    
    print(f"Total size: {total_size_mb:.2f} MB")
    print(f"CD capacity: {cd_size_mb} MB")
    
    if total_size_bytes == 0:
        print("No files found or directory inaccessible.")
    elif total_size_bytes <= cd_size_bytes:
        print("Files fit on the CD!")
    else:
        print("Files do NOT fit on the CD.")

def main():
    """Main function to parse arguments and run the CD size check."""
    parser = argparse.ArgumentParser(
        description="Check if files fit on a CD (e.g., 700MB)."
    )
    parser.add_argument(
        "directory",
        help="Path to the directory to check"
    )
    parser.add_argument(
        "--cd-size",
        type=float,
        default=None,
        help="Custom CD size in MB (e.g. 730.5). Overrides --preset-size if both are used."
    )
    parser.add_argument(
        "--preset-size",
        type=str,
        choices=CD_PRESETS.keys(),
        default="700MB",
        help="Choose from common CD sizes: " + ", ".join(CD_PRESETS.keys())
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory.")
        return

    # Determine final CD size to use
    cd_size = args.cd_size if args.cd_size is not None else CD_PRESETS[args.preset_size]

    # Run the check
    check_cd_fit(args.directory, cd_size)

if __name__ == "__main__":
    main()
