import os
from pydantic import BaseModel
from typing import Dict, Any


class SAMLConfig:
    SAML_SETTINGS = {
        "strict": True,
        "debug": True,
        "sp": {
            "entityId": "http://localhost:8000/saml/metadata",
            "assertionConsumerService": {
                "url": "http://localhost:8000/saml/acs",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST",
            },
            "singleLogoutService": {
                "url": "http://localhost:8000/saml/sls",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
            },
            "NameIDFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified",
            "x509cert": "",  # Your SP's certificate if available
            "privateKey": "",  # Your SP's private key if required
        },
        "idp": {
            "entityId": "https://auth.pingone.com/194c955a-00ad-4453-9e7e-6ea25b97fd43",
            "singleSignOnService": {
                "url": "https://auth.pingone.com/194c955a-00ad-4453-9e7e-6ea25b97fd43/saml20/idp/sso",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
            },
            "singleLogoutService": {
                "url": "https://auth.pingone.com/194c955a-00ad-4453-9e7e-6ea25b97fd43/saml20/idp/slo",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
            },
            "x509cert": """-----BEGIN CERTIFICATE-----
MIIDrjCCApagAwIBAgIGAZNdTHQOMA0GCSqGSIb3DQEBCwUAMIGXMQswCQYDVQQG
EwJVUzEWMBQGA1UECgwNUGluZyBJZGVudGl0eTEWMBQGA1UECwwNUGluZyBJZGVu
dGl0eTFYMFYGA1UEAwxPUGluZ09uZSBTU08gQ2VydGlmaWNhdGUgZm9yIFdvcmtm
b3JjZSBTb2x1dGlvbiBFbnZpcm9ubWVudCBkZmNmZDQ5ZSBlbnZpcm9ubWVudDAe
Fw0yNDExMjQwODMxNTFaFw0yNTExMjQwODMxNTFaMIGXMQswCQYDVQQGEwJVUzEW
MBQGA1UECgwNUGluZyBJZGVudGl0eTEWMBQGA1UECwwNUGluZyBJZGVudGl0eTFY
MFYGA1UEAwxPUGluZ09uZSBTU08gQ2VydGlmaWNhdGUgZm9yIFdvcmtmb3JjZSBT
b2x1dGlvbiBFbnZpcm9ubWVudCBkZmNmZDQ5ZSBlbnZpcm9ubWVudDCCASIwDQYJ
KoZIhvcNAQEBBQADggEPADCCAQoCggEBAKmm5x78/h32kBQF8469i8nAdTicoZth
sJx6hpTFNrETkd0bkZy+zywTd7VMexpsz9bMLgxiIvMzaNChxYsBYiX08FsHadsO
hlDEqZsp/sYHpT4PJgyR3GqNZjbyPu/6dTDEVm2UgwRRoFsc38rVJzwHtppKmCQa
oQpjQ6T8gYYiU37ezuQkHubqGBgb212ALDGZL/Amx8LliaAq0oU7zIPiNTWgMjOb
LoGSSWpTFEXKodxdSfX8x2pYzRy8iuY0B6d/NMLl7ZSBW1HU3x7P0kYkZSBOaWJe
LwsLM+fyWSybOKXs1V82D3nynMFGN5zywt/fMvxeFREYmr9RyxxCorECAwEAATAN
BgkqhkiG9w0BAQsFAAOCAQEAYdtkv8cReSHGSQi4u6YjDv/IQNAGRFs8vh1zdMDq
yWIe+5yasZUVNFvDtMHtTWD93xe3AAvZThcGpbuuXnevxla7sBnDgRWdxGiYhYx9
R6eU3MHNG7Fa3LofSrGg6ubECkPPsUrjfd47/jSbF5UwKJTswhCaNBchySVwmAi/
O9ngI6DvNgjDTIVMbdR3FPsQI0ytVg02ON2S4BGa6V94rckMLNYVU0SGGVXFxmFb
u2yRgPnjUMTmw9kmVN8JreWB9elxVrDBd2csnZ+2STcMeKkxJPB/a6/V4Tgpz0kr
PFUZcB+C3XTtGnM6Nn1YTgkTHrrHnR9Zs8AgFF7nPe4ZpQ==
-----END CERTIFICATE-----""",
        },
        "security": {
            "nameIdEncrypted": False,
            "authnRequestsSigned": False,
            "logoutRequestSigned": False,
            "logoutResponseSigned": False,
            "signMetadata": False,
            "wantMessagesSigned": False,
            "wantAssertionsSigned": False,
            "wantNameIdEncrypted": False,
            "requestedAuthnContext": True,
        },
    }
