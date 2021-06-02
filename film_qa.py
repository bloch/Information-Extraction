import sys
import create
import question
import rdflib

if len(sys.argv) == 0:
	pass
else:
	if sys.argv[1] == "create":
		create.createOntology()

	if sys.argv[1] == "question":
		ontology = rdflib.Graph()
		ontology.parse("ontology.nt", format="nt")
		question.answer_question(sys.argv[2], ontology)
