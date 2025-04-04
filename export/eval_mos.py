import json
import os
import csv
import numpy as np
import collections


ResultsExt = ".txt"
ResultsFolder = "/home/yfliu/simbeaqlejs/results/"

# Check if folder with results exists and retrieve list of all result files
if os.path.exists(ResultsFolder):
    dirListing = os.listdir(ResultsFolder)
    dirListing = [name for name in dirListing if name.endswith(ResultsExt)]
    if len(dirListing) < 1:
        print("ERROR: empty ResultsFolder!")
        raise SystemExit()
else:
    print("ERROR: invalid ResultsFolder!")
    raise SystemExit()

# Import and decode all result files
ResJSONList = list()
ResMetaData = list()
for ResFileName in dirListing:
    ResFile = open(os.path.join(ResultsFolder, ResFileName))
    ResMetaStruct = collections.OrderedDict()
    ResMetaStruct['FileName'] = ResFileName
    ResMetaStruct['UserID'] = -1
    ResMetaStruct['UserName'] = ""
    ResMetaStruct['UserEmail'] = ""
    ResMetaStruct['UserComment'] = ""
    try:
        ResJSONList.append(json.load(ResFile))
        ResMetaData.append(ResMetaStruct)
    except:
        print(os.path.join(ResultsFolder, ResFileName) + " is not a valid JSON file.")
    finally:
        ResFile.close()

# Group results by test sets
numResults = len(ResJSONList)
RatingsDict = dict()
RuntimesDict = dict()
for n, ResJSONData in enumerate(ResJSONList):
    ResMetaData[n]['UserID'] = n
    for i in range(0, len(ResJSONData)):
        if 'TestID' in ResJSONData[i]:
            testID = ResJSONData[i]['TestID']

            if testID not in RatingsDict:
                RatingsDict[testID] = dict()

            if testID not in RuntimesDict:
                RuntimesDict[testID] = list()

            # if runtime entry exists
            if 'Runtime' in ResJSONData[i]:
                RuntimesDict[testID].append(ResJSONData[i]['Runtime'])

            # if rating entry exists
            if 'rating' in ResJSONData[i]:
                for testItem in ResJSONData[i]['rating']:
                    if testItem not in RatingsDict[testID]:
                        RatingsDict[testID][testItem] = list()
                    RatingsDict[testID][testItem].append(ResJSONData[i]['rating'][testItem])

        elif 'UserComment' in ResJSONData[i]:
            ResMetaData[n]['UserName'] = ResJSONData[i]['UserName']
            ResMetaData[n]['UserEmail'] = ResJSONData[i]['UserEmail']
            ResMetaData[n]['UserComment'] = ResJSONData[i]['UserComment']

# write csv file with metadata to map columns of the CSV file
CsvFile = open('metadata.csv', 'w')
fieldnames = ResMetaData[0].keys()
CsvWriter = csv.DictWriter(CsvFile, fieldnames=fieldnames, delimiter="\t")
for ResMetaStruct in ResMetaData:
    try:
        CsvWriter.writerow(ResMetaStruct)
    except:
        pass
CsvFile.close()

# plot and evaluate every single test set, output results to a csv file
numTests = sum(1 for dict in ResJSONList[0] if 'TestID' in dict)
for testID in sorted(RatingsDict, key=lambda s: s.lower()):

    # write test set results to a csv file
    CsvFile = open(testID + '.csv', 'w')
    CsvWriter = csv.writer(CsvFile)

    testResArr = None
    labels = list()
    for testDataKey in sorted(RatingsDict[testID], key=lambda s: s.lower()):
        testData = RatingsDict[testID][testDataKey]
        row = list()
        row.append(testDataKey)
        row.extend(testData)
        CsvWriter.writerow(row)
        npTestData = np.array(testData)
        labels.append(testDataKey)
        if testResArr is None:
            testResArr = npTestData
        else:
            testResArr = np.column_stack((testResArr, npTestData.T))

    CsvFile.close()



import numpy as np

def calculate_mos_and_ci(scores):
    n = len(scores)
    mean = np.mean(scores)
    std = np.std(scores, ddof=1)  # Sample standard deviation
    ci = 1.96 * (std / np.sqrt(n))  # 95% confidence interval
    return mean, ci

combined_scores = {}
for test_name, categories in RatingsDict.items():
    for category, scores in categories.items():
        if category not in combined_scores:
            combined_scores[category] = []
        combined_scores[category].extend(scores)

final_mos_scores = {}
for category, scores in combined_scores.items():
    mean, ci = calculate_mos_and_ci(scores)
    final_mos_scores[category] = f"{mean:.2f}±{ci:.2f}"

print("Overall Similarity Scores:")
for category, mos_score in final_mos_scores.items():
    print(f"{category}: {mos_score}")
