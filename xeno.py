#!/usr/bin/env python
# -*- coding: utf-8; -*-

import sys, os
import re
import enum
import time
import logging
from typing import List

import requests
from lxml import etree

logging.basicConfig(level=logging.INFO)

class XenobladeLocation(enum.Enum):
    Colony9 = enum.auto()
    TephraCave = enum.auto()
    BionisLeg = enum.auto()
    Colony6 = enum.auto()
    EtherMine = enum.auto()
    SatorlMarsh = enum.auto()
    BionisInterior = enum.auto()
    MaknaForest = enum.auto()
    FrontierVillage = enum.auto()
    ErythSea = enum.auto()
    Alcamoth = enum.auto()
    HighEntiaTomb = enum.auto()
    ValakMountain = enum.auto()
    SwordValley = enum.auto()
    GalahadFortress = enum.auto()
    FallenArm = enum.auto()
    MechonisField = enum.auto()
    CentralFactory = enum.auto()
    Agniratha = enum.auto()
    MechonisCore = enum.auto()
    PrisonIsland = enum.auto()

    def __str__(self):
        if self == XenobladeLocation.Colony9:
            return "Colony 9"
        if self == XenobladeLocation.TephraCave:
            return "Tephra Cave"
        if self == XenobladeLocation.BionisLeg:
            return "Bionis' Leg"
        if self == XenobladeLocation.Colony6:
            return "Colony 6"
        if self == XenobladeLocation.EtherMine:
            return "Ether Mine"
        if self == XenobladeLocation.SatorlMarsh:
            return "Satorl Marsh"
        if self == XenobladeLocation.BionisInterior:
            return "Bionis' Interior"
        if self == XenobladeLocation.MaknaForest:
            return "Makna Forest"
        if self == XenobladeLocation.FrontierVillage:
            return "Frontier Village"
        if self == XenobladeLocation.ErythSea:
            return "Eryth Sea"
        if self == XenobladeLocation.Alcamoth:
            return "Alcamoth"
        if self == XenobladeLocation.HighEntiaTomb:
            return "High Entia Tomb"
        if self == XenobladeLocation.ValakMountain:
            return "Valak Mountain"
        if self == XenobladeLocation.SwordValley:
            return "Sword Valley"
        if self == XenobladeLocation.GalahadFortress:
            return "Galahad Fortress"
        if self == XenobladeLocation.FallenArm:
            return "Fallen Arm"
        if self == XenobladeLocation.MechonisField:
            return "Mechonis Field"
        if self == XenobladeLocation.CentralFactory:
            return "Central Factory"
        if self == XenobladeLocation.Agniratha:
            return "Agniratha"
        if self == XenobladeLocation.MechonisCore:
            return "Mechonis Core"
        if self == XenobladeLocation.PrisonIsland:
            return "Prison Island"

    @classmethod
    def fromStr(cls, s):
        if s == "Colony 9":
            return XenobladeLocation.Colony9
        if s == "Tephra Cave":
            return XenobladeLocation.TephraCave
        if s == "Bionis' Leg":
            return XenobladeLocation.BionisLeg
        if s == "Colony 6":
            return XenobladeLocation.Colony6
        if s == "Ether Mine":
            return XenobladeLocation.EtherMine
        if s == "Satorl Marsh":
            return XenobladeLocation.SatorlMarsh
        if s == "Bionis' Interior":
            return XenobladeLocation.BionisInterior
        if s == "Makna Forest":
            return XenobladeLocation.MaknaForest
        if s == "Frontier Village":
            return XenobladeLocation.FrontierVillage
        if s == "Eryth Sea":
            return XenobladeLocation.ErythSea
        if s == "Alcamoth":
            return XenobladeLocation.Alcamoth
        if s == "High Entia Tomb":
            return XenobladeLocation.HighEntiaTomb
        if s == "Valak Mountain":
            return XenobladeLocation.ValakMountain
        if s == "Sword Valley":
            return XenobladeLocation.SwordValley
        if s == "Galahad Fortress":
            return XenobladeLocation.GalahadFortress
        if s == "Fallen Arm":
            return XenobladeLocation.FallenArm
        if s == "Mechonis Field":
            return XenobladeLocation.MechonisField
        if s == "Central Factory":
            return XenobladeLocation.CentralFactory
        if s == "Agniratha":
            return XenobladeLocation.Agniratha
        if s == "Mechonis Core":
            return XenobladeLocation.MechonisCore
        if s == "Prison Island":
            return XenobladeLocation.PrisonIsland


