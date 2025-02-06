from numpy import round

list_of_nums = [3, 3, 6, 9, 5, 6, 9, 4, 6, 19, 38, 45, 45, 42]
nums = [num for num in (range(0, 51, 3))]
list_of_answers = []
for num in nums:
	cnt, answer = 0, 0
	for number_from_list in list_of_nums:
		if num > number_from_list:
			answer += number_from_list
			cnt += 1
	list_of_answers.append(float(round(answer / cnt, 2))) if cnt != 0 else list_of_answers.append(0)
print(list_of_answers)