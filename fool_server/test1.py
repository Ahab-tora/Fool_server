from watchfiles import watch
from data import global_variables
# Directory to monitor (Change this to your desired path)
directory_to_watch = "C:\\Users\\laure\\OneDrive\\Bureau\\sauvegarde1"  # Windows
# directory_to_watch = "/path/to/your/folder"  # macOS/Linux

import asyncio,os
from watchfiles import awatch



async def updatesWatcher(queue,path:str):
    async for changes in awatch(path):
        for event,file_path in changes:
            if not os.path.isdir(file_path):
                continue
            print(f"Change detected on {file_path}")
            await queue.put(file_path)

async def test(queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(item)


async def main(path):
    queue = asyncio.Queue()
    await asyncio.gather(updatesWatcher(queue=queue,path=path), test(queue=queue))

asyncio.run(main('\\\\Storage\\esma\\3D4\\threeLittlePigs'))  # Change path accordingly



