from watchfiles import watch

# Directory to monitor (Change this to your desired path)
directory_to_watch = "C:\\Users\\laure\\OneDrive\\Bureau\\sauvegarde1"  # Windows
# directory_to_watch = "/path/to/your/folder"  # macOS/Linux

import asyncio,os
from watchfiles import awatch


async def updatesWatcher(path:str):
    async for changes in awatch(path):
        for event,file_path in changes:
            if not os.path.isdir(file_path):
                continue
            print(f"Change detected on {file_path}")

# Run the async watcher
asyncio.run(updatesWatcher(directory_to_watch))  # Change path accordingly