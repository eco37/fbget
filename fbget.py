#! /usr/bin/env python
# -*- coding: utf-8 -*-
 
import urllib
import urllib2
import ClientCookie
import cookielib
import argparse

from os.path import expanduser

def Login(username, password):

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    resp = opener.open('http://www.facebook.com/') # save a cookie
    theurl = 'http://www.facebook.com/login.php' # an example url that sets a cookie, try different urls here and see the cookie collection you can make !
    body={'email':username,'pass':password}

    txdata = urllib.urlencode(body) # if we were making a POST type request, we could encode a dictionary of values here - using urllib.urlencode
    txheaders = {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'} # fake a user agent, some websites (like google) don't like automated exploration
 
    req = urllib2.Request(theurl, txdata, txheaders) # create a request object
    handle = opener.open(req) # and open it to return a handle on the url
    
    source = handle.read()
    source = source.split(' ')
 
    user = []

    for s in source:
        if 'envFlush({"user"' in s:
            s = s.split(',')
            #user.append( s[:] )

            for x in s:
                if 'user' in x:
                    x = x.split('{')

                    for y in x:
                        if 'user' in y:
                            y = y.split('"')
                            y = y[3]
                            user.append( y )
    
    #print user

    handle.close()

    return opener, user[0]

def getAddresses( opener, url ):
    print "Addresses"
    handle = opener.open( url )
    
    source = handle.read()
    source = source.split(' ')
 
    images = []

    for s in source:
        if 'http' in s:
            s = s.split('"')
            for x in s:
                if 'photo.php' in x and '.js' not in x and '.css' not in x and 'src' not in x:
                    m = x.split('<')
                    m = m[0]
                    images.append( m[:] )
    
    handle.close()
    return images


#===========================================================================#
# Class for downloading the image.                                          #
#===========================================================================#
def DownloadImage( opener, url ):

    print "Download"
    handle = opener.open( url )
    
    source = handle.read()
    source = source.split(' ')
 
    image = []

    for s in source:
        if 'http' in s:
            s = s.split('"')
            for x in s:
                if 'fbcdn-sphotos' in x and 'dl=1' in x:
                    m = x.split('<')
                    m = m[0]
                    image.append( m[:] )

    handle.close()
    print image
    print image[0]

    file_name = image[0].split('/')[-1]
    file_name = file_name[:-5]
    u = urllib2.urlopen(image[0])
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()

def ParseArgs():
    
    parser = argparse.ArgumentParser(
            description='Script that allows a user on Facebook to download profile taged pictures. '
            'Author: Max Sidenstjärna, License: GPLv3')

    parser.add_argument('Username', 
            help='Facebook profile username or mail')

    parser.add_argument('Password',
            help='Facebook profile password')

    parser.add_argument('-c', '--check-files', action='store_true', 
            dest='check_files', help='NOT YET IMPLEMENTED! check if file have been downloaded')
    
    parser.add_argument('-s', '--save-path', default=expanduser("~")+'/fbget',
            dest='save_path', help='NOT YET IMPLEMENTED! set save path, default: $HOME/fbget')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

    return parser.parse_args()



def test():
    foo = 1
    bar = 2
    return (foo,bar)


if __name__ == "__main__":
    
    #print expanduser("~")+'/fbget'
    
    args = ParseArgs()

    if( args.check_files ):
        print "File check not done yet!"

    #print args.save_path
    
    (opener, userid) = Login( args.Username, args.Password )
    
    print userid

    #images = getAddresses(opener, 'https://www.facebook.com/media/set/?set=a.1271022982571.2035475.1439770062&type=3')
    
    #for i in images:
    #    print i
    #    DownloadImage( opener, i )


