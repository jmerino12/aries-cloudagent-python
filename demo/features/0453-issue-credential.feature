Feature: RFC 0453 Aries Agent Issue Credential

  @T001-RFC0453 @DIDExchangeConnection
  Scenario Outline: Issue a credential with the Issuer beginning with an offer
    Given "2" agents
      | name | role   | capabilities        |
      | Acme | issuer | <Acme_capabilities> |
      | Bob  | holder | <Bob_capabilities>  |
    Given "Acme" is ready to issue a "<credential_format>" credential
    And "Acme" and "Bob" have an existing connection
    When "Acme" offers a "<credential_format>" credential with data <Credential_data>
    And "Bob" requests the "<credential_format>" credential
    And "Acme" issues the "<credential_format>" credential
    And "Bob" acknowledges the "<credential_format>" credential issue
    Then "Bob" has the "<credential_format>" credential issued

    @CredFormat_Indy @Schema_DriversLicense_v2 @DidMethod_sov
    Examples: Indy
      | Acme_capabilities                      | Bob_capabilities  | credential_data   | credential_format |
      | --public-did                           |                   | Data_DL_MaxValues | indy              |

    @CredFormat_JSON-LD @Schema_DriversLicense_v2 @ProofType_Ed25519Signature2018 @DidMethod_key
    Examples: Json-LD
      | Acme_capabilities                      | Bob_capabilities  | credential_data   | credential_format |
      | --public-did                           |                   | Data_DL_MaxValues | json-ld           |

    @CredFormat_JSON-LD @Schema_DriversLicense_v2 @ProofType_BbsBlsSignature2020 @DidMethod_key
    Examples: Json-LD-BBS
      | Acme_capabilities                      | Bob_capabilities  | credential_data   | credential_format |
      | --public-did                           |                   | Data_DL_MaxValues | json-ld           |


  @T003-RFC0453 @GHA
  Scenario Outline: Issue a credential with the Issuer beginning with an offer
    Given we have "2" agents
      | name  | role    | capabilities        |
      | Acme  | issuer  | <Acme_capabilities> |
      | Bob   | holder  | <Bob_capabilities>  |
    And "Acme" and "Bob" have an existing connection
    And "Acme" is ready to issue a credential for <Schema_name>
    When "Acme" offers a credential with data <Credential_data>
    Then "Bob" has the credential issued

    Examples:
       | Acme_capabilities                      | Bob_capabilities          | Schema_name    | Credential_data          |
       | --public-did                           |                           | driverslicense | Data_DL_NormalizedValues |
       | --public-did --did-exchange            | --did-exchange            | driverslicense | Data_DL_NormalizedValues |
       | --public-did --mediation               | --mediation               | driverslicense | Data_DL_NormalizedValues |
       | --public-did --multitenant             | --multitenant             | driverslicense | Data_DL_NormalizedValues |


  @T004-RFC0453 @GHA
  Scenario Outline: Issue a credential with revocation, with the Issuer beginning with an offer, and then revoking the credential
    Given we have "2" agents
      | name  | role    | capabilities        |
      | Acme  | issuer  | <Acme_capabilities> |
      | Bob   | holder  | <Bob_capabilities>  |
    And "Acme" and "Bob" have an existing connection
    And "Bob" has an issued <Schema_name> credential <Credential_data> from "Acme"
    Then "Acme" revokes the credential
    Then "Bob" has the credential issued

    Examples:
       | Acme_capabilities                        | Bob_capabilities  | Schema_name    | Credential_data          |
       | --revocation --public-did                |                   | driverslicense | Data_DL_NormalizedValues |
       | --revocation --public-did --did-exchange | --did-exchange    | driverslicense | Data_DL_NormalizedValues |
       | --revocation --public-did --mediation    | --mediation       | driverslicense | Data_DL_NormalizedValues |
       | --revocation --public-did --multitenant  | --multitenant     | driverslicense | Data_DL_NormalizedValues |
