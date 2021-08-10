import asyncio
from aiopath import AsyncPath
from normalization import normalize
import os
import sys
import aioshutil
from time import time


async def creating_sorting_folders(path_new, name):
    path_new_folder = path_new / name
    if not await path_new_folder.exists():
        await path_new_folder.mkdir()
    return path_new_folder


async def creates_new_path_for_images(path_old, path_new):
    rename_stem = normalize(path_old.stem)

    return path_new / 'images' / (rename_stem + path_old.suffix), path_old


async def creates_new_path_for_video(path_old, path_new):
    rename_stem = normalize(path_old.stem)

    return path_new / 'video' / (rename_stem + path_old.suffix), path_old


async def creates_new_path_for_documents(path_old, path_new):
    rename_stem = normalize(path_old.stem)

    return path_new / 'documents' / (rename_stem + path_old.suffix), path_old


async def creates_new_path_for_audio(path_old, path_new):
    rename_stem = normalize(path_old.stem)

    return path_new / 'audio' / (rename_stem + path_old.suffix), path_old


async def creates_new_path_for_archives(path_old, path_new):
    unpacking_path = path_old.parent / path_old.stem
    await aioshutil.unpack_archive(path_old, unpacking_path)
    await path_old.unlink()

    return path_new / 'archives' / path_old.stem, unpacking_path


async def creates_new_path_for_others(path_old, path_new):

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


async def sorting_files(path_old, path_new):
    creator_new_path = get_path_handler(path_old.suffix)
    new_path, old_path = await creator_new_path(path_old, path_new)

    # I had to add this check because when moving a folder (unzipped archive) (using the - replace () method),
    # if the path where it was moved already exists, the error "PermissionError: [WinError 5] Access Denied:" is thrown
    if await old_path.is_dir():
        await new_path.mkdir(exist_ok=True)
        async for el in old_path.iterdir():
            await el.replace(new_path / el.name)
        if not os.listdir(old_path):
            await old_path.rmdir()

    else:
        await old_path.replace(new_path)


async def folder_processing(path_old, path_new, sorting_folders):
    if await path_old.is_dir() and path_old not in sorting_folders:
        async for path in path_old.iterdir():
            await folder_processing(path, path_new, sorting_folders)

        if not os.listdir(path_old):
            await path_old.rmdir()

    elif await path_old.is_file():
        await sorting_files(path_old, path_new)


async def main():
    path_old = AsyncPath(sys.argv[1])
    path_new = AsyncPath(input('\nEnter the path (on the same drive) where the sorted files will be saved: ').strip())

    if not await path_new.exists():
        await path_new.mkdir()

    if await path_old.exists():
        started = time()

        sorting_folders = await asyncio.gather(*(creating_sorting_folders(path_new, name) for name in FORMATS))
        await folder_processing(path_old, path_new, sorting_folders)

        elapsed = time() - started
        print('Lead time:', round(elapsed, 3), 's')

    else:
        print(f'The path {path_old} does not exist.')


if __name__ == '__main__':
    asyncio.run(main())


# Tread
# Lead time: 1.801 s
# Lead time: 3.042 s
# Lead time: 2.997 s
# Lead time: 2.794 s

# asyncio
# Lead time: 3.188 s
# Lead time: 3.779 s