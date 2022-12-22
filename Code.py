# NAME : AKSHAT TOOLAJ SINHA
# ENTRY NUBMBER : 2020CSB1068

# Importing Libraries for usage

# for opening the .bz2 file
from bz2 import BZ2File as bzopen
# to use regex to get specific patterns in the text
import re
# to utilize random function for random walk
import random
# to get specific line from a file very fast
import linecache as lc

'''
                The format for wikidump is 
                        <page>
                        ....
                        <title>.....</title>
                        
                        <revision>.......
                        ........ Wikilinks are founded here only which we are considering
                        </revision>
                        
                        </page>
                        
'''


def adj_list_file_creation(file_name):
    """
        Creates a adjacency list of the given file in .txt format with ADJ_LIST_{file_name} as it's name
        and return the name of the file as output.

        Arguments: file_name : Name of the file ( has to be a WikiDump ) to be converted to adjacency list
    """

    print("ADJACENCY LIST CREATION STARTED")

    # Opening the bz2 file
    with bzopen(file_name, "r") as wikidump:

        # Making Pattenn for Regex to check
        pattern = "\[\[[\w|\s]+\]\]"
        pattern_check = re.compile(pattern)

        # Boolean variable to determine whether I am in revision or not
        in_revision = 0
        # It holds the current line in XML which I am parsing through
        curr = ''
        # For each line, it holds all the links being pointed to
        links_matched = []

        # Opening the file to dump adjacency list
        fd = open("ADJ_LIST_{v1}.txt".format(
            v1=file_name), 'w', encoding="utf-8")

        # iterating over .bz2 file and storing the contents in line
        for i, line in enumerate(wikidump):

            # any line in bz2 starts with b'{actual_line}' , hence have to typecast for string operations

            # removing '\n' from the line and type casting to string
            curr = str(line.rstrip())

            if ('<title>' in curr):      # When I encounter title tag for a web page
                # Removing tags & uneccesary charachters from the string
                fd.write(curr[13:-9].lower())
                fd.write(":")  # using : as a delimiter

            # We use revision tag to determine whether we are in wikilinks portion of web or not

            if ('<revision>' in curr):
                in_revision = 1  # I am in text portion of the webpage
            if ('</revision>' in curr):
                # I am not in text portion of the webpage , hence go to new line for another web page
                fd.write("\n")
                in_revision = 0

            # If I am in text portion of a webpage, I need to capture wikilinks of the pages
            if (in_revision == 1):
                # Find all the wikilinks in the present line.
                links_matched = pattern_check.findall(curr)
                for i in links_matched:  # Iterating over all the wikilinks
                    if ('|' in i):       # If there is a placeholder in the wikilinks,
                        # Take the first part
                        fd.write((i.split('|')[0])[2:].lower())
                    else:
                        # Otherwise take the whole part
                        fd.write(i[2:-2].lower())
                    fd.write(",")  # Separator between different wikilinks

        fd.close()  # Close the file

    print("ADJACECNY LIST FILE CREATED SUCCESSFULLY") # completion message

    return "ADJ_LIST_{v1}.txt".format(v1=file_name)




def random_walk(file_name, prob, iter):
    """
        Performs random walk on the given file and dumps Page Rank in a file and returns the name of page rank file as output
        Arguments: 
            file_name: Adjacency list file name to perform random-walk
            prob: Probability of teleportation
            iter: Number of iterations to perform random walk on
    """

    link_offset = {}  # store the offset of the link in the dictionary for faster retrieval
    visited = {}  # store the number of times a link is visited

    fd = open(file_name, 'r')   # Open the file
    link_number = 0  # tracking number of links in the file
    while True:
        line = fd.readline()   # Read a line

        if not line:   # break the loop when line is empty i.e EOF
            break

        title = line.split(':', 2)[0]  # title of the link

        visited[title] = 0  # Initialize the number of times visited to 0
        link_number += 1  # link_number is incremented
        link_offset[title] = link_number  # Store the offset of the link

        if (link_number % 100000 == 0):  # Printing the progress of my code
            print(link_number," Web pages processed")

    fd.close()  # Close the file

    print("LINK OFFSET & VISITED COUNTER CREATED") # for user info

#   Until Now, We are doing some pre-computation in RAM for faster retrieval of data


    curr_web = random.randint(1, link_number)  # Choosing a random starting page

    count = 0

    # Running the random walk for given number of iterations

    while (count < iter):

        temp = lc.getline(file_name, curr_web).split(
            ':')  # Get the line of the current web page

        visited[temp[0]] += 1  # Increment the number of times visited
        # fetch the out links of the current web page
        out_links = temp[1].split(',')

        if (out_links[0] != ''): # if there are no outlinks, then out_links[0] will be empty string
            if (random.random() <= prob):  # If random number is less than given probability, teleport to a random web page
                curr_web = random.randint(1, link_number)
            else:
                going_to = random.choice(out_links)  # Choose a random out link
                if (going_to in link_offset):
                    # If the outlink is present in the whole of webpage, go to that web page
                    curr_web = link_offset[going_to]
                else:
                    # If the out link is not in the file, teleport to a random one
                    curr_web = random.randint(1, link_number)
        else:
            # If the current web page has no out links, teleport to random one
            curr_web = random.randint(1, link_number)

        count += 1  # one iteration done
        if (count % (iter//1000) == 0):  # Progress Bar
            print(count,'Steps completed')

    # Open the file to dump the page rank
    fd = open("PAGE_RANK_CACHED_{x}".format(x=file_name), 'w')

    # Sort the page rank in descending order
    for wp in sorted(visited, key=visited.get, reverse=True):
        if (visited[wp] != 0):  # If the page is visited, dump it
            fd.write(wp+" : "+str(visited[wp])+'\n')  # Dump the page rank

    fd.close()

    print("RANDOM WALK COMPLETED")  # Print the completion message

    return "PAGE_RANK_CACHED_{x}".format(x=file_name)  # Return the file name




def top_k_pageranked(file_name, k):
    """Print the Top K Page Ranked Pages stored in a file( given as input )"""
    fd = open(file_name, 'r')  # Open the file

    line_count = 0  # To keep track of the number of lines in the file

    while (line_count < k):  # Iterate over the file till the number of lines iterated is less than k
        line = fd.readline()
        title = line.split(':')[0]  # Get the title of the page
        print('PageRank-', line_count+1, ' : ', title)  # Print the page rank
        line_count += 1  # Increment the number of lines iterated

    fd.close()

    print("PAGE RANK COMPLETED")  # Print the completion message



file_name = input("Enter the file name: ")  # Name of the file

k = 1000  # Number of top page ranked pages to be printed

prob=0.2 # Probability of teleportation

iteration=1000000 # Number of iterations

adj_list_file = adj_list_file_creation(file_name)

page_rank_file = random_walk(adj_list_file, prob, iteration)

top_k_pageranked(page_rank_file, k)
