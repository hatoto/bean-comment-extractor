""" 
    beanParser.py
    把JAVA POJO物件中field 轉換為欄位說明
"""

import re

def parseBeanField(rsFileContent):
    """ 程式主進入點，
        傳入字串List(java檔的每一行程式)，
        回傳拆解後的內容
    """
    newLines = clearSymbols(rsFileContent)
    prefixRegex = re.compile(r'^private\s(?!static)(.+)\s(.+)(;)(.*)')
    resultList = []
    for idx, line in enumerate(newLines):
        mo = prefixRegex.search(line)
        if mo is not None:
            typeStr = lowerTypeName(mo.group(1))
            fieldName = mo.group(2)
            comment = getComment(idx, newLines)
            resultList.append('"'+fieldName + '": '+ typeStr  +' '+ comment)

    return '\n'.join(resultList)


def clearSymbols(rsFileContent):
    """  """
    newLines = []
    commentReg = re.compile(r'(.+;)\s*(/\*(.*)\*/|//.*)')
    for line in rsFileContent:
        if not isLineEmpty(line):
            line = line.replace('\n', '')
            line = line.replace('\t', '')
            line = line.strip()
            mo = commentReg.search(line) #檢查該行程式是否為欄位註解混合：private String field; /* comment */
            if mo is not None and mo.group(2) is not None:
                #欄位混註解時，把註解內容取出放在欄位內容上一行
                newLines.append(mo.group(2).strip())
                newLines.append(mo.group(1).strip())
            else:
                line = removeDefault(line)
                newLines.append(line)
    return newLines


def isLineEmpty(line):
    """ 檢查傳入內容是否為空白行 """
    return len(line.strip()) < 1 

def removeDefault(line):
    """ 若欄位有寫'='和預設值，進行移除 """
    if '@ApiModelProperty' not in line:
        if line.find('=') > -1:
            line = line[:line.find('=')]+';'
    
        if line.find(';') > -1:
            if line[-2].isspace():
                line = line[:-2]+';'
                return removeDefault(line)
    return line

def lowerTypeName(type):
    """ 把型態字串轉成小寫，如果是數值型態，全部換成number """
    primTypes = 'String,BigDecimal,Date,Integer,Boolean,boolean,int,double,long,Long'
    numberTypes = 'bigdecimal,integer,int,double,double,long,Long'
    if type in primTypes:
        type = type.lower()
        if type in numberTypes:
            type = 'number'
        return type
    return type

    

def getComment(fieldIdx, lines):
    """ 取得欄位註解 """
    commentReg = re.compile(r'/\*(.*)\*/|//.*')
    lineBefore = lines[fieldIdx-1]    
    mo = commentReg.search(lineBefore)
    if mo is not None:
        return mo.group()
    elif '@ApiModelProperty' in lineBefore:
        return '/**' + lineBefore.split('"')[-2] + '*/'
    elif '*/' in lineBefore:
        return getMultiLineComment(fieldIdx-1, lines)
    else:
        return '/** */'
    
    
def getMultiLineComment(endCommonentIdx, allLines):
    """ 取得多行欄位註解 """
    commentStartReg = re.compile(r'/\*(.*)')
    commentAll = []
    startIndex = 0;
    for i in range( endCommonentIdx - 1, -1, -1) :
        so = commentStartReg.search(allLines[i])        
        if so is not None:
            startIndex = i
            break

    for i in range( startIndex, endCommonentIdx+1):
        currLine = allLines[i];
        if i !=startIndex and i != endCommonentIdx:
            currLine = currLine.replace('*', '')
        commentAll.append(currLine)
    
    return ''.join(commentAll)




if __name__ == "__main__":
    pass