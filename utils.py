from os import path, walk


def files_to_watch(extra_dirs=["./static"]):
    """What files we want to watch

    Args:
        extra_dirs (list, optional): Files to watch. Defaults to ["./static"].

    Returns:
        [list]: files to watch
    """
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)

    return extra_files
