import sirius_sdk
import asyncio
from helpers import *


async def run():
    client_agent_params = await get_agent_params("agent2")

    # Работаем от имени клиента
    async with sirius_sdk.context(**client_agent_params):
        # Данный вызов создает новый DID и сохраняет его в Wallet
        agent_did, agent_verkey = await sirius_sdk.DID.create_and_store_my_did()
        print(agent_did)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run())