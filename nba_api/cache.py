import json
import os


class FileSystemCache:
    # TODO: Eventually support other storage formats
    ext = 'json'

    def __init__(self, root):
        """
        A FileSystemCache caches data in a local file system. It acts as a
        key-value store, mapping identifiers to file names.

        Result sets are saved and loaded via the file system.

        :param str root: Path to directory where data should be stored
        """
        # TODO: Consider subclassing dict instead directly
        self._known_paths = dict()
        self.root = os.path.normpath(root)

    def path(self, key):
        if key in self._known_paths:
            # Paths are cached, so return the known path for the given key
            return self._known_paths[key]
        else:
            # Compute the path for the given key and cache it
            path = os.path.normpath(f'{self.root}/{key}.{self.ext}')
            self._known_paths[key] = path
            return path

    def __contains__(self, key):
        return key in self._known_paths

    def __getitem__(self, key):
        # TODO: Potential read error should be handled
        with open(self.path(key), 'r') as data:
            return json.load(data)

    def __setitem__(self, key, results):
        path = self.path(key)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as fh:
            json.dump(results, fh)
