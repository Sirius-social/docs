# Выдача и получение проверяемых учетных данных
IndiLynx SDK позволяет выдавать и получать проверяемые учетные данные в соответствии с протоколом
[0036-issue-credential](https://github.com/hyperledger/aries-rfcs/tree/main/features/0036-issue-credential).

В процессе выдачи проверяемых учетных данных участвуют две стороны: Issuer и Holder. Issuer выдает VC, выпущенный
в соответствии с ранее созданной схемой и Credential Definition и подписанный его цифровой подписью. Holder сохраняет
данный VC в своем защищенном кошельке.

IndiLynx SDK инкапсулирует всю внутреннюю логику протокола [0036-issue-credential](https://github.com/hyperledger/aries-rfcs/tree/main/features/0036-issue-credential)
в двух конечных автоматах: Issuer и Holder.

Предполагается, что между Issuer и Holder установлено доверенное соединение.

Выдача VC со стороны ПО Issuer-а выглядит следующим образом: 
```python
# Подключаемся к агенту Issuer-а и работаем от его имени
async with sirius_sdk.context(**ISSUER):
    # Создаем конечный автомат для выдачи VC
    issuer_machine = sirius_sdk.aries_rfc.Issuer(holder=holder_pairwise)
    
    # Заполняем поля схемы данными
    values = {
        'first_name': 'Mike',
        'last_name': 'L.', 
        'birthday': '17.03.1993'
    }

    # Запускаем процедуру выдачи VC
    ok = await issuer_machine.issue(
        values=values,
        schema=schema,
        cred_def=cred_def,
        comment="Here is your document",
        locale="en"
    )
```

Для агента Holder-а процедура получения VC выглядит так же просто:
```python
# Работаем от лица агента Holder-а
async with sirius_sdk.context(**HOLDER):
    holder_machine = sirius_sdk.aries_rfc.Holder(pairwise)
    listener = await sirius_sdk.subscribe()
    async for event in listener:
        # Holder получает предложение получения VC (OfferCredentialMessage) от Issuer-а
        if isinstance(event['message'], OfferCredentialMessage):
            offer: OfferCredentialMessage = event.message
            # Holder запускает процесс получения VC. Результат записывается в его кошелек
            success, cred_id = await holder_machine.accept(
                offer=offer,
                master_secret_id=PROVER_SECRET_ID
            )
```