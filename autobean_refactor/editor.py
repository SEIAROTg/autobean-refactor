import collections
import contextlib
import glob
import io
import os.path
import pathlib
from typing import Iterator, Optional
from autobean_refactor import parser as parser_lib, models, printer


def _get_include_paths(path: str, file: models.File) -> Iterator[str]:
    for directive in file.raw_directives:
        if not isinstance(directive, models.Include):
            continue
        matches = glob.glob(os.path.join(os.path.dirname(path), directive.filename), recursive=True)
        if not matches:
            lineno = directive.token_store.get_position(directive.first_token).line
            raise ValueError(f'No files match {directive.filename!r} ({path}:{lineno})')
        for match in matches:
            yield os.path.normpath(match)


class Editor:

    def __init__(self, parser: Optional[parser_lib.Parser] = None) -> None:
        self._parser = parser or parser_lib.Parser()

    @contextlib.contextmanager
    def edit_file(self, path: os.PathLike) -> Iterator[models.File]:
        p = pathlib.Path(path)
        text = p.read_text()
        file = self._parser.parse(text, models.File)

        yield file

        updated_text = printer.print_model(file, io.StringIO()).getvalue()
        if updated_text != text:
            p.write_text(updated_text)

    @contextlib.contextmanager
    def edit_file_recursive(self, path: os.PathLike) -> Iterator[dict[str, models.File]]:
        texts = dict[str, str]()
        files = dict[str, models.File]()
        queue = collections.deque([os.path.normpath(path)])

        while queue:
            current_path = queue.popleft()
            if current_path in texts:
                continue
            with open(current_path) as f:
                texts[current_path] = f.read()
            files[current_path] = self._parser.parse(texts[current_path], models.File)
            queue.extend(_get_include_paths(current_path, files[current_path]))

        yield files

        for current_path in set(texts) - set(files):
            os.unlink(current_path)
        for current_path, file in files.items():
            os.makedirs(os.path.dirname(current_path), exist_ok=True)
            updated_text = printer.print_model(file, io.StringIO()).getvalue()
            if updated_text != texts.get(current_path):
                with open(current_path, 'w') as f:
                    f.write(updated_text)
