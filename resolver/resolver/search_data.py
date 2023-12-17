from qdrant_client import QdrantClient
import ask_chatgpt
import os

class NeuralSearcher:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        # initialize Qdrant client
        self.qdrant_client = QdrantClient("http://localhost:6333")
        self.qdrant_client.set_model("sentence-transformers/all-MiniLM-L6-v2")

    def search(self, text: str):
        search_result = self.qdrant_client.query(
            collection_name=self.collection_name,
            query_text=text,
            query_filter=None,  # If you don't want any filters for now
            limit=3  # 3 the most closest results is enough
        )
        # `search_result` contains found vector ids with similarity scores along with the stored payload
        # In this function you are interested in payload only
        metadata = [hit.metadata for hit in search_result]
        return metadata


def display_record(rec, verbose):
    print(rec["severity"] + " " + rec["title"] + " (" + str(len(rec["instances"])) + " files) ")
    
    if verbose:
        for (idx, instance) in enumerate(rec["instances"]):
            print(str(idx) + ": " + instance["contract_path"] + " " + str(instance["line_no"]))

def go_read_from(filepath, line_no):
    filepath = os.path.join("data", "contract-playground", filepath)
    req_line = None
    with open(filepath) as f:
        for (idx, line) in enumerate(f):
            if idx + 1 == line_no:
                req_line = line 
                break
    return req_line


neural_searcher = NeuralSearcher(collection_name='aderyn_reports')

while True:

    question = input("Enter search query: (start with 'vvv ' for verbose matches) ")
    print()

    verbose = False
    if question.startswith("vvv"):
        verbose = True
        question = question[len("vvv"):]
        
    answer = neural_searcher.search(text=question)

    print("---- Top Matches ----")

    for (idx, rec) in enumerate(answer):
        print("Match #" + str(idx))
        display_record(rec, verbose=verbose)
        print()

    while True:

        ask_to_ask = input("Ask chatgpt for help ? (y/n)")

        if ask_to_ask.lower() == "y":
            match_number = int(input("match #"))
            rec_number = int(input("rec#"))

            source_code_line = answer[match_number]["instances"][rec_number]
            source_code_line = go_read_from(source_code_line["contract_path"], source_code_line["line_no"])

            prompt = f"""
            The vulnerability detected is described as follows:
            {answer[match_number]['document']}

            Source code line: 
            {source_code_line}

            Please suggest a fix. Keep you answer to maximum of 5 sentences.
            """

            confirmation = input(f"This will be exposed. \n{source_code_line}\nGo ahead ? (y/n) ")
            if confirmation.lower() == "y":
                ask_chatgpt.ask_chatgpt(prompt)

        else:
            break        


    print()
    print()



