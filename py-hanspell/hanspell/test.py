from hanspell import spell_checker

text = '외않되 아니근데 진짜 설겆이 안녕 하세요 안녕'

print('text: ', text)
spelled_text = spell_checker.check(text)
#print("spelled_text: ", spelled_text.as_dict())

# 출력 형태
# spelled_text:  {'result': True, 'original': '외않되 아니근데진짜 설겆이', 'checked': '왜 안돼 아니 근데 진짜 설거지', 
#                 'errors': 3, 'words': OrderedDict([('왜', 1), ('안돼', 1), ('아니', 2), ('근데', 2), ('진짜', 2), 
#                 ('설거지', 1)]), 'time': 0.48680996894836426}


# Extract original and checked text from the spelled_text dictionary
original_text = spelled_text.original
corrected_text = spelled_text.checked

# Print the extracted texts
print("Original Text:", original_text)
print("Corrected Text:", corrected_text)

num_error = spelled_text.errors
print('num_error: ', num_error)

words = spelled_text.words

wrong_spelling = []
wrong_spacing = []

for key, value in words.items():
    #print((key, value))
    if value == 1:
        wrong_spelling.append(key)
    elif value == 2:
        wrong_spacing.append(key)


print('corrected_spelling: ', wrong_spelling)
print('corrected_spacing: ', wrong_spacing)


#print(f"({original_char} -> {corrected_char})")


# Extract original and checked text from the spelled_text dictionary
# original_text = spelled_text.original
# corrected_text = spelled_text.checked

# # Print the extracted texts
# print("Original Text:", original_text)
# print("Corrected Text:", corrected_text)


