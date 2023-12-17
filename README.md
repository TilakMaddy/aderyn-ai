# Aderyn AI 

![Logo](aderyn_ai_widescreen.png)

## What is Aderyn AI ?
It is a personal assitant that will supercharge your experience with [aderyn](https://github.com/Cyfrin/aderyn). Aderyn AI indexes your report using `fast-all-MiniLM-L6-v2` embeddings which is a [Qdrant](http://qdrant.tech) native version of [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)  and loads it in the vector store. It then uses [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) on a 384 dimensional space to perform semantic search on the reported vulnerabitites. Finally chatgpt kicks in to recommend code fixes. Also there is a safety layer attached to it, so that you will be warned on the data that is sent to openai.

## How to use it ?

#### Create a locally running vector store
```
docker pull qdrant/qdrant
docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
```

#### Clone this repository and put your data inside it.

[Aderyn](https://github.com/Cyfrin/aderyn) generated `report.json` should go to `resolver/data`

The `root` (hardhat / foundry project folder) should also be copied to `resolver/data` under the name `contract-playground` like one that already exists.

####  Setup python inference

```
cd resolver
```

Now, install the dependencies from pyproject.toml 

Load the data into the vector store - 
```
python resolver/load_data.py
```

(Optional step)

Put your *OPENAI_API_KEY* in `.env` as shown in `.env.sample`

Now, let's go inference !!

```bash
python resolver/search_data.py
```

It should startup a chat like prompt. 

-------


Shown below is a conversation thread where I tried to find out all of the **hashing related** vulnerabilities and asked chatgpt to suggest a fix for the code.

### Sample chat 
*Enter search query: (start with 'vvv ' for verbose matches)* **vvv hashing risks**

---------

*Match #0*

*Low `abi.encodePacked()` should not be used with dynamic types when passing the result to a hash function such as `keccak256()` (3 files)*

*0 src/KeccakContract.sol 18*

*1 src/KeccakContract.sol 22*

*2: src/KeccakContract.sol 26*

---------

*Match #1*

*Medium Centralization Risk for trusted owners (4 files)*

*0: src/AdminContract.sol 7*

---------

*Match #2*

*High Arbitrary `from` passed to `transferFrom` (or `safeTransferFrom`) (6 files)*

*0: src/ArbitraryTransferFrom.sol 16*

*1: src/ArbitraryTransferFrom.sol 20*

---------

*Ask chatgpt for help ? (y/n)* **y**

*match #* **0**

*rec* **#2**

*This will be exposed.*

> *return keccak256(abi.encodePacked(a, b));*

*Go ahead ? (y/n)* **y**

*To fix the vulnerability, you should replace the use of `abi.encodePacked` with `abi.encode`.
By using `abi.encode`, the items will be padded to 32 bytes and prevent hash collisions.
The updated code would look like this: `return keccak256(abi.encode(a, b));`. This change ensures 
that the arguments are properly encoded and avoids potential security risks associated with 
hash collisions.*

-----------

### Feedbacks
Any and all feedbacks are welcome ! Positive or negative doesn't matter. (just don't insult people)