def scrapHTML(uri: str) -> etree._Element:
    time.sleep(1)
    Headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'}
    Res = requests.get(uri, headers=Headers)
    Res.raise_for_status()
    return etree.HTML(Res.text)

class BlockerType(enum.Enum):
    AreaClear = enum.auto()
    AreaAccess = enum.auto()
    Quest = enum.auto()
    MutualExclusiveQuests = enum.auto()
    AreaAffinity = enum.auto()
    RegisterNPC = enum.auto()
    NPCInviteToC6 = enum.auto()
    Unknown = enum.auto()

class QuestBlocker:
    def __init__(self):
        self.Type: BlockerType = None
        self.Data = None

    def __str__(self):
        if self.Type == BlockerType.AreaClear:
            return str(self.Data) + " cleared"
        if self.Type == BlockerType.AreaAccess:
            return "Access to " + str(self.Data)
        elif self.Type == BlockerType.Quest:
            return str(self.Data)
        elif self.Type == BlockerType.MutualExclusiveQuests:
            return " or ".join(str(q) for q in self.Data)
        elif self.Type == BlockerType.AreaAffinity:
            return "{} affinity at {}".format(*self.Data)
        elif self.Type == BlockerType.RegisterNPC:
            if self.Data[1]:
                return "{} registered on {} affinity chart".format(*self.Data)
            else:
                return self.Data[0] + " registered on affinity chart"
        elif self.Type == BlockerType.NPCInviteToC6:
            return self.Data + " invited to Colony 6"
        elif self.Type == BlockerType.Unknown:
            return '?' + self.Data
        else:
            raise TypeError("Invalid quest blocker type")

    def toXML(self) -> etree.ElementBase:
        Root = etree.Element("blocker")
        Root.attrib["type"] = self.Type.name
        if self.Type == BlockerType.AreaClear:
            Root.text = str(self.Data)
        elif self.Type == BlockerType.AreaAccess:
            Root.text = str(self.Data)
        elif self.Type == BlockerType.Quest:
            Root.append(self.Data.toXML())
        elif self.Type == BlockerType.MutualExclusiveQuests:
            for ele in self.Data:
                Root.append(ele.toXML())
        elif self.Type == BlockerType.AreaAffinity:
            for ele in self.Data:
                etree.SubElement(Root, "element").text = str(ele)
        elif self.Type == BlockerType.RegisterNPC:
            etree.SubElement(Root, "element").text = self.Data[0]
            if self.Data[1]:
                etree.SubElement(Root, "element").text = str(self.Data[1])
        elif self.Type == BlockerType.NPCInviteToC6:
            Root.text = str(self.Data)
        elif self.Type == BlockerType.Unknown:
            Root.text = str(self.Data)
        return Root

    @classmethod
    def fromXML(cls, node: etree.ElementBase):
        Result = cls()
        Result.Type = QuestBlocker[node.get("type")]

        if Result.Type == BlockerType.AreaClear:
            Result.Data = XenobladeLocation.fromStr(node.text)
        elif Result.Type == BlockerType.AreaAccess:
            Result.Data = XenobladeLocation.fromStr(node.text)
        elif Result.Type == BlockerType.Quest:
            QuestNode = node.find("quest-id")
            Result.Data = QuestID(
                XenobladeLocation.fromStr(QuestNode.get("location")),
                QuestNode.text)
        elif Result.Type == BlockerType.MutualExclusiveQuests:
            Result.Data = tuple(QuestID(
                XenobladeLocation.fromStr(ele.get("location")),
                ele.text) for ele in node)
        elif Result.Type == BlockerType.AreaAffinity:
            Subs = node.findall("element")
            Result.Data = (Subs[0].text, float(Subs[1].text))
        elif Result.Type == BlockerType.RegisterNPC:
            Subs = node.findall("element")
            if len(Subs) == 1:
                Result.Data = (Subs[0].text, None)
            else:
                Result.Data = (Subs[0].text,
                               XenobladeLocation.fromStr(Subs[1].text))
        elif Result.Type == BlockerType.NPCInviteToC6:
            Result.Data = node.text
        elif Result.Type == BlockerType.Unknown:
            Result.Data = node.text

        return Result

class QuestID:
    def __init__(self, loc: XenobladeLocation, name: str):
        self.Name = name
        self.Location = loc

    def __str__(self):
        return "{} ({})".format(self.Name, self.Location)

    def __hash__(self):
        return hash((self.Location, self.Name))

    def toXML(self) -> etree.ElementBase:
        Root = etree.Element("quest-id")
        Root.attrib["location"] = str(self.Location)
        Root.text = self.Name
        return Root

