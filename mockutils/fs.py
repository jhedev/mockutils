import os


class VirtualFile(object):
    def __init__(self, name, content=None):
        self.name = name
        self.content = content

    def __str__(self):
        return self.name

class VirtualDir(object):
    def __init__(self, name, content={}):
        self.name = name
        self.content = content

    def __str__(self):
        res = "{}/\n".format(self.name)
        for c in self.content:
            res += '\t{}'.format(str(c))
        return res

class VirtualFS(object):
    def __init__(self, content={}):
        self.root = VirtualDir('/', content=content)
        self.cwd = self.root.name

    def __str__(self):
        return str(self.root)

    @staticmethod
    def isdir_obj(obj):
        if type(obj) is VirtualDir:
            return True
        else:
            return False

    @staticmethod
    def isfile_obj(obj):
        if type(obj) is VirtualDir:
            return True
        else:
            return False

    def absolute_path(self, path):
        if path.startswith('/'):
            return os.path.normpath(path)
        else:
            return os.path.normpath(os.path.join(self.cwd, path))


    def resolve_path(self, path):
        path_components = list(filter(bool,
                                      self.absolute_path(path).split('/')))
        current_file = self.root
        for p in path_components:
            if p in current_file.content:
                current_file = current_file.content[p]
            else:
                raise FileNotFoundError
        return current_file

    def get_content(self, path):
        fs_object = self.resolve_path(path)
        if fs_object.content is not None:
            return list(fs_object.content.keys())

    def exists(self, path):
        try:
            f = self.resolve_path(path)
        except FileNotFoundError:
            return False
        return True

    def chdir(self, path):
        if self.exists(path):
            self.cwd = self.absolute_path(path)
        else:
            raise FileNotFoundError

    def isdir(self, path):
        resolved = self.resolve_path(path)
        return VirtualFS.isdir_obj(resolved)


class MockOS(object):
    def __init__(self, filesystem):
        self.fs = filesystem
        self.path = _MockOSPath(filesystem)

    def listdir(self, path='.'):
        return self.fs.get_content(path)

    def getcwd(self):
        return self.fs.cwd

    def chdir(self, path):
        self.fs.chdir(path)


class _MockOSPath(object):
    def __init__(self, filesystem):
        self.fs = filesystem

    def isdir(self, path):
        return self.fs.isdir(path)

    def exists(self, path):
        return self.fs.exists(path)
