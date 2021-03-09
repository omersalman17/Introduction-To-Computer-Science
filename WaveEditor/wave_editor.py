import wave_helper
import math
import os.path

# magic numbers:
CHOICE_NUMBER_ONE = str(1)
CHOICE_NUMBER_TWO = str(2)
CHOICE_NUMBER_THREE = str(3)
CHOICE_NUMBER_FOUR = str(4)
CHOICE_NUMBER_FIVE = str(5)
CHOICE_NUMBER_SIX = str(6)
# input() default return is str type, so in order to compare between
#  the variables correctly we should cast "choice number" from int to str
MAX_AUDIO_DATA_VALUE = 32767
MIN_AUDIO_DATA_VALUE = -32768
CH1 = 0
CH2 = 1
DEFAULT_SAMPLE = 2000
SIX_SIXTEENTH = 125


def new_list_based_on_frame_rate(lst, big_fr, small_fr):
    # function gets a list, a big frame rate and a small frame rate
    # function returns new list that fits to small frame rate
    new_lst = list()
    for index in range(0, len(lst)):
        if index % big_fr < small_fr:
            new_lst.append(lst[index])
    return new_lst


def merged_lst(lst1, lst2):
    # function gets 2 lists and merges them
    new_list = list()
    lst = list()
    if len(lst1) > len(lst2):
        for place in range(0, len(lst1)):
            for i in range(0, 2):
                if place < len(lst2):
                    x = int((lst1[place][i] + lst2[place][i]) / 2)
                    lst.append(x)
                else:
                    lst.append(lst1[place][i])
            new_list.append(lst)
            lst = list()
    else:
        for place in range(0, len(lst2)):
            for i in range(0, 2):
                if place < len(lst1):
                    x = int((lst1[place][i] + lst2[place][i]) / 2)
                    lst.append(x)
                else:
                    lst.append(lst2[place])
            new_list.append(lst)
            lst = list()
    return new_list


def enter_menu():
    # function manage the program
    # player chooses an option and the menu calls the proper function
    print("please input the action number you would like to do:")
    print("1 - change wav file")
    print("2 - merge two wav files")
    print("3 - compose a new melody in a suitable format for wav file")
    print("4 - exit the program")
    choice_number = input()
    max_options = str(4)
    if invalid_input(choice_number, max_options):  # checks if input is valid
        enter_menu()
    if choice_number == CHOICE_NUMBER_ONE:
        wav_file_name = wav_file_input()
        load_wave = wave_helper.load_wave(wav_file_name)
        frame_rate = load_wave[0]
        audio_data = load_wave[1]
        change_wav_file_menu(frame_rate, audio_data)
    if choice_number == CHOICE_NUMBER_TWO:
        merge_two_wav_files_menu()
    if choice_number == CHOICE_NUMBER_THREE:
        print("please enter txt file path")
        txt_file = input()
        compose_new_melody(txt_file)


def invalid_input(choice_number, max_options):
    # checks if input is invalid- used in menu
    if len(choice_number) == 1:
        if ord(max_options) >= ord(choice_number) >= 49:
            return False
    print("invalid input")
    return True


def check_text_file(txt):
    # checks if given text file exists
    if os.path.isfile(txt):
        return True
    return False


def calc_melody(tuple_lst):
    # gets a list of (note ,number between 1-16)
    # function calculate new fr and creates a new melody
    new_list = list()  # new melody
    for note_tupe in tuple_lst:
        for i in range(0, int(note_tupe[1]) * SIX_SIXTEENTH):
            if note_tupe[0] == "Q":
                new_list.append([0, 0])
            else:
                samples_per_cycle = DEFAULT_SAMPLE / frequency_of_sign(note_tupe[0])
                sample_for_i = int(MAX_AUDIO_DATA_VALUE * math.sin(math.pi * 2 * (i / samples_per_cycle)))
                new_list.append([sample_for_i, sample_for_i])
    return new_list


def compose_new_melody(txt_file):
    # function gets a text file- with notes and fr
    # return a new melody based on inputs
    if check_text_file(txt_file) is False:
        print("invalid path")
    else:
        sign_file = open(txt_file, "r")
        str = ""
        for line in sign_file.readlines():
            str += line.rstrip("\n")
        str = str.strip(" ")
        lst = str.split(" ")
        tuple_lst = list()
        sign_file.close()
        for i in range(0, len(lst), 2):
            tupe = lst[i], lst[i + 1]
            tuple_lst.append(tupe)
        passage_menu(2000, calc_melody(tuple_lst))


