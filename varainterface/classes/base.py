import typing as tp

from logging import getLogger

from .account import Account
from .service_functions import ServiceFunctions

logger = getLogger(__name__)


class BaseClass:
    """
    Base class for different modules to initialize `service_functions` instance for further work.
    """

    def __init__(
        self,
        account: Account,
        wait_for_inclusion: bool = True,
        return_block_num: bool = False,
    ):
        """
        Assign Account dataclass parameters and create an empty interface attribute for a decorator.

        :param account: Account dataclass with seed, websocket address and node type_registry.
        :param wait_for_inclusion: Whether wait for a transaction to included in block. You will get the hash anyway.
        :param return_block_num: If set to True, any executed extrinsic function will return a tuple of form
            ``(<extrinsic_hash>, <block_number-idx>)``. ONLY WORKS WHEN ``wait_for_inclusion`` IS SET TO TRUE.

        """
        self.account: Account = account
        self._service_functions: ServiceFunctions = ServiceFunctions(
            account,
            wait_for_inclusion=wait_for_inclusion,
            return_block_num=return_block_num,
        )
