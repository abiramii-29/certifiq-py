from flask import Blueprint, render_template, request, jsonify # type: ignore
import json
import os

customization_bp = Blueprint('customization', __name__)

# Directory to store saved certificates
CERTIFICATE_DIR = "saved_certificates"
os.makedirs(CERTIFICATE_DIR, exist_ok=True)

@customization_bp.route('/', methods=['GET'])
def template_customization():
    return render_template('customization.html')  # Placeholder for customization page

@customization_bp.route('/save_customizations', methods=['POST'])
def save_customizations():
    try:
        data = request.json  # Get JSON data from the frontend

        print("Received customizations:", data)

        # Predefined Template Metadata
        template_metadata = {
            "template_name": "Certificate Template 1",
            "template_html": """<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="/static/css/certificate.css">
</head>
<body>
    <div class="certificate-container">
        <div class="watermark">Certificate</div>
        
        <div class="certificate-content">
            <!-- Header with Logos -->
            <div class="certificate-header">
                <img id="certificate-logo" src="/static/images/reclogo.png" alt="Logo" />
            </div> 

            <!-- Title Section -->
            <div class="title">
                <h1>CERTIFICATE</h1>
                <h2>OF APPRECIATION</h2>
            </div>

            <!-- Recipient Information -->
            <div class="recipient">
                This certificate is proudly presented to
                <div class="recipient-name">{{name}}</div>
                <div class="divider"></div>
            </div>

            <!-- Certificate Message -->
            <div class="message">
                In recognition of your dedication and valued contribution to our event. We deeply appreciate your commitment and efforts.
            </div>

            <!-- Signature Section -->
            <div class="signature-section">
                <div class="signature">
                    <div class="signature-line"></div>
                    <div class="signature-name"></div>
                </div>
                <div class="signature">
                    <div class="signature-line"></div>
                    <div class="signature-name"></div>
                </div>
            </div>
        </div>

        <!-- Footer Bar -->
        <div class="footer-bar"></div>
    </div>
</body>
</html>
""",
            "css_file": "/static/css/certificate.css"
        }

        # Combine template metadata with user customizations
        certificate_data = {
            "template": template_metadata,
            "customizations": data  # Include text, logos, and other customizations
        }

        # Save certificate data to a file
        cert_id = f"certificate_{len(os.listdir(CERTIFICATE_DIR)) + 1}"  # Unique file name
        file_path = os.path.join(CERTIFICATE_DIR, f"{cert_id}.json")
        with open(file_path, 'w') as f:
            json.dump(certificate_data, f, indent=4)

        return jsonify({"message": "Certificate saved successfully!", "certificate_id": cert_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
