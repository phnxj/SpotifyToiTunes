import csv
import sys, getopt
import glob, os

def main(argv):
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'SpotifyToiTunes.py -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'SpotifyToiTunes.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg

	# If there's no provided files, search for the files automatically
	if inputfile == '' and outputfile == '':
		for file in os.listdir("."):
			if file.endswith(".txt"):
				inputfile = file
				outputfile = str.format("{}{}", "iTunes", file)
				convert(inputfile, outputfile)	
	else:
		convert(inputfile, outputfile)



def convert(inputfile, outputfile):
	with open(inputfile, 'rb') as csvin, open(outputfile, 'wb') as csvout:
		print str.format("Converting {} to {}", inputfile, outputfile)
		r = csv.reader(csvin, delimiter=',', quotechar='"')
		w = csv.writer(csvout, delimiter="\t")

		next(r, None)  # skip the first row from the reader, the old header
		# write new header
		w.writerow(['Name', 'Artist', 'Album', 'Disc Number', 'Track Number', 'Time', 'Date Added'])

		for row in r:
			print row
			del row[0]
			del row[6]
			row[5] = int(row[5]) / 1000
			row[6] = parseDate(row[6])
			w.writerow(row)

def parseDate(date):
	# From 2012-08-23T05:00:27Z to 23/08/2012
	splitted = date.split("-")
	new = str.format("{}/{}/{}", splitted[2][:2], splitted[1], splitted[0])
	return new

if __name__ == "__main__":
   main(sys.argv[1:])