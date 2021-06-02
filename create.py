import requests
import lxml.html
import lxml.etree as etree
import rdflib

problems = ['Directed by', '\n', 'Produced by', '[a]', '[1]', '[2]', '[3]', '[4]', '[5]', '[6]', '[7]', '[8]',
                '[9]',':','(, )','&#91;N 1&#93;','[N 1]','Luna Lauren Velez','(',')', ' (p.g.a.)', 'Ashley Thomas', 'p.g.a.', '(p.g.a.)', 'Joe Mazzello', 'Executive Producer', ': ', ' ', ', ', '', 'Running time', 'Steven Rales', 'Starring', 'Producers Mark','Aaron Johnson']

directors_problems = ['Charles Ferguson']
link_problems = ["/wiki/Producers_Mark", "#cite_note-comingsoon-1", "#cite_note-1", "#cite_note-Elliot-1", "#cite_note-Fletcher-2", "#cite_note-2", "#cite_note-Elliot-2", "#cite_note-Fletcher-3"]
running_time_problems = ["Roadshow", "General"]
occupation_problems = [", ", "", "[1]"]

duplications_tuple = [("producer","/wiki/Film_producer"), ("producer","/wiki/Film_Producer"), ("actress", "/wiki/Actor"), ("director","/wiki/Film_Director"), ("director","/wiki/Film_director"), ("voice actor","/wiki/Voice_acting"), ("attorney","/wiki/Attorney_at_law"), ("journalist","/wiki/Journalism"), ("writer","/wiki/Screenwriter"), ("editor","/wiki/Film_Editor"), ("film","/wiki/Film_producer"), ("film editor","/wiki/Film_editing"), ("actors","/wiki/Actor"), ("animators","/wiki/Animator"), ("filmmakers","/wiki/Filmmakers"), ("screenwriter","/wiki/Screenwriting"), ("businessman","/wiki/Businessperson"), ("producer","/wiki/Executive_producer"), ("singer","/wiki/Singing")]

def get_producers(doc, people_set):
    producers = []
    titles = []

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Produced by')]//@href"):
    	if t not in link_problems:
    	    people_set.add("http://en.wikipedia.org" + t)
    	    producers.append(t[6:].replace('_', ' '))

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Produced by')]//@title"):
        titles.append(t)

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Produced by')]//text()"):
         t = t.strip()
         if t not in problems:
             skip = False
             for producer in titles:
                 if t in producer:
                     skip = True
                     break
             if(not skip):
                producers.append(t)

    producers.sort()
    return producers

def get_directors(doc, people_set):
    directors = []
    titles = []

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Directed by')]//@href"):
    	if t not in link_problems:
    	    people_set.add("http://en.wikipedia.org" + t)
    	    directors.append(t[6:].replace('_', ' '))

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Directed by')]//@title"):
        titles.append(t)

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Directed by')]//text()"):
        t = t.strip()
        if t not in problems and t not in directors_problems:
            skip = False
            for director in titles:
                if t in director:
                    skip = True
                    break
            if not skip:
                directors.append(t)

    directors.sort()
    return directors

def get_running_time(doc):
    runningtime = []

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Running time')]//text()"):
        if t not in problems and t not in running_time_problems:
            runningtime.append(t.replace('\xa0', ' ').strip())

    return runningtime

def get_starring(doc, people_set):
    starring = []
    titles = []

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Starring')]//@href"):
    	if t not in link_problems:
    	    people_set.add("http://en.wikipedia.org" + t)
    	    starring.append(t[6:].replace('_', ' '))

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Starring')]//@title"):
        titles.append(t)

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Starring')]//text()"):
        t = t.strip()
        if t not in problems:
            skip = False
            for star in titles:
                if t in star:
                    skip = True
                    break
            if not skip:
                starring.append(t)

    starring.sort()
    return starring

def get_release_date(doc):
    release_dates = []

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Release date')]//span[@class = 'bday dtstart published updated']//text()"):
        release_dates.append(t)

    return release_dates

def get_based_on(doc):
    based_on = []

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Based on')]"):
        based_on.append("Yes")
        return based_on

    based_on.append("No")
    return based_on

def get_bdays(doc):
    bdays = set()

    for t in doc.xpath("//table[@class = 'infobox biography vcard' or @class = 'infobox vcard' or @class = 'infobox vcard plainlist']//span[@class = 'bday' or @class = 'dtstart bday']//text()"):
        bdays.add(t)

    if len(bdays) > 0:
        return bdays

    for t in doc.xpath("//table[@class = 'infobox biography vcard' or @class = 'infobox vcard' or @class = 'infobox vcard plainlist']//tr[contains(.//text(),'Born')]//td[@class = 'infobox-data']//text()"):
    	terms = t.replace('\xa0', ' ').split()
    	for term in terms:
    		if len(term) == 4 and term.isdigit():
    			bdays.add(term)
    		if len(term) == 9 and term[4] == "/" and term[:4].isdigit() and term[5:].isdigit():
    			bdays.add(str(min(int(term[:4]), int(term[5:]))))
    		if len(term) == 10 and term[2] == "." and term[5] == "." and term[:2].isdigit() and term[3:5].isdigit() and term[6:].isdigit():
    			bdays.add(term[6:])
    return bdays



