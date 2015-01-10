import unittest
import mockutils.fs as fs


class VirtualFileTest(unittest.TestCase):

    def test_simple_file(self):
        file1 = fs.VirtualFile('file1name')
        self.assertEqual(file1.name, 'file1name')
        self.assertEqual(file1.content, None)

    def test_additional_file(self):
        file2 = fs.VirtualFile('file2name', "content")
        self.assertEqual(file2.name, 'file2name')
        self.assertEqual(file2.content, 'content')

class VirtualDirTest(unittest.TestCase):

    def test_simple_dir(self):
        dir1 = fs.VirtualDir('dirname')
        self.assertEqual(dir1.name, 'dirname')
        self.assertEqual(dir1.content, {})

    def test_additional_dir(self):
        files = {'file': fs.VirtualFile('file')}
        dir2 = fs.VirtualDir('dir2name', files)
        self.assertEqual(dir2.name, 'dir2name')
        self.assertEqual(dir2.content['file'], files['file'])

class VirtualFSTest(unittest.TestCase):

    def setUp(self):
        self.file1 = fs.VirtualFile('file1')
        self.fs1 = fs.VirtualFS({'file1': self.file1})

    def test_simple_absolute_path(self):
        self.assertEqual(self.fs1.absolute_path('/a/b/c'), '/a/b/c')
        self.assertEqual(self.fs1.absolute_path('a/b/c'), '/a/b/c')

    def test_absolute_path_with_dot(self):
        self.assertEqual(self.fs1.absolute_path('./b/c'), '/b/c')
        self.assertEqual(self.fs1.absolute_path('./b/./c'), '/b/c')

    def test_absolute_path_with_dots(self):
        self.assertEqual(self.fs1.absolute_path('..'), '/')
        self.assertEqual(self.fs1.absolute_path('../..'), '/')
        self.assertEqual(self.fs1.absolute_path('./a/..'), '/')
        self.assertEqual(self.fs1.absolute_path('./a/b/..'), '/a')

    def test_resolve_path(self):
        self.assertEqual(self.fs1.resolve_path('file1'), self.file1)
        with self.assertRaises(FileNotFoundError):
            self.fs1.resolve_path('file2')

    def test_get_contents(self):
        self.assertEqual(self.fs1.get_content('/'), ['file1'])
        self.assertEqual(self.fs1.get_content('/file1'), None)

    def test_exists(self):
        self.assertTrue(self.fs1.exists('/'))
        self.assertTrue(self.fs1.exists('/file1'))
        self.assertTrue(self.fs1.exists('file1'))
        self.assertFalse(self.fs1.exists('/file2'))
        self.assertFalse(self.fs1.exists('file2'))

    def test_chdir(self):
        pass

    def test_isdir(self):
        self.assertTrue(self.fs1.isdir('/'))


class MockOSTest(unittest.TestCase):

    def setUp(self):
        self.file1 = fs.VirtualFile('file1')
        self.fs1 = fs.VirtualFS({'file1': self.file1})
        self.os = fs.MockOS(self.fs1)

    def test_listdir(self):
        self.assertEqual(self.os.listdir(), ['file1'])
        with self.assertRaises(FileNotFoundError):
            self.os.listdir('dir1')

    def test_getcwd(self):
        self.assertEqual(self.os.getcwd(), '/')

    def test_chdir(self):
        pass

    def test_path_isdir(self):
        self.assertTrue(self.os.path.isdir('/'))
