import optparse
import sys
import os
import xml.sax
from simple_data_handler import SimpleDataHandler


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-l", '--library-file', dest='library_file', 
                      default=os.path.expanduser('~/Music/iTunes/iTunes Music Library.xml'),
                      help='Location of iTunes library xml file')
    parser.add_option("--test", action='store_true', dest='test',
                      default=False, help='Run parser against test.xml')
    options, args = parser.parse_args()

    if options.test:
        file_loc = 'test.xml'
    else:
        file_loc = options.library_file
    
    f = open(file_loc, 'r')
    handler = SimpleDataHandler()
    
    xml.sax.parse(f, handler)

    final_item = handler.final_item

    if options.test:
        print final_item

    else:
        library = final_item
        num_tracks = len(library['Tracks'])
        num_playlists = len(library['Playlists'])
        print "Library Summary"
        print "%i tracks and %i playlists" % (num_tracks, num_playlists)
