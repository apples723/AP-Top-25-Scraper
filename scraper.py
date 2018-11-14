import requests
from bs4 import BeautifulSoup
import csv
import re
class rankingWeekObj(object):
	def __init__(self,week):
		self.week = week
		self.ranks = []
		headers = ["team_name", "rank"]
		self.ranks.append(headers)
	def addRanking(self, ranking):
		for rank in ranking: 
			team = rank[0]
			rank_no = rank[1]
			rank_obj = [team, rank_no]
			self.ranks.append(rank_obj)
	def getRankings(self):
		print(self.week)
		for ranks in self.ranks:
			print("%s: %s" % (ranks[1], ranks[0]))
			
class rankingYearObj(object):
	def __init__(self, year):
		self.year = year
		self.weeks = {}
	def addWeek(self, weekObj):
		self.weeks[weekObj.week] = weekObj
def findAllWeeks(soup_obj):
	filter_divs = soup_obj.find(class_="filters")
	divs = filter_divs.find_all("ul", class_="dropdown-menu")
	weeks = list()
	for obj in divs[1]:
		search = re.findall(r"\d.*", obj.string)
		if search:
			weeks.append(search[0])
	return weeks

	
def findAllAvailibleYears():
	url = "http://www.espn.com/college-football/rankings/_/poll/1/"
	req = requests.get(url)
	soup_obj = BeautifulSoup(req.content, features="html.parser")
	filter_divs = soup_obj.find(class_="filters")
	divs = filter_divs.find_all("ul", class_="dropdown-menu")
	years = list()
	for obj in divs[0]:
		search = re.findall(r"[?\d].*[?=\d]", obj.string)
		if search:
			years.append(search[0])
	return years
def GetAllRanks(year):
	year = year
	url = "http://www.espn.com/college-football/rankings/_/poll/1/year/%s" % (year)
	req = requests.get(url)
	soup_obj = BeautifulSoup(req.content, features="html.parser")
	num_weeks = findAllWeeks(soup_obj)
	yearObj = rankingYearObj(year)
	for week_num in num_weeks:
		weekObj = rankingWeekObj(week_num)
		url = "http://www.espn.com/college-football/rankings/_/poll/1/week/%s/year/%s" % (week_num, year)
		req = requests.get(url)
		soup_obj2 = BeautifulSoup(req.content, features="html.parser")
		table = soup_obj2.find("tbody")
		rows = table.find_all("tr")
		rankings = []
		for row in rows:
			team_name = row.find(class_="team-names").text
			try:
				ranking_number = row.find(class_="number").text
			except:
				ranking_number = "NotFound"
			rankings.append([team_name, ranking_number])
		weekObj.addRanking(rankings)
		yearObj.addWeek(weekObj)
	return yearObj	
def AllData():
	years = findAllAvailibleYears()
	AllYears = []
	for year in years:
		YearRanks = GetAllRanks(year)
		AllYears.append(YearRanks)
	return AllYears
def WriteToCSV(allYears):
	for data in allYears:
		keys = list(data.weeks.keys())
		csv_name = data.year + ".csv"
		with open(csv_name, "w") as csv_file:
			for key in keys:
				ranks = data.weeks[key].ranks
				writer = csv.writer(csv_file)
				writer.writerow([key, ranks])
if __name__ == '__main__':
	AllYearsData = AllData()
	WriteToCSV(AllYearsData)