def merge_two_wav_files_menu():
    # function responsible for  merging 2 melodys into one
    print("please enter two WAV files name you would like to merge")
    files_names = input()
    files_names = files_names.split()
    # checks if input is good
    if len(files_names) != 2:
        print("invalid input")
        merge_two_wav_files_menu()
    first_file_name = files_names[0]
    second_file_name = files_names[1]
    first_file_load = wave_helper.load_wave(first_file_name)
    second_file_load = wave_helper.load_wave(second_file_name)
    if first_file_load == -1 or second_file_load == -1:
        print("not intact file or not exist")
        merge_two_wav_files_menu()
    else:
        # if input is good:
        merged_file = merge_two_wav_files(first_file_name, second_file_name)
        frame_rate = merged_file[0]
        audio_data = merged_file[1]
        print(merged_file)
        passage_menu(frame_rate, audio_data)


def gcd(x, y):
    # calc. gcd of 2 numbers
    while y > 0:
        x, y = y, x % y
    return x


def frequency_of_sign(sign):
    # gets a sign and return it's frequency
    if sign == "A":
        return 440
    elif sign == "B":
        return 494
    elif sign == "C":
        return 523
    elif sign == "D":
        return 587
    elif sign == "E":
        return 659
    elif sign == "F":
        return 698
    else:
        return 784


def merge_two_wav_files(first_file_name, second_file_name):
    # function gets 2 wav files and merges them- called by merged_menu function
    first_file = wave_helper.load_wave(first_file_name)
    second_file = wave_helper.load_wave(second_file_name)
    frame_rate_1 = first_file[0]
    frame_rate_2 = second_file[0]
    if frame_rate_1 > frame_rate_2:
        better_frame_rate = frame_rate_2
        gc = gcd(frame_rate_1, frame_rate_2)
        sample1 = frame_rate_1 / gc
        sample2 = frame_rate_2 / gc
        fixed_lst = new_list_based_on_frame_rate(first_file[1], sample1, sample2)
        merged_list = merged_lst(fixed_lst, second_file[1])
    elif frame_rate_2 > frame_rate_1:
        better_frame_rate = frame_rate_1
        gc = gcd(frame_rate_2, frame_rate_1)
        sample1 = int(frame_rate_1 / gc)
        sample2 = int(frame_rate_2 / gc)
        fixed_lst = new_list_based_on_frame_rate(second_file[1], sample2, sample1)
        merged_list = merged_lst(fixed_lst, first_file[1])
    else:
        better_frame_rate = frame_rate_1
        merged_list = merged_lst(first_file[1], second_file[1])
    return merged_list, better_frame_rate


def wav_file_input():
    # gets a file path from the user
    # if path is not good- calls the function again
    print("please input the file name you would like to change")
    wav_file_name = input()
    if wave_helper.load_wave(wav_file_name) == -1:
        print("not intact file or not exist")
        wav_file_input()
    return wav_file_name


def change_wav_file_menu(frame_rate, audio_data):
    # if player chose to change wav file, start this menu
    print("please input the action number you would like to do on the file")
    print("1 - reversal")
    print("2 - speed up")
    print("3 - lower speed")
    print("4 - increase volume")
    print("5 - lower volume")
    print("6 - low pass filter")
    choice_number = input()
    max_options = str(6)
    if invalid_input(choice_number, max_options):
        change_wav_file_menu(frame_rate, audio_data)
    if choice_number == CHOICE_NUMBER_ONE:
        audio_data = reversal(audio_data)
    if choice_number == CHOICE_NUMBER_TWO:
        audio_data = speed_up(audio_data)
    if choice_number == CHOICE_NUMBER_THREE:
        audio_data = lower_speed(audio_data)
    if choice_number == CHOICE_NUMBER_FOUR:
        audio_data = increase_volume(audio_data)
    if choice_number == CHOICE_NUMBER_FIVE:
        audio_data = lower_volume(audio_data)
    if choice_number == CHOICE_NUMBER_SIX:
        audio_data = low_pass_filter(audio_data)
    passage_menu(frame_rate, audio_data)


