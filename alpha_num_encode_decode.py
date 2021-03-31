def alpha_encode (letr_message):
    cipher_encode_dictinary = {'a':'1','b':'2','c':'3','d':'4','e':'5','f':'6','g':'7','h':'8','i':'9','j':'10','k':'11','l':'12','m':'13'
    ,'n':'14','o':'15','p':'16','q':'17','r':'18','s':'19','t':'20','u':'21','v':'22','w':'23','x':'24','y':'25','z':'26',' ':'27'
    }
    encoded_numbers = []

    msg_cln = letr_message.lower()
    msg_chars = list(msg_cln)

    for i in range(len(msg_chars)):
        number = cipher_encode_dictinary[msg_chars[i]]
        encoded_numbers.append(number)

    return encoded_numbers

def alpha_decode (numb_message):
    cipher_decode_dictinary = {'1':'a','2':'b','3':'c','4':'d','5':'e','6':'f','7':'g','8':'h','9':'i','10':'j','11':'k','12':'l','13':'m',
    '14':'n','15':'o','16':'p','17':'q','18':'r','19':'s','20':'t','21':'u','22':'v','23':'w','24':'x','25':'y','26':'z','27':' '
    }
    decoded_letters = []

    msg_numb = numb_message.split(' ')

    for j in range(len(msg_numb)):
        letter = cipher_decode_dictinary[msg_numb[j]]
        decoded_letters.append(letter)

    return decoded_letters

en_or_de = input("Would you like to Encode [E] or Decode [D]?")
anwser_cln = en_or_de.lower()

if anwser_cln == 'e':
    encoded_msg = alpha_encode(input('What is the message that you would like to encode? '))
    listToStr = ' '.join([str(elem) for elem in encoded_msg])

    print(listToStr)

elif anwser_cln == 'd':
    stri = ""
    decoded_msg = alpha_decode(input('what is the message that you would like to decode? '))

    print (stri.join(decoded_msg))
    
else:
    print('Your input was wrong. Input is either E or D')