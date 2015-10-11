# encoding: utf-8
'''
This package uses the EDICT and KANJIDIC dictionary files. (see http://www.csse.monash.edu.au/~jwb/kanjidic.html)
These files are the property of the Electronic Dictionary Research and Development Group,
and are used in conformance with the Group's licence.
'''
import os.path
import pickle
import xml.etree.ElementTree as ET
from collections import OrderedDict
from math import sqrt

tree = ET.parse('kanjidic2.xml')
root = tree.getroot()
masterDictionary = OrderedDict()

if not os.path.isfile("kanjiPickle.p"):
    for kanji in root.findall('character'):
        if kanji[3].find('grade') is not None:
            tempdict = OrderedDict()
            tempdict["grade"] = int(kanji[3].find('grade').text)
            symbol = kanji.find('literal').text
            try:
                tempdict["freq"] = int(kanji[3].find('freq').text)
            except:
                tempdict["freq"] = "NA"

            try:
                tempdict["jlpt"] = int(kanji[3].find('jlpt').text)
            except:
                tempdict["jlpt"] = "NA"

            for node in kanji.find('dic_number'):
                if node.attrib["dr_type"] == "nelson_c":
                    tempdict["Nelson"] = node.text
                elif node.attrib["dr_type"] == "oneill_kk":
                    tempdict["O'Neill"] = node.text
                else:
                    pass

            meaning = []
            onyomi = []
            kunyomi = []
            nanori = []

            for child in kanji.find('reading_meaning')[0]:
                #python seems to behave badly with series of if statements,
                #preferred this to be set up as if, elif, elif, else
                if (child.tag == "meaning") and (child.attrib == {}):
                    meaning.append(child.text)
                elif ("r_type" in child.attrib) and (child.attrib["r_type"] == "ja_on"):
                    onyomi.append(child.text)
                elif ("r_type" in child.attrib) and (child.attrib["r_type"] == "ja_kun"):
                    kunyomi.append(child.text)
                else:
                    pass

            #nanori is in a different level of the xml file
            for child in kanji.find('reading_meaning'):
                if child.tag == "nanori":
                    nanori.append(child.text)
                else:
                    pass

            tempdict["ja_on"] = onyomi
            tempdict["ja_kun"] = kunyomi
            tempdict["meaning"] = meaning
            tempdict["nanori"] = nanori

            masterDictionary[symbol] = tempdict
    pickle.dump(masterDictionary, open("kanjiPickle.p", "wb"))
else:
    masterDictionary = pickle.load(open("kanjiPickle.p", "rb"))

print(len(masterDictionary), "\n")

#putting together a list of characters that are not kanji
kana = 'ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖー'
kana += 'ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶヷヸヹヺ・ー'
punct = '。、「」　（）'
alphaNum = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 '
notKanji = kana + punct + alphaNum

#may want to just use numpy in the future.
def avg(x):
    return sum(x)/len(x)

def variance(x):
    '''
    returns the variance for a list of numbers
    '''
    x_bar = avg(x)
    squareDiffList = [(x_i - x_bar)**2 for x_i in x]
    return sum(squareDiffList)/(len(squareDiffList) - 1)

def sd(x):
    '''
    returns the standard deviation for a list of numbers
    '''
    return sqrt(variance(x))

def correlation(tuplist):
    '''
    returns the correlation coefficient of a list of tupples
    '''
    x_list = [item[0] for item in tuplist]
    y_list = [item[1] for item in tuplist]
    x_bar = avg(x_list)
    s_x = sd(x_list)
    y_bar = avg(y_list)
    s_y = sd(y_list)
    n = len(tuplist)
    numerator_list = [(item[0] - x_bar) * (item[1] - y_bar) for item in tuplist]
    r = sum(numerator_list)/((n-1) * s_x * s_y)
    return r

def strip(text):
    for char in text:
        if char in notKanji:
            text = text.replace(char, "")
    return text

def gradeStats(text):
    text = strip(text)
    charArray = []
    for char in text:
        if char in masterDictionary:
            grade = int(masterDictionary[char]["grade"])
            charArray.append(grade)
        else:
            pass
    return [avg(charArray), variance(charArray), sd(charArray), len(charArray)]

