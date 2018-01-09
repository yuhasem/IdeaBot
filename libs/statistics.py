import datetime, dataloader

def runTimeReport(discordClient, interval=3600, filename="./data/msgtimedump.csv"):
    '''(discord.Client object, int) -> list of [datetime object, int]
    interval is interpreted as seconds
    checks messages' times for data analysis purposes '''
    messages = discordClient.messages
    now = datetime.datetime.utcnow()
    results1 = [None]*((now - messages[-1].timestamp).total_seconds()//interval)
    results2 = [None]*((now - messages[0].timestamp).total_seconds()//interval)
    if len(results1) > len(results2):
        results = results1
    else:
        results = results2
    for i in range(len(results)):
        results[i] = [now-datetime.timedelta(seconds=(i*interval)%3600, hours=(i*interval)//3600), 0]
    for i in messages:
        delta = now - i.timestamp
        location = delta.total_seconds() // interval
        results[location][1] += 1
    results = [[x[0].isoformat(timespec="seconds"), x[1]] for x in results]
    msgInfoFile = dataloader.newdatafile(filename)
    msgInfoFile.content = results
    msgInfoFile.save()
    return results

def dumpMessagesTime(discordClient, filename = "./data/msgdump.csv"):
    messages = discordClient.messages
    msgFile = dataloader.newdatafile(filename)
    for i in messages:
        msgFile.content.append([i.timestamp.isoformat(timespec="seconds")])
    msgFile.save()