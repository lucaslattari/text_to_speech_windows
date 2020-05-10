# coding: utf-8
import os
from pydub import AudioSegment
import stringUtils as s
from argparse import ArgumentParser
import sys

def saveMP3OfTextMicrosoft(speechText, mp3File):
    f = open("gpt2.vbs","w+")
    speechText = s.cleanSentence(speechText)
    speechText = speechText.replace("\"", "")
    speechText = speechText.replace("\'", "")
    f.writelines(["Const SAFT48kHz16BitStereo = 39\n",
        "Const SSFMCreateForWrite = 3\n",
        "Dim oFileStream, oVoice\n",
        "Set oFileStream = CreateObject(\"SAPI.SpFileStream\")\n",
        "oFileStream.Format.Type = SAFT48kHz16BitStereo\n",
        "oFileStream.Open \"" + os.getcwd() + "\\temp.wav\", SSFMCreateForWrite\n",
        "Set oVoice = CreateObject(\"SAPI.SpVoice\")\n",
        "Set oVoice.AudioOutputStream = oFileStream\n",
        "oVoice.Speak \"" + speechText + "\"\n",
        "oFileStream.Close"])
    f.close()
    os.system("gpt2.vbs")

    sound = AudioSegment.from_file("temp.wav")
    sound.export(mp3File, format="mp3")
    os.remove("temp.wav")
    os.remove("gpt2.vbs")

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('file')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()

def main():
    arguments = parse_args()

    if not os.path.exists(arguments.file):
        print(f'{arguments.file} não existe (not found)')
        return

    f = open(arguments.file)
    fl = f.readlines()
    text = ""
    for x in fl:
        text += " " + x
    saveMP3OfTextMicrosoft(text, "output.mp3")
    f.close()

if __name__ == "__main__":
    main()
