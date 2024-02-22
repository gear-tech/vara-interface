import typing as tp

from logging import getLogger

from .base import BaseClass
from ..exceptions import DigitalTwinMapException
from ..types import ProgramTyping
from ..utils import dt_encode_topic

logger = getLogger(__name__)


class Program(BaseClass):
    """
    Class for interacting with `Programs`_..
    """

    @staticmethod
    def _process_topic(topic: str) -> str:
        """
        Hash topic to a certain length if it doesn't meet topic format requirements.

        :param topic: Topic name to process.

        :return: Processed topic name

        """

        try:
            int(topic, 16)
            if len(topic) == 66:
                return topic
            else:
                return dt_encode_topic(topic)
        except ValueError:
            return dt_encode_topic(topic)

    def get_info(self, p_id: str, block_hash: tp.Optional[str] = None) -> tp.Optional[ProgramTyping]:
        """
        Fetch information about existing program.

        :param p_id: Program object ID.
        :param block_hash: Retrieves data as of passed block hash.

        :return: List of Program associated mapping. ``None`` if no Program with such id.

        """
        logger.info(f"Fetching info about Program with ID {p_id}")

        return self._service_functions.chainstate_query("gearProgram", "ProgramStorage", p_id, block_hash=block_hash)

    def create(self, nonce: tp.Optional[int] = None) -> tp.Tuple[int, str]:
        """
        Create a new digital twin.

        :param nonce: Account nonce. Due to the feature of substrate-interface lib, to create an extrinsic with
            incremented nonce, pass account's current nonce. See
            https://github.com/polkascan/py-substrate-interface/blob/85a52b1c8f22e81277907f82d807210747c6c583/substrateinterface/base.py#L1535
            for example.

        :return: Tuple of newly created Digital Twin ID and hash of the creation transaction.

        """

        tr_hash: str = self._service_functions.extrinsic("DigitalTwin", "create", nonce=nonce)
        dt_total: int = self.get_total()
        dt_id: int = dt_total
        for ids in reversed(range(dt_total)):
            if self.get_owner(ids) == self.account.get_address():
                dt_id: int = ids
                break

        return dt_id, tr_hash

    def set_source(self, dt_id: int, topic: str, source: str, nonce: tp.Optional[int] = None) -> tp.Tuple[str, str]:
        """
        Set DT topics and their sources. Since ``topic_name`` is byte encoded and then sha256-hashed, it's considered as
        good practice saving the map of digital twin in human-readable format in the very first DT topic. Still there is
        a ``get_source`` function which transforms given string to the format as saved in the chain for comparing.

        :param dt_id: Digital Twin ID, which should have been created by account, calling this function.
        :param topic: Topic to add. Any string you want. It will be sha256 hashed and stored in blockchain.
        :param source: Source address in ss58 format.
        :param nonce: Account nonce. Due to the feature of substrate-interface lib, to create an extrinsic with
            incremented nonce, pass account's current nonce. See
            https://github.com/polkascan/py-substrate-interface/blob/85a52b1c8f22e81277907f82d807210747c6c583/substrateinterface/base.py#L1535
            for example.

        :return: Tuple of hashed topic and transaction hash.

        """

        topic_hashed = self._process_topic(topic)
        return (
            topic_hashed,
            self._service_functions.extrinsic(
                "DigitalTwin", "set_source", {"id": dt_id, "topic": topic_hashed, "source": source}, nonce=nonce
            ),
        )
