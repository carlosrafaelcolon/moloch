import os
from dotenv import load_dotenv

from server.chat.create_embeddings import create_embeddings_for_pdf

# Load environment variables
load_dotenv()

def main():
    # Example: pass a configuration value to your function
    pdf_path = "server/static/pdf/2022_Statistical_Annex_Final__508_Compliant-revised.pdf"
    create_embeddings_for_pdf(pdf_path)

    print("Embedding process completed.")
    
    # Call the function with your PDF path
    #print_pdf_content(pdf_path)   

if __name__ == "__main__":
    main()
