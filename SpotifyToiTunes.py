import csv
import sys, getopt
import glob, os

def main(argv):
	inputfile = ''
	outputfile = ''
	directory = '.'
	try:
		opts, args = getopt.getopt(argv,"hi:o:d:",["ifile=","ofile=","directory=="])
	except getopt.GetoptError:
		print 'SpotifyToiTunes.py -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print "Usage:"
			print ''
			print 'SpotifyToiTunes.py -i <inputfile> -o <outputfile>'
			print 'SpotifyToiTunes.py -d <directory of playlists>'
			print ''
			print '-- Automatic Conversion --'
			print 'To use the automatic conversion feature, specify a directory using -d or use no arguments to use the current directory'
			print 'You also need to add the word "Spotify" in front of your exported Spotify playlist to automatically convert multiple files'
			print 'e.g. you have a directory "Playlist" with "SpotifyFirstPlaylist.txt" and "SpotifySecondPlaylist" in it,'
			print '     use "SpotifyToiTunes.py -d Playlist" to convert both of them at the same time'
			sys.exit()
		elif opt in ("-d", "--directory"):
			directory = arg
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg

	# If there's no provided files, search for the files automatically
	if inputfile == '' and outputfile == '':
		for file in os.listdir(directory):
			if file.startswith("Spotify"):
				inputfile = os.path.join(directory, file)
				outputfile = os.path.join(directory, file[7:])
				convert(inputfile, outputfile)	
	else:
		convert(inputfile, outputfile)



def convert(inputfile, outputfile):
	with open(inputfile, 'rb') as csvin, open(outputfile, 'wb') as csvout:
		print str.format("Converting {} to {}", inputfile, outputfile)
		r = csv.reader(csvin, delimiter=',', quotechar='"', skipinitialspace=True)
		w = csv.writer(csvout, delimiter="\t")

		next(r, None)  # skip the first row from the reader, the old header
		# write new header
		w.writerow(['Name', 'Artist', 'Album', 'Disc Number', 'Track Number', 'Time', 'Date Added'])

		for row in r:
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
