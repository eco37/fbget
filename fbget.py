#! /usr/bin/python
# -*- coding: utf8 -*-

"""
Script that allows a user on Facebook to download profile taged pictures. '

"""

import urllib
import urllib2
import ClientCookie
import cookielib
import argparse
from os.path import expanduser

__author__    = "Max Sidenstjärna"
__copyright__ = "Copyright 2012 Max Sidenstjärna"
__license__   = "GPLv3"


#===========================================================================#
# Method that authenticates the user and creates a cookie for the session.  #
#===========================================================================#
def Login(username, password):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    resp = opener.open('http://www.facebook.com/') 
    theurl = 'http://www.facebook.com/login.php' 
    body={'email':username,'pass':password}

    txdata = urllib.urlencode(body)     
    txheaders = {'User-agent' : 'Mozilla/5.0 (Ubuntu; X11; Linux i686; rv:9.0.1) Gecko/20100101; Firefox/9.0.1'} 
 
    req = urllib2.Request(theurl, txdata, txheaders) 
    handle = opener.open(req) 
    
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
    

    handle.close()

    return opener, user[0]


#===========================================================================#
# Method for collecting  all the urls to every image.                       #
#===========================================================================#
def getAddresses( opener, url ):
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
# Method for downloading the image.                                         #
#===========================================================================#
def DownloadImage( opener, url ):

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


#===========================================================================#
# Method that handels all arguments.                                        #
#===========================================================================#
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



#===========================================================================#
# Main function.                                                            #
#===========================================================================#
if __name__ == "__main__":
    
    #print expanduser("~")+'/fbget'
    
    args = ParseArgs()

    if( args.check_files ):
        print "File check not done yet!"

    #print args.save_path
    
    (opener, userid) = Login( args.Username, args.Password )
       
    print "Profile userid: " + userid
    url = "https://www.facebook.com/media/set/?set=t." + userid + "&type=3"

    images = getAddresses( opener, url )
    
    for i in images:
        DownloadImage( opener, i )
    


