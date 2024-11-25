import sys
import re

def format_certificate(cert_file):
    """
    Reads and formats an X509 certificate for use in SAML settings
    
    Args:
        cert_file (str): Path to the certificate file
    
    Returns:
        str: Formatted certificate string
    """
    try:
        with open(cert_file, 'r') as f:
            cert_content = f.read()
        
        # Remove BEGIN and END tags
        cert_content = re.sub(r'-+BEGIN CERTIFICATE-+', '', cert_content)
        cert_content = re.sub(r'-+END CERTIFICATE-+', '', cert_content)
        
        # Remove newlines and spaces
        cert_content = ''.join(cert_content.split())
        
        return cert_content
        
    except FileNotFoundError:
        print(f"Error: Certificate file '{cert_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing certificate: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cert_formatter.py <path_to_certificate>")
        sys.exit(1)
    
    cert_file = sys.argv[1]
    formatted_cert = format_certificate(cert_file)
    print("\nFormatted Certificate (copy this to your settings.json):\n")
    print(formatted_cert)