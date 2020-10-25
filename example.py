import artistSpecific
import lyricsParser


# for a certain artist
songListPath = 'temp1.json'
artistSpecific.extractArtistSong('https://www.azlyrics.com/t/taylorswift.html', songListPath)
lyricsParser.parseDisplay(songListPath)

# for one song
# lyricsParser.parseSongDisplay('https://www.azlyrics.com/lyrics/taylorswift/whitechristmas.html', 'White Christmas', 'temp.json')