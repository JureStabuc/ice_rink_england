#!/usr/bin/env python
#import the libraries containing our functions
import scraperwiki
import lxml.html
import urllib
# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
  
  rows = root.cssselect("table#AutoNumber2 tr") #selects all <tr blocks in <table id="AutoNumber2"
  
  for row in rows[0:-1]:
    
    #Set up our data record
    
    record = {}
    table_cells = row.cssselect("td")
    
    #if there's anything in the table_cells variable (a list)
    
    if table_cells:
      
      #grab the text contents of the first and put in 'record' under the key 'Rink':
      
      record['Rink'] = table_cells[0].text_content()
      
      #grab the <a> tags in the first:
      
      rinkurls = table.cells[0].cssselect('a')
      
      #if there are any <a> tags: 
      
      if rinkurls: 
        
        #grab the first href=" attribute (the URL of the link) and put into 'rinklink'
        
        rinklink = rinkurls[0].attrib.get('href')
        
        #combine with base url and scrape into 'rinkhtml'
        rinkhtml = scraperwiki.scrape('http://www.eiharec.co.uk/'+rinklink)
        
        #convert into lxml object and put into 'rinkroot'
        
        rinkroot = lxml.html.fromstring(rinkhtml)
        
        #grab all the <td><a> tags from 'rinkroot' and put into 'rinktds'
        
        rinktds = rinkroot.cssselect('td a')
        
        #print a string followed by the 3rd href=" attribute of that list of <td>s:
        
        print "rink url from linked page:", rinktds[2].attrib.get('href')
        
        #store that value in 'record' under key 'rinklink'
        
        record['rinklink'] = rinktds[2].attrib.get('href')
        
        #these lines repeat the process earlier using the <td> tags from main page <tr>s
        
        record['Address'] = table_cells[1].text_content()
        
        #in some rows there is no table_cells[2].text_content(), so this tests the length first
        
        if len(table_cells[2].text_content())>0:
          record['Area'] = table_cells[2].text_content()
          recors['County'] = table_cells[3].text_content()
          record['Phone'] = table_cells[4].text_content()
          
          #grab all the <a> tags in these two <td>s and put in a list variable
          
          showteamsurls = table_cells[5].cssselect('a')
          
          mapurls = table_cells[6].cssselect('a')
          
          #test the length of the list before storing anything - some have no links
          
          if len(mapurls)>0:
            record ['Maplink'] = mapurls[0].attrib.get('href')
          
          else:
            record['Maplink'] = "NO MAP LINK"
            
          if len(showteamsurls)>0:
            record['teamslink'] = showteamsurls[0].attrib.get('href')
              
          else:
            record['teamslink'] = "NO MAP LINK"
            
          #Print out the data we've gathered
          
          print record, '---------------'
          
          #Finally, save the record to the datastore - 'Rink'
          
          scraperwiki.sql.save(["Rink"], record)
          
          #scrape_and_look_for_next_link function: scrapes page, converts to lxml object then calls the scrape_table function
          def scrape_and_look_for_next_link(url):
            html = scraperwiki.scrape(url)
            print html
            root = lxml.html.fromstring(html)
            scrape_table(root)
            
            starting_url = 'http://www.eiharec.co.uk/rink_list.php'
            scrape_and_look_for_next_link(starting_url)
              
            
    
        
