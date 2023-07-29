import os
import sys
import ptrack
from ptrack.methods import format_file_size, regular_copy, verbose_copy, hlp
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, FileSizeColumn
from rich.console import Console
import shutil

verbose = ptrack.verbose
argCopy = ptrack.copy
argMove = ptrack.move


def run(process):
    console = Console()

    if len(sys.argv) < 3:
        hlp()
        if process == "Copying":
            console.print("[bold cyan]Usage: ptc [OPTIONS] SOURCE... DESTINATION[/bold cyan]")
        elif process == "Moving":
            console.print("[bold cyan]Usage: ptm [OPTIONS] SOURCE... DESTINATION[/bold cyan]")
        sys.exit(1)

    src_paths = sys.argv[1:-1]
    dst = sys.argv[-1]
    srcPaths = []

    for path in src_paths:
        if path.endswith('/'):
            path = path[:-1]
        srcPaths.append(path)

    if os.path.isdir(dst):
        dst_dir = dst
        new_name = None
    else:
        dst_dir = os.path.dirname(dst)
        new_name = os.path.basename(dst)

    total_files = sum(len(files) for path in srcPaths for r, d, files in os.walk(path) if os.path.isdir(path)) + sum(1 for path in srcPaths if os.path.isfile(path))
    total_size = sum(os.path.getsize(os.path.join(r, f)) for path in srcPaths for r, d, files in os.walk(path) for f in files) + sum(os.path.getsize(path) for path in srcPaths if os.path.isfile(path))
    current_file = 1

    if total_files > 1:
        console.print(f"\n[#ea2a6f]{process}:[/#ea2a6f] [bold cyan]{total_files} files[/bold cyan]\n")
    else:
        for src_path in srcPaths:
            if os.path.isfile(src_path):
                console.print(f"\n[#ea2a6f]{process}:[/#ea2a6f] [bold cyan] {os.path.basename(src_path)} [/bold cyan]\n")

    if verbose:
        for src_path in srcPaths:
            if os.path.isfile(src_path):
                dst_path = os.path.join(dst_dir, os.path.basename(src_path) if not new_name else new_name)
                verbose_copy(src_path, dst_path, console, current_file, total_files)
                current_file += 1
            else:
                for root, dirs, files in os.walk(src_path):
                    for file in files:
                        src_file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(src_file_path, start=src_path)
                        dst_file_path = os.path.join(dst_dir, os.path.basename(src_path) if not new_name else new_name, relative_path)
                        os.makedirs(os.path.dirname(dst_file_path), exist_ok=True)
                        verbose_copy(src_file_path, dst_file_path, console, current_file, total_files)
                        current_file += 1
    else:
        with Progress(
            BarColumn(bar_width=50),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
            "[#ea2a6f][[/#ea2a6f]",
            FileSizeColumn(),
            "[#ea2a6f]/[/#ea2a6f]",
            TextColumn("[bold cyan]{task.fields[total_size]}[/bold cyan]"),
            "[#ea2a6f]][/#ea2a6f]",
            console=console,
            auto_refresh=False
        ) as progress:
            task = progress.add_task("", total=total_size, total_size=format_file_size(total_size))

            for src_path in srcPaths:
                if os.path.isfile(src_path):
                    dst_file_path = os.path.join(dst_dir, os.path.basename(src_path) if not new_name else new_name)
                    regular_copy(src_path, dst_file_path, console, task, progress)
                else:
                    for root, dirs, files in os.walk(src_path):
                        for file in files:
                            src_file_path = os.path.join(root, file)
                            relative_path = os.path.relpath(src_file_path, start=src_path)
                            dst_file_path = os.path.join(dst_dir, os.path.basename(src_path) if not new_name else new_name, relative_path)
                            os.makedirs(os.path.dirname(dst_file_path), exist_ok=True)
                            regular_copy(src_file_path, dst_file_path, console, task, progress)

    return srcPaths


def copy():
    run('Copying')


def move():
    src_paths = run('Moving')
    for src_path in src_paths:
        if os.path.isfile(src_path):
            os.remove(src_path)
        else:
            shutil.rmtree(src_path)


def main():
    if argMove:
        move()
    elif argCopy:
        copy()
    else:
        hlp()


if __name__ == "__main__":
    main()
