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

