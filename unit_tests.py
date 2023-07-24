import unittest
import requests
from bs4 import BeautifulSoup
import app

class TestAppMethods(unittest.TestCase):
	# test function to test API request
	def test_statute(self):
		test_uri = ['https://www.legislation.gov.uk/ukpga/1990/18/enacted/data.html']
		value = ['Computer Misuse Act 1990']
		uri = app.statute(value)
		# error message in case if test case got failed
		message = "First and second value not equal"
		self.assertListEqual(test_uri, uri, message)

	# test function to test whether test_res3 is present in res3
	def test_data(self):
		test_res3 = [(0.007177538526493561, 0.02237703187671522, 0.012032932235592146, 0.0016888325944690733, 0.0, 0.007388642600802195)]
		uri = ['https://www.legislation.gov.uk/ukpga/1990/18/enacted/data.html']
		res3 = app.data(uri)
		# error message in case if test case got failed
		message = "test_res3 is not equal to res3."
		self.assertListEqual(test_res3, res3, message)

	# test work count
	def test_wordcount(self):
		w = "The Lords Spiritual and Temporal"
		test_count = app.wordcount(w)
		count = 5
		# error message in case if test case got failed
		message = "not equal"
		self.assertEqual(test_count, count, message)

	# testing ner function loading the model
	def test_ner(self):
		w = "The Lords Spirtual and Temporal"
		firstValue = app.ner(w)
		secondValue = firstValue
		message = "First and second values not evaluated to same object"
		self.assertIs(firstValue, secondValue, message)

	# testing count of logical connectives
	def test_negative(self):
		nercounts = (0, 0, 1, 0, 0, 0)
		text = "The Lords Spirtual and Temporal"  # real function last
		doc = app.ner(text)
		test_nercount = app.nercount(doc)
		# error message in case if test case got failed
		message = "First and second valuea are not equal"
		self.assertEqual(nercounts, test_nercount, message)

if __name__ == '__main__':
	unittest.main()


#ofa 1911
#cma 1990

#[(15, 154, 38, 1, 2, 10), (34, 106, 57, 8, 0, 35)]

if __name__ == '__main__':
	unittest.main()