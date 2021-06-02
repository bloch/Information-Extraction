import rdflib


def answer_question(question, ontology):
	question = question[:-1]
	if question.startswith("Who directed"):
		words = question.split()
		film_name = '_'.join(words[2:])
		film_entity = "<http://example.org/" + film_name + ">"
		
		query = "select ?p where {" \
    			" "+ film_entity +" <http://example.org/directed_by> ?p ." \
    			"}"

		answers = []
		directors = ontology.query(query)
		for director in directors:
			answers.append(str(director).split('/')[-1][:-4].replace('_', ' '))

		answers.sort()
		final_answer = ", ".join(answers)
		
		print(final_answer)
		return

	if question.startswith("Who produced"):
		words = question.split()
		film_name = '_'.join(words[2:])

		film_entity = "<http://example.org/" + film_name + ">"
		
		query = "select ?p where {" \
    			" "+ film_entity +" <http://example.org/produced_by> ?p ." \
    			"}"

		answers = []
		producers = ontology.query(query)
		for producer in producers:
			answers.append(str(producer).split('/')[-1][:-4].replace('_', ' '))

		answers.sort()
		final_answer = ", ".join(answers)
		
		print(final_answer)
		return
		

	if question.startswith("Is ") and question.endswith("based on a book"):
		words = question.split()
		film_name = "_".join(words[1:-4])
		film_entity = "<http://example.org/" + film_name + ">"
		query = "select ?p where {" \
    			" "+ film_entity +" <http://example.org/based_on> ?p ." \
    			"}"
		
		answers = []
		based_on = ontology.query(query)
		for base_on in based_on:
			answers.append(str(base_on).split('/')[-1][:-4].replace('_', ' '))

		answers.sort()
		final_answer = ", ".join(answers)

		print(final_answer)
		return

	if question.startswith("When was ") and question.endswith("released"):
		words = question.split()
		film_name = "_".join(words[2:-1])
		film_entity = "<http://example.org/" + film_name + ">"
		query = "select ?p where {" \
    			" "+ film_entity +" <http://example.org/release_dates> ?p ." \
    			"}"

		answers = []
		release_dates = ontology.query(query)
		for release_date in release_dates:
			answers.append(str(release_date).split('/')[-1][:-4].replace('_', ' '))

		answers.sort()
		final_answer = ", ".join(answers)

		print(final_answer)	
		return

	if question.startswith("How long is "):
		words = question.split()
		film_name = "_".join(words[3:])
		
		film_entity = "<http://example.org/" + film_name + ">"
		query = "select ?p where {" \
    			" "+ film_entity +" <http://example.org/running_time> ?p ." \
    			"}"

		answers = []
		running_times = ontology.query(query)
		for running_time in running_times:
			answers.append(str(running_time).split('/')[-1][:-4].replace('_', ' '))

		answers.sort()
		final_answer = ", ".join(answers)

		print(final_answer)	
		return

	if question.startswith("Who starred in "):
		words = question.split()
		film_name = "_".join(words[3:])
		film_entity = "<http://example.org/" + film_name + ">"
		query = "select ?p where {" \
    			" "+ film_entity +" <http://example.org/starring> ?p ." \
    			"}"

		answers = []
		starring = ontology.query(query)
		for star in starring:
			answers.append(str(star).split('/')[-1][:-4].replace('_', ' '))

		answers.sort()
		final_answer = ", ".join(answers)

		print(final_answer)
		return

	if question.startswith("Did ") and " star in " in question:
		entity_index = question.find(" star in ")
		entity_name = question[4:entity_index].replace(' ', '_')
		star_entity = "<http://example.org/" + entity_name + ">"
		
		film_name = question[4+len(entity_name)+9:].replace(' ', '_')
		film_entity = "<http://example.org/" + film_name + ">"
		query = "select ?p where {" \
    			" "+ film_entity +" <http://example.org/starring> ?p ." \
    			" FILTER(?p = " + star_entity +")" \
    			"}"

		answers = ontology.query(query)

		if len(answers) > 0:
			print("Yes")
			return
		else:	
			print("No")
			return


	if question.startswith("When was ") and question.endswith("born"):
		words = question.split()
		entity_name = "_".join(words[2:-1])
		person_entity = "<http://example.org/" + entity_name + ">"
		query = "select ?p where {" \
    			" "+ person_entity +" <http://example.org/birthday> ?p ." \
    			"}"

		answers = []
		bdays = ontology.query(query)
		for bday in bdays:
			answers.append(str(bday).split('/')[-1][:-4].replace('_', ' '))

		answers.sort()
		final_answer = ", ".join(answers)

		print(final_answer)	
		return

	if question.startswith("What is the occupation of "):
		entity_name = question[26:].replace(' ', '_')
		person_entity = "<http://example.org/" + entity_name + ">"
		query = "select ?p where {" \
    			" "+ person_entity +" <http://example.org/occupation> ?p ." \
    			"}"

		answers = []
		occupations = ontology.query(query)
		for occupation in occupations:
			answers.append(str(occupation).split('/')[-1][:-4].replace('_', ' ').lower())

		answers.sort()
		final_answer = ", ".join(answers)

		print(final_answer)	
		return final_answer
 
	if question.startswith("How many films starring ") and question.endswith(" won an academy award"):
		entity_name_index = question.find(" won an academy award")
		entity_name = question[24:entity_name_index].replace(' ', '_')
		star_entity = "<http://example.org/" + entity_name + ">"
		query = "select ?p where {" \
    			" ?p <http://example.org/starring> "+ star_entity +" ." \
    			"}"

		answers = ontology.query(query)
		
		print(len(answers))
		return

	if question == "How many films are based on books":
		query = "select ?p where {" \
    			" ?p <http://example.org/based_on> <http://example.org/Yes> ." \
    			"}"
		
		answers = ontology.query(query)

		print(len(answers))
		return

	if question.startswith("How many ") and " are also " in question:
		occupation1_name_index = question.find(" are also ")
		occupation1_name = question[9:occupation1_name_index].replace(' ', '_')
		occupation2_name = question[occupation1_name_index +10:].replace(' ', '_')
		
		occupation1_entity = "<http://example.org/" + occupation1_name + ">"
		occupation2_entity = "<http://example.org/" + occupation2_name + ">"

		query = "select ?p where {" \
    			" ?p <http://example.org/occupation> " + occupation1_entity + " ." \
    			" ?p <http://example.org/occupation> " + occupation2_entity + " ." \
    			"}"


		answers = []
		people = ontology.query(query)
		for person in people:
			answers.append(str(person).split('/')[-1][:-4].replace('_', ' ').lower())
		
		print(len(answers))
		return


	if question.startswith("Who was born in "):
		date = question[16:]
		
		date_entity = "<http://example.org/" + date + ">"

		query = "select ?p where {" \
    			" ?p <http://example.org/birthday> " + date_entity + " ." \
    			"}"

		answers = []
		people = ontology.query(query)
		for person in people:
			answers.append(str(person).split('/')[-1][:-4].replace('_', ' '))


		answers.sort()
		final_answer = ", ".join(answers)

		print(final_answer)
		return
