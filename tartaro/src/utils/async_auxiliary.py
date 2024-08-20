import asyncio
from typing import Dict, Coroutine
import nest_asyncio


application_loop = asyncio.get_event_loop()
nest_asyncio.apply(application_loop)


async def gather_dict_values(dictionary: Dict[str, Coroutine]):
    dictionary_values = await asyncio.gather(*dictionary.values())
    dictionary_keys = tuple(dictionary.keys())
    awaited_dict = {
        dictionary_keys[index]: dictionary_values[index]
        for index in range(len(dictionary_values))
    }
    return awaited_dict


def execute_coroutine(function: Coroutine):
    future = application_loop.run_until_complete(function)
    coroutine = asyncio.ensure_future(future, loop=application_loop)
    result = asyncio.run(coroutine)
    return result


__all__ = ["application_loop"]
