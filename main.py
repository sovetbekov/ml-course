import math
import random

glob_word_dict = {}
array_doc_term = []
num_of_doc = 10
num_of_centroid = 3
num_of_iteration = 100

count_doc_term = [0] * num_of_doc
term_matrix = [[]] * num_of_doc
centroid_array = [[]] * num_of_centroid
doc_cluster = [-1] * num_of_doc


def main():
    insert_doc_terms()
    count_doc_terms()
    print(array_doc_term)
    set_matrix()
    calc_matrix()
    normalize_matrix()
    calc_centroid()


def calc_distance(centroid: [int], doc_matrix: [int]):
    distance_sq = 0
    for word_id in range(len(centroid)):
        distance_sq += (centroid[word_id] - doc_matrix[word_id])**2
    return math.sqrt(distance_sq)


def calc_avg_centroid_distance(doc_array: [int]) -> ([int], bool):
    if len(doc_array) == 0:
        # return centroid_array[centroid_id]
        return [], False

    new_centroid = [0] * len(glob_word_dict)

    for doc_id in doc_array:
        for word_id in range(len(glob_word_dict)):
            new_centroid[word_id] += term_matrix[doc_id][word_id]

    for word_id in range(len(new_centroid)):
        new_centroid[word_id] /= len(doc_array)

    return new_centroid, True


def calc_cluster():
    cluster_doc_array = []
    for _ in range(num_of_centroid):
        cluster_doc_array.append([])

    for doc_id in range(num_of_doc):
        cluster_doc_array[doc_cluster[doc_id]].append(doc_id)

    for centroid_id in range(num_of_centroid):
        centroid_array[centroid_id], is_good = \
            calc_avg_centroid_distance(cluster_doc_array[centroid_id])
        if not is_good:
            for cluster_id in range(num_of_centroid):
                centroid_array[cluster_id] = randomize_centroid()
            break
    calc_doc_near_centroid()


def calc_doc_near_centroid():
    for doc_id in range(num_of_doc):
        doc_distance = 1000000
        for j in range(num_of_centroid):
            sample_distance = calc_distance(centroid_array[j], term_matrix[doc_id])
            if doc_distance > sample_distance:
                doc_distance = sample_distance
                doc_cluster[doc_id] = j


def calc_centroid():
    for centroid_id in range(num_of_centroid):
        centroid_array[centroid_id] = randomize_centroid()


    calc_doc_near_centroid()
    print(doc_cluster)
    for i in range(num_of_iteration):
        calc_cluster()
        print(doc_cluster)


def randomize_centroid() -> [int]:
    centroid = [0.0] * len(glob_word_dict)
    for word_id in range(len(glob_word_dict)):
        centroid[word_id] = random.random()
    return centroid


def normalize_matrix():
    max_matrix_val = 0
    for word_id in range(len(glob_word_dict)):
        for doc_id in range(num_of_doc):
            if term_matrix[doc_id][word_id] > max_matrix_val:
                max_matrix_val = term_matrix[doc_id][word_id]

    for word_id in range(len(glob_word_dict)):
        for doc_id in range(num_of_doc):
            term_matrix[doc_id][word_id] *= 1 / max_matrix_val


def calc_matrix():
    words = list(glob_word_dict.keys())
    for word_id in range(len(words)):
        for doc_id in range(num_of_doc):
            term_matrix[doc_id][word_id] = \
                calcTF(words[word_id], doc_id) * calcIDF(words[word_id])


def set_matrix():
    for doc_id in range(num_of_doc):
        term_matrix[doc_id] = [0] * len(glob_word_dict)


def insert_doc_terms():
    for number in range(num_of_doc):
        sample_dict = get_doc_dict(f"task_1//text_{number + 1}.txt")
        array_doc_term.append(sample_dict)
        insert_doc_dict(sample_dict)


def count_doc_terms():
    for doc_id in range(num_of_doc):
        count_doc_term[doc_id] = count_words(array_doc_term[doc_id])


def count_words(sample_dict: dict):
    return sum(list(sample_dict.values()))


def insert_doc_dict(sample_dict: dict):
    for word, count in sample_dict.items():
        try:
            _ = glob_word_dict[word]
        except (Exception,):
            glob_word_dict[word] = 0
        glob_word_dict[word] += count


def get_doc_dict(doc: str):
    doc_words = read_file(doc)

    sample_dict = {}
    for word in doc_words:
        try:
            sample_dict[word] += 1
        except (Exception,):
            sample_dict[word] = 1

    return sample_dict


def read_file(name) -> [str]:
    doc_words = []

    with open(name) as f:
        lines = f.readlines()

    for line in lines:
        for word in line.split():
            doc_words.append(check_word(word))

    return doc_words


def check_word(word: str):
    word = word.replace(",", "")
    word = word.replace(".", "")
    word = word.replace("?", "")
    word = word.replace("!", "")
    word = word.replace("(", "")
    word = word.replace(")", "")
    word = word.replace("\"", "")

    return word.lower()


def calcTF(word: str, doc_id: int):
    try:
        return array_doc_term[doc_id][word] / count_doc_term[doc_id]
    except (Exception,):
        return 0


def calcIDF(word: str):
    count = 0
    for doc_id in range(num_of_doc):
        try:
            _ = array_doc_term[doc_id][word]
            count += 1
        except (Exception,):
            pass
    return math.log(num_of_doc / count)


if __name__ == '__main__':
    main()
