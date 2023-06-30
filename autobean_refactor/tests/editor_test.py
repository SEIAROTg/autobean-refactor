import os
import pathlib
import tempfile
from typing import Iterator
import pytest
from autobean_refactor import editor as editor_lib
from autobean_refactor import models

_FILES_FOO = {
    'index.bean': '''\
plugin "foo"
include "2020/index.bean"
include "2021/index.bean"
''',
    '2020/index.bean': '''\
include "*.bean"
2020-01-01 *
''',
    '2020/02.bean': '''\
2020-02-01 *
''',
    '2020/03/01.bean': '''\
2020-03-01 *
''',
    '2021/index.bean': '''\
include "**/*.bean"
2021-01-01 *
''',
    '2021/02.bean': '''\
2021-02-01 *
''',
    '2021/03/01.bean': '''\
2021-03-01 *
include "../index.bean"
''',
}


@pytest.fixture()
def testdir() -> Iterator[pathlib.PurePath]:
    with tempfile.TemporaryDirectory() as tmpdir:
        for filename, content in _FILES_FOO.items():
            path = os.path.join(tmpdir, filename)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
        yield pathlib.PurePath(tmpdir)


@pytest.fixture(scope='module')
def editor() -> editor_lib.Editor:
    return editor_lib.Editor()


class TestEditor:

    @pytest.fixture(autouse=True)
    def editor(self, editor: editor_lib.Editor) -> None:
        self._editor = editor

    def test_read_file(self, testdir: pathlib.PurePath) -> None:
        path = testdir / 'index.bean'
        mtime = os.stat(path).st_mtime_ns
        with self._editor.edit_file(path) as file:
            assert len(file.raw_directives) == 3
        assert os.stat(path).st_mtime_ns == mtime

    def test_edit_file(self, testdir: pathlib.PurePath) -> None:
        path = testdir / 'index.bean'
        mtime = os.stat(path).st_mtime_ns
        with self._editor.edit_file(path) as file:
            assert len(file.raw_directives) == 3
            file.directives.pop(0)
        assert os.stat(path).st_mtime_ns > mtime
        with open(path) as f:
            assert f.read() == '''\
include "2020/index.bean"
include "2021/index.bean"
'''

    def test_read_file_recursive(self, testdir: pathlib.PurePath) -> None:
        expected_paths = {
            'index.bean': 3,
            '2020/index.bean': 2,
            '2020/02.bean': 1,
            # '2020/03/01.bean': 1,  # '*' doesn't match children directories
            '2021/index.bean': 2,
            '2021/02.bean': 1,
            '2021/03/01.bean': 2,
        }
        mtimes = {
            p: os.stat(testdir / p).st_mtime_ns
            for p in expected_paths
        }
        path = testdir / 'index.bean'
        with self._editor.edit_file_recursive(path) as files:
            assert {
                p: len(f.directives)
                for p, f in files.items()
            } == {
                str(testdir / p): n
                for p, n in expected_paths.items()
            }
            files[str(testdir / '2020/02.bean')].raw_directives_with_comments.append(
                models.BlockComment.from_value('updated'))
            files.pop(str(testdir / '2021/02.bean'))

        for p in expected_paths:
            if p == '2021/02.bean':
                assert not os.path.exists(testdir / p)
                continue
            mtime = os.stat(testdir / p).st_mtime_ns
            with open(testdir / p) as f:
                updated_text = f.read()
            if p == '2020/02.bean':
                assert mtime > mtimes[p]
                assert updated_text == '2020-02-01 *\n\n; updated\n'
            else:
                print(mtimes)
                assert mtime == mtimes[p]
                assert updated_text == _FILES_FOO[p]
