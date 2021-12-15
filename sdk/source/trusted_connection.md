## Установка доверенного соединения между агентами
IndiLynx SDK позволяет устанавливать защищенное соединение между двумя агентами в соответствии с протоколом 
[0160-connection-protocol](https://github.com/hyperledger/aries-rfcs/tree/main/features/0160-connection-protocol).

В процессе установки защищенного соединения участвуют две стороны: Inviter и Invitee. Inviter инициирует процесс установки
соединения путем выпуска приглашения (Invitation). Приглашение может быть публичным для неопределенного круга лиц или 
приватным и выпускаться для конкретного пользователя.

IndiLynx SDK инкапсулирует всю внутреннюю логику протокола
[0160-connection-protocol](https://github.com/hyperledger/aries-rfcs/tree/main/features/0160-connection-protocol) в двух
конечных автоматах: sirius_sdk.aries_rfc.Inviter и sirius_sdk.aries_rfc.Invitee.

Inviter создает приглашение на установку соединения:
```python
# Работаем от имени агента Inviter
async with sirius_sdk.context(**inviter_agent_params):
    connection_key = await sirius_sdk.Crypto.create_key()  # уникальный ключ соединения
    inviter_endpoint = [e for e in await sirius_sdk.endpoints() if e.routing_keys == []][0]
    invitation = Invitation(
        label='Inviter',
        endpoint=inviter_endpoint.address,  # URL адрес Inviter
        recipient_keys=[connection_key]
    )
```
Invitee получает от Invter-а приглашение по независимому каналу связи (например через qr-код):
```python
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
```

Установка соединения на стороне Inviter-а:
```python
# Работаем от имени Inviter
async with sirius_sdk.context(**inviter_agent_params):
    # Создадим новый приватный DID для соединений в рамках ранее созданного invitation
    my_did, my_verkey = await sirius_sdk.DID.create_and_store_my_did()
    me = sirius_sdk.Pairwise.Me(did=my_did, verkey=my_verkey)
    inviter_endpoint = [e for e in await sirius_sdk.endpoints() if e.routing_keys == []][0]
    # Создадим экземпляр автомата для установки соединения на стороне Inviter-а
    inviter_machine = Inviter(
        me=me,
        connection_key=connection_key,
        my_endpoint=inviter_endpoint,
        logger=Logger()
    )
    listener = await sirius_sdk.subscribe()
    # Ждем сообщение от Invitee
    async for event in listener:
        request = event['message']
        # Inviter получает ConnRequest от Invitee и проверяет, что он относится к ранее созданному приглашению
        if isinstance(request, ConnRequest) and event['recipient_verkey'] == connection_key:
            # запускаем процесс установки соединения
            ok, pairwise = await inviter_machine.create_connection(request)
```
Весь пример [доступен здесь](examples/python/establish_connection/main.py).

Результатом установки соединения у обеих сторон является объект Pairwise, который хранится в Wallet обеих сторон. 
Следует отметить, что установка соединения
в общем случае производится один раз и не зависит жизненного цикла агентов или внутренних сетевых соединений. Аналогом установки
соединения между агентами является обмен визитками или номерами телефонов, с той лишь разницей, что в рассматриваемом
случае уставленное соединение защищено современной криптографией и основано на технологии [DID](https://www.w3.org/TR/did-core/).