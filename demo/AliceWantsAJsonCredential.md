
# How to Issue JSON-LD Credentials using Aca-py

Aca-py has the capability to issue and verify both Indy and JSON-LD (W3C compliant) credentials.

The JSON-LD support is documented [here](../JsonLdCredentials.md) - this document will provide some additional detail in how to use the demo and admin api to issue and prove JSON-LD credentials.


## Setup Agents to Issue JDON-LD Credentials

Clone this repository to a directory on your local:

```bash
git clone https://github.com/hyperledger/aries-cloudagent-python.git
cd aries-cloudagent-python/demo
```

Open up a second shell (so you have 2 shells open in the `demo` directory) and in each shell:

```bash
./run_demo faber --did-exchange`
```

```bash
./run_demo alice`
```

Note that you start the `faber` agent with AIP2.0 options.

Copy the "invitation" json text from the Faber shell and paste into the Alice shell to establish a connection between the two agents.

Using the Faber admin api, you have to create a DID with the appropriate:

- DID method ("key" or "sov")
- key type "ed25519" or "bls12381g2" (corresponding to signature types "Ed25519Signature2018" or "BbsBlsSignature2020")
- if you use DID method "sov" you must use key type "ed25519"

"did:sov" must be a public DID, but "did:key" is not

For example, call the `/wallet/did/create` endpoint with the following payload:

```
{
  "method": "key",
  "options": {
    "key_type": "bls12381g2" // or ed25519
  }
}
```

You do *not* create a schema or cred def for a JSON-LD credential (these are only required for "indy" credentials).

Congradulations, you are now in a position to start issuing JSON-LD credentials!

- You have two agents with a connection established betwee the agents - you will need to copy Faber's connection_id into the examples below.
- You have created a (non-public) DID for Faber to use to sign/issue the credentials - you will need to copy the DID that you created above into the examples below.

