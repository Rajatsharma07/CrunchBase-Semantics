from bs4 import BeautifulSoup
from Scrap import readurls
import urllib2


#url = 'https://www.linkedin.com/in/benelowitz'
#page = urllib2.urlopen(url)
#soup = BeautifulSoup(page.read(),"lxml")
#print soup

myData = []

soup = BeautifulSoup(open('/Users/rajat/Desktop/linkedInProfileBen.html'), 'html.parser')
#print soup.title.string
print soup.find("div", {"class": "profile-overview-content"}).h1.get_text()
myData.append(soup.find("div", {"class": "profile-overview-content"}).h1.get_text())
print soup.find("p", {"class": "headline title"}).get_text()
myData.append(soup.find("p", {"class": "headline title"}).get_text())
print soup.find("span", {"class": "locality"}).get_text()
myData.append(soup.find("span", {"class": "locality"}).get_text())

#print soup.find("dd", {"class": "descriptor"})
#print soup.find("div", {"class": "profile-overview-content"}).dd.contents

industry = []
sections = []
for link in soup.find_all('dd',{"class": "descriptor"}):
    industry.append(link.get_text())

print (industry[1])
myData.append(industry[1])
#previous = soup.find_all("table", {"data-section": "currentPositionsDetails"})
#print previous

sCurrentPosition = []
try:
    for ul in soup.find("tr", {"data-section": "currentPositionsDetails"}):
        if ul is not None:
         for li in ul.findAll('a'):
                print li.get_text()
                sCurrentPosition.append(li.get_text())
except:
    print "None CPD"
    sCurrentPosition.append("None")

myString1 = ",".join(sCurrentPosition)
myData.append(myString1)

sPastPosition = []
try:
    for ul in soup.find("tr", {"data-section": "pastPositionsDetails"}):
        for li in ul.findAll('a'):
            print li.get_text()
            sPastPosition.append(li.get_text())
except:
    print "None PPD"
    sPastPosition.append("None")

myString2 = ",".join(sPastPosition)
myData.append(myString2)

sEducationDetail = []
try:
    for ul in soup.find("tr", {"data-section": "educationsDetails"}):
        for li in ul.findAll('a'):
            print li.get_text()
            sEducationDetail.append(li.get_text())
except:
    print "None ED"
    sEducationDetail.append("None")

myString3 = ",".join(sEducationDetail).encode('utf-8').strip()
myData.append(myString3)
#for link in previous:
    #previousWork.append(link)
    #print(link)

#print (previousWork)


for tag in soup.find_all('section'):
    if str(tag.get('id')) == 'None':
        break
    else:
        sections.append(tag.get('id'))

print sections


certificates = soup.find_all("section", {"data-section": sections[2]})
#print certificates

#for tag in soup.find("section", {"data-section": sections[2]}):
        #for data in tag:
            #print data.find('header')



#for ul in soup.find("section", {"data-section": sections[2]}):
    #for li in ul.findAll('h4'):
        #print(li.get_text())
        #print(li.h4.a.get_text())
    #for li in ul.findAll('h5'):
        #print(li.get_text())

print "-------Skills-------"
#---------------------------------Skills
sSkills = []
try:
    for ul in soup.find("section", {"id": "skills"}):
        for li in ul.findAll('a'):
            print li.get_text()
            sSkills.append(li.get_text())
except:
    print "None Skills"
    sSkills.append("None")

myString4 = ",".join(sSkills)
myData.append(myString4)

print "-------Education-------"
#---------------------------------Education
sEducationUni = []
sEducationTitle = []
try:
    for ul in soup.find("section", {"id": "education"}):
        for li in ul.findAll('h4'):
            print(li.get_text())
            sEducationUni.append(li.get_text())
            print +1
        for li in ul.findAll('h5'):
            print(li.get_text())
            sEducationTitle.append(li.get_text())
        for li in ul.findAll('time'):
            print(li.get_text())
except:
    print "None Education"
    sEducationUni.append("None")
    sEducationTitle.append("None")

myString5 = ",".join(sEducationUni)
myString6 = ",".join(sEducationTitle)
myData.append(myString5)
myData.append(myString6)

print "-------Experience-------"
# ---------------------------------Experience
sExperienceTitle = []
sExperienceCompany = []
sExperienceResponsibility = []
try:
    for ul in soup.find("section", {"id": "experience"}):
        for li in ul.findAll('h4'):
            print(li.get_text())
            sExperienceTitle.append(li.get_text())
            print +1
        for li in ul.findAll('h5'):
            print(li.get_text())
            sExperienceCompany.append(li.get_text())
        for li in ul.findAll('time'):
            print(li.get_text())
        for li in ul.findAll('p'):
            print(li.get_text())
            sExperienceResponsibility.append(li.get_text())
except:
    print "None Experience"
    sExperienceTitle.append("None")
    sExperienceCompany.append("None")
    sExperienceResponsibility.append("None")

myString7 = ",".join(sExperienceTitle)
myString8 = ",".join(sExperienceCompany)
myString9 = ",".join(sExperienceResponsibility)
myData.append(myString7)
myData.append(myString8)
myData.append(myString9)

print "-------Projects-------"
# ---------------------------------Projects
sProjectTitle = []
sProjectDescription = []
try:
    for ul in soup.find("section", {"id": "projects"}):
        for li in ul.findAll('h4'):
            print(li.get_text())
            sProjectTitle.append(li.get_text())
            print +1
        for li in ul.findAll('h5'):
            print(li.get_text())
        for li in ul.findAll('time'):
            print(li.get_text())
        for li in ul.findAll('p'):
            print(li.get_text())
            sProjectDescription.append(li.get_text())
except:
    print "None Project"
    sProjectTitle.append("None")
    sProjectDescription.append("None")

myString10 = ",".join(sProjectTitle)
myString11 = ",".join(sProjectDescription)
myData.append(myString10)
myData.append(myString11)

print "------"


#myData = myData.encode('utf-8').strip()

print len(myData)

import csv
import sys

f = open('output.csv', 'wt')
try:
    writer = csv.writer(f)
    writer.writerow( ('Name', 'CurrentTitle', 'CurrentLocation', 'Field', 'CurrentPositionDetails', 'PastPositionDetails', 'EducationDetails', 'Skills', 'EducationUniName', 'EducationUniTitle', 'ExperienceTitle', 'ExperienceCompany', 'ExperienceResponsibility', 'ProjectTitle', 'ProjectDescription') )
    writer.writerow( (myData[0], myData[1], myData[2], myData[3], myData[4], myData[5], myData[6], myData[7],myData[8], myData[9], myData[10], myData[11], myData[12], myData[13], myData[0]) )
finally:
    f.close()


readurls()

