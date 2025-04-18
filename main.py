import os
import argparse
from pathlib import Path
import sys
import time
from rich.console import Console
from rich.progress import track

# Optional import for readline functionality
try:
    import readline
except ImportError:
    try:
        import pyreadline3 as readline
    except ImportError:
        readline = None

console = Console()

CD_PRESETS = {
    "CD_650MB": 650.0,
    "CD_700MB": 700.0,
    "DVD_4.7GB": 4482.0,
    "DVD_8.5GB": 8145.0,
    "MiniCD_210MB": 210.0,
    "MiniDVD_1.4GB": 1396.0
}

def display_help_menu(quiet=False):
    if quiet:
        return
    current_dir = os.getcwd()
    console.print(f"\n[bold cyan]=== CD Size Checker Help Menu ===[/bold cyan]")
    console.print(f"Current Directory: {current_dir}")
    console.print("This tool checks if files or directories fit on a CD or DVD.")
    console.print("\nAvailable Commands:")
    console.print("  python main.py <paths> [options]")
    console.print("\nArguments:")
    console.print("  paths                One or more file or directory paths to check")
    console.print("  --current-dir        Use the current directory")
    console.print("  --cd-size <size>     Custom disc size in MB (e.g., 730.5)")
    console.print("  --preset-size <name> Choose a preset disc size (default: CD_700MB)")
    console.print("  --extensions <exts>  Comma-separated file extensions (e.g., mp3,wav)")
    console.print("  --verbose            Show live processing count")
    console.print("  --quiet              Show only essential results")
    console.print("  --show-errors        Show detailed error messages")
    console.print("  --show-skipped       Show list of skipped files")
    console.print("  --help-menu          Show this help menu")
    console.print("\nPreset Sizes:")
    for preset, size in CD_PRESETS.items():
        console.print(f"  {preset:<15} {size:.1f} MB")
    console.print("\nExamples:")
    console.print(f"  python main.py \"{current_dir}\" --preset-size CD_700MB")
    console.print("  python main.py file.txt --cd-size 730.5 --verbose")
    console.print("  python main.py dir1 dir2 --extensions mp3,wav --current-dir")
    console.print("\nFor more details, see README.md or use --help-menu.")
    console.print("[bold cyan]===============================[/bold cyan]\n")

def clean_path(path: str) -> str:
    """Remove quotes and normalize path."""
    path = path.strip().strip('"').strip("'")
    return str(Path(path).resolve())

def get_path_size(path: str, allowed_extensions=None, verbose=False, quiet=False) -> dict:
    result = {
        'total_size': 0,
        'num_files': 0,
        'largest_file_size': 0,
        'largest_file_path': None,
        'errors': [],
        'skipped_files': [],
        'total_files': 0
    }
    path_obj = Path(path)
    if path_obj.is_file():
        files = [path_obj]
    elif path_obj.is_dir():
        files = [f for f in path_obj.rglob('*') if f.is_file() and (allowed_extensions is None or f.suffix[1:].lower() in allowed_extensions)]
    else:
        result['errors'].append(f"{path} is neither a file nor a directory.")
        files = []

    result['total_files'] = len(files)
    spinner_chars = '⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    spinner_index = 0

    if verbose and not quiet:
        for i, file in enumerate(files):
            console.clear()
            if allowed_extensions is None or file.suffix[1:].lower() in allowed_extensions:
                try:
                    size = file.stat().st_size
                    result['total_size'] += size
                    result['num_files'] += 1
                    if size > result['largest_file_size']:
                        result['largest_file_size'] = size
                        result['largest_file_path'] = str(file)
                except (OSError, FileNotFoundError) as e:
                    result['errors'].append(f"Could not access file {file}: {e}")
            else:
                result['skipped_files'].append(str(file))
            console.print(f"Processed: {result['num_files']} files [yellow]{spinner_chars[spinner_index % len(spinner_chars)]}[/yellow]")
            spinner_index += 1
            time.sleep(0.01)  # Reduced delay to 0.01 seconds for faster processing of large amount of files
        console.print(f"[green]Completed ✓ Processed: {result['num_files']}, Skipped: {len(result['skipped_files'])}, Errors: {len(result['errors'])}[/green]")
    else:
        for file in track(files, description="Scanning files", disable=quiet):
            if allowed_extensions is None or file.suffix[1:].lower() in allowed_extensions:
                try:
                    size = file.stat().st_size
                    result['total_size'] += size
                    result['num_files'] += 1
                    if size > result['largest_file_size']:
                        result['largest_file_size'] = size
                        result['largest_file_path'] = str(file)
                except (OSError, FileNotFoundError) as e:
                    result['errors'].append(f"Could not access file {file}: {e}")
            else:
                result['skipped_files'].append(str(file))
    return result

