import sirius_sdk
import asyncio
from helpers import *


async def run():
    # В данном примере участвуют два агента, один из которых является Steward (т.е. имеет право записи в реестр),
    steward_agent_params = await get_agent_params("agent1")
    # Второго агента назовем клиент
    client_agent_params = await get_agent_params("agent2")

    # Работаем от имени клиента
    async with sirius_sdk.context(**client_agent_params):
        # Клиентский агент создает новый DID и записывает его в свой кошелек
        agent_did, agent_verkey = await sirius_sdk.DID.create_and_store_my_did()
        print(agent_did)

    # Клиент по независимому каналу связи передает свой новый DID и verkey (публичный ключ, ассоциированый с DID) Steward-у,
    # чтобы он зарегистрировал его в реестре

    # Работаем от имени Steward-а
    async with sirius_sdk.context(**steward_agent_params):
        # Получаем DID первого агента, под которым он известен как Steward
        steward_did, _ = await sirius_sdk.DID.create_and_store_my_did(seed='000000000000000000000000Steward1')
        # работаем с реестром под именем default
        dkms = await sirius_sdk.ledger('default')
        # записываем DID клинета в реестр
        ok, resp = await dkms.write_nym(
            submitter_did=steward_did,
            target_did=agent_did,
            ver_key=agent_verkey
        )
        print(ok)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run())