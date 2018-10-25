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


def rename_subpaths(parent_dir, flt, rule, abs_path=True, force=False):
    """
    renames certain subdirs to a new path with specific rules
    :param parent_dir: str, parent dir which contains all dirs to be renamed
    :param flt: callable or None, filter for files to be renamed, should be str -> bool
    :param rule: callable, rule for renaming each subpath, should be str -> str
    :param abs_path: bool, indicates whether `rule` and `flt` accept and return absolute paths, default=True
    :param force: bool, force rename in case of a conflict if True, default=False
    :return: None
    """

    subdirs = os.listdir(parent_dir)
    if abs_path:
        subdirs = [os.path.join(parent_dir, subdir) for subdir in subdirs]
    for subdir in filter(flt, subdirs):
        rename_path(subdir, rule, force)


if __name__ == '__main__':
    rename_subpaths("foo", lambda s: '2' in s.split("/")[-1], lambda s: s.replace("foo", "bar").replace("2", "5"))
