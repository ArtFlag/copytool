from copytool import check_path_params, copy_paths_to_target, get_containing_folder
import os
import pytest
import shutil
import glob


@pytest.fixture()
def create_dir(request):
    dir = "existing_subfolder"
    dir2 = "existing_subfolder2"

    os.mkdir(dir)
    os.mkdir(dir2)

    def del_dir():
        shutil.rmtree(dir)
        shutil.rmtree(dir2)

    request.addfinalizer(del_dir)


@pytest.fixture()
def create_dirs_target(request):
    dir = "existing_subfolder"
    subdir = "subdir"
    dir2 = "existing_subfolder2"
    file = "file.txt"

    os.mkdir(dir)
    os.mkdir(os.path.join(dir, subdir))
    os.mkdir(dir2)
    open(os.path.join(dir, file), 'a').close()

    def del_dir():
        shutil.rmtree(dir)
        shutil.rmtree(dir2)

    request.addfinalizer(del_dir)


def test_get_containing_folder_unknown(create_dirs_target):
    path = "existing_subfolder/subdir"
    assert get_containing_folder(path) == "subdir"


def test_copy_path_dir(create_dirs_target):
    paths = ("existing_subfolder", "existing_subfolder2")
    target = "target_dir"
    copy_paths_to_target(paths, target)
    target_content = [f for f in glob.glob(target + "/**/", recursive=True)]
    shutil.rmtree(target)
    assert "target_dir/existing_subfolder/" in target_content
    assert "target_dir/existing_subfolder/subdir/" in target_content
    assert "target_dir/existing_subfolder2/" in target_content


def test_copy_path_dir_subpath(create_dirs_target):
    paths = ("existing_subfolder/subdir",)
    target = "target_dir"
    copy_paths_to_target(paths, target)
    target_content = [f for f in glob.glob(target + "/**/", recursive=True)]
    shutil.rmtree(target)
    assert "target_dir/existing_subfolder/" not in target_content
    assert "target_dir/subdir/" in target_content


def test_copy_path_files(create_dirs_target):
    paths = ("existing_subfolder", "existing_subfolder2")
    target = "target_dir"
    copy_paths_to_target(paths, target)
    target_content = [f for f in glob.glob(target + "/**/*", recursive=True)]
    shutil.rmtree(target)
    assert "target_dir/existing_subfolder/file.txt" in target_content


def test_check_several_paths_false(create_dir):
    dir = "existing_subfolder"
    paths = (dir, "non_existing_subfolder")

    result = check_path_params(paths)
    assert result is False


def test_check_several_paths_true(create_dir):
    dir = "existing_subfolder"
    dir2 = "existing_subfolder2"
    paths = (dir, dir2)
    result = check_path_params(paths)
    assert result is True


def test_check_1_path_true(create_dir):
    dir = "existing_subfolder"
    paths = ()
    result = check_path_params(paths)
    assert result is True


def test_check_1_path_false():
    dir = "non-existing_subfolder"
    paths = dir
    result = check_path_params(paths)
    assert result is False
