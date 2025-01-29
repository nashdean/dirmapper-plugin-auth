from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from dirmapper_core.models.directory_structure import DirectoryStructure

class RepositoryManager(ABC):
    @abstractmethod
    def fetch_directory_structure(self, owner: str, repo: str, path: str = "") -> DirectoryStructure:
        pass

    @abstractmethod
    def get_repository_contents(self, owner: str, repo: str, path: str = "") -> Optional[List[Dict]]:
        pass
