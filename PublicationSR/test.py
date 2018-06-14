from SPARQLWrapper import SPARQLWrapper, JSON, CSV

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
SELECT * WHERE
{
dbr:A_Trip_to_the_Moon dct:subject ?o .
?movie dct:subject ?o
FILTER (?movie != dbr:A_Trip_to_the_Moon) .
} GROUP BY ?movie
ORDER BY DESC(COUNT(?movie))
LIMIT 100

""")
sparql.setReturnFormat(JSON)
result = sparql.query().convert()

print(result)