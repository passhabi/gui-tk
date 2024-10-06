# import logging
import yara
import asyncio
from pathlib import Path
import psutil
import time
import sys
from typing import Union
import os
from colorama import Fore


# import threading
# from concurrent.futures import ThreadPoolExecutor


class YaraScanner:
    """Class for scanning files using Yara rules."""

    def __init__(self, directory:Union[str, Path], rule_path:Union[str, Path]):
        """
        Initialize YaraScanner with directory and rule path.
            directory: root directory to search over all files and sub directories.
            rule_path: str path to Yara rules.
        """
        self.directory = Path(directory)
        self.rule = yara.compile(filepath=str(rule_path), includes=False)
        
        # self.logger = logging.getLogger(__name__)

    
    async def scan_directory(self):
        """Scan files in the directory."""
        async with asyncio.TaskGroup() as tg:
            for file_path in self.directory.rglob("*"):
                if file_path.is_file():
                    tg.create_task(self.scan_file(file_path))
                
                    
    def start_scan(self):
        print(Fore.GREEN + f"Scanning {self.directory} ...", Fore.RESET)
        asyncio.run(self.scan_directory())


    async def scan_file(self, file_path):
        """Scan a specific file."""        
        # todo: use Semaphore?
        print(file_path)
        self.file_path = file_path
        try:
            result = self.rule.match(
                str(file_path),
                callback=self.find_match,
                which_callbacks=yara.CALLBACK_MATCHES,
            )
        
        except yara.Error:
            print(Fore.LIGHTRED_EX + f"Couldn't read the file {file_path},", Fore.RESET)


    def find_match(self, data):
        """Find a match in the scanned file."""
        print(Fore.RED + f"{data['rule']}: {self.file_path}", Fore.RESET)
        return yara.CALLBACK_CONTINUE


if __name__ == "__main__":
    
    directory = Path(os.path.expanduser("~")) / 'Desktop' / 'test'
    rule_path = Path("./rules.yar")

    scanner = YaraScanner(directory, rule_path)
    scanner.start_scan()