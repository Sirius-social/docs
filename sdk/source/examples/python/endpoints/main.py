import sirius_sdk
import asyncio
from helpers import *


async def run():
    agent_params = await get_agent_params("agent1")

    # Работаем от имени agent1
    async with sirius_sdk.context(**agent_params):
        # получаем список адресов агента
        endpoints = await sirius_sdk.endpoints()
        for e in endpoints:
            print('address: {}; routing_keys: {}'.format(e.address, e.routing_keys))


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run())