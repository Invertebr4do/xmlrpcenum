#!/usr/bin/python3

import signal
import html2text
from pwn import *
import xmlrpc.client as xc
from wordpress_xmlrpc import Client
import wordpress_xmlrpc.methods as wp
from wordpress_xmlrpc.compat import xmlrpc_client

#Colors
class colors():
	END = "\033[0m"
	GREEN = "\033[0;32m\033[1m"
	RED = "\033[0;31m\033[1m"
	BLUE = "\033[0;34m\033[1m"
	YELLOW = "\033[0;33m\033[1m"
	PURPLE = "\033[0;35m\033[1m"
	TURQUOISE = "\033[0;36m\033[1m"
	GRAY = "\033[0;37m\033[1m"

def def_handler(sig, frame):
	print(colors.RED + "\n[!] Exiting..." + colors.END)
	sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

url = "http://10.10.56.64/xmlrpc.php"	#» CHANGE
user = "wpsAdmin"			#» CHANGE
password = "p4ssw0rd123$!"		#» CHANGE

try:
	client = Client(url, user, password)

except Exception as e:
	log.failure(str(e))
	sys.exit(1)

def helpPanel():
	print(colors.GREEN + "\n\t\txmlrpcenum commands" + colors.END)
	print(colors.GREEN + "─"*80 + colors.END)
	print(colors.YELLOW + '\n\tupload' + colors.TURQUOISE + "               »  " + colors.GRAY + "To upload files." +
		colors.YELLOW + '\n\tedit.post' + colors.TURQUOISE + "            »  " + colors.GRAY + "Edit an especific post." +
		colors.YELLOW + '\n\tget.methods' + colors.TURQUOISE + "          »  " + colors.GRAY + "List all existing methods." +
		colors.YELLOW + '\n\tget.users' + colors.TURQUOISE + "            »  " + colors.GRAY + "List users." +
		colors.YELLOW + '\n\tget.post' + colors.TURQUOISE + "             »  " + colors.GRAY + "To List specific(s) post(s)." +
		colors.YELLOW + '\n\tget.posts' + colors.TURQUOISE + "            »  " + colors.GRAY + "List all posts found." +
		colors.YELLOW + '\n\tget.postContent' + colors.TURQUOISE + "      »  " + colors.GRAY + "Read specific(s) post(s) in legible format." +
		colors.YELLOW + '\n\tget.postsContent' + colors.TURQUOISE + "     »  " + colors.GRAY + "Read all posts found in legible format." +
		colors.YELLOW + '\n\tget.postRawContent' + colors.TURQUOISE + "   »  " + colors.GRAY + "Read specific(s) post(s) in html format." +
		colors.YELLOW + '\n\tget.postsRawContent' + colors.TURQUOISE + "  »  " + colors.GRAY + "Read all posts found in html format." +
		colors.YELLOW + '\n\tget.postLink' + colors.TURQUOISE + "         »  " + colors.GRAY + "List specific(s) post(s) link(s)." +
		colors.YELLOW + '\n\tget.postsLink' + colors.TURQUOISE + "        »  " + colors.GRAY + "List all posts links found." +
		colors.YELLOW + '\n\tget.postStruct' + colors.TURQUOISE + "       »  " + colors.GRAY + "View the specific(s) post(s) struct(s)." +
		colors.YELLOW + '\n\tget.postsStruct' + colors.TURQUOISE + "      »  " + colors.GRAY + "View all posts found struct."
	+ colors.END)

	if sys.argv[1] == 'interactive':
		print(colors.YELLOW + '\texit' + colors.TURQUOISE + " ~ " + colors.YELLOW + "quit" + colors.TURQUOISE + "          »  " + colors.RED + "Exit." + colors.END)

def methods():
	counter = 1
	m = xc.ServerProxy(url)
	m = m.system.listMethods()
	print("")
	for i in m:
		print(colors.YELLOW + f'[{str(counter)}]' + colors.GREEN + " → " + colors.GRAY + i + colors.END)
		counter += 1

def users():
	print("")
	for u in client.call(wp.users.GetUsers()):
		print(colors.YELLOW + "[" + colors.GREEN + "+" + colors.YELLOW + "] User found" + colors.GREEN + " » " + colors.GRAY + str(u) + colors.END)