def get_occupation(doc):
	occupations = []

	for t in doc.xpath("//table[@class = 'infobox biography vcard' or @class = 'infobox vcard' or @class = 'infobox vcard plainlist']//tr[contains(.//text(),'Occupation')]//li"):
		t = t.text_content()
		t = t.replace('[1]', '')
		if t not in occupation_problems:
			for dup_tuple in duplications_tuple:
				if t.strip().lower() == dup_tuple[0]:
					s =  doc.xpath("//table[@class = 'infobox biography vcard' or @class = 'infobox vcard' or @class = 'infobox vcard plainlist']//tr[contains(.//text(),'Occupation')]//li//a[@href = '" + dup_tuple[1] + "']")
					if len(s) > 0:
						t = dup_tuple[1][6:].replace('_', ' ').lower()
			occupations.append(t.strip().lower())

	if len(occupations) > 0:
		return occupations

	for t in doc.xpath("//table[@class = 'infobox biography vcard' or @class = 'infobox vcard' or @class = 'infobox vcard plainlist']//tr[contains(.//text(),'Occupation')]//td[@class = 'infobox-data role' or @class = 'infobox-data']"):
		s = str(etree.tostring(t)).replace('<br/>', ', ')
		t = lxml.html.fromstring(s[2:-1])
		t = t.text_content()
		terms = t.split(' \u2022 ')
		terms = [term.split(', ') for term in terms]

		flat_list = [item for sublist in terms for item in sublist]	
		terms = flat_list

		for term in terms:
			term = term.strip()
			if term not in occupation_problems:
				for dup_tuple in duplications_tuple:
					if term.replace('\\n', '').lower() == dup_tuple[0]:
						s = doc.xpath("//table[@class = 'infobox biography vcard' or @class = 'infobox vcard' or @class = 'infobox vcard plainlist']//tr[contains(.//text(),'Occupation')]//td[@class = 'infobox-data role' or @class = 'infobox-data']//a[@href = '" + dup_tuple[1] + "']")
						if len(s) > 0:
							term = dup_tuple[1][6:].replace('_', ' ').lower()
				
				occupations.append(term.replace('\\n', '').replace(',', '').lower())

	return occupations


def createOntology():
    start_link = "http://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films"

    ontology = rdflib.Graph()

    r = requests.get(start_link)
    doc = lxml.html.fromstring(r.content)

    people_set = set()

    for t in doc.xpath("//table[@class = 'wikitable sortable']//tr[position() > 1 and td[position()=2]//text() > 2009]//td[position() = 1]//a"):
        film_link = "http://en.wikipedia.org" + t.xpath('.//@href')[0]

        film_name = t.xpath('.//@href')[0][6:]

        r = requests.get(film_link)
        doc = lxml.html.fromstring(r.content)

        film_entity = rdflib.URIRef("http://example.org/" + film_name.replace(' ', '_'))

        producers = get_producers(doc, people_set)
        producer_relation = rdflib.URIRef("http://example.org/produced_by")
        for producer in producers:
            producer_entity = rdflib.URIRef("http://example.org/" + producer.replace(' ', '_'))
            ontology.add((film_entity, producer_relation, producer_entity))

        directors = get_directors(doc, people_set)
        director_relation = rdflib.URIRef("http://example.org/directed_by")
        for director in directors:
            director_entity = rdflib.URIRef("http://example.org/" + director.replace(' ', '_'))
            ontology.add((film_entity, director_relation, director_entity))

        running_time = get_running_time(doc)
        running_time_relation = rdflib.URIRef("http://example.org/running_time")
        for rt in running_time:
            rt_entity = rdflib.URIRef("http://example.org/" + rt.replace(' ', '_'))
            ontology.add((film_entity, running_time_relation, rt_entity))

        stars = get_starring(doc, people_set)
        starring_relation = rdflib.URIRef("http://example.org/starring")
        for star in stars:
            star_entity = rdflib.URIRef("http://example.org/" + star.replace(' ', '_'))
            ontology.add((film_entity, starring_relation, star_entity))

        release_dates = get_release_date(doc)
        release_dates_relation = rdflib.URIRef("http://example.org/release_dates")
        for release_date in release_dates:
            release_date_entity = rdflib.URIRef("http://example.org/" + release_date.replace(' ', '_'))
            ontology.add((film_entity, release_dates_relation, release_date_entity))

        based_on = get_based_on(doc)
        based_on_relation = rdflib.URIRef("http://example.org/based_on")
        for based_on_elem in based_on:
            based_on_entity = rdflib.URIRef("http://example.org/" + based_on_elem.replace(' ', '_'))
            ontology.add((film_entity, based_on_relation, based_on_entity))
	

    for person_link in people_set:
	    r = requests.get(person_link)
	    doc = lxml.html.fromstring(r.content)
	    person_name = person_link.split('/')[-1]
	    person_entity = rdflib.URIRef("http://example.org/" + person_name)

	    bdays = get_bdays(doc)
	    bday_relation = rdflib.URIRef("http://example.org/birthday")
	    for bday in bdays:
	    	bday_entity = rdflib.URIRef("http://example.org/" + bday)
	    	ontology.add((person_entity, bday_relation, bday_entity))

	    occupations = get_occupation(doc)
	    occupations = [occupation.lower() for occupation in occupations]
	    occupations.sort()

	    occupation_relation = rdflib.URIRef("http://example.org/occupation")
	    for occupation in occupations:
	    	occupation_entity = rdflib.URIRef("http://example.org/" + occupation.replace(' ', '_'))
	    	ontology.add((person_entity, occupation_relation, occupation_entity))


    ontology.serialize("ontology.nt", format="nt")


