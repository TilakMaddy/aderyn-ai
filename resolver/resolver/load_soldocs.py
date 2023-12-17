import os
from urllib.parse import urljoin

docs_path = os.path.join("solidity-docs", "docs")

BASE_URL = "https://docs.soliditylang.org/"

url2fs = {} # url -> file system (*.rst) mapping

for root, dirnames, filenames in os.walk(docs_path):
    for filename in filenames:
        if not filename.endswith(".rst"):
            continue
        rel_path = root.removeprefix("solidity-docs/docs")

        if len(rel_path) == 0:
            u = urljoin(BASE_URL, "en/v0.8.23/" + filename[:-4] + ".html")
        else:
            if "examples" in rel_path:
                continue
            if "internals" in rel_path:
                u = urljoin(BASE_URL, "en/v0.8.23/" + rel_path + "/" + filename[:-4] + ".html")
            else:
                u = urljoin(BASE_URL, "en/v0.8.23/" + rel_path + ".html" + "#" + filename[:-4])
        
        live_url = u # where you can go to find docs
        path_to_rst = os.path.join(root, filename)
        url2fs[live_url] = path_to_rst


from qdrant_client import QdrantClient
import json
from tqdm import tqdm


qdrant_client = QdrantClient("http://localhost:6333")
qdrant_client.set_model("sentence-transformers/all-MiniLM-L6-v2")

qdrant_client.recreate_collection(
    collection_name="solidity-docs",
    vectors_config=qdrant_client.get_fastembed_vector_params(),
)

metadata = []
documents = []

for (live_url, local_path) in url2fs.items():
    
    with open(local_path) as f:
        document = f.read()

    _metadata = {
        "url": live_url
    }

    documents.append(document)
    metadata.append(_metadata)


qdrant_client.add(
    collection_name="solidity-docs",
    documents=documents,
    metadata=metadata,
    ids=tqdm(range(len(documents))),
)