class XenobladeQuest:
    Cache = dict()              # URI –> quest

    def __init__(self):
        self.Name: str = ""
        self.Client: str = ""
        self.Location: XenobladeLocation = None
        self.Blockers: List[QuestBlocker] = []
        self.Link: str = ""

    @property
    def ID(self):
        return QuestID(self.Location, self.Name)

    def __hash__(self):
        return hash(self.ID)

    def __str__(self):
        return str(self.ID)

    def toXML(self) -> etree.ElementBase:
        Root = etree.Element("quest")
        Root.append(self.ID.toXML())
        etree.SubElement(Root, "client").text = self.Client
        Blockers = etree.SubElement(Root, "blockers")
        for Blocker in self.Blockers:
            Blockers.append(Blocker.toXML())
        etree.SubElement(Root, "link").text = self.Link
        return Root

    @staticmethod
    def _parseBlockers(blocker_nodes):
        def list2Strs(stuff):
            Result = []
            for ele in stuff:
                if isinstance(ele, str):
                    Result.append(ele)
                else:
                    Result += ele.xpath('text()|*//text()')
                    if ele.tail:
                        Result.append(ele.tail)
            return Result

        def getQuestID(node):
            if not hasattr(node, "tag"):
                return None

            if node.tag == 'a':
                Link = node.get("href")
            elif node.tag == 'i':
                Link = node.find('a').get("href")
            else:
                return None

            return XenobladeQuest.scrap("https://xenoblade.fandom.com" + Link).ID

        def parseBlocker(nodes):
            # `Nodes` contains a tail text from a previous <br>, plus a bunch of
            # nodes. Mostly we’ll convert these into a list of containing texts,
            # and just match the texts. But due to fact that quests fram
            # different areas may share name, we also need the <a> of the quest
            # to distiguish them. Whenever we need to do it, we’ll find the href
            # of the <a>, scrap that to find the name and location of the quest
            # (`getQuestID()`).
            logging.debug(str(nodes))
            Texts = list2Strs(nodes)
            logging.debug(str(Texts))
            Blocker = QuestBlocker()

            def unknownBlocker(the_texts):
                b = QuestBlocker()
                b.Type = BlockerType.Unknown
                b.Data = ''.join(the_texts)
                return b

            if ' or ' in Texts:
                # Example: Texts is ["A Young Captain's Trust", ' or ',
                # 'Revival']
                if len(Texts) != 3:
                    return unknownBlocker(Texts)
                Blocker.Type = BlockerType.MutualExclusiveQuests
                Blocker.Data = (getQuestID(nodes[0]), getQuestID(nodes[1]))
            elif Texts[-1].strip() == "cleared":
                # Example: Texts is ['Mechonis Core', ' cleared']
                if len(Texts) != 2:
                    return unknownBlocker(Texts)
                Blocker.Type = BlockerType.AreaClear
                Blocker.Data = XenobladeLocation.fromStr(Texts[0])
            elif '☆' in Texts:
                # Example: Texts is ['Colony 9 area ', '☆', '4¼']
                if len(Texts) != 3:
                    return unknownBlocker(Texts)
                Blocker.Type = BlockerType.AreaAffinity
                Match = re.match(r"^(.+?)( area)?$", Texts[0].strip())
                if not Match:
                    return unknownBlocker(Texts)

                Area = Match.group(1)
                if len(Texts[2]) == 1:
                    Aff = float(Texts[2])
                elif len(Texts[2]) == 2:
                    Aff = float(Texts[2][0])
                    if Texts[2][1] == '¼':
                        Aff += 0.25
                    elif Texts[2][1] == '½':
                        Aff += 0.5
                    elif Texts[2][1] == '.':
                        pass
                    else:
                        return unknownBlocker(Texts)
                else:
                    return unknownBlocker(Texts)

                Blocker.Data = (Area, Aff)

            elif len(Texts) == 2 and Texts[1].strip() == "accepted":
                Blocker.Type = BlockerType.Quest
                Blocker.Data = getQuestID(nodes[0])

            elif len(Texts) == 2 and Texts[1].strip().endswith("completed"):
                if re.match(r"\(?.* route\)? completed", Texts[1].strip()):
                    Blocker.Type = BlockerType.Quest
                    Blocker.Data = getQuestID(nodes[0])
                else:
                    return unknownBlocker(Texts)

            elif len(Texts) == 2 and Texts[0].strip().lower() == "access to":
                Blocker.Type = BlockerType.AreaAccess
                Blocker.Data = XenobladeLocation.fromStr(Texts[1])
                if Blocker.Data == None:
                    return unknownBlocker(Texts)
            elif len(Texts) == 1 and Texts[0].strip().endswith("reached"):
                Blocker.Type = BlockerType.AreaAccess
                Match = re.match(r"^(.+?) (area )?reached$", Texts[0].strip())
                if Match:
                    Blocker.Data = XenobladeLocation.fromStr(Match.group(1))
                else:
                    return unknownBlocker(Texts)
                if Blocker.Data == None:
                    return unknownBlocker(Texts)

            elif len(Texts) == 2 and Texts[1].strip().endswith("invited to Colony 6"):
                Blocker.Type = BlockerType.NPCInviteToC6
                Blocker.Data = Texts[0].strip()

            elif len(Texts) == 1:
                Text = Texts[0].strip()
                if Text.endswith("must be the active party leader"):
                    return unknownBlocker(Texts)
                elif Text.endswith("in the lead"):
                    return unknownBlocker(Texts)

                # Plain quest prerequisite
                Blocker.Type = BlockerType.Quest
                Blocker.Data = getQuestID(nodes[0])
                if Blocker.Data is None:
                    return unknownBlocker(Texts)

            elif len(Texts) == 3 and \
                 Texts[1].strip().startswith("registered") and \
                 Texts[2].strip().lower() == "affinity chart":
                # NPC register required. Example: ['Moritz', ' registered on the
                # Colony 9 area ', 'Affinity Chart'], or ['Sonia', ' registered
                # on the ', 'Affinity Chart'].
                Blocker.Type = BlockerType.RegisterNPC
                Match = re.match("registered (on|in) (the )?(.+) area", Texts[1].strip())
                if Match:
                    Blocker.Data = (Texts[0].strip(),
                                    XenobladeLocation.fromStr(Match.group(3)))
                else:
                    Blocker.Data = (Texts[0].strip(), None)

            else:
                return unknownBlocker(Texts)

            logging.debug("--> %s", Blocker)
            return Blocker

        if len(blocker_nodes) == 0:
            Text = blocker_nodes.text.strip()
            if Text.lower() == "none":
                return

        # The blockers are written as a mixure of nodes seperated by <br>s. Each
        # blocker consists not only the nodes between the two <br>s, but also
        # the tail of the former <br>.
        BlockerNodes = []
        # Of course the 1st blocker doesn’t have a <br> before it. If it has any
        # prefixing text, it’s the text of the value box.
        if blocker_nodes.text:
            BlockerNodes.append(blocker_nodes.text)

        for Node in blocker_nodes:
            if isinstance(Node, etree._Element) and Node.tag == "br":
                try:
                    Blocker = parseBlocker(BlockerNodes)
                except Exception as e:
                    logging.exception(str(e))
                    Blocker = None
                if Blocker:
                    yield Blocker
                BlockerNodes = []
                # If this <br> has a tail, it belongs to the next blocker.
                if Node.tail:
                    BlockerNodes.append(Node.tail)
            else:
                BlockerNodes.append(Node)
        try:
            Blocker = parseBlocker(BlockerNodes)
        except Exception as e:
            logging.exception(str(e))
            Blocker = None
        if Blocker:
            yield Blocker

    @classmethod
    def scrap(cls, uri: str):
        if uri in cls.Cache:
            return cls.Cache[uri]

        logging.info("Scraping %s ...", uri)
        Root = scrapHTML(uri)
        Quest = cls()
        InfoBox = Root.xpath('//div[@class="WikiaArticle"]'
                             '//aside[contains(@class, "portable-infobox")]')[0]
        Quest.Name = InfoBox.find("h2").text
        GiverValue = InfoBox.xpath('div[@data-source="giver"]'
                                   '/div[contains(@class, "pi-data-value")]')[0]
        Quest.Client = ''.join(GiverValue.xpath('text()|*//text()'))
        # LinkMaybe = GiverValue.find('a')
        # if LinkMaybe is None:
        #     Quest.Client = GiverValue.text.strip()
        # else:
        #     Quest.Client = LinkMaybe.text.strip()

        LocationNode = InfoBox.xpath(
            'div[@data-source="location"]'
            '/div[contains(@class, "pi-data-value")]')[0]
        if LocationNode.text:
            Text = LocationNode.text.strip()
            if Text.endswith('('):
                Text = Text[:-1].strip()
        else:
            Text = LocationNode.find('a').text
        # Exception: for some reason the quest “Hode Attack” lists Ether Plant
        # as location, instead of Eryth Sea.
        if Text == "Ether Plant":
            Text = "Eryth Sea"
        Quest.Location = XenobladeLocation.fromStr(Text)

        ValueNode = InfoBox.xpath(
            'div[@data-source="prereqs"]'
            '/div[contains(@class, "pi-data-value")]')[0]

        Quest.Blockers = list(cls._parseBlockers(ValueNode))
        Quest.Link = uri

        cls.Cache[uri] = Quest
        return Quest

