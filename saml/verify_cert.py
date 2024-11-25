# verify_cert.py
from onelogin.saml2.settings import OneLogin_Saml2_Settings
import json

def verify_saml_settings():
    try:
        with open('saml/settings.json', 'r') as f:
            settings = json.load(f)
        
        saml_settings = OneLogin_Saml2_Settings(settings)
        valid = saml_settings.is_valid()
        
        if valid:
            print("Certificate and SAML settings are valid!")
        else:
            print("Invalid settings found:")
            print(saml_settings.validate())
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    verify_saml_settings()