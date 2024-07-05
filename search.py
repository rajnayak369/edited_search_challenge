import json
import sys
from collections import defaultdict


def load_dataset(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def tokenize(text):
    stop_words = {"the", "a", "an", "and", "is", "in", "on", "of", "for", "to", "at", "by", "with", "which", "as",
                  "have", "be", "or", "that", "it", "ya", "you", "your", "me", "my", "we", "our", "i", "has",
                  "was"}  # Define custom stop words
    tokens = [word.lower() for word in text.split() if word.isalpha() and word not in stop_words]
    return tokens


def tokenize_weights(text):
    tokens = [word.lower() for word in text.split() if word.isalnum()]
    token_weights = {token: round((len(tokens) - i) / len(tokens), 2) for i, token in
                     enumerate(tokens)}  # Weight based on position
    return token_weights


# Build the divided inverted index from the dataset
def build_divided_inverted_index(dataset):
    id_index = dict()
    brand_index = defaultdict(list)
    name_index = defaultdict(list)

    for idx, product in enumerate(dataset):
        id_index[str(product['id'])] = idx
        brand_tokens = tokenize(product['brand'])
        for token in set(brand_tokens):
            brand_index[token].append(idx)
        name_tokens = tokenize(product['name'])
        for token in set(name_tokens):
            name_index[token].append(idx)

    return id_index, brand_index, name_index


def search_inverted_index(query,dataset, id_index, brand_index, name_index):
    query_tokens = tokenize_weights(query)
    # product_indices = set()
    print(query_tokens.items())
    scored_results = defaultdict(int)  # Dictionary to store cumulative scores for each product index
    for token in query_tokens:
        # Check for ID matches
        if token in id_index:
            scored_results[id_index[token]] += 3 + query_tokens[token] # High priority score for ID match
            # product_indices.add(id_index[token])

        # Check for brand matches
        if token in brand_index:
            for idx in brand_index[token]:
                scored_results[idx] += 2 + query_tokens[token] # Medium priority score for brand match
                # product_indices.add(idx)

        # Check for name matches
        if token in name_index:
            for idx in name_index[token]:
                scored_results[idx] += 1 + query_tokens[token] # Lower priority score for name match
                # product_indices.add(idx)

    # Convert the scored results to a list of tuples and sort them by score in descending order
    scored_results_list = [(score, dataset[idx]) for idx, score in scored_results.items()]
    scored_results_list.sort(reverse=True, key=lambda x: x[0])

    return scored_results_list[:20]




def main():
    # if len(sys.argv) < 2:
    #     print("Usage: python search.py <query>")
    #     return
    # query = sys.argv[1]

    query = "red shirt"
    dataset = load_dataset('search_dataset.json')
    id_index, brand_index, name_index = build_divided_inverted_index(dataset)

    results = search_inverted_index(query, dataset, id_index, brand_index, name_index)

    for score, product in results:
        print(f"Score: {score}, {product}")


if __name__ == "__main__":
    main()