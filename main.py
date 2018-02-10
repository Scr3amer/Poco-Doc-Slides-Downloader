import urllib.request
import time

if __name__ == "__main__":
    # Configuration variables.
    SAVE_FOLDER_PATH        = './' # Be sure that the folder exists. Otherwise it will crash. That's why I take the current directory as a default one.
    BUFFER_SIZE             = 8192
    POCO_DOCUMENTATION_URL  = 'https://pocoproject.org/documentation/index.html'
    POCO_ROOT_URL           = 'https://pocoproject.org/'

    print("### Start downloading POCO Documentation slides ###")
    
    print("Fetch the documentation webpage...")
    startingTime    = time.perf_counter()
    response        = urllib.request.urlopen(POCO_DOCUMENTATION_URL)
    webpageData     = response.read()
    webpageData     = webpageData.decode("utf-8")

    occurences = webpageData.count(".pdf")
    print("{} PDFs found".format(occurences))
    print('Extracting URLs...')

    extensionStartingSearchIndex = 0 # Used to know where we are in the HTML not to take twice the same PDF.
    for pdfProcessed in range(1,occurences + 1):
        finalExtensionIndex             = webpageData.find('.pdf', extensionStartingSearchIndex)
        startingPDFUrlIndex             = webpageData.rfind('href="', extensionStartingSearchIndex, finalExtensionIndex)
        startingPDFUrlIndex             += len('href="')
        finalExtensionIndex             += len('.pdf')
        fileToDownloadURL               = webpageData[startingPDFUrlIndex : finalExtensionIndex]
        extensionStartingSearchIndex    = finalExtensionIndex

        if(not fileToDownloadURL.startswith('http')):
            fileToDownloadURL = POCO_ROOT_URL + fileToDownloadURL

        filename            = fileToDownloadURL[fileToDownloadURL.rfind('/')+1:]
        fileToDownload      = urllib.request.urlopen(fileToDownloadURL)
        fileSize            = fileToDownload.length
        finalSavedFilePath  = SAVE_FOLDER_PATH + filename
        fileOnDisk          = open(finalSavedFilePath, 'wb')

        downloadSize = 0
        print('Downloading Pdf #{0}'.format(pdfProcessed) + ' : ' + filename + ' to ' + finalSavedFilePath)
        cumulatedEffectiveDLTime = 0
        while True:
            startDLTime = time.perf_counter()
            buffer = fileToDownload.read(BUFFER_SIZE)
            cumulatedEffectiveDLTime += (time.perf_counter() - startDLTime)
            if not buffer:
                break

            downloadSize += len(buffer)
            fileOnDisk.write(buffer)
            print("[{:.2f}KB / {:.2f}KB] ({:.2f}%) {:.2f}KB/s".format(downloadSize/1000, fileSize/1000, downloadSize/fileSize*100, downloadSize / cumulatedEffectiveDLTime / 1000))

        fileOnDisk.close()
        print('Downloaded')
        print()

    endingTime = time.perf_counter()
    print("### Finished downloading POCO Documentation slides - {:.2f}s ###".format(endingTime - startingTime))
