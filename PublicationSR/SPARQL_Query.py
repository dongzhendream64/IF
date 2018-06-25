# coding: UTF-8
from SPARQLWrapper import SPARQLWrapper, JSON
from PublicationSR.pachong import get_infor
from PublicationSR.langconv import *
from PublicationSR.recomment import film_recommend

# 转换繁体到简体
def cht_to_chs(line):
    line = Converter('zh-hans').convert(line)
    line.encode('utf-8')
    return line

# 转换简体到繁体
def chs_to_cht(line):
    line = Converter('zh-hant').convert(line)
    line.encode('utf-8')
    return line

def get_content_list(searchtxt):
    query_str = """
        PREFIX dbo:<http://dbpedia.org/ontology/>
        SELECT * WHERE{
            ?url rdfs:label ?label;
            foaf:name ?name;
            dbo:wikiPageID ?wikiPageID;
            dbo:abstract ?abstract
            OPTIONAL{?url dbo:writer ?writer}
            {?url rdf:type<http://dbpedia.org/ontology/Film>}
            UNION
            {?url rdf:type<http://dbpedia.org/ontology/Book>}
            UNION
            {?url rdf:type<http://dbpedia.org/ontology/Game>}
            filter regex(str(?label), '""" + searchtxt + "')}"
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_str)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()

    table = []
    wikiPageIDs = []
    for item in result["results"]["bindings"]:
        _item = {}
        language = item["abstract"]["xml:lang"]
        if(str(language) != str("en") and str(language) != str("zh")):
            continue

        # 同一条检索结果只需显示一次
        wikiPageID = item["wikiPageID"]["value"]
        if(wikiPageID not in wikiPageIDs):
            wikiPageIDs.append(wikiPageID)
        else:
            continue

        url = item["url"]["value"]
        _item['url'] = url

        label = item["label"]["value"]
        _item['label'] = label

        _item['name'] = add_property(item, "name")
        _item['writer'] = add_property(item, "writer")

        abstract = add_property(item, "abstract")
        strlen = len(abstract)
        if strlen > 150:
            abstract = str(abstract)[0:150] + "..."
        _item['abstract'] = abstract

        print(cht_to_chs(_item['label']))
        _item['label'] = cht_to_chs(_item['label'])

        # 获取推荐信息
        recomment_info = film_recommend(_item['name'], 1)
        _item['recomment_info'] = recomment_info
        _item['reccount'] = len(recomment_info)

        # 以下信息由爬虫所得
        orter = get_infor(_item['label'])
        _item['writer'] = orter['writer']
        _item['staring'] = orter['staring']
        _item['style'] = orter['style']
        _item['picture'] = orter['picture']

        table.append(_item)
    return table

def add_property(item, propertyname):
    try:
        property = item[propertyname]["value"]
    except KeyError:
        property = ""
    return property