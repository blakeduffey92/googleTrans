import praw
import time
import goslate

def check_validLang(langCheck):
	print("Validating language...")
	found = False
	i = 0
	
	#loop through languages to check if destLang is a valid lang code
	while i < len(langList) and found != True:
		if langCheck == langList[i]:
			found = True
			return True
		i += 1
	return False

def get_translation(commentText):
	print("Parcing comment...")
	beg = None
	end = None
	transString = ""
	langString = ""
	destLang = ""
	replyStr = ""
	quoteIndex = []

	if commentText.count('"') >= 2:
		try:
			i = 0
			j = 0
			
			for i in range(commentText.count('"')):
				quoteIndex.append(commentText.index('"', j + 1))
				j = quoteIndex[i]

		except ValueError:
			print("missing quotes")
			return replyStr
	else:
		print("Missing Quotes")

	transString = commentText[quoteIndex[0] + 1:quoteIndex[-1]].strip()

	if len(transString) <= 5000: #google can only support a translation of up to 5000 characters
		langString = commentText[quoteIndex[-1] + 1:].strip()
		destLang = langString[langString.index("to") + 3:].strip()

		if destLang != "":
			if check_validLang(destLang) == True:
				print("Translating...")
				replyStr = "Translated\n\n" + ">" + transString + "\n\nto " + gs.translate("'" + transString + "'", destLang)
				replyStr += "\n\n &nbsp;\n\nThis was translated from " + languages[gs.detect(transString)] + " to " + languages[destLang] + " using Google Translate with goslate API."
				replyStr += "\n\nAll supported language codes can be found [here](https://drive.google.com/file/d/0B1cl6_p8q1VfbHd3enU4Z2RKT0k/view?usp=sharing)."
				return replyStr

			else:
				print("invalid dest lang")
				return replyStr
				
		else:
			print("no dest lang")
			return replyStr
			
	else:
		print("5000 character limit exceeded.")
		return replyStr

def run_bot():
	print("getting Subreddit")
	subreddit = r.get_subreddit("thebutton")
	print("Getting comments...")

	#limit amount of comments to 300
	comments = subreddit.get_comments(limit = 300)

	for comment in comments:

		#find comments not cached to avoid double replies
		if comment.id not in cache:

			#search comment for username call and check to make sure it isnt this bot
			if comment.body.find("/u/googleTrans") != -1 and comment.author != "googleTrans":
				commentText = comment.body.lower()
				replyStr = get_translation(commentText)
				#make sure a translation has been made before replying
				if replyStr != "":
					comment.reply(replyStr)

				#append comment id to cache
				cache.append(comment.id)
				print("appending to comment cache")

				#append comment id to cacheFile
				with open("ReplyCache.txt", "a") as cacheFile:
					cacheFile.write("\n" + cache[-1])
				cacheFile.close()

	print("sleeping")

def main():
	for i in languages:
		langList.append(i)

	print("Logging in...")

	#try to get user login info, close program if failed
	with open("UserLogin.txt", "r") as loginFile:
		r.login(loginFile.readline().replace("\n", ""), loginFile.readline().replace("\n", ""))

	#try to get comment reply id cache file, close program if failed
	with open("ReplyCache.txt", "r") as cacheFile:
		lines = cacheFile.readlines()
		for line in lines:
			cache.append(line.replace("\n", ""))

	while True:
		run_bot()
		time.sleep(10)

r = praw.Reddit(user_agent = "Google Translate Bot by Blake /u/googleTrans")
gs = goslate.Goslate()
languages = gs.get_languages()
langList = []
cache = []
main()
