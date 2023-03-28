import os
import tempfile
from .. import base

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


class TestRecursiveParsing(base.BaseTestModel):

    def test_recursive_parsing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            for filename, content in _FILES_FOO.items():
                path = os.path.join(tmpdir, filename)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w') as f:
                    f.write(content)
            
            files = self.parser.parse_file_recursive(os.path.join(tmpdir, 'index.bean'))
            expected_paths = {
                'index.bean': 3,
                '2020/index.bean': 2,
                '2020/02.bean': 1,
                # '2020/03/01.bean': 1,  # '*' doesn't match children directories
                '2021/index.bean': 2,
                '2021/02.bean': 1,
                '2021/03/01.bean': 1,
            }
            actual_paths = {
                path: len(file.raw_directives)
                for path, file in files.items()
            }
            assert actual_paths == {
                os.path.join(tmpdir, path): count
                for path, count in expected_paths.items()
            }
