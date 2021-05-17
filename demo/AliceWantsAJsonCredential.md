
Setup:

- start the agents with "AIP 2" setting
- establish a connection between the agents using OOB and DID exchange.

`./run_demo faber --did-exchange`
`./run_demo alice`

Faber has to create a DID with the appropriate:

- DID method ("key" or "sov")
- key type ("Ed25519Signature2018" or "BbsBlsSignature2020")
- "sov" must use "Ed25519Signature2018"

"did:sov" must be a public DID, but "did:key" is not

For example, call the "/wallet/did/create" endpoint with the following payload:

{
  "method": "key",
  "options": {
    "key_type": "bls12381g2" // or ed25519
  }
}

Faber does *not* create a schema or cred def for a JSON credential (these are only required for "indy" credentials).

Issue a credential, use the "/issue-credential-2.0/send" endpoint, example payload (replace the connection_id and "issuer" key) (and "proofType"):

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
          "degree": {
            "type": "BachelorDegree",
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

Note that if you have the "auto" settings on, this is all you need to do.  Otherwise you need to call the "send-request", "store", etc endpoints to complete the protocol.

Note also that the above example uses the "https://www.w3.org/2018/credentials/examples/v1" context, which should not be used in a real application.

A realistic example, with "real" contexts, is:

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


