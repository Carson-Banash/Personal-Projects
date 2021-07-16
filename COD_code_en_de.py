cipher_encode_dictinary = {'a':'1','b':'2','c':'3','d':'4','e':'5','f':'6','g':'7','h':'8','i':'9','j':'10','k':'11','l':'12','m':'13'
    ,'n':'14','o':'15','p':'16','q':'17','r':'18','s':'19','t':'20','u':'21','v':'22','w':'23','x':'24','y':'25','z':'26',' ':'27','.':'28'
    }

cipher_decode_dictinary = {'1':'a','2':'b','3':'c','4':'d','5':'e','6':'f','7':'g','8':'h','9':'i','10':'j','11':'k','12':'l','13':'m',
    '14':'n','15':'o','16':'p','17':'q','18':'r','19':'s','20':'t','21':'u','22':'v','23':'w','24':'x','25':'y','26':'z','27':' ', '28':'.'
    }

punctiation_encode_list = [27,28]
def alpha_encode (letr_message):
    
    encoded_numbers = []

    msg_cln = letr_message.lower()
    msg_chars = list(msg_cln)

    for i in range(len(msg_chars)):
        number = cipher_encode_dictinary[msg_chars[i]]
        encoded_numbers.append(number)

    return encoded_numbers

def final_combi_en_msg (letr_book_msg, letr_actual_msg):

    letr_book_msg = [int(i) for i in letr_book_msg]
    letr_actual_msg = [int(i) for i in letr_actual_msg]

    final_encoded_msg = []

    
    for k in range(len(letr_actual_msg)):
        if letr_actual_msg[k] in punctiation_encode_list:
            final_encoded_msg.append(letr_actual_msg[k])
        else:    
            final_number = letr_actual_msg[k] + letr_book_msg[k]
            final_encoded_msg.append(final_number)


    return final_encoded_msg

def alpha_decode (encoded_msg, book_numb):
    cipher_decode_dictinary = {'1':'a','2':'b','3':'c','4':'d','5':'e','6':'f','7':'g','8':'h','9':'i','10':'j','11':'k','12':'l','13':'m',
    '14':'n','15':'o','16':'p','17':'q','18':'r','19':'s','20':'t','21':'u','22':'v','23':'w','24':'x','25':'y','26':'z','27':' ', '28':'.'
    }

    decoded_letters = []
    subtracted_numbers = []
    msg_numb = encoded_msg
    msg_numb = encoded_msg.split(' ')
    #book_numb = book_msg_.split(' ')

    msg_numb = [int(i) for i in msg_numb]
    book_numb = [int(i) for i in book_numb]
    
    
    for i in range(len(msg_numb)):
        sub_num = msg_numb[i] - book_numb[i]
        subtracted_numbers.append(sub_num)

    subtracted_numbers = [str(x) for x in subtracted_numbers]

    for j in range(len(subtracted_numbers)):
        letter = cipher_decode_dictinary[subtracted_numbers[j]]
        decoded_letters.append(letter)

    return decoded_letters

en_or_de = input("Would you like to Encode [E] or Decode [D]? ")
anwser_cln = en_or_de.lower()

if anwser_cln == 'e':
    print('\nWelcome to the COD Code message encoder!\nHere you will input a message and then a exerpt from a book for the purpose of encoding the message.')
    print('You will have to format the message and book exerpt the EXACT same otherwise the format will be messed up.')
    print('Here is an example, Message: hello there ,Book Exerpt: onceu ponat')
    actual_msg = alpha_encode(input('What is the message that you would like to encode?\n: '))
    book_msg = alpha_encode(input('What is the passage from the book? \nEnsure that it has the same amount of characters. \n: '))

    if len(actual_msg) == len(book_msg):
        final_encoded_msg = final_combi_en_msg(book_msg, actual_msg)
        final_message = ' '.join([str(elem) for elem in final_encoded_msg])

        final_message_formated = input('What page number did the book passage come from? \n: ') + ' ' + final_message
        print(final_message_formated)
    
    else: 
        print('Please ensure that the book and message contain the same amount of characters.')

elif anwser_cln == 'd':
    msg = ""
    #decoded_msg = alpha_decode(input('what is the message that you would like to decode? '))

    encoded_msg = input('What is the message you would like to decode?\n: ')
    book_msg_ = alpha_encode(input('What is the book exerpt?\n: '))

    final_decoded_msg = alpha_decode(encoded_msg, book_msg_)

    print (msg.join(final_decoded_msg))
    
else:
    print('Your input was wrong. Input is either E or D')