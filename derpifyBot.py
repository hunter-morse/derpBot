import argparse, sys, time, praw, json
from random import randrange as rr
"""
mods for steve
"""

def initReddit():
	with open('creds.json') as c:
		data = json.load(c)

	reddit = praw.Reddit(client_id = data['client_id'],
					client_secret = data['client_secret'],
					username = data['username'],
					password = data['password'],
					user_agent = data['user_agent'])
	return reddit

def derpify(message):
	rmin = 0; rmax = 3; rmod=3
	derped = message.lower()
	for i in range(len(message)):
		if(rr(rmin,rmax)%rmod == 0):
			derped = derped[:i]+derped[i].upper()+derped[i+1:]

	return derped

def grabParent(reddit, message):
	parent = message.parent()
	if(isinstance(parent, praw.models.Comment)):
		return parent.body.lower()

def parseMessage(comment, options):
	optsCalled = []
	uName = ['/u/derpifybot', 'u/derpifybot']
	for name in uName:
		if name in comment:
			uName = name

	comment=comment.split(' ')
	iArg = comment.index(uName)
	del comment[iArg]				# get rid of username
	# remove and keep track of each additional arg from the comment
	while(len(comment)):
		if (comment[iArg] in options):
			optsCalled.append(comment[iArg])
			del comment[iArg]
		else:
			break

	return(' '.join(comment), optsCalled)

def respond(reddit):
	options =['\-above']
	parsed = ('', [])

	print('responding...')
	for message in reddit.inbox.unread(limit=50):
		print('message: ' + message.body)
		if(message.subject.lower() == 'username mention'
			and isinstance(message, praw.models.Comment)):
			body = message.body.lower()
			parsed = parseMessage(body, options)
			print('parsed: ', parsed[0], parsed[1])
			
			if(options[0] in parsed[1]):
				body = grabParent(reddit, message)
			else:
				body = parsed[0]

			response = derpify(body)
			print('\n-----\n' + message.body + '\n' + response + '\n----')
			message.reply(response)
			message.mark_read()

def main(argv):
	reddit = initReddit()
	respond(reddit)
	argList={
		#dest: 		  arg,	metavar,			dest, 		def,	help
		'sub'		:['-r',	'subreddit',		'sub', 		"all",	'subreddit to scan'],
		'num_coms'	:['-c', 'comment count',	'num_coms', 10000,	'number of downvotes'],
		'num_dv'	:['-dv','downvote count',	'num_dv', 		5,	'number of downvotes']
	}

	parser = argparse.ArgumentParser()

	for arg in argList.keys():
		parser.add_argument(argList[arg][0],
			metavar=argList[arg][1],
			dest=argList[arg][2],
			default=argList[arg][3],
			type=type(argList[arg][3]),
			help=argList[arg][4])

if __name__ == "__main__":
	main(sys.argv)




