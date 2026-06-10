import os

def generate_simple_dummy_files(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Generate a dummy JPG by writing a minimal valid JPG header/structure
    # This is better than nothing, but let's just use open/write if we can't use PIL
    photo_path = os.path.join(directory, "official_photo.jpg")
    with open(photo_path, "wb") as f:
        # Minimal JPEG header
        f.write(b'\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00\x60\x00\x60\x00\x00\xFF\xDB\x00\x43\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\x0d\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xFF\xC0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xFF\xC4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xDA\x00\x08\x01\x01\x00\x00\x3f\x00\xcc\x00\xff\xd9')
    print(f"Generated minimal JPG: {photo_path}")

    sig_path = os.path.join(directory, "official_signature.jpg")
    with open(sig_path, "wb") as f:
        f.write(b'\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00\x60\x00\x60\x00\x00\xFF\xDB\x00\x43\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\x0d\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xFF\xC0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xFF\xC4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xDA\x00\x08\x01\x01\x00\x00\x3f\x00\xcc\x00\xff\xd9')
    print(f"Generated minimal JPG: {sig_path}")

    # Generate a dummy PDF
    pdf_path = os.path.join(directory, "official_certificate.pdf")
    with open(pdf_path, "wb") as f:
        f.write(b"%PDF-1.1\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 40 >>\nstream\nBT /F1 12 Tf 100 700 Td (Dummy Document) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000062 00000 n\n0000000117 00000 n\n0000000174 00000 n\ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n265\n%%EOF")
    print(f"Generated: {pdf_path}")

if __name__ == "__main__":
    generate_simple_dummy_files("/Users/anujjha/Bridge-Automation.-Framework-/test_data")
