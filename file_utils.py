import os
import shutil


def rename_path(src, rule, force=False):
    """
    renames src path to a new path with specific rules
    :param src: str, source path to be renamed
    :param rule: callable, should be a str -> str mapping
    :param force: bool, force rename in case of a conflict if True, default=False
    :return: None
    """

    dest = rule(src)
    if not force and os.path.exists(dest):
        raise FileExistsError("The destination file {} exists".format(dest))

    if force and os.path.isdir(dest):
        shutil.rmtree(dest)
        os.makedirs(dest, exist_ok=True)

    os.rename(src, rule(src))  # This line does force renaming


if __name__ == '__main__':
    rename_path("foo_dir", lambda s: "bar_dir/bar_subdir", force=True)