def posts():
	if command == 'get.posts':
		print("")
		for p in client.call(wp.posts.GetPosts()):
			print(colors.YELLOW + "[" + colors.GREEN + "+" + colors.YELLOW + "] Post found" + colors.GREEN + " » " + colors.GRAY + str(p) + colors.END)

	elif command == 'get.post':
		try:
			id = input(colors.BLUE + "[xmlrpcenum]" + colors.YELLOW + "(POSTS-ID)" + colors.BLUE + "> " + colors.END).rstrip().split(" ")
			print("")
			for i in id:
				print(colors.YELLOW + f'[{str(i)}]' + colors.GREEN + " →" + colors.GRAY, client.call(wp.posts.GetPost(int(i))))
		except:
			print(colors.RED + f"\n[X] Invalid post ID: {i}" + colors.END)

	elif command == 'get.postContent':
		try:
			id = input(colors.BLUE + "[xmlrpcenum]" + colors.YELLOW + "(POSTS-ID)" + colors.BLUE + "> " + colors.END).rstrip().split(" ")
			print("")
			for i in id:
				p = client.call(wp.posts.GetPost(int(i)))
				text = html2text.html2text(p.content)
				print(colors.YELLOW + f'\t«{str(i)}»' + colors.GREEN, p, colors.END)
				print("\n", text)
		except:
			print(colors.RED + f"\n[X] Invalid post ID: {i}" + colors.END)

	elif command == 'get.postsContent':
		counter = 1
		print("")
		for p in client.call(wp.posts.GetPosts()):
			p = client.call(wp.posts.GetPost(int(counter)))
			text = html2text.html2text(p.content)
			print(colors.YELLOW + f'\t[{str(counter)}]' + colors.GRAY + ":" + colors.GREEN + f'[{client.call(wp.posts.GetPost(int(counter)))}]\n' + colors.END, text, colors.END)
			counter += 1

	elif command == 'get.postRawContent':
		try:
			id = input(colors.BLUE + "[xmlrpcenum]" + colors.YELLOW + "(POSTS-ID)" + colors.BLUE + "> " + colors.END).rstrip().split(" ")
			print("")
			for i in id:
				p = client.call(wp.posts.GetPost(int(i)))
				print(colors.YELLOW + f'\n\t\t«{str(i)}»' + colors.GREEN, p, colors.END)
				print("\n", p.content)
		except:
				print(colors.RED + f"\n[X] Invalid post ID: {i}" + colors.END)

	elif command == 'get.postsRawContent':
		counter = 1
		for p in client.call(wp.posts.GetPosts()):
			print(colors.YELLOW + f'\n[{str(counter)}]' + colors.GRAY + ":" + colors.TURQUOISE + f'[{client.call(wp.posts.GetPost(int(counter)))}]' + colors.GREEN + " →" + colors.END, client.call(wp.posts.GetPost(int(counter))).content, colors.END)
			counter += 1

	elif command == 'get.postLink':
		try:
			id = input(colors.BLUE + "[xmlrpcenum]" + colors.YELLOW + "(POSTS-ID)" + colors.BLUE + "> " + colors.END).rstrip().split(" ")
			print("")
			for i in id:
				print(colors.YELLOW + f'[{str(i)}]' + colors.GREEN + " →" + colors.GRAY, client.call(wp.posts.GetPost(int(i))).link, colors.END)
		except:
			print(colors.RED + f"\n[X] Invalid post ID: {i}" + colors.END)

	elif command == 'get.postsLink':
		print("")
		for p in client.call(wp.posts.GetPosts()):
			print(colors.GREEN + " » " + colors.GRAY + p.link + colors.END)

	elif command == 'get.postStruct':
		try:
			id = input(colors.BLUE + "[xmlrpcenum]" + colors.YELLOW + "(POSTS-ID)" + colors.BLUE + "> " + colors.END).rstrip().split(" ")
			print("")
			for i in id:
				print(colors.YELLOW + f'\n[{str(i)}]' + colors.GRAY + ":" + colors.TURQUOISE + f'[{client.call(wp.posts.GetPost(int(i)))}]' + colors.GREEN + " →" + colors.END, client.call(wp.posts.GetPost(int(i))).struct, colors.END)
		except:
			print(colors.RED + f"\n[X] Invalid post ID: {i}" + colors.END)

	elif command == 'get.postsStruct':
		counter = 1
		for p in client.call(wp.posts.GetPosts()):
			print(colors.YELLOW + f'\n[{str(counter)}]' + colors.GRAY + ":" + colors.TURQUOISE + f'[{client.call(wp.posts.GetPost(int(counter)))}]' + colors.GREEN + " →" + colors.END, client.call(wp.posts.GetPost(int(counter))).struct, colors.END)
			counter += 1

	elif command == 'edit.post':
		try:
			id = input(colors.BLUE + "[xmlrpcenum]" + colors.YELLOW + "(POST-ID)" + colors.BLUE + "> " + colors.END).rstrip()
			print("")

			p = client.call(wp.posts.GetPost(int(id)))
			p.content = input(str(colors.BLUE + "[xmlrpcenum]" + colors.YELLOW + "(POST-CONTENT)" + colors.BLUE + "> " + colors.END).rstrip())
			client.call(wp.posts.EditPost(int(id), p))
			print(colors.GREEN + "\n » " + colors.GRAY + "Post " + colors.YELLOW + f'[{str(id)}]' + colors.TURQUOISE + " →" + colors.GREEN, f'[{client.call(wp.posts.GetPost(int(id)))}]', colors.GRAY + "edited successfully!" + colors.END)
		except:
			print(colors.RED + f"\n[X] Invalid post ID: {id}" + colors.END)


