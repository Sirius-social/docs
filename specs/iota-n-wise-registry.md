# IOTA n-wise registry

This document describes a method of implementing a registry of n-wise states using the [IOTA Ledger](https://www.iota.org/).

Version 1.0

ledgerType: "iota@1.0",

## N-wise registry creation

To create a new n-wise, creator writes the following message to the IOTA tangle
 
 ```json
{
    "transaction": {
        "type": "genesisTx",
        "label": "Council",
        "creatorNickName": "Alice",
        "creatorDid": "did:alice",
        "creatorDidDoc": {
            ...
            "publicKey": [
                {
                    "id": "1",
                    "type": "Ed25519VerificationKey2018",
                    "controller": "did",
                    "publicKeyBase58": "verkey"
                }
            ]
        },
        "ledgerType": "iota@1.0",
        "metaInfo" {

        }
        "proof" {
            "type": "JcsEd25519Signature2020",
            "verificationMethod": "did:alice#key1",
            "signatureValue": "..."
            }
    }
}
 ```

 ## Tag

All messages added to the IOTA Tangle are indexed by the tag. The tag is computed from the creator's verkey, defined in genesisTx. The procedure is presented in [IOTA DID Method](https://wiki.iota.org/identity.rs/specs/did/iota_did_method_spec#iota-tag). All further transactions are also indexed by this tag.

## Commit transaction

The commit of a new transaction to the n-wise registry is carried out by adding a message in the following format to the IOTA Tangle

 ```json
{
    "transaction": {
        "type": "...",
        ...
        "proof" {
            ...
        }
    }
    "meta" {
        "previousMessageId": "..."
    }
}
 ```

 - `previousMessageId` (required for all transactions, except GenesisTx): IOTA MessageId for the previous transaction.

## Transactions execution

N-wise party receives a list of n-wise transactions by the tag.
The order of transactions and resolution of collisions is carried out following [IOTA DID Method](https://wiki.iota.org/identity.rs/specs/did/iota_did_method_spec).

## Implementations

[Sirius SDK-Java](https://github.com/Sirius-social/sirius-sdk-java/blob/master/src/test/java/TestNWise.java)