import PyPDF2
import unstructured_client
from unstructured_client.models import operations, shared

client = unstructured_client.UnstructuredClient(
    api_key_auth="dEXAiAvPdKF9MQHa4MJgBIlI3m94se",
    server_url="https://api.unstructuredapp.io",
)


def extract_text_pdf(file_path):
    with open(file_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        content = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            content += page.extract_text()
    return content


def extract_text(file_path):
    filename = file_path
    file_type = file_path.split(".")[-1]
    if file_type == "pdf":
        try:
            text = extract_text_pdf(filename)
            return text
        except Exception as e:
            print(e)
            return ""
    with open(filename, "rb") as f:
        data = f.read()
    req = operations.PartitionRequest(
        partition_parameters=shared.PartitionParameters(
            files=shared.Files(
                content=data,
                file_name=filename,
            ),
            # --- Other partition parameters ---
            # Note: Defining 'strategy', 'chunking_strategy', and 'output_format'
            # parameters as strings is accepted, but will not pass strict type checking. It is
            # advised to use the defined enum classes as shown below.
            strategy=shared.Strategy.AUTO,
            languages=['eng'],
        ),
    )
    try:
        res = client.general.partition(request=req)
        chunks = [i['text'] for i in res.elements]
        text = " ".join(chunks)
        return text
    except Exception as e:
        print(e)
        return ""
