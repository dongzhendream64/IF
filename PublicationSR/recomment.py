from SPARQLWrapper import SPARQLWrapper, JSON
import re
def film_recommend(film_name):
    if bool(re.search('[a-z]', film_name)):
        name = film_name
    else:
        query_str_0 ="""
            PREFIX dbo:<http://dbpedia.org/ontology/>
            SELECT * WHERE{
            ?url rdf:type<http://dbpedia.org/ontology/Film>;
            rdfs:label ?label;
            foaf:name ?name;
            dbo:wikiPageID ?wikiPageID;
            dbo:abstract ?abstract
            OPTIONAL{?url dbo:writer ?writer}
            filter regex(str(?label), '""" + film_name + "')}"
        sparql_0 = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql_0.setQuery(query_str_0)
        sparql_0.setReturnFormat(JSON)
        result_0 = sparql_0.query().convert()
        name = result_0["results"]["bindings"][0]["name"]["value"]


    name = name.replace(" ","_")
    query_str = """
    SELECT COUNT(?movie) SAMPLE(?movie)
    WHERE
    {
    dbr:"""+name+""" dct:subject ?o .
    ?movie dct:subject ?o
    FILTER (?movie != dbr:"""+name+""") .
    } GROUP BY ?movie
    ORDER BY DESC(COUNT(?movie))
    LIMIT 100

    """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_str)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()


    l = []
    for item in result["results"]["bindings"]:
        i = item["callret-1"]["value"].split("/")[-1].replace('_',' ')
        l.append(i)
    return l