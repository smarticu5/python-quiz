import argparse
import json
import random
import sys

def get_arguments():
	'''
	Reads CLI options and returns the arguments object
	'''
	
	parser = argparse.ArgumentParser(description='Revision quiz')
	parser.add_argument('-q', '--question-file', default='questions.json', type=str, help='JSON file containing questions')
	parser.add_argument('-n', '--number', default=5, type=int, help='Number of questions to ask')

	args = parser.parse_args()
	return args

def load_questions(filepath):
	''' 
	Reads questions from a user-specified file, and returns a JSON object

	str filepath - relative file path for the queustions file
	obj questions - JSON object with all question information
	'''

	with open(filepath, 'r') as question_file:
		questions = json.load(question_file)
		return questions

def ask_question(question):
	'''
	Ask the user a question, and get user input as a reponse

	obj question - A JSON object containing question, options, and answer
	bool correct - Returns True/False based on correctness
	'''

	# Default to user being wrong. 
	correct = False

	print (question["Question"])

	# Shuffle optional answers
	options = question["Options"]

	# Need to duplicate list. Using option from 
	# https://stackoverflow.com/questions/2612802/how-to-clone-or-copy-a-list
	options_shuffled = options[:]
	random.shuffle(options_shuffled)

	option_number = 0
	for option in options_shuffled:
		# Print out options with a letter at the start
		print ("{0}. {1}".format(chr(option_number + 65), option))
		option_number = option_number + 1

	# Check provided answer against correct answer in JSON
	user_answer = input("Choose an answer: ").upper()

	user_answer_number = ord(user_answer) - 65

	correct_answer_number = question["Answer"]

	if options[int(correct_answer_number)] == options_shuffled[int(user_answer_number)]:
		correct = True

	# Return True/False
	return correct

def main():
	'''
	Ask the user a number of questions (currently a hard-coded 5)
	Give the user a score and a pass/fail grade at the end.

	No parameters required (yet...)
	'''

	# Constants for the quiz, and read CLI arguments
	# TODO: Make these parameters or read from a file

	try:
		assert (sys.version_info.major == 3)
	except AssertionError:
		sys.exit('Please run this script using Python 3')

	arguments = get_arguments()

	score = 0
	questions_asked_count = 0
	questions_asked_list = []
	pass_mark = 66
	str_pass_fail = "failed"
	question_file_path = arguments.question_file
	number_of_questions = arguments.number
	already_asked = True

	# Get questions from file
	questions = load_questions(question_file_path)

	# Check if the number of questions to ask is bigger than the number of questions
	if len(questions) < number_of_questions:
		number_of_questions = len(questions)

	# Actually ask the questions
	while questions_asked_count < number_of_questions:
		question_count = len(questions)

		# TODO: Is there a better way of selecting a random object from a list?

		while already_asked == True:
			current_question_number = random.randint(1,question_count)
			if current_question_number not in questions_asked_list:
				already_asked = False

		current_question = questions[str(current_question_number)]

		already_asked = True
		questions_asked_list.append(current_question_number)

		# Increment number of asked questions
		questions_asked_count = questions_asked_count + 1

		print ("Question {0}".format(questions_asked_count))
		correct = ask_question(current_question)

		# Print question result
		if correct == True:
			print ("That's right!")
			score = score + 1
		else:
			correct_answer_number = int(current_question["Answer"])
			correct_answer = current_question["Options"][correct_answer_number]
			print ("Sorry. The correct answer was '{0}'".format(correct_answer))
		print ()

	# Calculate percentge and pass/fail
	percentage = score / questions_asked_count * 100
	if percentage > pass_mark:
		str_pass_fail = "passed"

	# Output results
	print ("You got {0}% correct".format(percentage))
	print ("The pass mark is {0}%.".format(pass_mark))
	print ("You {0}!".format(str_pass_fail))

if __name__ == '__main__':
	main()