def scrapAreaQuests(uri: str) -> List[XenobladeQuest]:
    Root = scrapHTML(uri)
    Table = Root.xpath('//div[@class="WikiaArticle"]'
                       '//table[contains(@class, "questlist")]')[0]
    # print(etree.tostring(Table, encoding="unicode", pretty_print=True))
    for Row in Table.findall('tr'):
        Cells = Row.findall("td")
        if len(Cells) != 5:
            continue

        RelURI = Cells[1].find('a').attrib["href"]
        FullURI = "https://xenoblade.fandom.com" + RelURI
        yield XenobladeQuest.scrap(FullURI)

def scrapAllQuests():
    Root = scrapHTML("https://xenoblade.fandom.com/wiki/Quest_(XC1)")
    Table = Root.xpath('//div[@class="WikiaArticle"]'
                       '//table[contains(@class, "xc1")]')[0]
    # print(etree.tostring(Table, encoding="unicode", pretty_print=True))
    for Row in Table.findall('tr'):
        Cells = Row.findall("td")
        if len(Cells) != 5:
            continue

        RelURI = Cells[0].find('a').attrib["href"]
        FullURI = "https://xenoblade.fandom.com" + RelURI
        yield from scrapAreaQuests(FullURI)

class UniqueMonster:
    def __init__(self):
        self.Name: str = ""
        self.Location: XenobladeLocation = None
        self.Level: int = 0
        self.Uri: str = ""

    def toXML(self) -> etree.ElementBase:
        Root = etree.Element("monster")
        etree.SubElement(Root, "level").text = str(self.Level)
        etree.SubElement(Root, "location").text = str(self.Location)
        etree.SubElement(Root, "name").text = self.Name
        etree.SubElement(Root, "link").text = self.Uri
        return Root

