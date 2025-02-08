import json

# Mapping types to numbers
type_mapping = {
    "p": 1,  # prescribed
    "b": 2,  # biglist
    "sl": 3,  # short list
    "seq": 4,  # sequence
    "or": 5  # pick one
}

def create_document():
    document = {}

    # Common fields
    document["_id"] = input("Enter _id: ")
    while True:
        doc_type = input("Enter type (p - prescribed, b - biglist, sl - short_list, seq - sequence, or - pick one): ").strip().lower()
        if doc_type in type_mapping:
            document["type"] = type_mapping[doc_type]
            break
        else:
            print("Invalid type. Please enter one of: p, b, short_list, seq, or.")

    document["grade"] = input("Enter grade (T/F): ").strip().lower() == "t"

    # Conditional fields based on type
    if doc_type == "p":
        document["courses"] = input("Enter courses as comma-separated values: ").split(", ")
    elif doc_type == "b":
        document["list_names"] = input("Enter list names (comma seperated): ").split(", ")
        metric_type = int(input("Enter metric type (1 for Courses, 2 for Credits): "))
        document["metrics"] = {
            "Type": "Courses" if metric_type == 1 else "Credits",
            "Value": int(input("Enter metric value: "))
        }
        excluded = input("Enter exclusions as comma-separated values (or leave empty): ").strip()
        document["exclude"] = excluded.split(", ") if excluded else []

        #exclude can exclude lists and they can also exclude a specific set of courses
        excludedCourses = input("Enter excluded courses as comma-separated values: ").split(", ")
        document["exclude"].append(excludedCourses)
        recommended = input("Enter recommended courses as comma-separated values (or leave empty): ").strip()
        document["recommended"] = recommended.split(", ") if recommended else []
    elif doc_type == "short_list":
        metric_type = int(input("Enter metric type (1 for Courses, 2 for Credits): "))
        document["metrics"] = {
            "Type": "Courses" if metric_type == 1 else "Credits",
            "Value": int(input("Enter metric value: "))
        }
        recommended = input("Enter recommended courses as comma-separated values (or leave empty): ").strip()
        document["recommended"] = recommended.split(", ") if recommended else []
    elif doc_type == "or":
        document["courses"] = input("Enter courses as comma-separated values: ").split(", ")
    elif doc_type == "seq":
        sequences = input("Enter sequences as lists, separated by semicolons (e.g., 'BIOL141; CHEM111,PHYS214'): ")
        document["sequences"] = [seq.split(",") for seq in sequences.split(";")]

    return document

def main():
    documents = []

    print("Create JSON Documents (type 'done' for _id to finish)\n")

    while True:
        _id = input("Enter _id for the next document (or type 'done' to finish): ")
        if _id.lower() == 'done':
            break
        doc = create_document()
        documents.append(doc)

    # Save to a JSON file
    with open("documents.json", "w") as f:
        json.dump(documents, f, indent=4)
        print("JSON saved to 'documents.json'")

if __name__ == "__main__":
    main()
