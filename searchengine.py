from bs4 import BeautifulSoup
import urllib.request
wiki="https://en.wikipedia.org/wiki/List_of_state_and_union_territory_capitals_in_India"
#print("%s %s"%(tocrawl[i][0],tocrawl[i][1]))
index={}
graph={}

def getURL(page):                                      #get all urls from page
    start_link = page.find("a href")
    if start_link == -1:
        return None
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url, end_quote

def get_src_code(url):                                  #check if the page has loaded successfully
    while(1):
        src_code=urllib.request.urlopen(url)
        return src_code
        #except HTTPError as e:
         #   print('Error code: ', e.code)
           # get_src_code(url) """
        #except URLError as e:
         #   print('Reason: ', e.reason)
          #  get_src_code(url)

def graph_form(url):                                    #Form the graph of connected pages
    if tocrawl[i] not in graph:
        graph[tocrawl[i]]=[x]
    else:
        graph[tocrawl[i]].append(x)

ranks={}
def Urank(graph):                                       #For Ranking Of Pages
    global ranks
    d=.8
    numloops=10
    npages=len(graph)
    for page in graph:
        ranks[page]=1/npages
    for i in range(numloops):
        newranks={}
        for page in graph:
            newrank=(1-d)/npages
            for node in graph:
                if page in graph[node]:
                    newrank+=d*(ranks[node]/len(graph[node]))
            newranks[page]=newrank
        ranks=newranks

#wiki=input("Enter Source Page:-")
sumto=0
sum=0
tocrawl=[wiki]
crawled=[]
visited={}
union={wiki:1}
i=0
j=0
count1=1
count2=0

while i<len(tocrawl) and j<3:                             #main()work of calling functions
    if tocrawl[i] not in visited.keys():
        if "https:"==tocrawl[i][:6]:
            page=get_src_code(tocrawl[i])
            #html1=page.read().decode('utf-8')
            visited[tocrawl[i]]=1
            crawled.append(tocrawl[i])
            sum+=1
            all_links=[]
            soup=BeautifulSoup(page,"lxml")
            all_links=soup.find_all("a")
            """while True:
                url, n = getURL(html1)
                html1= html1[n:]
                if url:
                    all_links.append(url)
                else:
                    break"""
            #html=page.read().decode('utf-8')
            pretty=soup.prettify()
            words=pretty.split()
            for word in words:
                if word in index:
                    index[word].append(tocrawl[i])
                else:
                    index[word]=[tocrawl[i]]
            for link in all_links:
                x=link.get("href")
                if x!=None:
                    if "https:"==x[:6]:
                        graph_form(tocrawl[i])
                        if x not in union.keys():
                            count2+=1
                            sumto+=1
                            tocrawl.append(x)
                            union[x]=1
    count1-=1
    i+=1
    if count1==0:
        j+=1
        count1=count2
        count2=0

Urank(graph)
diction={}
keyword=input("Enter the Keyword:-")
while keyword!="0":
    if keyword in index:
        for links in index[keyword]:
            value=ranks[links]
            diction[links]=value
        sort1=sorted(diction,key=diction.__getitem__)
        for i in range(len(sort1)-1,-1,-1):
            print(sort1[i])
    else:
        print(None)
    keyword=input("Do you want to search more \nif yes enter keyword else press 0:-")

#print(diction)
