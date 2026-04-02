import os

def load_documents(case_id):
    folder = case_id.replace("/", "_")
    path = f"memory/legal_cases/{folder}/documents"

    documents = []

    if not os.path.exists(path):
        return documents

    for file in sorted(os.listdir(path)):
        file_path = os.path.join(path, file)

        if os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except:
                content = ""

            documents.append({
                "name": file,
                "content": content.lower()
            })

    return documents


def extract_facts_from_documents(documents):
    facts = {
        "claims": [],
        "persons": [],
        "keywords": []
    }

    for doc in documents:
        text = doc["content"]

        if "rozwód" in text:
            facts["keywords"].append("divorce")

        if "dziecko" in text:
            facts["keywords"].append("child")

        if "alimenty" in text:
            facts["keywords"].append("alimony")

        if "wnosyę o" in text:
            facts["claims"].append(text)

    return facts
