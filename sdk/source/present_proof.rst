Запрос и предоставление проверяемых учетных данных
==================================================

IndiLynx SDK позволяет запрашивать сведения и формировать
криптографические доказательства о проверяемых учетных данных владельца
в соответствии с протоколом
`0037-present-proof <https://github.com/hyperledger/aries-rfcs/tree/main/features/0037-present-proof>`__.
Важно отметить, что владелец учетных данных (Prover) передает не сами
учетные данные, а криптографические доказательства, подтверждающие факт
владения Prover-а указанными VC и содержащие только тот минимальный
объем информации, которую запросил Verifier. Вместе с самими данными
автоматически передается доказательство факта передачи этих данных от
Prover-а к Verifier-у.

В процессе выдачи проверяемых учетных данных участвуют две стороны:
Verifier и Prover.

IndiLynx SDK инкапсулирует всю внутреннюю логику протокола
`0037-present-proof <https://github.com/hyperledger/aries-rfcs/tree/main/features/0037-present-proof>`__
в двух конечных автоматах: Verifier и Prover.

Предполагается, что между Verifier и Prover установлено доверенное
соединение.

.. code:: python

   # Работаем от лица агента Verifier-а
   async with sirius_sdk.context(**VERIFIER):
       # Verifier указывает требуемые поля VC и требования к ним
       proof_request = {
           "name": "Demo Proof Request",
           "version": "0.1",
           "requested_attributes": {
               'attr1_referent': {
                   "name": "first_name",
                   "restrictions": {
                       "issuer_did": GOV_DID
                   }
               },
               'attr2_referent': {
                   "name": "last_name",
                   "restrictions": {
                       "issuer_did": GOV_DID
                   }
               },
               'attr3_referent': {
                   "name": "birthday",
                   "restrictions": {
                       "issuer_did": GOV_DID
                   }
               }
           },
           "nonce": await sirius_sdk.AnonCreds.generate_nonce()
       }
       # Подключение к инфраструктуре публичных ключей
       dkms = await sirius_sdk.ledger(network_name)
           verifier_machine = sirius_sdk.aries_rfc.Verifier(
               prover=prover_pairwise,
               ledger=dkms
           )
       # Запуск процесса верификации VC
       success = await verifier_machine.verify(proof_request)

.. code:: python

   # Работаем от лица агента Prover-а
   async with sirius_sdk.context(**PROVER):
   listener = await sirius_sdk.subscribe()
   async for event in listener:
       if isinstance(event.message, RequestPresentationMessage):
           proof_request: sirius_sdk.aries_rfc.RequestPresentationMessage = event.message
           holder_machine = sirius_sdk.aries_rfc.Prover(
               verifier=verifier,
               ledger=dkms
           )
           # Prover самостоятельно ищет в своем кошельке необходимые поля VC, формирует криптографическое доказательство
           # их корректности и направляет доказательство Verifier-у
           success = await holder_machine.prove(
               request=proof_request,
               master_secret_id=PROVER_SECRET_ID
           )
