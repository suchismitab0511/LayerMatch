import os
import pdfplumber
import docx


def extract_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"  Could not read {file_path}: {e}")
        return ""

    if not text.strip():
        print(f"  Warning: no text extracted from {file_path} (possibly corrupted or scanned)")

    return text.strip()


def extract_from_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs if p.text])
    return text.strip()


def parse_all_resumes(resume_dir):
    resumes = {}

    for filename in os.listdir(resume_dir):
        file_path = os.path.join(resume_dir, filename)

        if filename.endswith(".pdf"):
            print(f"  Reading: {filename}")
            resumes[filename] = extract_from_pdf(file_path)

        elif filename.endswith(".docx"):
            print(f"  Reading: {filename}")
            resumes[filename] = extract_from_docx(file_path)

        else:
            print(f"  Skipping: {filename}")

    valid_count = sum(1 for v in resumes.values() if v.strip())
    print(f"\n  Total files found: {len(resumes)}")
    print(f"  Successfully parsed: {valid_count}")
    print(f"  Failed/empty: {len(resumes) - valid_count}")

    return resumes