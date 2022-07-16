from autobean_refactor import token_store as token_store_lib
from . import base
from . import asterisk
from . import flag
from . import internal


@base.tree_model
class PostingFlag(base.RawTreeModel):
    RULE = 'posting_flag'

    def __init__(
            self,
            token_store: token_store_lib.TokenStore,
            flag: flag.Flag | asterisk.Asterisk,
    ):
        super().__init__(token_store)
        self.raw_flag = flag

    @property
    def first_token(self) -> token_store_lib.Token:
        return self.raw_flag

    @property
    def last_token(self) -> token_store_lib.Token:
        return self.raw_flag

    @internal.required_token_property
    def raw_flag(self) -> flag.Flag | asterisk.Asterisk:
        pass