def check_cd_fit(path, cd_size_mb, allowed_extensions=None, verbose=False, quiet=False, show_errors=False, show_skipped=False):
    if cd_size_mb <= 0:
        if not quiet:
            console.print(f"[red]Error: CD size must be positive, got {cd_size_mb} MB[/red]")
        return
    cd_size_bytes = cd_size_mb * 1024 * 1024
    size_info = get_path_size(path, allowed_extensions, verbose, quiet)
    total_size_bytes = size_info['total_size']
    total_size_mb = total_size_bytes / (1024 * 1024)
    completion_percentage = (size_info['num_files'] / size_info['total_files'] * 100) if size_info['total_files'] > 0 else 0

    if not quiet:
        console.print(f"Total size: {total_size_mb:.2f} MB ({size_info['num_files']} files)")
        if size_info['largest_file_path']:
            largest_size_mb = size_info['largest_file_size'] / (1024 * 1024)
            console.print(f"Largest file: {size_info['largest_file_path']} ({largest_size_mb:.2f} MB)")
        console.print(f"CD capacity: {cd_size_mb} MB")
        console.print(f"Completion: {completion_percentage:.1f}%")
    if total_size_bytes == 0:
        if not quiet:
            console.print("[yellow]No files found or path inaccessible.[/yellow]")
    elif total_size_bytes <= cd_size_bytes:
        remaining = cd_size_bytes - total_size_bytes
        remaining_mb = remaining / (1024 * 1024)
        console.print(f"[green]Files fit on the CD! Remaining space: {remaining_mb:.2f} MB[/green]")
    else:
        console.print(f"[red]Files do NOT fit on the CD.[/red]")

    if (completion_percentage < 100 or size_info['errors']) and not quiet:
        if size_info['errors'] and (show_errors or input("Show detailed error messages? (y/n): ").strip().lower() == 'y'):
            for error in size_info['errors']:
                console.print(f"[red]{error}[/red]")
        if size_info['skipped_files'] and (show_skipped or input("Show list of skipped files? (y/n): ").strip().lower() == 'y'):
            for skipped in size_info['skipped_files']:
                console.print(f"Skipped file: {skipped}")

def interactive_mode(quiet=False):
    current_dir = os.getcwd()
    paths = []
    cd_size = None
    allowed_extensions = None
    verbose = False
    show_errors = False
    show_skipped = False

    if not quiet:
        console.print("\n[bold cyan]=== CD Size Checker Interactive Mode ===[/bold cyan]")
        console.print(f"Current Directory: {current_dir}")
        console.print("Enter a path (file or directory) to check.")

    while True:
        path = input("Path (or press Enter to use current directory): ").strip() if not quiet else current_dir
        if not path:
            paths.append(current_dir)
            if not quiet:
                console.print(f"Added: {current_dir}")
            break
        path = clean_path(path)
        if not os.path.exists(path):
            if not quiet:
                console.print(f"[red]Error: {path} does not exist. Try again.[/red]")
            continue
        paths.append(path)
        if not quiet:
            console.print(f"Added: {path}")
        break

    preset_choice = input("Choose a preset size (or press Enter for custom size): \n" +
                         "\n".join(f"  {k}: {v} MB" for k, v in CD_PRESETS.items()) + "\n> ").strip() if not quiet else "CD_700MB"
    if preset_choice in CD_PRESETS:
        cd_size = CD_PRESETS[preset_choice]
    else:
        while True:
            custom_size = input("Enter custom disc size in MB (e.g., 730.5): ").strip() if not quiet else "700"
            try:
                cd_size = float(custom_size)
                if cd_size <= 0:
                    if not quiet:
                        console.print("[red]Error: Size must be positive.[/red]")
                    continue
                break
            except ValueError:
                if not quiet:
                    console.print("[red]Error: Invalid number. Try again.[/red]")

    extensions = input("Enter file extensions to include (e.g., mp3,wav, or press Enter for all): ").strip() if not quiet else ""
    if extensions:
        allowed_extensions = [ext.strip().lstrip('.').lower() for ext in extensions.split(',')]

    verbose_input = input("Enable verbose mode (live file count)? (y/n): ").strip().lower() if not quiet else "n"
    verbose = verbose_input == 'y'

    quiet_input = input("Enable quiet mode (minimal output)? (y/n): ").strip().lower() if not quiet else "y"
    quiet = quiet_input == 'y' or quiet

    if not quiet:
        show_errors_input = input("Show detailed error messages? (y/n): ").strip().lower()
        show_errors = show_errors_input == 'y'
        show_skipped_input = input("Show list of skipped files? (y/n): ").strip().lower()
        show_skipped = show_skipped_input == 'y'

    for path in paths:
        if not quiet:
            console.print(f"\nChecking {path}:")
        check_cd_fit(path, cd_size, allowed_extensions, verbose, quiet, show_errors, show_skipped)
        if not quiet:
            console.print()

