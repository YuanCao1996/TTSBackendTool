from extractNaSentence import extractNaSentence
import updateLeResultToOrgFile as UR
import utils

if __name__ == '__main__':
    originalTrainTxt = r"D:\data\prcess_audiobook\FeatureExtract\CharacterVoice\xiaotang_youngfemale_erhua\wav_mel\mel_0.05_0.1\train_update_label_reid.txt"
    outDataPath = r"D:\Work\zh-CN_checkna\Xiaotang"
    wavePath = r"D:\data\prcess_audiobook\FeatureExtract\CharacterVoice\xiaotang_youngfemale_erhua\Data\Wave16kNormalize"
    LEResult = r"D:\Work\zh-CN_checkna\Yunye\export.json"
    xmlPath=r"\\ttsdata\ttsdata\zh-CN\Voices\749\AudioBook_RecordingCheck\XmlScripts"

    extractNaSentence(originalTrainTxt, outDataPath,wavePath)
    UR.updateToTrainTxt(originalTrainTxt, outDataPath, LEResult)
    UR.updateToXml(xmlPath,outDataPath, LEResult)
    print(utils.getWaveLength(wavePath))
