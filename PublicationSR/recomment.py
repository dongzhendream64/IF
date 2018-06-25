from SPARQLWrapper import SPARQLWrapper, JSON
import re
def film_recommend(name, recnum):
    if not bool(re.search('[a-z]', name)):
        return []

    name = name.replace(" ", "_")
    name = name.replace(":", "")
    print("推荐电影名:" + name)
    query_str = """
    SELECT COUNT(?movie) SAMPLE(?movie)
    WHERE
    {
    dbr:"""+name+""" dct:subject ?o .
    ?movie dct:subject ?o
    FILTER (?movie != dbr:"""+name+""") .
    } GROUP BY ?movie
    ORDER BY DESC(COUNT(?movie))
    LIMIT """ + str(recnum)

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_str)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()

    pubreclist = []
    for index, item in enumerate(result["results"]["bindings"]):
        pubsum = item["callret-0"]["value"]
        pubname = item["callret-1"]["value"].split("/")[-1].replace('_', ' ')
        puburl = item["callret-1"]["value"]
        if len(pubname) > 24:
            pubname = pubname[0:21] + "..."
        pubrecdic = {'index': index + 1, 'sum': pubsum, 'name': pubname, 'url': puburl, 'color': index % 2}
        pubreclist.append(pubrecdic)
    print("推荐的电影", pubreclist)
    return pubreclist