import sirius_sdk
import asyncio
from helpers import *


async def run():
    gov_did, _ = await sirius_sdk.DID.create_and_store_my_did(seed='000000000000000000000000Steward1')

    # Создаем схему
    schema_id, anon_schema = await sirius_sdk.AnonCreds.issuer_create_schema(
        issuer_did=gov_did,
        name='demo_passport',
        version='1.0',
        attrs=['first_name', 'last_name', 'birthday']
    )

    dkms = await sirius_sdk.ledger('default')
    # Регистрируем схему в реестре
    schema = await dkms.ensure_schema_exists(
        schema=anon_schema,
        submitter_did=gov_did
    )

    # Регистрируем credential definition
    ok, cred_def = await dkms.register_cred_def(
        cred_def=sirius_sdk.CredentialDefinition(tag='TAG', schema=schema),
        submitter_did=gov_did
    )

    print(ok)


if __name__ == '__main__':
    gov_agent_params = asyncio.get_event_loop().run_until_complete(get_agent_params("agent1"))
    # Устанавливаем глобальные параметры агента
    sirius_sdk.init(**gov_agent_params)
    asyncio.get_event_loop().run_until_complete(run())