def passage_menu(frame_rate, audio_data):
    # passage menu- player chooses to save audio or change it
    print("please input the action number you would like to do:")
    print("1 - saving audio")
    print("2 - changing audio")
    choice_number = input()
    max_options = str(2)
    if invalid_input(choice_number, max_options):
        passage_menu(frame_rate, audio_data)
    if choice_number == CHOICE_NUMBER_ONE:
        print("please enter file name you would like to to save the audio in")
        new_saved_file_name = input()
        wave_helper.save_wave(frame_rate, audio_data, new_saved_file_name)
        enter_menu()
    if choice_number == CHOICE_NUMBER_TWO:
        change_wav_file_menu(frame_rate, audio_data)


def reversal(audio_data):
    # reverse an audio
    audio_data = audio_data[::-1]
    return audio_data


def speed_up(audio_data):
    # speeds up an audio
    even_audio_data = []
    for i in range(len(audio_data)):
        if i % 2 == 0:
            even_audio_data.append(audio_data[i])
    return even_audio_data


def lower_speed(audio_data):
    # lowers the speed of an audio
    if not audio_data:
        return []
    slower_audio = []
    i = 0
    while i < len(audio_data) - 1:
        slower_audio.append(audio_data[i])
        slower_audio.append(audio_sum(audio_data[i], audio_data[i + 1]))
        i += 1
    slower_audio.append(audio_data[-1])
    return slower_audio


def audio_sum(audio_first_i, audio_second_i):
    # calculate sum of the audio
    sum = []
    sum_first_channel = int((audio_first_i[CH1] + audio_second_i[CH1]) / 2)
    sum.append(sum_first_channel)
    sum_second_channel = int((audio_first_i[CH2] + audio_second_i[CH2]) / 2)
    sum.append(sum_second_channel)
    return sum


def increase_volume(audio_data):
    # increases audio's sound
    for i in range(len(audio_data)):
        audio_data[i][CH1] = int(audio_data[i][CH1] * 1.2)
        audio_data[i][CH2] = int(audio_data[i][CH2] * 1.2)
        first_channel = audio_data[i][CH1]
        second_channel = audio_data[i][CH2]
        if first_channel > MAX_AUDIO_DATA_VALUE:
            audio_data[i][CH1] = MAX_AUDIO_DATA_VALUE
        elif first_channel < MIN_AUDIO_DATA_VALUE:
            audio_data[i][CH1] = MIN_AUDIO_DATA_VALUE
        if second_channel > MAX_AUDIO_DATA_VALUE:
            audio_data[i][CH2] = MAX_AUDIO_DATA_VALUE
        elif second_channel < MIN_AUDIO_DATA_VALUE:
            audio_data[i][CH2] = MIN_AUDIO_DATA_VALUE
    return audio_data


def lower_volume(audio_data):
    # lowers volume
    for i in range(len(audio_data)):
        audio_data[i][CH1] = int(audio_data[i][CH1] / 1.2)
        audio_data[i][CH2] = int(audio_data[i][CH2] / 1.2)
    return audio_data


def low_pass_filter(audio_data):
    # function low pass filter the audio
    if not audio_data:
        return []
    low_pass_audio = []
    i = 1
    if len(audio_data) == 1:
        low_pass_audio.append(audio_data[0])
        return low_pass_audio
    low_pass_audio.append(audio_sum(audio_data[0], audio_data[1]))
    while i < len(audio_data) - 1:
        low_pass_audio.append(sum_for_low_pass_filter(audio_data, i))
        i += 1
    low_pass_audio.append(audio_sum(audio_data[i - 1], audio_data[i]))
    return low_pass_audio


def sum_for_low_pass_filter(audio_data, i):
    # sums the low pass ilter
    low_pass_sum = []
    lp_ch1 = audio_data[i - 1][CH1] + audio_data[i][CH1] + audio_data[i + 1][CH1]
    lp_ch1 = int(lp_ch1 / 3)
    low_pass_sum.append(lp_ch1)
    lp_ch2 = audio_data[i - 1][CH2] + audio_data[i][CH2] + audio_data[i + 1][CH2]
    lp_ch2 = int(lp_ch2 / 3)
    low_pass_sum.append(lp_ch2)
    return low_pass_sum


def main():
    # starts the function
    enter_menu()


if __name__ == '__main__':
    main()
