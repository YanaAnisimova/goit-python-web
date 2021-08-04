from concurrent.futures import ThreadPoolExecutor
from normalization import normalize
import os
from pathlib import Path
import sys
import shutil
from time import time
from threading import Thread, RLock, enumerate


FORMATS = {
    'images': ['.jpeg', '.png', '.jpg', '.svg', '.psd'],
    'video': ['.avi', '.mp4', '.mov', '.mkv'],
    'documents': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx', '.xls'],
    'audio': ['.mp3', '.ogg', '.wav', '.amr'],
    'archives': ['.zip', '.tar', '.bztar', '.gztar', '.xztar', '.gz'],
    'others': []
    }


def creating_sorting_folders(path_new):
    sorting_folders = []

    for name in FORMATS:
        path_new_folder = path_new / name
        sorting_folders.append(path_new_folder)
        if not path_new_folder.exists():
            path_new_folder.mkdir()

    return sorting_folders


def sorting_files(path_old, path_new, lock):

    rename_stem = normalize(path_old.stem)

    if path_old.suffix in FORMATS['archives']:

        new_path = path_new / 'archives' / path_old.stem
        lock.acquire()
        shutil.unpack_archive(path_old, new_path)
        lock.release()
        path_old.unlink()
        return None

    if path_old.suffix in FORMATS['images']:
        new_path = path_new / 'images' / (rename_stem + path_old.suffix)

    elif path_old.suffix in FORMATS['video']:
        new_path = path_new / 'video' / (rename_stem + path_old.suffix)

    elif path_old.suffix in FORMATS['documents']:
        new_path = path_new / 'documents' / (rename_stem + path_old.suffix)

    elif path_old.suffix in FORMATS['audio']:
        new_path = path_new / 'audio' / (rename_stem + path_old.suffix)

    else:
        new_path = path_new / 'others' / path_old.name

    lock.acquire()
    try:
        path_old.replace(new_path)
    except OSError as e:
        print(e)
    finally:
        lock.release()


def folder_processing(path_old, path_new, lock, sorting_folders):

    # threads = []
    #
    # for i in path_old.iterdir():
    #     t = Thread(target=path_processing, args=(i, path_new, lock, sorting_folders))
    #     t.start()
    #     threads.append(t)
    #
    # while threads:
    #     a = threads.pop()
    #     a.join()

    folder_contents = list(path_old.iterdir())
    paths_new = [path_new for i in range(len(folder_contents))]
    locks = [lock for i in range(len(folder_contents))]
    sorting_folders = [sorting_folders for i in range(len(folder_contents))]

    with ThreadPoolExecutor(max_workers=25) as executor:
        executor.map(path_processing, folder_contents, paths_new, locks, sorting_folders)

    if not os.listdir(path_old):
        path_old.rmdir()


def path_processing(path_old, path_new, lock, sorting_folders):

    if path_old.is_dir() and path_old not in sorting_folders:
        folder_processing(path_old, path_new, lock, sorting_folders)

    elif path_old.is_file():
        sorting_files(path_old, path_new, lock)


if __name__ == '__main__':

    path_old = Path(sys.argv[1])
    path_new = Path(input('\nEnter the path (on the same drive) where the sorted files will be saved: ').strip())

    if not path_new.exists():
        path_new.mkdir()

    if path_old.exists():

        started = time()
        sorting_folders = creating_sorting_folders(path_new)
        lock = RLock()

        path_processing(path_old, path_new, lock, sorting_folders)

        print('\nList of all Thread objects currently active:', enumerate())
        elapsed = time() - started
        print('Lead time:', round(elapsed, 3), 's')

    else:
        print(f'The path {path_old} does not exist.')

# Lead time: 1.264 s
# Lead time: 2.703 s
# Lead time: 1.41 s