import sirius_sdk
import asyncio
from helpers import *
from sirius_sdk.agent.aries_rfc.feature_0160_connection_protocol import *


async def run():
    invitee_agent_params = {
        'server_uri': 'https://demo.socialsirius.com',
        'credentials': 'BXXwMmUlw7MTtVWhcVvbSVWbC1GopGXDuo+oY3jHkP/4jN3eTlPDwSwJATJbzwuPAAaULe6HFEP5V57H6HWNqYL4YtzWCkW2w+H7fLgrfTLaBtnD7/P6c5TDbBvGucOV'.encode(),
        'p2p': sirius_sdk.P2PConnection(
            my_keys=('EzJKT2Q6Cw8pwy34xPa9m2qPCSvrMmCutaq1pPGBQNCn',
                     '273BEpAM8chzfMBDSZXKhRMPPoaPRWRDtdMmNoKLmJUU6jvm8Nu8caa7dEdcsvKpCTHmipieSsatR4aMb1E8hQAa'),
            their_verkey='342Bm3Eq9ruYfvHVtLxiBLLFj54Tq6p8Msggt7HiWxBt'
        )
    }

    invitation = Invitation(**{"@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/invitation",
                                "@id": "a989e882-5af6-48d0-8660-560567df767d",
                                "recipientKeys": ["4n8ri1UUbqQv3dEVzyaVR4hbdxzLDV5dVwownUpWpHps"],
                                "serviceEndpoint": "http://lab.cardea.indiciotech.io:3005", "label": "Lab"})

    async def invitee_routine():
        # Работаем от имени Invitee
        async with sirius_sdk.context(**invitee_agent_params):
            # Создадим новый приватный DID для соединения с Inviter-ом
            my_did, my_verkey = await sirius_sdk.DID.create_and_store_my_did()
            me = sirius_sdk.Pairwise.Me(did=my_did, verkey=my_verkey)
            # Создадим экземпляр автомата для установки соединения на стороне Invitee
            invitee_machine = Invitee(
                me=me,
                my_endpoint=[e for e in await sirius_sdk.endpoints() if e.routing_keys == []][0],
                logger=Logger()
            )

            # Запускаем процесс установки соединения
            ok, pairwise = await invitee_machine.create_connection(
                invitation=invitation,
                my_label='Invitee'
            )
            # Сохраняем соединение в Wallet
            await sirius_sdk.PairwiseList.ensure_exists(pairwise)

    async def invitee_routine2():
        async with sirius_sdk.context(**invitee_agent_params):
            listener = await sirius_sdk.subscribe()
            # Ждем сообщение от Invitee
            async for event in listener:
                print(event)

    await asyncio.wait([invitee_routine2(), invitee_routine()])


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run())
