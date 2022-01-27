# coding=utf-8

from scrape_utils import utils
import json
import threading
import sys
import argparse

parser=argparse.ArgumentParser()


def launch_scraper(page_num_var,concelho,scraper):

    print("Processing " +  concelho['Name'] + "(ID="+str(concelho['Id'])+") | Page "+str(page_num_var))

    listing_results = scraper.get_listings(concelho['Url'],page_num_var)

    if listing_results != None:

        scraper.process_and_save_result(listing_results,concelho,page_num_var)

        print("Saved " + concelho['Name'] + "(ID="+str(concelho['Id'])+") | Page " +  str(page_num_var))

if __name__ == "__main__":

    #We'll usually want to run something like
    # processing.py -s 1 -e 6 -t 2
    #meaning, we'll leave startpage and endpage with default values
    parser.add_argument('--start', '-s', help='Municipality Id from concelhos.json where scraping should start - will default to 1')
    parser.add_argument('--end', '-e', help='Municipality Id from concelhos.json where scraping should start - will default to the same as --start')
    parser.add_argument('--threads', '-t', help='Number of Maximum Threads allowed - will default to 2')
    parser.add_argument('--startpage', '-sp', help='Page on which to start scraping, usually will be 1, specially if more than on Municipality is being scraped')
    parser.add_argument('--endpage', '-ep', help='Page on which to end scraping, usually will be the maximum possible')

    args=parser.parse_args()

    scraper = utils()

    with open('concelhos.json', encoding="utf-8") as json_file:

        list_concelhos = json.load(json_file)

    if args.start:

        start_Id = int(args.start)
    
    else:
        #USER VARIABLE
        start_Id = 1

    if args.end:

        end_Id = int(args.end)
    
    else:
        #USER VARIABLE
        end_Id = start_Id

    print("---\nProcessing Municipalities with ID's",start_Id,"to",end_Id,"(both inclusive)")

    #lista só com os concelhos que usamos nesta run
    to_process = list_concelhos[start_Id-1:end_Id]

    for concelho in to_process:

        print("---\nStarted processing:" + str(concelho['Name']) + "(ID=" + str(concelho['Id'])+")\n---")

        num_listings = scraper.get_num_listings(concelho['Url']) #número de imóveis à venda no concelho

        if num_listings%25 == 0:
            #handle case where number of listings is a multiple of 25 (and so the next page would have no listings)

            num_pages = int(num_listings/25)

        else:
            #any other case
            
            num_pages = int(num_listings/25)+1
        
        #USER VARIABLES
        ### Páginas de resultados do Concelho a serem scraped
        if args.startpage:
            start_page = int(args.startpage)
        else:

            start_page = 1 #comment and overwrite if needed

        if args.endpage:

            end_page = int(args.endpage)

        else:
            
            end_page = num_pages #comment and overwrite if needed
        ###

        #USER VARIABLES
        # Número Máximo de threads ao mesmo tempo
        if args.threads:
            max_threads = int(args.threads)
        else:
            max_threads = 3
        
        #one thread per page
        threads = list()

        print("Processing pages",start_page, "to", end_page,"(both inclusive) using at most", max_threads, "threads at a time.")

        for page_num in range(start_page,end_page+1):
            t_scraper = utils()
            t = threading.Thread(target=launch_scraper,args=(page_num,concelho,t_scraper))
            threads.append(t)
            t.start()

            while True:
                if threading.active_count()<max_threads+1: 
                    break

    print("---\nFinished all tasks. Quitting after all remaining threads finish.\n---")