"""
This script copies all specified folders to the target folder and optionally starts a webserver
from the target folder
"""
from typing import Tuple
from distutils.dir_util import copy_tree
import click
import os
import shutil
import http.server
import socketserver


def start_server(folder: str, port: int = 8080):
    """Starts a local webserver on the provided port"""
    os.chdir(folder)
    handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            try:
                print(f"🎉 Serving on http://localhost:{port}")
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("Shutting down server...")
            finally:
                httpd.server_close()
    except OSError as e:
        if e.errno == 48:
            print("The port is currently used by another application.")
        else:
            print(e)


def copy_paths_to_target(paths: Tuple, target: str):
    """Copies the folders in 'paths' to the 'target' folder."""
    if os.path.exists(target):
        shutil.rmtree(target)
    os.mkdir(target)
    for path in paths:
        if path[-1] == "/":
            path = path[:-1]
        folder_name = get_containing_folder(path)
        os.mkdir(
            os.path.join(target, folder_name)
        )  # set containing folder for current path
        sub_target = os.path.join(target, folder_name)
        copy_tree(path, sub_target)


def get_containing_folder(path: str) -> str:
    """Takes a path and returns a folder name that should contain
    the provided path in the target folder. If this path is
    unknown, return the same folder name as in the path"""
    # Add special cases here
    return path.split("/")[-1]


def check_path_params(paths: Tuple) -> bool:
    """Checks if all paths in 'paths' exist."""
    for path in paths:
        if not os.path.isdir(path):
            print(f"Path does not exist: {path}")
            return False
    return True


@click.command()
@click.option(
    "--target",
    "-t",
    required=True,
    help="The target folder that will contain the provided paths.",
)
@click.option(
    "--path",
    "-p",
    multiple=True,
    required=True,
    help="A path to a folder to be copied to the target path.",
)
@click.option(
    "--serve",
    "-s",
    is_flag=True,
    help="Starts a local webserver from the target folder.",
)
def main(path: Tuple, target: str, serve: bool):
    if not check_path_params(path):
        exit()
    copy_paths_to_target(path, target)
    if serve:
        start_server(target)


if __name__ == "__main__":
    main()
