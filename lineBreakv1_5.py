# Python 3.x
# Author: BlueM1ST
# License: MIT
# Version: 1.5
# Purpose: adds line breaks.
# Method: splits a line into words, counts their characters and adds linebreaks as needed.
# Known bug: will sometimes lock the output folder (not the files inside) so you can't delete it.
#             ^-- I assume it is something to do with listdir()

from sys import exit, path
from json import load
from os import path, listdir, makedirs
from time import sleep


# default config file name, path
CONFIG_FILE = 'config.json'
# default output dir
OUTPUT_DIR = 'output/'


def main():
    print('== Line Break Tool version 1.5 ==')
    # if the config file is not found, exit the program
    if not path.exists(CONFIG_FILE):
        print('Could not find config.json. It must be in the same directory as the program.')
        sleep(2)
        exit('Exiting.')

    # if the output directory doesn't exist, try to create it
    if not path.exists(OUTPUT_DIR):
        print('Output dir does not exist, attempting to create.')
        try:
            makedirs(OUTPUT_DIR)
            print('Successfully created output dir.')
        except:
            print('Could not create output dir.')
            sleep(2)
            exit('Exiting.')
    lineBreak()


def lineBreak():
    # open the config file
    config = load(open(CONFIG_FILE, encoding='utf_8'))
    try:
        fileDirectory = config['fileDirectory']

        # make sure the directory is valid
        if not path.exists(fileDirectory):
            if fileDirectory == '':
                fileDirectory = '.'
            else:
                print('Could not find the directory \"{}\", please check to make sure it is correct.'
                      .format(fileDirectory))
                sleep(2)
                exit('Exiting.')
    except:
        print('Could not find the file directory defined in config.json')
        sleep(2)
        exit('Exiting.')

    # load values from config.json
    try:
        charMax = int(config['maxCharacters'])
        breakCharacter = config['breakCharacter']
        fileTypes = config['fileTypes'].split(', ')
        # if no file types are defined, exit the program
        if fileTypes == ['']:
            print('No file types have been defined in config.json.')
            sleep(2)
            exit('Exiting.')
        selectedType = config['chosenType']
        skipCountCharacters = config['skipCountCharacters'].split(', ')
        if skipCountCharacters == ['']:
            skipCountCharacters = ''
        setEncoding = config['encoding']
        cleanupEnabled = config['enableCleanup']
        lineTypeIgnoreJson = config[selectedType]
        lineTypeIgnoreList = []
        for key, value in lineTypeIgnoreJson.items():
            lineTypeIgnoreList.append(value)
    except:
        print('Some values in config.json can not be found or are entered incorrectly.')
        sleep(2)
        exit('Exiting')

    for file in listdir(fileDirectory):
        if file.endswith(tuple(fileTypes)):
            # check and handle different encodings
            try:
                openFile = open(path.join(fileDirectory, file), 'r', encoding=setEncoding)
            except:
                try:
                    openFile = open(path.join(fileDirectory, file), 'r', encoding='utf_8')
                    print('Opened the file in utf-8 instead of {}.'.format(setEncoding))
                except UnicodeDecodeError:
                    print('Could not decode file \"{}\", set a different encoding in config.json'.format(file))
                    continue

            readFile = openFile.readlines()

            outputFile = open(OUTPUT_DIR + file, 'w', encoding=setEncoding)
            for line in readFile:
                if any(x in line for x in lineTypeIgnoreList):
                    outputFile.write(line)

                else:
                    # if cleanup is enabled in the config
                    if cleanupEnabled == 'true':
                        # remove existing break characters
                        line = line.replace(breakCharacter, '')

                        # replace double spaces with single spaces
                        line = line.replace('  ', ' ')

                        # replace those weird ellipses'
                        line = line.replace('…', '...')

                    # split the string into a list of words
                    wordList = line.split(' ')
                    characterCount = 0
                    finishedLine = ''
                    for word in wordList:
                        # count the characters in the word, add one for the space that was taken out
                        characterCount += len(word) + 1
                        # if the word has characters than are set to be skipped, subtract them from the count
                        if any(x in word for x in skipCountCharacters):
                            for value in skipCountCharacters:
                                if value in word:
                                    subtract = len(value)
                                    characterCount -= subtract
                        # if the character count exceeds the maximum allowed
                        if characterCount > charMax:
                            finishedLine += breakCharacter
                            characterCount = 0
                            characterCount += len(word) + 1
                            finishedLine += word
                            continue
                        finishedLine += ' ' + word
                    # remove the space at the beginning of the string
                    outputFile.write(finishedLine[1:])

            openFile.close()
            outputFile.close()
            print('Successfully added line breaks to \"{}\".'.format(file))

        else:
            print('File \"{}\" was skipped over.'.format(file))
            continue


main()
