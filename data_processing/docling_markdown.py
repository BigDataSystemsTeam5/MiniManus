import tempfile
from docling.document_converter import DocumentConverter

def convert_and_save_document(pdf_bytes: bytes):

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        temp_file.write(pdf_bytes)
        temp_file_path = temp_file.name
    
    # Initialize converter
    converter = DocumentConverter()

    result = converter.convert(temp_file_path)

    # Convert document
    #result = converter.convert(document)
    final_result = result.document.export_to_markdown()

    return final_result


    # Create the base output directory if it doesn't exist
    #foldername = "dockling_output_md"
    #os.makedirs(foldername, exist_ok=True)

    #filename = "new_docling"
    #file_path = os.path.join(foldername, filename)

    # Save markdown content
    #with open(file_path.md, 'w', encoding='utf-8') as f:
    #    f.write(final_result)
    

# Example usage
#file_path = r"C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Assignment 5 A\NVIDIA.pdf"
#output_path = convert_and_save_document(file_path, output_folder)
#print("Markdown file saved")