def main():
    parser = argparse.ArgumentParser(
        description="Check if files fit on a CD or DVD (e.g., 700MB or 4.7GB).",
        add_help=False
    )
    parser.add_argument(
        "paths",
        nargs='*',
        help="Paths to the files or directories to check"
    )
    parser.add_argument(
        "--current-dir",
        action="store_true",
        help="Use the current directory"
    )
    parser.add_argument(
        "--cd-size",
        type=float,
        default=None,
        help="Custom disc size in MB (e.g., 730.5). Overrides --preset-size."
    )
    parser.add_argument(
        "--preset-size",
        type=str,
        choices=CD_PRESETS.keys(),
        default=None,
        help="Choose from common disc sizes."
    )
    parser.add_argument(
        "--extensions",
        type=str,
        help="Comma-separated file extensions to include (e.g., mp3,wav)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show live processing count"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Show only essential results"
    )
    parser.add_argument(
        "--show-errors",
        action="store_true",
        help="Show detailed error messages"
    )
    parser.add_argument(
        "--show-skipped",
        action="store_true",
        help="Show list of skipped files"
    )
    parser.add_argument(
        "--help-menu",
        action="store_true",
        help="Show detailed help menu"
    )

    args = parser.parse_args()

    if args.help_menu:
        display_help_menu(args.quiet)
        return

    paths = [clean_path(p) for p in args.paths] if args.paths else []
    if args.current_dir:
        current_dir = os.getcwd()
        paths.append(current_dir)
        if not args.quiet:
            console.print(f"Added: {current_dir}")

    if not paths and args.cd_size is None and args.preset_size is None:
        interactive_mode(args.quiet)
        return

    if not paths:
        if not args.quiet:
            console.print("[red]Error: Missing directory or file paths.[/red]")
        paths = []
        current_dir = os.getcwd()
        while True:
            path = input(f"Please enter a path (e.g., {current_dir}\\Music, or Enter for current dir): ").strip() if not args.quiet else current_dir
            if not path:
                paths.append(current_dir)
                if not args.quiet:
                    console.print(f"Added: {current_dir}")
                break
            path = clean_path(path)
            if not os.path.exists(path):
                if not args.quiet:
                    console.print(f"[red]Error: {path} does not exist. Try again.[/red]")
                continue
            paths.append(path)
            if not args.quiet:
                console.print(f"Added: {path}")
            break

    if args.extensions:
        allowed_extensions = [ext.strip().lstrip('.').lower() for ext in args.extensions.split(',')]
    else:
        allowed_extensions = None

    if args.cd_size is not None:
        cd_size = args.cd_size
    elif args.preset_size is not None:
        cd_size = CD_PRESETS[args.preset_size]
    else:
        if not args.quiet:
            console.print("[red]Error: Missing disc size.[/red]")
        preset_choice = input("Choose a preset size (or press Enter for custom size): \n" +
                             "\n".join(f"  {k}: {v} MB" for k, v in CD_PRESETS.items()) + "\n> ").strip() if not args.quiet else "CD_700MB"
        if preset_choice in CD_PRESETS:
            cd_size = CD_PRESETS[preset_choice]
        else:
            while True:
                custom_size = input("Enter custom disc size in MB (e.g., 730.5): ").strip() if not args.quiet else "700"
                try:
                    cd_size = float(custom_size)
                    if cd_size <= 0:
                        if not args.quiet:
                            console.print("[red]Error: Size must be positive.[/red]")
                        continue
                    break
                except ValueError:
                    if not args.quiet:
                        console.print("[red]Error: Invalid number. Try again.[/red]")

    for path in paths:
        if not args.quiet:
            console.print(f"Checking {path}:")
        check_cd_fit(path, cd_size, allowed_extensions, args.verbose, args.quiet, args.show_errors, args.show_skipped)
        if not args.quiet:
            console.print()

if __name__ == "__main__":
    main()