def scrapMonsters(uri: str):
    Root = scrapHTML(uri)
    Table = Root.xpath('//div[@class="WikiaArticle"]'
                       '//table[contains(@class, "xc1")]')[0]
    for Row in Table.findall('tr'):
        Cells = Row.findall("td")
        if len(Cells) == 0:
            continue
        Link = Cells[0].find('a')
        Monster = UniqueMonster()
        Monster.Name = Link.text
        Monster.Uri = "https://xenoblade.fandom.com" + Link.get("href")
        Monster.Location = XenobladeLocation.fromStr(Cells[2].find('a').text)
        Monster.Level = int(Cells[1].text)
        yield Monster

def test():
    q = XenobladeQuest.scrap("https://xenoblade.fandom.com/wiki/Hode_Attack")
    print(XenobladeQuest.Cache)
    print(etree.tostring(q.toXML(), encoding="unicode", pretty_print=True))
    # Root = etree.Element("quests")
    # for Quest in scrapAreaQuests("https://xenoblade.fandom.com/wiki/Colony_9_Quests"):
    #     Root.append(Quest.toXML())

    # print(etree.tostring(Root, encoding="unicode", pretty_print=True))

def main():
    import argparse

    Parser = argparse.ArgumentParser(description='Process some integers.')
    Parser.add_argument('Action', metavar="ACTION",
                        choices=["quests", "uniquemonsters"],
                        help='Info to scrap. Can be "quests" or "uniquemonsters".')
    Parser.add_argument('--output', '-o', dest='Output', metavar="FILE",
                        help='Save the result to FILE. Default: stdout')

    Args = Parser.parse_args()

    if Args.Action == "quests":
        Root = etree.Element("quests")
        for Quest in scrapAllQuests():
            Root.append(Quest.toXML())
    elif Args.Action == "uniquemonsters":
        Root = etree.Element("monsters")
        Monsters = list(scrapMonsters("https://xenoblade.fandom.com/wiki/Unique_Monster_(XC1)"))
        Monsters.sort(key=lambda m: (m.Location.value, m.Level))
        for m in Monsters:
            Root.append(m.toXML())

    UseStdout = False
    Coding = "unicode"
    Header = True
    if (not Args.Output) or (Args.Output == '-'):
        OutFile = sys.stdout
        UseStdout = True
        Header = False
    else:
        OutFile = open(Args.Output, 'wb')
        Coding = "utf-8"

    OutFile.write(etree.tostring(Root, encoding=Coding, pretty_print=True,
                                 xml_declaration=Header))

    if not UseStdout:
        OutFile.close()

if __name__ == "__main__":
    main()
