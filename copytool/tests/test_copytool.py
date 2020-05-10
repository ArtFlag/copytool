from copytool import check_path_params, copy_paths_to_target, get_containing_folder
import pytest
import shutil
import glob
from pathlib import Path

@pytest.fixture()
def create_dir(request):
    dir1 = Path("folder1")
    dir2 = Path("folder2")

    dir1.mkdir(exist_ok=True)
    dir2.mkdir(exist_ok=True)

    def del_dir():
        dir1.rmdir()
        dir2.rmdir()

    request.addfinalizer(del_dir)


@pytest.fixture()
def create_dirs_target(request):
    dir1 = Path("folder1")
    subfolder = dir1 / "subfolder"
    dir2 = Path("folder2")
    file = dir1 / "file.txt"

    subfolder.mkdir(parents=True, exist_ok=True)
    dir2.mkdir(parents=True, exist_ok=True)
    file.touch()

    def del_dir():
        shutil.rmtree(str(dir1))
        shutil.rmtree(str(dir2))

    request.addfinalizer(del_dir)


def test_get_containing_folder_unknown(create_dirs_target):
    path = "folder1/subfolder"
    assert get_containing_folder(path) == "subfolder"


def test_copy_path_dir(create_dirs_target):
    paths = ("folder1", "folder2")
    target = "target_dir"
    copy_paths_to_target(paths, target)
    target_content = [f for f in glob.glob(target + "/**/", recursive=True)]
    shutil.rmtree(target)
    assert "target_dir/folder1/" in target_content
    assert "target_dir/folder1/subfolder/" in target_content
    assert "target_dir/folder2/" in target_content


def test_copy_path_dir_subpath(create_dirs_target):
    paths = ("folder1/subfolder",)
    target = "target_dir"
    copy_paths_to_target(paths, target)
    target_content = [f for f in glob.glob(target + "/**/", recursive=True)]
    shutil.rmtree(target)
    assert "target_dir/folder1/" not in target_content
    assert "target_dir/subfolder/" in target_content


def test_copy_path_files(create_dirs_target):
    paths = ("folder1", "folder2")
    target = "target_dir"
    copy_paths_to_target(paths, target)
    target_content = [f for f in glob.glob(target + "/**/*", recursive=True)]
    shutil.rmtree(target)
    assert "target_dir/folder1/file.txt" in target_content


def test_check_several_paths_false(create_dir):
    dir1 = "folder1"
    paths = (dir1, "dummy")

    result = check_path_params(paths)
    assert result is False


def test_check_several_paths_true(create_dir):
    dir1 = "folder1"
    dir2 = "folder2"
    paths = (dir1, dir2)
    result = check_path_params(paths)
    assert result is True


def test_check_1_path_true(create_dir):
    dir1 = "folder1"
    paths = ()
    result = check_path_params(paths)
    assert result is True


def test_check_1_path_false():
    dir1 = "dummy"
    paths = dir1
    result = check_path_params(paths)
    assert result is False
