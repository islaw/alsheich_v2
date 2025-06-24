import os
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError

# --- Configuration ---
PDF_PATH = 'full_ground_truth_protocol.pdf'
OUTPUT_DIR = 'protocol_images'

# This path has been updated with the correct location of the Poppler 'bin' directory.
POPPLER_PATH = r'C:\Users\עידושיפוני\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin'

def prepare_images_from_pdf(pdf_path, output_dir, poppler_path):
    """
    Converts all pages of a PDF file to JPEG images and saves them
    in a specified directory with a clear naming convention (page_1.jpg, page_2.jpg, etc.).
    """
    print("--- Starting PDF to Image Conversion ---")

    # 1. Validate inputs
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at '{pdf_path}'")
        return

    # A basic check to see if the poppler path seems plausible.
    if not os.path.isdir(poppler_path):
         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
         print("!!! CRITICAL: Poppler path is not a valid directory.        !!!")
         print(f"!!! Path provided: {poppler_path}")
         print("!!! Please double-check the path and try again.             !!!")
         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
         return

    # 2. Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory is: '{output_dir}'")

    # 3. Perform the conversion
    try:
        print("Converting pages... This may take a moment.")
        # Using a prefix and letting the library handle the numbering
        # The first page will be 1, which matches the PDF page numbering.
        images = convert_from_path(
            pdf_path=pdf_path,
            output_folder=output_dir,
            poppler_path=poppler_path,
            fmt='jpeg',
            output_file='page_', # Creates page_-1.jpg, page_-2.jpg etc.
            paths_only=True, # We just need to know the paths, not load images in memory
            use_pdftocairo=True # Often more reliable on Windows
        )
        
        # Renaming files to a 1-based index (page_1.jpg, page_2.jpg, etc.)
        print("Renaming output files for consistency...")
        for i, image_path in enumerate(images):
            page_number = i + 1
            new_path = os.path.join(output_dir, f"page_{page_number}.jpg")
            if os.path.exists(new_path):
                os.remove(new_path) # Remove if it exists to avoid errors
            os.rename(image_path, new_path)

        print(f"Successfully converted and renamed {len(images)} pages.")

    except PDFInfoNotInstalledError:
        print("\n--- ERROR ---")
        print("Poppler is not installed or its path is incorrect, even though the path seems valid.")
        print("Please ensure the extracted Poppler folder is complete and accessible.")
        print(f"Path used: {poppler_path}")
        print("-------------")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print("--- Conversion Process Finished ---")


if __name__ == "__main__":
    prepare_images_from_pdf(PDF_PATH, OUTPUT_DIR, POPPLER_PATH)