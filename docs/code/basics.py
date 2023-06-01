%xmode minimal
import copy
import datetime
import decimal
import io
from autobean_refactor import models, parser, printer

p = parser.Parser()


def _print_model(model: models.RawModel) -> None:
    print(printer.print_model(model, io.StringIO()).getvalue())
