# next steps
- * new instructions for running it (notes below)
- * Git setup, organize, push, clone & pull instructions
- - organize a little bit and make sure new locations are logged so I can make changes linking to classes, for example
        make sure search terms are updated, in Git, maybe a better filename, and maybe on Box as well for version control
- - push to GitHub
- - new clone and pull instructions

## Friday Aug30 meeting
- * now that the excel script is running, I'm diving into the PDF process - I don't know how long this will take
- * would it be a good use of time to go through some GitHub best practices
- - haven't reorganized - haven't looked at others'
- - haven't pushed or updated clone/pull instructions
- - this would be a good next step because I think we now have something folks can use

## PDF process outline
- Init method could take excel status sheet,
- Create file structure,
- maybe create pdf status sheet
- Basically the same thing in download setup until download options window, then the window options are different

- notes for PDF
- * py PDF package
- * deals with the size issue of PDF

## notes for new instructions
- first it'll be the git instructions
- and any other setup instructions
- * like updating/installing pip/python/selenium/driver etc
- then it'll be the running instructions
- * change user name and basin code
- * make sure screen doesn't go to sleep


## lower priority/optional next steps

- * clean up other classes

- * timeline (which weirdly hasn't been an issue yet?? but still...)
- - maybe put this on hold because it wasn't a problem at all in testing?

- * (optional) add the tally back in? 
- - just because I'm curious where we're hitting the limit
- - like, where does the banner start to appear? how many downloads after that do we need to reset login?
- - test and save

## try to automate previously manual processes

- * Automate creating folders (only happens once, probably early in the process)
- - if f"geography/geography/downloads/{basin_code}" does not exist, create folder basin_code
- - if f"geography/geography/downloads/{basin_code}/{file_type}" does not exist, create folder {file_type}
-  would be something like
- import os 
- os.makedirs("name/of/directory", exist_ok=True)

- * automate over_thousand handling: 
- - a while loop - the way it works is while (some condition), if the condition never changes, it'll run forever, so the last row changes the condition
- - result_check function (with the number as an integer)
- - num rescheck init as 0
- - while result_check>999
- - another function slider_move
- - a method like split_over_thousand():
        "if over thousand result count 1000-2000, df append 2 rows, split timeline in half somehow (timeline slider?? or check analytics????); if 2000-3000 df append 3 rows, split in 3rds..."
- - and then if this  or whatever runs, how to handle unfinished row ...
- - maybe: mark result_count as 0 or null, but keep over_thousand as 1, mark finished=1?, create empty resultslist df in the download folder (this could have implications for combination script)

- * update/debug combination script, maybe turn it into a method I can use in the script, something like
- - if all rows = finished, or all in download match index rows in status sheet, run combination()
- - would be extremely cool if we could automate, it could tell us which are missing
- - and test that full process with one of the tiny basins

- * could even add in the excel/csv/pdf conversions?


## other questions and notes (August)
- should I make status_data a df before writing to csv? that's what David had
- - df = pd.DataFrame(status_data) 

## github
- what are the files it's using
- * running: fullprocess.py
- * downloadclass.py
- * loginclass, nolinkclass, userclass - folder from top level called classes

- geography top level



- PATH UPDATES (check in UserClass)
- * download folder is in geography/data/download
- * status folder is in geography/data/status
- * userclass - geography/geography/classes/userclass.py or classes.UserClass
- * downloadclass - geography/geography/classes/downloadclass.py or classes.DownloadClass
- * loginclass - geography/geography/classes/loginclass.py classes.LoginClass
- * nolinkclass - geography/geography/classes/NoLinkClass.py, classes.NoLinkClass

- * geography folder
- - full process there
- - search_terms.xlsx
- - classes folder containing downloadclass, userclass, nolinkclass, loginclass
- * data folder
- - status files
- - download folder
- * post-processing folder
- * readme.md instructions
- - and so I can write this in here
- * license
- * notebooks

- * requirements.txt 
- - just made this with pip freeze > requirements.txt

- * .gitignore 
- - anything I don't want to push, 
- - anything that's 25mb or just big

## how to actually update it 
- git status - so it's aware of my changes (just did this 8/30)
- then manually copy over changes (incl add/delete)
- git add .
- git commit -m "a message like ~this is the new thing"
- git push


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



# and then also - how to use markdown
- add file name.md 
- # = title
- ## = subsection
- reg text
- * bullet
- - sub bullet

