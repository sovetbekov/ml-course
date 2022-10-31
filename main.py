import math
import random

glob_word_dict = {}
array_doc_word = []
NUM_OF_DOC = 10
NUM_OF_CENTROID = 3
NUM_OF_ITERATION = 100

count_doc_word = [0] * NUM_OF_DOC
word_matrix = [[]] * NUM_OF_DOC
centroid_array = [[]] * NUM_OF_CENTROID
doc_cluster = [-1] * NUM_OF_DOC


def main():
    insert_doc_words()
    count_doc_words()
    print(array_doc_word)
    set_matrix()
    calculate_matrix()
    normalize_matrix()
    calculate_centroid()


def calculate_distance(centroid: [int], doc_matrix: [int]):
    distance_sq = 0
    for word_id in range(len(centroid)):
        distance_sq += (centroid[word_id] - doc_matrix[word_id])**2
    return math.sqrt(distance_sq)


def calculate_avg_centroid_distance(doc_array: [int]) -> ([int], bool):
    if len(doc_array) == 0:
        # return centroid_array[centroid_id]
        return [], False

    new_centroid = [0] * len(glob_word_dict)

    for doc_id in doc_array:
        for word_id in range(len(glob_word_dict)):
            new_centroid[word_id] += word_matrix[doc_id][word_id]

    for word_id in range(len(new_centroid)):
        new_centroid[word_id] /= len(doc_array)

    return new_centroid, True


def calculate_cluster():
    cluster_doc_array = []
    for _ in range(NUM_OF_CENTROID):
        cluster_doc_array.append([])

    for doc_id in range(NUM_OF_DOC):
        cluster_doc_array[doc_cluster[doc_id]].append(doc_id)

    for centroid_id in range(NUM_OF_CENTROID):
        centroid_array[centroid_id], is_good = \
            calculate_avg_centroid_distance(cluster_doc_array[centroid_id])
        if not is_good:
            for cluster_id in range(NUM_OF_CENTROID):
                centroid_array[cluster_id] = create_rand_centroid()
            break
    calculate_doc_near_centroid()


def calculate_doc_near_centroid():
    for doc_id in range(NUM_OF_DOC):
        doc_distance = 1000000
        for j in range(NUM_OF_CENTROID):
            sample_distance = calculate_distance(centroid_array[j], word_matrix[doc_id])
            if doc_distance > sample_distance:
                doc_distance = sample_distance
                doc_cluster[doc_id] = j


def calculate_centroid():
    for centroid_id in range(NUM_OF_CENTROID):
        centroid_array[centroid_id] = create_rand_centroid()

    calculate_doc_near_centroid()
    print(doc_cluster)
    for i in range(NUM_OF_ITERATION):
        calculate_cluster()
        print(doc_cluster)


def create_rand_centroid() -> [int]:
    centroid = [0.0] * len(glob_word_dict)
    for word_id in range(len(glob_word_dict)):
        centroid[word_id] = random.random()
    return centroid


def normalize_matrix():
    max_matrix_val = 0
    for word_id in range(len(glob_word_dict)):
        for doc_id in range(NUM_OF_DOC):
            if word_matrix[doc_id][word_id] > max_matrix_val:
                max_matrix_val = word_matrix[doc_id][word_id]

    for word_id in range(len(glob_word_dict)):
        for doc_id in range(NUM_OF_DOC):
            word_matrix[doc_id][word_id] *= 1 / max_matrix_val


def calculate_matrix():
    words = list(glob_word_dict.keys())
    for word_id in range(len(words)):
        for doc_id in range(NUM_OF_DOC):
            word_matrix[doc_id][word_id] = \
                calcTF(words[word_id], doc_id) * calcIDF(words[word_id])


def set_matrix():
    for doc_id in range(NUM_OF_DOC):
        word_matrix[doc_id] = [0] * len(glob_word_dict)


def insert_doc_words():
    for number in range(NUM_OF_DOC):
        sample_dict = get_doc_dict(f"task_1//text_{number + 1}.txt")
        array_doc_word.append(sample_dict)
        insert_doc_dict(sample_dict)


def count_doc_words():
    for doc_id in range(NUM_OF_DOC):
        count_doc_word[doc_id] = count_words(array_doc_word[doc_id])


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
        return array_doc_word[doc_id][word] / count_doc_word[doc_id]
    except (Exception,):
        return 0


def calcIDF(word: str):
    count = 0
    for doc_id in range(NUM_OF_DOC):
        try:
            _ = array_doc_word[doc_id][word]
            count += 1
        except (Exception,):
            pass
    return math.log(NUM_OF_DOC / count)


if __name__ == '__main__':
    main()
