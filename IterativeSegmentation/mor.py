#!/usr/bin/env python
#coding = utf-8
import codecs
import sys
import math
import re
reload(sys)
sys.setdefaultencoding('utf-8')

#MDL (minimum description length)
#input the words segmented, eg: word space word space...

word_dict = {}



#load corpus, statistic words and their frequencies to be used afterhere
def load_corpus(word_seq_file_name):
	list2d = []
	data_file = open(word_seq_file_name, "r")
	for line in data_file:
		line = line.strip()
		word_list = line.split(" ")
		for word in word_list:
			word_dict.setdefault(word, float(0))
			word_dict[word] += 1
		list2d.append(word_list)
	return list2d		

def outfile(list2d):
	#load_corpus(word_seq_file_name)
	#data_file = open(word_seq_file_name, "r")
	t = 1 #let the while loop do once
	#i = 0 #number of lines
	l = 0 #number of loops, only statistic words and their frequencies in first loop, make adjustment in the following loop
	while t>=1 and l < 1:  #the iterations
		t = 0 #whether the list and dict change in one loop
		tot_list = []
		for word_list in list2d:
			#line = line.strip()
			#word_list = line.split(" ")  # chinese in list ???
			#str(word_list).decode('string_escape') #translate to chinese
			j = 0 #index of list
			for word in word_list:
				#str(word_list).decode('string_escape')
				#word1_dict = word_dict
				#word_dict.setdefault
				global word_dict
				for oldword in word_dict.keys(): #*********have a dict
					if (re.match(oldword, word)) and (len(oldword) < len(word)): #********
						a = get_mdl()
						#t_word_dict = word_dict #backup
						word_dict.setdefault(word, float(0))
						#k = word_dict[word]
						suffixword = word[len(oldword):]
						#print suffixword
						word_dict.setdefault(suffixword, float(0)) #*****
						#word_dict.setdefault(word, float(0))
						word_dict[suffixword] += 1 #****word yishan
						word_dict[oldword] += 1
						word_dict[word] -= 1
						if word_dict[word] == 0:
							del word_dict[word] # i don't know why the program needs this line
						b = get_mdl()
						#print a
						#print b
						if a < b:
							#word_dict = t_word_dict
							word_dict[suffixword] -= 1 #****word yishan
							word_dict[oldword] -= 1
							word_dict[word] = 1
							#if word_dict[suffixword] == 0:
							#	del word_dict[suffixword]
							#j += 1
							#if l == 0:
							#	word_dict.setdefault(word, float(0))
							#	word_dict[word] += 1
						else:
							t += 1
							del word_list[j]
							word_list.insert(j, suffixword) #******
							word_list.insert(j, oldword) #******
							#j += 2
							#print t
							break
					#else:
						#if l == 0:
						#	word_dict.setdefault(word, float(0))
						#	word_dict[word] += 1
						#j += 1
				j += 1
			tot_list.append(word_list)
		l +=  1
	# print "iterations:",l
	print "New Cost:",get_mdl()
	#print str(word_dict).decode('string_escape')
	#print str(tot_list).decode('string_escape')
	#print data_file.read() #*******
	
	
	f = codecs.open("02_MF_tagging.txt",'w','utf-8')
#	f.write(str(tot_list).decode('string_escape'))
	for m in tot_list:
		s = str(m).strip('[')
		s = s.strip(']')
		s = s.strip("'")
		s = s.replace("', '"," ")
		f.write(s.decode('string_escape')+'\r\n')

	f.close()
	# print "New file.txt is generated and saved!"		
	return 0

#get the description length of character
#def get_char_info():
#	char_dict = {}
#	for word in word_dict:
#		for char in word:
#			char_dict.setdefault(char, 0)
#			char_dict[char] += 1
#
#	char_num = float(len(char_dict))
#	char_info = math.log(char_num, 2)

#	return char_info

#get the total length of words in word dictionary
def get_dict_info():
	word_length_sum = 0
	for word in word_dict:
		word_length_sum += len(word)
# 000000100000010000001
	return word_length_sum

#get the description length of word sequence
def get_word_seq_info():
	word_info_sum = 0
	freq_sum = sum(word_dict.itervalues())
	for word in word_dict:
		word_freq = word_dict[word]
		#print word_freq
		if word_freq > 0:
			word_info = math.log(word_freq, 2) - math.log(freq_sum, 2)
			word_info_sum += word_info

	word_seq_info = -1 * word_info_sum
	return word_seq_info

def get_mdl():
#	char_info = get_char_info()
	dict_info = get_dict_info()
	word_seq_info = get_word_seq_info()
	mdl = 11 * dict_info / 3 + word_seq_info
	return mdl

if __name__ == "__main__":
	if len(sys.argv)!=2:
		print "please input word corpus filename"
		sys.exit()
	list2d = load_corpus(sys.argv[1])
	print "Old Cost:",get_mdl()
	#print str(word_dict).decode('string_escape')
	#print str(list2d).decode('string_escape')
	outfile(list2d)

