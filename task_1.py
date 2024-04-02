import argparse
import logging
from pathlib import Path
from shutil import copyfile
from threading import Thread

parser = argparse.ArgumentParser(description="Sorting folders.")
parser.add_argument("--source", "-s", required=True)
parser.add_argument("--output", "-o", default="dist")

args = vars(parser.parse_args())

source = Path(args.get("source"))
output = Path(args.get("output"))

files_dict = {}


def group_files_by_extension(source_folder: Path):
    for el in source_folder.iterdir():
        if el.is_dir():
            group_files_by_extension(el)
        else:
            extension = el.suffix[1:]

            if extension not in files_dict.keys():
                files_dict[extension] = [el]
            else:
                files_dict[extension].append(el)


def copy_files(extension: str):
    extension_folder = output / extension
    extension_folder.mkdir(exist_ok=True, parents=True)

    for el in files_dict[extension]:
        try:
            copyfile(el, extension_folder / el.name)
        except Exception as e:
            logging.error(e)


if __name__ == "__main__":
    group_files_by_extension(source)

    threads = []

    for key in files_dict.keys():
        thread = Thread(target=copy_files, args=(key,))
        thread.start()
        threads.append(thread)

    [th.join() for th in threads]