def jlptStats(text):
    text = strip(text)
    charArray = []
    for char in text:
        if (char in masterDictionary) and (masterDictionary[char]["jlpt"] != 'NA'):
            jlpt = int(masterDictionary[char]["jlpt"])
            charArray.append(jlpt)
        else:
            pass
    return [avg(charArray), variance(charArray), sd(charArray), len(charArray)]

def frequncyStats(text):
    text = strip(text)
    charArray = []
    for char in text:
        if (char in masterDictionary) and (masterDictionary[char]["freq"] != "NA"):
            frequency = int(masterDictionary[char]["freq"])
            charArray.append(frequency)
        else:
            pass
    return [avg(charArray), variance(charArray), sd(charArray), len(charArray)]

marsArticle = open("火星.txt", "r").read()
print("Article about Mars from Japanese Wikipedia: \n",
      "Grade Level Stats: ", gradeStats(marsArticle), "\n",
      "JLPT Level Stats: ", jlptStats(marsArticle), "\n",
      "Character Frequency Stats: ", frequncyStats(marsArticle), "\n\n")

historyArticle = open("戦国時代.txt", "r").read()
print("Article on the Warring-States Period from Japanese Wikipedia: \n"
      "Grade Level Stats: ", gradeStats(historyArticle), "\n",
      "JLPT Level Stats: ", jlptStats(historyArticle), "\n",
      "Character Frequency Stats: ", frequncyStats(historyArticle), "\n\n")

jinmeiyouKanji = '''
丑 丞 乃 之 乎 也 云 亘‐亙 些 亦 亥 亨 亮 仔 伊 伍 伽 佃 佑 伶 侃 侑 俄 俠 俣 俐 倭 俱 倦 倖 偲 傭 儲 允 兎
兜 其 冴 凌 凜‐凛 凧 凪 凰 凱 函 劉 劫 勁 勺 勿 匁 匡 廿 卜 卯 卿 厨 厩 叉 叡 叢 叶 只 吾 吞 吻 哉 哨 啄 哩
喬 喧 喰 喋 嘩 嘉 嘗 噌 噂 圃 圭 坐 尭‐堯 坦 埴 堰 堺 堵 塙 壕 壬 夷 奄 奎 套 娃 姪 姥 娩 嬉 孟 宏 宋 宕 宥
寅 寓 寵 尖 尤 屑 峨 峻 崚 嵯 嵩 嶺 巌‐巖 巫 已 巳 巴 巷 巽 帖 幌 幡 庄 庇 庚 庵 廟 廻 弘 弛 彗 彦 彪 彬 徠
忽 怜 恢 恰 恕 悌 惟 惚 悉 惇 惹 惺 惣 慧 憐 戊 或 戟 托 按 挺 挽 掬 捲 捷 捺 捧 掠 揃 摑 摺 撒 撰 撞 播 撫
擢 孜 敦 斐 斡 斧 斯 於 旭 昂 昊 昏 昌 昴 晏 晃‐晄 晒 晋 晟 晦 晨 智 暉 暢 曙 曝 曳 朋 朔 杏 杖 杜 李 杭 杵
杷 枇 柑 柴 柘 柊 柏 柾 柚 桧‐檜 栞 桔 桂 栖 桐 栗 梧 梓 梢 梛 梯 桶 梶 椛 梁 棲 椋 椀 楯 楚 楕 椿 楠 楓 椰
楢 楊 榎 樺 榊 榛 槙‐槇 槍 槌 樫 槻 樟 樋 橘 樽 橙 檎 檀 櫂 櫛 櫓 欣 欽 歎 此 殆 毅 毘 毬 汀 汝 汐 汲 沌 沓
沫 洸 洲 洵 洛 浩 浬 淵 淳 渚‐渚 淀 淋 渥 湘 湊 湛 溢 滉 溜 漱 漕 漣 澪 濡 瀕 灘 灸 灼 烏 焰 焚 煌 煤 煉 熙
燕 燎 燦 燭 燿 爾 牒 牟 牡 牽 犀 狼 猪‐猪 獅 玖 珂 珈 珊 珀 玲 琢‐琢 琉 瑛 琥 琶 琵 琳 瑚 瑞 瑶 瑳 瓜 瓢 甥
甫 畠 畢 疋 疏 皐 皓 眸 瞥 矩 砦 砥 砧 硯 碓 碗 碩 碧 磐 磯 祇 祢‐禰 祐‐祐 祷‐禱 禄‐祿 禎‐禎 禽 禾 秦 秤 稀
稔 稟 稜 穣‐穰 穹 穿 窄 窪 窺 竣 竪 竺 竿 笈 笹 笙 笠 筈 筑 箕 箔 篇 篠 簞 簾 籾 粥 粟 糊 紘 紗 紐 絃 紬 絆
絢 綺 綜 綴 緋 綾 綸 縞 徽 繫 繡 纂 纏 羚 翔 翠 耀 而 耶 耽 聡 肇 肋 肴 胤 胡 脩 腔 脹 膏 臥 舜 舵 芥 芹 芭
芙 芦 苑 茄 苔 苺 茅 茉 茸 茜 莞 荻 莫 莉 菅 菫 菖 萄 菩 萌‐萠 萊 菱 葦 葵 萱 葺 萩 董 葡 蓑 蒔 蒐 蒼 蒲 蒙
蓉 蓮 蔭 蔣 蔦 蓬 蔓 蕎 蕨 蕉 蕃 蕪 薙 蕾 蕗 藁 薩 蘇 蘭 蝦 蝶 螺 蟬 蟹 蠟 衿 袈 袴 裡 裟 裳 襖 訊 訣 註 詢
詫 誼 諏 諄 諒 謂 諺 讃 豹 貰 賑 赳 跨 蹄 蹟 輔 輯 輿 轟 辰 辻 迂 迄 辿 迪 迦 這 逞 逗 逢 遥‐遙 遁 遼 邑 祁
郁 鄭 酉 醇 醐 醍 醬 釉 釘 釧 銑 鋒 鋸 錘 錐 錆 錫 鍬 鎧 閃 閏 閤 阿 陀 隈 隼 雀 雁 雛 雫 霞 靖 鞄 鞍 鞘 鞠
鞭 頁 頌 頗 顚 颯 饗 馨 馴 馳 駕 駿 驍 魁 魯 鮎 鯉 鯛 鰯 鱒 鱗 鳩 鳶 鳳 鴨 鴻 鵜 鵬 鷗 鷲 鷺 鷹 麒 麟 麿 黎
黛 鼎
'''

