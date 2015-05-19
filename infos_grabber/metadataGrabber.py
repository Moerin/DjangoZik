#!/usr/bin/python

from coverGrabber import CoverGrabber
from imageDownloader import ImageDownloader
from artistInfos import ArtistInfos


class MetadataGrabber:

    def __init__(self):
        self.cover_grabber = CoverGrabber()
        #self.artist_infos = ArtistInfos()

    def get_and_save_artist(self, keyword, destination, filename):
        infos = self.artist_infos.get(keyword, None)

        if infos['success']:
            image_downloader = ImageDownloader(destination)
            if infos['infos']['image']:
                file_path = image_downloader.download(infos['infos']['image'],
                                                      filename)
                if file_path:
                    infos['infos']['image'] = file_path
                    return infos
                else:
                    return None
            else:
                return None

    def get_and_save_cover(self, keyword, destination, filename):
        image_url = self.cover_grabber.grab(keyword)
        if image_url:
            image_downloader = ImageDownloader(destination)
            file_path = image_downloader.download(image_url, filename)
            if file_path:
                return file_path
            else:
                return None
        else:
            return None


if __name__ == "__main__":
    print "test function"
    metadata_grabber = MetadataGrabber()
    image = metadata_grabber.get_and_save_cover("black ice", "/tmp/",
                                                "black_ice.jpg")
    if image:
        print image
    else:
        print "Error"