To issue a credential, use the `/issue-credential-2.0/send` (or `/issue-credential-2.0/create-offer`) endpoint, you can test with this example payload (just replace the "connection_id", "issuer" key and "proofType" with appropriate values:

```
{
  "connection_id": "31f1948f-aaf9-4f92-9962-47dca61256e4",
  "filter": {
    "ld_proof": {
      "credential": {
        "@context": [
          "https://www.w3.org/2018/credentials/v1",
          "https://www.w3.org/2018/credentials/examples/v1"
        ],
        "type": ["VerifiableCredential", "UniversityDegreeCredential"],
        "issuer": "did:key:zUC77Ndp6jMNNmmpgkJFZkW2YFkjcav5rBEJJTN872Lq3Lg2RT969gXi1uEwCbbWm8ct5xZJjWMHLzjs1kkogRKwbezCQ89ufRY74aEK7AhqFMeY1j1kqoGfRGmiZQoyXwUmk62",
        "issuanceDate": "2020-01-01T12:00:00Z",
        "credentialSubject": {
          "givenName": "Sally",
          "familyName": "Student",
          "degree": {
            "type": "BachelorDegree",
            "degreeType": "Undergraduate",
            "name": "Bachelor of Science and Arts"
          },
          "college": "Faber College"
        }
      },
      "options": {
        "proofType": "BbsBlsSignature2020"
      }
    }
  }
}
```

Note that if you have the "auto" settings on, this is all you need to do.  Otherwise you need to call the "send-request", "store", etc endpoints to complete the protocol.

To see the issued credential, call the `/credentials/w3c` endpoint on Alice's admin api.


## Building More Realistic JSON-LD Credentials

The above example uses the "https://www.w3.org/2018/credentials/examples/v1" context, which should not be used in a real application.

To build real-life credentials, determine which attributes you need and then include the appropriate contexts.


### Context schema.org

You can use attributes defined on [schema.org](https://schema.org) as follows:

```
"@context": [
  "https://www.w3.org/2018/credentials/v1",
  "https://schema.org"
],
```

For example to issue a credetial with [givenName](https://schema.org/givenName), [familyName](https://schema.org/familyName) and [alumniOf](https://schema.org/alumniOf) attributes, submit the following:

```
{
  "connection_id": "31f1948f-aaf9-4f92-9962-47dca61256e4",
  "filter": {
    "ld_proof": {
      "credential": {
        "@context": [
          "https://www.w3.org/2018/credentials/v1",
          "https://schema.org"
        ],
        "type": ["VerifiableCredential", "Person"],
        "issuer": "did:key:zUC77Ndp6jMNNmmpgkJFZkW2YFkjcav5rBEJJTN872Lq3Lg2RT969gXi1uEwCbbWm8ct5xZJjWMHLzjs1kkogRKwbezCQ89ufRY74aEK7AhqFMeY1j1kqoGfRGmiZQoyXwUmk62",
        "issuanceDate": "2020-01-01T12:00:00Z",
        "credentialSubject": {
          "givenName": "Sally",
          "familyName": "Student",
          "alumniOf": "Example University"
        }
      },
      "options": {
        "proofType": "BbsBlsSignature2020"
      }
    }
  }
}
```

You can include more complex schemas, for example to use the schema.org [Person](https://schema.org/Person) schema (which includes `givenName` and `familyName`):

```
{
  "connection_id": "31f1948f-aaf9-4f92-9962-47dca61256e4",
  "filter": {
    "ld_proof": {
      "credential": {
        "@context": [
          "https://www.w3.org/2018/credentials/v1",
          "https://schema.org"
        ],
        "type": ["VerifiableCredential", "Person"],
        "issuer": "did:key:zUC77Ndp6jMNNmmpgkJFZkW2YFkjcav5rBEJJTN872Lq3Lg2RT969gXi1uEwCbbWm8ct5xZJjWMHLzjs1kkogRKwbezCQ89ufRY74aEK7AhqFMeY1j1kqoGfRGmiZQoyXwUmk62",
        "issuanceDate": "2020-01-01T12:00:00Z",
        "credentialSubject": {
          "student": {
            "type": "Person",
            "givenName": "Sally",
            "familyName": "Student",
            "alumniOf": "Example University"
          }
        }
      },
      "options": {
        "proofType": "BbsBlsSignature2020"
      }
    }
  }
}
```

TBD

To retrieve credentials from the wallet use the "/credentials/w3c" endpoint.

Another example:

{
  "connection_id": "31f1948f-aaf9-4f92-9962-47dca61256e4",
  "filter": {
    "ld_proof": {
      "credential": {
        "@context": [
          "https://www.w3.org/2018/credentials/v1",
          "https://w3id.org/citizenship/v1"
        ],
        "type": ["VerifiableCredential", "PermanentResidentCard"],
        "issuer": "did:key:zUC77Ndp6jMNNmmpgkJFZkW2YFkjcav5rBEJJTN872Lq3Lg2RT969gXi1uEwCbbWm8ct5xZJjWMHLzjs1kkogRKwbezCQ89ufRY74aEK7AhqFMeY1j1kqoGfRGmiZQoyXwUmk62",
        "issuanceDate": "2020-01-01T12:00:00Z",
        "credentialSubject": {
            "id": "did:example:b34ca6cd37bbf23",
            "type": ["PermanentResident", "Person"],
            "givenName": "JOHN",
            "familyName": "SMITH",
            "gender": "Male",
            "image": "data:image/png;base64,iVBORw0KGgo...kJggg==",
            "residentSince": "2015-01-01",
            "lprCategory": "C09",
            "lprNumber": "999-999-999",
            "commuterClassification": "C1",
            "birthCountry": "Bahamas",
            "birthDate": "1958-07-17"
        }
      },
      "options": {
        "proofType": "BbsBlsSignature2020"
      }
    }
  }
}


{
  "connection_id": "31f1948f-aaf9-4f92-9962-47dca61256e4",
  "filter": {
    "ld_proof": {
      "credential": {
        "@context": [
          "https://www.w3.org/2018/credentials/v1",
          "https://w3id.org/vaccination/v1"
        ],
        "type": ["VerifiableCredential", "VaccinationCertificate"],
        "issuer": "did:key:zUC77Ndp6jMNNmmpgkJFZkW2YFkjcav5rBEJJTN872Lq3Lg2RT969gXi1uEwCbbWm8ct5xZJjWMHLzjs1kkogRKwbezCQ89ufRY74aEK7AhqFMeY1j1kqoGfRGmiZQoyXwUmk62",
        "issuanceDate": "2020-01-01T12:00:00Z",
        "credentialSubject": {
            "type": "VaccinationEvent",
            "batchNumber": "1183738569",
            "administeringCentre": "MoH",
            "healthProfessional": "MoH",
            "countryOfVaccination": "NZ",
            "recipient": {
              "type": "VaccineRecipient",
              "givenName": "JOHN",
              "familyName": "SMITH",
              "gender": "Male",
              "birthDate": "1958-07-17"
            },
            "vaccine": {
              "type": "Vaccine",
              "disease": "COVID-19",
              "atcCode": "J07BX03",
              "medicinalProductName": "COVID-19 Vaccine Moderna",
              "marketingAuthorizationHolder": "Moderna Biotech"
            }
        }
      },
      "options": {
        "proofType": "BbsBlsSignature2020"
      }
    }
  }
}


