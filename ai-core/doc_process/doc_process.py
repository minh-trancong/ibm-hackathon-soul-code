from langchain.text_splitter import RecursiveCharacterTextSplitter
import unstructured_client
from unstructured_client.models import operations, shared


def extract_text(file_path):
    client = unstructured_client.UnstructuredClient(
        api_key_auth="dEXAiAvPdKF9MQHa4MJgBIlI3m94se",
        server_url="https://api.unstructuredapp.io",
    )

    filename = file_path
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
        return text, chunks
    except Exception as e:
        print(e)
        return "", []


def chunk_text(text, chunk_size=1000, chunk_overlap=100):
    """
    Phân chia văn bản thành các chunk nhỏ hơn.

    :param text: Văn bản cần phân chia
    :param chunk_size: Kích thước tối đa của mỗi chunk
    :param chunk_overlap: Kích thước chồng lấp giữa các chunk
    :return: Danh sách các chunk văn bản
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split(text)