def upload():
	file = input(colors.BLUE + "[xmlrpcenum]" + colors.YELLOW + "(FILE-PATH)" + colors.BLUE + "> " + colors.END).rstrip()
	fn = input(colors.BLUE + "[xmlrpcenum]" + colors.YELLOW + "(FILENAME)" + colors.BLUE + "> " + colors.END).rstrip()

	with open(file, 'rb') as f:
		f = f.read()

	data = {
		'name': fn,
		'bits': f,
		'type': 'text/plain'
	}

	up = client.call(wp.media.UploadFile(data))

	print(colors.GREEN + "\n » " + colors.GRAY + "File " + colors.YELLOW + f'[{file}]' + colors.TURQUOISE + " » " + colors.GREEN + f'[{fn}]' + colors.GRAY + " uploaded successfully!" + colors.TURQUOISE + " ~»» " + colors.YELLOW + " [ID]> " + colors.GREEN + f'[{up["id"]}]' + colors.TURQUOISE + "  «~»  " + colors.YELLOW + "[LINK]>" + colors.GREEN, f'[{up["link"]}]')

def cmd(command):
	if command == "exit" or command == "quit":
		print(colors.RED + "\n[!] Exiting...\n" + colors.END)
		sys.exit(0)
	elif command == "help":
		helpPanel()
	elif command == "clear":
		print("\n"*100)
	elif command == "get.methods":
		methods()
	elif command == "get.users":
		users()
	elif command == "get.posts" or command == "get.post" or command == 'edit.post' or command == "get.postContent" or command == 'get.postsContent' or command == "get.postRawContent" or command == "get.postsRawContent" or command == "get.postLink" or command == "get.postsLink" or command == "get.postStruct" or command == "get.postsStruct" or command == "new.post":
		posts()
	elif command == "upload":
		upload()
	else:
		log.failure("Unrecognized option")

if __name__ == '__main__':

	try:
		if len(sys.argv) < 2 or len(sys.argv) > 3:
			print(colors.RED + "\n[ł] Usage: " + sys.argv[0] + colors.END)
			print(colors.RED + "̣─"*80 + colors.END)
			print(colors.BLUE + "\n\t┃  " + colors.YELLOW + "interactive" + colors.BLUE + " » " + colors.GRAY + "Switch to interactive mode" + colors.END)
			print(colors.BLUE + "\t┃  " + colors.YELLOW + "exec" + colors.BLUE + "        » " + colors.GRAY + "execute a command" + colors.END)
			print(colors.PURPLE + "\n\tUse examples:\n" + colors.END)
			print(colors.GREEN + "\t\t{}".format(sys.argv[0]) + colors.YELLOW + " interactive" + colors.END)
			print(colors.GREEN + "\t\t{}".format(sys.argv[0]) + colors.YELLOW + " exec" + colors.TURQUOISE + " help" + colors.END)
			sys.exit(1)

		elif len(sys.argv) == 2 and sys.argv[1] == 'exec':
			print(colors.RED + "\nUse: " + colors.GRAY + f"{sys.argv[0]} exec " + colors.YELLOW + "«help»" + colors.GREEN + " ~» " + colors.GRAY + "To list all comands." + colors.END)
			sys.exit(1)

		elif len(sys.argv) == 3 and sys.argv[1] == 'exec':
			command = sys.argv[2]
			cmd(command)

		elif len(sys.argv) == 2 and sys.argv[1] == 'interactive':
			print(colors.GRAY + "\n· Type help to list all commands ·" + colors.END)

			while True:
				command = input(colors.BLUE + "\n[xmlrpcenum]> " + colors.END).rstrip()
				cmd(command)

	except Exception as e:
		log.failure(str(e))
		sys.exit(1)
