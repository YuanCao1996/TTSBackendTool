from extractNaSentence import extractNaSentence
import updateLeResultToOrgFile as UR
import utils

if __name__ == '__main__':
    originalTrainTxt = r"D:\data\prcess_audiobook\FeatureExtract\Xiaotang_new_recording\Mixlingual\wav_mel\mel_0.05_0.1\train_reid.txt"
    outDataPath = r"D:\Work\zh-CN_checkna\Xiaotang\Mixlingual"
    wavePath = r"D:\data\prcess_audiobook\FeatureExtract\hmtx_erhua\Data\Wave16kNormalize"
    LEResult = r"D:\Work\zh-CN_checkna\Xiaotang\export-xiaomo.json"
    xmlPath=r"D:\data\prcess_audiobook\FeatureExtract\Xiaotang_new_recording\Mixlingual\Data\XmlScripts"
    bookId = '25'

    # extractNaSentence(originalTrainTxt, outDataPath,wavePath)
    # UR.updateToTrainTxt(originalTrainTxt, outDataPath, LEResult)
    # UR.updateToXml(xmlPath,outDataPath, LEResult, bookId)
    # print(utils.getWaveLength(wavePath))
