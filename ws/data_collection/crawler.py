import httplib2
import re

def crawl_data(URL, choice='ORDERED'):
    # This is derived by oberving the raw data. If the text file
    # is download from 'ordered' link, then the data is separated
    # from description by 'Year'; otherwise, if 'ranked', the boundary
    # is 'JAN'
    if choice.upper()=='ORDERED':
        BOUNDARY = 'Year'
    else:
        BOUNDARY = 'JAN'

    h = httplib2.Http(".cache")
    resp, content = h.request(URL, "GET")

    if resp.get('status')=='200':
        content = content.decode('ascii')
        content = re.sub(r'(\r\n|\r|\n)', '\n', content)
        content = content.split(BOUNDARY)
        data_str = BOUNDARY + content[-1]

        if choice=='ORDERED':
            return parse_ordered_data(data_str)
        else:
            return parse_ranked_data(data_str)

    else:
        return ('ERROR', 'Data is NOT available')


def parse_ordered_data(data_str):
    """ Parsing ordered data set """
    DataBuffer = []
    ParsedList = data_str.splitlines()
    LabelStr = ParsedList[0]
    DataStrSet = ParsedList[1:]
    
    Labels = LabelStr.split(' ')
    Labels = [V for V in Labels if V != '']
    DataBuffer.append(Labels)
    for DataStr in DataStrSet:
        Data = DataStr.split(' ')
        Data = [V for V in Data if V != '']
        ValueBuffer = []
        FirstIsYear = True
        for ValStr in Data:
            if FirstIsYear:
                try:
                    ValueBuffer.append(int(ValStr))
                except ValueError:
                    # Here, we need to log message.
                    return ('ERROR', 'Invalid raw data format')
                FirstIsYear = False
            else:
                try:
                    Val = float(ValStr)
                except ValueError:
                    Val = None
                ValueBuffer.append(Val)
        DataBuffer.append(ValueBuffer)

    return  ('OK', DataBuffer)

def parse_ranked_data(data_str):
    DataBuffer = []
    ParsedList = data_str.splitlines()
    LabelStr = ParsedList[0]
    DataStrSet = ParsedList[1:]

    Labels = LabelStr.split(' ')
    Labels = [V for V in Labels if V != '']
    GroupedLabels = []

    while Labels:
        NewLabel = tuple(Labels[0:2])
        Labels = Labels[2:]
        GroupedLabels.append(NewLabel)

    DataBuffer.append(GroupedLabels)
    
    for DataStr in DataStrSet:
        GroupedValSet = []
        ValStrSet = DataStr.split(' ')
        ValStrSet = [V for V in ValStrSet if V != '']
        while ValStrSet:
            GroupedValStr = ValStrSet[0:2]

            try:
                Year = int(GroupedValStr[1])
            except ValueError:
                return ('ERROR', 'Invalid raw data format')
            
            try:
                Val = float(GroupedValStr[0])
            except ValueError:
                Val = None

            GroupedValSet.append(tuple([Val, Year]))
            ValStrSet = ValStrSet[2:]

        GroupedValSet
        DataBuffer.append(GroupedValSet)

    return normalise_ranked_data(DataBuffer)


def normalise_ranked_data(DataList):
    """
        Normalise the parsed ranked data. It is reported in the
        format of sorted data
    """
    DataDict = {}
    ANN_LABELS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP',
                  'OCT', 'NOV', 'DEC', 'WIN', 'SPR', 'SUM', 'AUT', 'ANN']

    NormalisedBuffer = []
    NormalisedBuffer.append(['Year'] + ANN_LABELS)

    Labels = DataList[0]
    DataSet = DataList[1:]

    for D in DataSet:
        for (ML, YL), (MV, YV) in zip(Labels, D):
            AvailableData = DataDict.get(YV)
            if AvailableData is None:
                DataDict[YV] = {}
                DataDict[YV][ML] = MV
            else:
                AvailableData[ML] = MV
    Years = sorted(DataDict.keys())

    for Year in Years:
        tmp = [Year]
        Data = DataDict.get(Year)
        for M in ANN_LABELS:
            V = Data.get(M)
            tmp.append(V)
        NormalisedBuffer.append(tmp)

    return ('OK', NormalisedBuffer)
