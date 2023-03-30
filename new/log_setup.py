import logging
from types import TracebackType
from typing import Callable, Mapping, Optional, Tuple, Type, Union

_SysExcInfoType = Tuple[Optional[Type[BaseException]], Optional[BaseException], Optional[TracebackType]]
_ExcInfoType = Union[None, bool, _SysExcInfoType, BaseException]

def get_log() -> Callable[[object, object, _ExcInfoType, bool, int, Optional[Mapping[str, object]]], None]:
    '''
    Sets up a logger and returns its debug method. Output will be formatted as '[%(filename)s:%(lineno)s] %(message)s'.

    Returns
    -------
    (object, object, _ExcInfoType, bool, int, (Mapping[str, object] | None)) -> None
        The debug method of the logger.
    '''
    logger = logging.getLogger(__name__)
    FORMAT = "[%(filename)s:%(lineno)s] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(logging.DEBUG)
    return logger.debug