print("List of Jinmeiyou Kanji: \n"
      "Grade Level Stats: ", gradeStats(jinmeiyouKanji), "\n",
      "JLPT Level Stats: ", jlptStats(jinmeiyouKanji), "\n",
      "Character Frequency Stats: ", frequncyStats(jinmeiyouKanji), "\n\n")

nekodearu = open("吾輩は猫である.txt", "r").read()
print("I am Cat by Natsume Soseki: \n"
      "Grade Level Stats: ", gradeStats(nekodearu), "\n",
      "JLPT Level Stats: ", jlptStats(nekodearu), "\n",
      "Character Frequency Stats: ", frequncyStats(nekodearu), "\n\n")

'''
2998

Article about Mars from Japanese Wikipedia:
 Grade Level Stats:  [3.2952624839948785, 4.035492406750535, 2.008853505547514, 3905]
 JLPT Level Stats:  [2.588628762541806, 0.8973796683747769, 0.9473012553431864, 3887]
 Character Frequency Stats:  [398.62240451166366, 158348.84379534522, 397.93070225272294, 3901]


Article on the Warring-States Period from Japanese Wikipedia:
Grade Level Stats:  [3.854122417455107, 5.450862119606459, 2.3347081444168687, 10358]
 JLPT Level Stats:  [2.4385620273057658, 1.1383910165108666, 1.0669540836000706, 10181]
 Character Frequency Stats:  [400.32424301242236, 210281.84525906038, 458.56498477212625, 10304]


List of Jinmeiyou Kanji:
Grade Level Stats:  [9.0, 0.0, 0.0, 650]
 JLPT Level Stats:  [1.0, 0.0, 0.0, 256]
 Character Frequency Stats:  [2068.5361445783133, 102524.40654460745, 320.19432622176095, 332]


I am Cat by Natsume Soseki:
Grade Level Stats:  [3.7968692967910815, 6.734580136856841, 2.5951069605811705, 95889]
 JLPT Level Stats:  [2.67897500846153, 1.1186363377423967, 1.0576560583395704, 91591]
 Character Frequency Stats:  [513.2243434701753, 314030.2432863047, 560.384014124515, 93027]

'''