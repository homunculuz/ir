import operator
import sys
import time

# implanted functions
from src.Clustering import do_clustering
from src.codings.CompressionPostingLists import compression_posting_list
from src.CreateDictionary import create_dictionary
from src.Remapping import tsp_medoids_mapping, get_remapping_dictionary

RADIUS = [.99, .98,.97]

if __name__ == '__main__':

    print("Wait! The results will saved  in \'data/result.txt\' after execution....")

    f = open("data/result.txt", 'w')
    sys.stdout = f

    # read dictionary
    d, n = create_dictionary()

    print("\n\n")

    # order the postings list of the dictionary in increasing order
    d = dict(sorted(d.items(), key=operator.itemgetter(1), reverse=False))

    # apply the VB, Elias Gamma, Elias Delta Encoding of the posting lists
    c1 = compression_posting_list(d)
    print("|Without TSP|", c1)

    i = 0
    # apply TSP-Clustering producing the new inducted number of documents by the similarity
    for r in RADIUS:
        start_time = time.time()
        medoids, clusters = do_clustering(d, n, r)
        print("\n With radius: ", RADIUS[i], " the number of medoids are: ", len(medoids))
        mapping = tsp_medoids_mapping(medoids, clusters, n)

        # get remapped dictionary with posting list sorted, gap motivation
        new_d = get_remapping_dictionary(d, mapping)

        # apply the VB, Elias Gamma, Elias Delta Encoding of the TSP remapped posting lists
        c2 = compression_posting_list(new_d)

        print("|With TSP|", c2)

        # Calculation of improvement of TSP compression respect others
        print("Improvements: ", [round((1 - (b / a)) * 100, 2) for a, b in zip(c1, c2)], " %")

        print("Finish: ", "%s seconds" % round(time.time() - start_time, 2))
        i += 1
    f.close()
