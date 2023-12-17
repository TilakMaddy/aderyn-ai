# Import client library
from qdrant_client import QdrantClient
import os
import json
from tqdm import tqdm


qdrant_client = QdrantClient("http://localhost:6333")
qdrant_client.set_model("sentence-transformers/all-MiniLM-L6-v2")

qdrant_client.recreate_collection(
    collection_name="startups",
    vectors_config=qdrant_client.get_fastembed_vector_params(),
)

payload_path = os.path.join("data", "report.json")
metadata = []
documents = []

report = None # JSON 

with open(payload_path) as fd:
    report = json.load(fd)

high_issues = (report["high_issues"], "High")
medium_issues = (report["medium_issue"], "Medium")
low_issues = (report["low_issues"], "Low")
nc_issues = (report["nc_issues"], "NC")

for i in (high_issues, medium_issues, low_issues, nc_issues):
    for j in i[0]["issues"]:
        desc = j["description"]
        instances = j["instances"]
        title = j["title"]
        severity = i[1]

        document =  severity + " severity. " + desc + ". " + title

        _metadata = {
            "title": title,
            "severity": severity,
            "instances": instances,
        }

        documents.append(document)
        metadata.append(_metadata)

# documents = documents[:20]
# metadata = metadata[:20]

qdrant_client.add(
    collection_name="aderyn_reports",
    documents=documents,
    metadata=metadata,
    ids=tqdm(range(len(documents))),
)
