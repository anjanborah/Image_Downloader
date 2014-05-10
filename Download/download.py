"""
A simple programme to download images from a webpage
GitHub - https://github.com/anjanborah/Image_Downloader
Author - Anjan Borah
Copyright ( c ) 2014 Anjan Borah
"""

import sys
import urlparse
import urllib
import os

class Image_Download:
    
    def __init__(self, url):
        self.url            = url # Main URL
        self.parsed_url     = urlparse.urlsplit(self.url)
        try:
            #--------------------------------------------------#
            #   If the URL does not exist, then the programme  #
            #                    will quit                     #
            #--------------------------------------------------#
            self.file_handle    = urllib.urlopen(self.url)
        except Exception as exception:
            print >> sys.stdout, '\n\tFailed to open the URL\n'
            sys.exit(0)
        self.file_data_raw  = self.file_handle.readlines()
        self.file_data      = []
        for line in self.file_data_raw:
            #--------------------------------------------------#
            # Some HTML file contain &quot; instead of "       #
            # So the following line will replace &quot; with " #
            #+-------------------------------------------------#
            self.file_data.append(line.replace('&quot;', '"'))
        self.links          = [] #This list will be used to store all types of links
        self.filtered_links = {\
            'rgb'  : [],\
            'gif'  : [],\
            'pbm'  : [],\
            'pgm'  : [],\
            'ppm'  : [],\
            'tiff' : [],\
            'rast' : [],\
            'xbm'  : [],\
            'jpeg' : [],\
            'bmp'  : [],\
            'png'  : [],\
            'jpg'  : [],\
            'webm' : []\
        }
        self.scan_pattern = {\
            'src="'          : { 'download' : 'yes', 'start_delimiter' : '"', 'end_delimiter' : '"'},\
            'href="'         : { 'download' : 'yes', 'start_delimiter' : '"', 'end_delimiter' : '"'},\
            'url("'          : { 'download' : 'yes', 'start_delimiter' : '"', 'end_delimiter' : '"'},\
            'url('           : { 'download' : 'yes', 'start_delimiter' : '(', 'end_delimiter' : ')'},\
            'data-mobile="'  : { 'download' : 'yes', 'start_delimiter' : '"', 'end_delimiter' : '"'},\
            'data-desktop="' : { 'download' : 'yes', 'start_delimiter' : '"', 'end_delimiter' : '"'}\
        }
        for pattern in self.scan_pattern.keys():
            if self.scan_pattern[pattern]['download'] == 'yes':
                self.scan(pattern)
        #Removing the duplicate elements from the list
        self.links = list(set(self.links))
        if(len(self.links) == 0):
            print >> sys.stdout, '\nNO LINKS FOUND. QUITING\n'
            sys.exit(0)
        else:
            self.filter_links()
            self.download()
    
    def scan(self, pattern):
        #----------------------------------------------------------------------------------------------------#
        #                     This function is used to populate the list self.links                          #
        #----------------------------------------------------------------------------------------------------#
        for line in self.file_data:
            count = line.count(pattern, 0, len(line))
            if count > 0:
                start_position = 0
                try:
                    while line.find(pattern, start_position, len(line)) != -1:
                        start_position = line.find(pattern, start_position, len(line))
                        index          = start_position + len(pattern)
                        while line[index] != self.scan_pattern[pattern]['end_delimiter']:
                            index = index + 1
                        start          = start_position + len(pattern)
                        end            = index
                        self.links.append(line[start:end])
                        start_position = start_position + len(pattern)
                except Exception as exception:
                    pass
                    
    def filter_links(self):
        #----------------------------------------------------------------------------------------------------#
        #                This function is used to populate the dictionary self.filtered_links                #
        #----------------------------------------------------------------------------------------------------#
        for link in self.links:
            splited_link = os.path.basename(link).split('.')
            if len(splited_link) >= 2:
                if splited_link[len(splited_link) - 1] == 'rgb':
                    self.filtered_links['rgb'].append(link)
                if splited_link[len(splited_link) - 1] == 'gif':
                    self.filtered_links['gif'].append(link)
                if splited_link[len(splited_link) - 1] == 'pbm':
                    self.filtered_links['pbm'].append(link)
                if splited_link[len(splited_link) - 1] == 'rgb':
                    self.filtered_links['rgb'].append(link)
                if splited_link[len(splited_link) - 1] == 'pgm':
                    self.filtered_links['pgm'].append(link)
                if splited_link[len(splited_link) - 1] == 'ppm':
                    self.filtered_links['ppm'].append(link)
                if splited_link[len(splited_link) - 1] == 'tiff':
                    self.filtered_links['tiff'].append(link)
                if splited_link[len(splited_link) - 1] == 'rast':
                    self.filtered_links['rast'].append(link)
                if splited_link[len(splited_link) - 1] == 'xbm':
                    self.filtered_links['xbm'].append(link)
                if splited_link[len(splited_link) - 1] == 'jpeg':
                    self.filtered_links['jpeg'].append(link)
                if splited_link[len(splited_link) - 1] == 'bmp':
                    self.filtered_links['bmp'].append(link)
                if splited_link[len(splited_link) - 1] == 'png':
                    self.filtered_links['png'].append(link)
                if splited_link[len(splited_link) - 1] == 'jpg':
                    self.filtered_links['jpg'].append(link)
                if splited_link[len(splited_link) - 1] == 'webm':
                    self.filtered_links['webm'].append(link)    
                    
    def download(self):
        print >> sys.stdout, '\t_______________________________________________________'
        for key in self.filtered_links.keys():
            print >> sys.stdout, '\t', len(self.filtered_links[key]), '\tnumbers of ', key, ' images found'
            print >> sys.stdout, '\t_______________________________________________________'
        download_file_format = str(raw_input('\n\tEnter the file format to download - ')).lower()
        if len(download_file_format) >= 3:
            if download_file_format in self.filtered_links.keys():
                #--------------------------------------------------------------------------------------------#
                #               This portion of the code is specifically for 4chan thread                    #
                #--------------------------------------------------------------------------------------------#
                print >> sys.stdout, '\t', 'DOWNLOADING FROM - ', self.parsed_url.netloc
                print >> sys.stdout, '\t', 'WEBPAGE          - ', self.parsed_url.path, '\n'
                download_number = 1
                for link in self.filtered_links[download_file_format]:
                    #----------------------------------------------------------------------------------------#
                    #   Eg: link = //picture.website.com/folder/image.jpg                                    #
                    #   The actual URL can be -                                                              #
                    #                           ( a ) http://picture.website.com/folder/image.jpg or         #
                    #                           ( b ) https://picture.website.com/folder/image.jpg           #
                    #   To make the actual download link, we have to find out the exact url scheme, ie http  #
                    #   or https. To find the scheme of the actual URL, we have to parse the URL. Which we   #
                    #   have done in the constructor ( self.parsed_url = urlparse.urlsplit(self.url) )       #
                    #   Now we can make the actual download link as self.parsed_url.scheme+':'+ link         #
                    #----------------------------------------------------------------------------------------#
                    if link.startswith('//') == 1:
                        remote_file = self.parsed_url.scheme+':'+link
                        local_file  = os.path.basename(link)
                        try:
                            #Don't download an existing file
                            if(os.path.exists(local_file) == False):
                                print >> sys.stdout, '\tDownloading ', os.path.basename(remote_file), '...',
                                urllib.urlretrieve(remote_file, local_file)
                                print >> sys.stdout, '\r\t[\t', download_number, '\t] ', os.path.basename(remote_file), ' downloaded\t\t'
                                download_number = download_number + 1
                        except Exception as exception:
                            try:
                                os.remove(local_file)
                            except Exception as exception:
                                pass
                            print >> sys.stdout, '\t', os.path.basename(remote_file), ' not downloaded'
                    #----------------------------------------------------------------------------------------#
                    #   If the link does not start with '//', then the links may look like these             #
                    #   Eg: link = http://picture.website.com/folder/image.jpg                               #
                    #       link = https://picture.website.com/folder/image.jpg                              #
                    #       link = /folder/image.jpg                                                         #
                    #       link = image.jpg                                                                 #
                    #----------------------------------------------------------------------------------------#
                    if link.startswith('//') == False:
                        #------------------------------------------------------------------------------------#
                        #   Some times a website may contain links, whose scheme may be different from the   #
                        #   scheme of the website. In that case we have to use the link as it is             #
                        #------------------------------------------------------------------------------------#
                        link_scheme   = urlparse.urlsplit(link).scheme                                       
                        if len(link_scheme) > 0:
                            remote_file = link
                        else:
                            #--------------------------------------------------------------------------------#
                            #   If the link has scheme same as the scheme of the website, then we have use   #
                            #   the link as it is                                                            #
                            #--------------------------------------------------------------------------------#
                            if link.startswith(self.parsed_url.scheme+'://') == True:
                                remote_file = link
                            #--------------------------------------------------------------------------------#
                            #   If the link does not start with the scheme of the website then two cases are #
                            #   are possible -                                                               #
                            #                 ( a ) link = /folder/image.jpg                                 #
                            #                 ( b ) link = image.jpg                                         #
                            #   For case (a) the image is inside the folder named root/folder/               #
                            #   So the download link will be scheme+'://'+netloc+'/'+link                    #
                            #       http://  + picture.website.com + /folder/image.jpg                       #
                            #       [scheme] + [      netloc     ] + link                                    #
                            #   For case (b) the image is in the same directory as the webpage               #
                            #   So the download link will be scheme+'://'+netloc+path+link                   #
                            #       http://  + picture.website.com + /folder/ + image.jpg                    #
                            #       [scheme] + [      netloc     ] + [ path ] + link                         #
                            #--------------------------------------------------------------------------------#
                            if link.startswith(self.parsed_url.scheme+'://') == False:
                                if link.startswith('/') == True:
                                    remote_file = self.parsed_url.scheme+'://'+self.parsed_url.netloc+'/'+link
                                else:
                                    remote_file = self.parsed_url.scheme+'://'+self.parsed_url.netloc+self.parsed_url.path+link
                        local_file  = os.path.basename(link)
                        try:
                            #Don't download an existing file
                            if(os.path.exists(local_file) == False):
                                print >> sys.stdout, '\tDownloading ', os.path.basename(remote_file), '...',
                                urllib.urlretrieve(remote_file, local_file)
                                print >> sys.stdout, '\r\t[\t', download_number, '\t] ', os.path.basename(remote_file), ' downloaded\t\t'
                                download_number = download_number + 1
                        except Exception as exception:
                            try:
                                #----------------------------------------------------------------------------#
                                #   If something goes wrong in the downloading process the local file        #
                                #                              is deleted                                    #
                                #----------------------------------------------------------------------------#
                                os.remove(local_file)
                            except Exception as exception:
                                pass
                            print >> sys.stdout, '\t', os.path.basename(remote_file), ' not downloaded'
                    #----------------------------------------------------------------------------------------
            else:
                print >> sys.stdout, '\tThe file format entered by you is not supported by the programme'
        else:
            print >> sys.stdout, '\tThe file format entered by you is not supported by the programme'
    
if __name__ == '__main__':
    if sys.platform.lower().startswith( "win" ):
      os.system( "cls" )
    if sys.platform.lower().startswith( "lin" ):
      os.system( "clear" )
    try:
        print >> sys.stdout, '\t+-----------------------------------------------------+'
        url = str(raw_input('\tEnter the url - '))
        print >> sys.stdout, '\t+-----------------------------------------------------+'
        print >> sys.stdout, '\n'
        if len(url) > 0:
            object = Image_Download(url)
        else:
            print >> sys.stdout, '\nYou have to provide an URL'
    except KeyboardInterrupt as exception:
        print >> sys.stdout, '\n\n\t+-----------------------------------------------------+'
        print >> sys.stdout, '\t|             Keyboard interrupt received             |'
        print >> sys.stdout, '\t|                       QUITING                       |'
        print >> sys.stdout, '\t+-----------------------------------------------------+\n'
    except Exception as exception:
        print >> sys.stderr, '\n'
        print >> sys.stderr, '\tSomething went wrong :-('
        print >> sys.stderr, exception
        print >> sys.stderr, '\n'
        