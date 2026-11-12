import os
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from docx import Document

print("Loading DocTR model...")

model = ocr_predictor(
    det_arch="db_resnet50",
    reco_arch="crnn_vgg16_bn",
    pretrained=True
)

print("DocTR model loaded successfully!")


def extract_text(file_path):

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = os.path.splitext(file_path)[1].lower()

    # PDF extraction using DocTR
    if extension == ".pdf":
        document = DocumentFile.from_pdf(file_path)
        result = model(document)
        return result.render()

    # Image extraction using DocTR
    elif extension in [".jpg", ".jpeg", ".png"]:
        document = DocumentFile.from_images(file_path)
        result = model(document)
        return result.render()

    # Word document extraction
    # elif extension == ".docx":
    #     doc = Document(file_path)

    #     paragraphs = [
    #         paragraph.text
    #         for paragraph in doc.paragraphs
    #         if paragraph.text.strip()
        #     ]
        
    elif extension == ".docx":
        doc = Document(file_path)

        extracted_content = []

        # Extract normal paragraphs
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                extracted_content.append(paragraph.text)

        # Extract table contents
        for table in doc.tables:
            for row in table.rows:
                row_data = []

                for cell in row.cells:
                    cell_text = cell.text.strip()

                    if cell_text:
                        row_data.append(cell_text)

                if row_data:
                    extracted_content.append(" | ".join(row_data))

        return "\n".join(extracted_content)


        return "\n".join(paragraphs)

    else:
        raise ValueError("Unsupported file format")
