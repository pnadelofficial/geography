# what I'm working on this week

## questions for friday
- * yeah let's do the github setup live
- * why is it asking me for password every time in the .py script still?

# July fixes
-  to match the Nexis Uni updates

- here I'll talk about the Nexis Uni updates - they updated their website and now element ids/css selectors or whatever aren't matching those in our script

## it starts at the group duplicates part
- * we have these options somewhere
- - Rachel is investigating which is the best grouping option

## I also made some changes to main (copy? geo2?)
- when I thought the issue was result count. so those need to be fixed
- or at least run to see if it's working
- * (my notes) - 282 added the variable result_count_selector, same with 288, 305


## search process is fixed

## what's working really well so far:

- * LoginClass
- - instantiated this way, pw is prompted before chrome opens
- - login runs (but still shows error msg, I think it's a timeout thing, will it work in a .py?)
- * NoLinkClass
- - updates work, this is great
- - consolidated into search process
- * timeline and change dates
- - so far so good
- - the stuff under here could all be in a "superclass" (??) called ~~ Download 
- - / a "subclass" (??) called ~~ class DownloadSetup

## what I'm working on next:

- * putting search process + basinclass url process together
- - I'm not sure why the error, it's saying something about currentuser?
- * I'll probably have a linkclass (basinclass) in addition to NLC, and some logic that asks whether the bcode is in basinclass (to run linkclass) and if not, run nolinkclass

- - ideally the rest of the process is the same for link and no link
- - would it be a problem/ can I grab the URL after search process
- - then store it as variable search_link and then keep the rest of the script the same?
- - can do the x timeline thing, but would have to put that back in somehow, this'll be speedier
- * should add in element exception



## QUESTIONS for 7/15
- * how can I use the click_css and send_keys the methods we did in loginclass, do I do the same thing in my next classes?
- - inheritance useful for this, a superclass ~~ "interactions"
- - can also copy-paste!
- * is Full Process (name tentative) the script "client" interacts with?
- * should we have userClass already include base paths and all that stuff? currentUser variable? I don't see why this is in main.py
- - how to refactor userClass to put it in?
- * big picture, still struggling with userinformation - like how would that go?

## github
- * make sharedwaterslab gmail (outlook?) free
- * pw = SharedWatersLab2022
- * and set up new github
- * find and delete .git file
- * push to new repository in new github
- - can be complicated, maybe do live
- * email peter when done, he'll send instructions

- other notes for github
- * maybe be pickier about which files move over


## I actually didn't send these questions  ^
- because the nexis uni snafu, so table them for now

# notes for work week of 7/15
- * next steps
- - fix group duplicates


- * didn't get to these but want to eventually:
- - I do want to add into options the iterate through the numbers for StoredLoginInformation
- - this is so not a priority but if perfection is the goal, I might want to put the basin search terms (box 3) all that pandas reading inside NoLinkClass. But I guess this depends on how much we anticipate needing to change out the search terms in the excel sheet??


## path fwd 
- I think I need help with this overarching part

        #new class "governing" with a method "reset"
        # full process fp, call fp.restart()
        #with self.number, method will increment that number +1, restart all freestanding variables but with the +1

        # set this in a class, this as the reset
        options.add_argument("user-data-dir=/tmp/storedLoginInformation" + number)
        number is a range
        when login fails
        go to next number in range, run again

## outline, each bullet is a class

- main

    - setup 
        - webdriver manager
        - options and everything
    
    - login
        - pw manager
        - same as internal user in main.py

        # setup and login drafted, in FullProcessExample.ipynb
        but there is a problem in the login, idk where, debug later
        # note also that 
        login for now assumes externalUser = False
        but can incorporate True option later

    - download

        - if download_type = pdf:
            - and then I think fullProcess will have some differences?
        - if download_type = excel:
            - 

        - excel interaction
            - check status sheet for dates (in main.py)
                - for 0 in column “finished” to find row with date range
                - set dates, convert to nexis uni format

        - check for bcode in basinclass.py
            - if yes, run base_search() download script
            - if no, run NoLinkClass()

        - search
            - SearchToMain_test.ipynb
            - or maybe it’s the search_link (could be from basinclass for NLC)

        - page setup
            - (maybe this is where we add the x in timeline, or at the end)
            - open timeline
            - change date in timeline
            - group_duplicates
            - sort_by_date
            - get result count
            - result count <1000, proceed to download


        - all the file_name actions


        - when finished download - add click x in timeline to reset (instead of going back to search step, which is how main.py is setup is just to return to the search_link defined in basinclass.py)


    - add in click x in timeline


"methods"

* superclass (inheritance)

    - download excel
        - nolink
        - basinclass
    - download pdf
        - nolink
        - basinclass

# currently the structure of single_basin_search is
- single basin search
    - base search
        - so this is where we can have those two processes
        - base search should be renamed to LinkClass maybe
    - change date
        - this will be the same no matter what
    - group duplicates
    - set sort by date
        - these two can be in a function called "nexis_sort" or something
    - get result count

    - download 
        - (use new naming convention from geo 1)
    - mark complete
    -   update status (0, 1)


# “inheritance”

    - future steps
        - to add a layer of complexity later on, maybe try to do like a “if there’s a URL …” or “if this column says URL”, use basin class, if it says search use NoLinkClass
    - and then if there’s a URL maybe print(“URL available, please use BasinClass URL-based process”

- X timeline box (instead of resetting search)



NOTES from June 28
- start thinking about this process
- somewhere to “if break, try logininformation2” …

- ask Peter
- the waiting for element piece of object orientation
    - might work for both login and timeline issues


## parallel process
    - how to implement it? do you have recommendations?
    - something in python library that can be imported (don’t need to install)
    - it’s called … multithread ?
        - they’ll need to be diff basins I’m pretty sure
    - there are packages to install “scrapey” which is for webscraping in parallel computing context
- see scrapy documentation from Peter
    - example where “parse” is is where we’d put all out selenium code
    - basically what it does is figure out parallel processing for you
    - okay this might also just be quicker so def try it

- timeline issue
    - I can give it a try with the click from css methods we created - more flexible timeout
        - the way this works in selenium:
        - javascript - server tells client there’s something that will be there but isn’t yet, but it’ll be there, just wait “promise”



and then also - how to use markdown
- add file name.md 
- # = title
- ## = subsection
- reg text
- * bullet
- - sub bullet

# Peter's outline from Friday 6/14 meeting:

## full process example
- Options...
- webdriver...

class FullProcess:
    def __init__(self, options=Options, webdriver=webdriver):
        self.number = 0
        self.temp_foldername = "storedLoginInformation" + str(self.number)
        self.options = Options...
        self.webdriver = webdriver...

    def reset(self):
        self.number += 1 # self.number = self.number + 1
        self.temp_foldername = "storedLoginInformation" + str(self.number)
        self.webdriver.close()

    def setup(self):
        # all of the free floating variables from the file


    def __call__(self):
        self.reset()
        self.setup()

fp = FullProcess()
fp()
# hit a nexus uni issue
fp()