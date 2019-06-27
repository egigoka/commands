from commands import *
class State:
	link = "https://en.wikipedia.org/wiki/Special:Random"
	link = "https://en.wikipedia.org/wiki/2013_Malaysian_Grand_Prix"
output_file = Path.combine("c:", Random.string(30)+".html")
Wget.download(State.link, output_file, no_check_certificate=True, quiet=True)