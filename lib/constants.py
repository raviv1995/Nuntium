NUNTIUM_VERSION = '0.1 (Alpha)'
COSINE_THRESHOLD = 0.15
DICE_THRESHOLD = 0.15

def clearFile():
    with open('/home/rvasista/Desktop/feed', 'w+') as f:
        f.write('')

def putInFile(A, B, matrix, cosine, dice):
    with open('/home/rvasista/Desktop/feed', 'a') as f:
        f.write('\n#########\n')
        f.write(A.get('title'))
        f.write('\n')
        f.write(A.get('summary'))
        f.write('\n\n')
        f.write(B.get('title'))
        f.write('\n')
        f.write(B.get('summary'))
        f.write('\n\n')    
        f.write(str(matrix))
        f.write('\n\n')
        f.write(str(cosine))
        f.write('\n\n')
        f.write(str(dice))
        f.write('\n\n')

def writeToFile(feeds):
    with open('/home/rvasista/Desktop/feed', 'a') as f:
        for feed in feeds:
            f.write('\n#########\n')
            f.write(feed.get('title'))
            f.write('\n')
            f.write(feed.get('summary'))
            f.write('\n')
            f.write(str(feed.get('cluster')))
            f.write('\n\n')
