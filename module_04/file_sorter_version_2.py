from concurrent.futures import ThreadPoolExecutor
from normalization import normalize
import os
from pathlib import Path
import sys
import shutil
from time import time
from threading import Thread, RLock, enumerate


def creating_sorting_folders(path_new):
    sorting_folders = []

    for name in FORMATS:
        path_new_folder = path_new / name
        sorting_folders.append(path_new_folder)
        path_new_folder.mkdir()

    return sorting_folders


def creates_new_path_for_images(path_old, path_new):
    rename_stem = normalize(path_old.stem)

    return path_new / 'images' / (rename_stem + path_old.suffix), path_old


def creates_new_path_for_video(path_old, path_new):
    rename_stem = normalize(path_old.stem)

    return path_new / 'video' / (rename_stem + path_old.suffix), path_old


def creates_new_path_for_documents(path_old, path_new):
    rename_stem = normalize(path_old.stem)

    return path_new / 'documents' / (rename_stem + path_old.suffix), path_old


def creates_new_path_for_audio(path_old, path_new):
    rename_stem = normalize(path_old.stem)

    return path_new / 'audio' / (rename_stem + path_old.suffix), path_old


def creates_new_path_for_archives(path_old, path_new):
    unpacking_path = path_old.parent / path_old.stem
    shutil.unpack_archive(path_old, unpacking_path)
    path_old.unlink()

    return path_new / 'archives' / path_old.stem, unpacking_path


def creates_new_path_for_others(path_old, path_new):

    return path_new / 'others' / path_old.name, path_old


FORMATS = {
    'images':
        [['.jpeg', '.png', '.jpg', '.svg', '.psd'], creates_new_path_for_images],
    'video':
        [['.avi', '.mp4', '.mov', '.mkv'], creates_new_path_for_video],
    'documents':
        [['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx', '.xls'], creates_new_path_for_documents],
    'audio':
        [['.mp3', '.ogg', '.wav', '.amr'], creates_new_path_for_audio],
    'archives':
        [['.zip', '.tar', '.bztar', '.gztar', '.xztar', '.gz'], creates_new_path_for_archives],
    'others':
        [[], creates_new_path_for_others]
    }


def get_path_handler(extension):
    # returns the signature of the function that creates the new path
    for k, v in FORMATS.items():
        if extension in v[0]:
            return FORMATS.get(k)[1]

    return creates_new_path_for_others


def sorting_files(path_old, path_new, lock):
    new_path, old_path = get_path_handler(path_old.suffix)(path_old, path_new)

    # I had to add this check because when moving a folder (unzipped archive) (using the - replace () method),
    # if the path where it was moved already exists, the error "PermissionError: [WinError 5] Access Denied:" is thrown
    if old_path.is_dir():
        lock.acquire()
        new_path.mkdir(exist_ok=True)
        lock.release()
        for el in old_path.iterdir():
            lock.acquire()
            el.replace(new_path / el.name)
            lock.release()
        if not os.listdir(old_path):
            old_path.rmdir()

    else:
        lock.acquire()
        old_path.replace(new_path)
        lock.release()


def folder_processing(path_old, path_new, lock, sorting_folders):

    threads = []

    for i in path_old.iterdir():
        t = Thread(target=path_processing, args=(i, path_new, lock, sorting_folders))
        threads.append(t)

    [thread.start() for thread in threads]

    while threads:
        a = threads.pop()
        a.join()

    # folder_contents = list(path_old.iterdir())
    # paths_new = [path_new for i in range(len(folder_contents))]
    # locks = [lock for i in range(len(folder_contents))]
    # sorting_folders = [sorting_folders for i in range(len(folder_contents))]
    #
    # with ThreadPoolExecutor(max_workers=25) as executor:
    #     executor.map(path_processing, folder_contents, paths_new, locks, sorting_folders)

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


# Lead time: 1.801 s
# Lead time: 3.042 s
# Lead time: 2.997 s
# Lead time: 2.794 s