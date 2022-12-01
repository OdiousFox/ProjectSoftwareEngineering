import re


# def splitter(message):
#     for x in message:
#         if len(message) < 100:
#             message.remove(message)
#
#     return message


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def formatMessage(message):
    list = []
    print(message)
    message = message.decode()
    list.append(find_between(message, "\"device_id\":\"", "\",\"application_ids\""))
    if message.__contains__("packetbroker"):
        list.append(find_between(message, "\"gateway_id\":\"", "\"},"))
    else:
        list.append(find_between(message, "\"gateway_id\":\"", "\",\"eui\":"))

    list.append(find_between(message, "\"time\":\"", "T"))
    time = find_between(message, "\"time\":\"", "\",\"")
    list.append(find_between(time, "T", "Z"))
    if message.__contains__("BatV"):
        list.append(find_between(message, "\"ILL_lmessage\":", ","))
        list.append(find_between(message, "\"Hum_SHT\":", ","))
        list.append(find_between(message, "\"TempC_SHT\":", ","))
        list.append(find_between(message, "\"BatV\":", ","))
    else:
        list.append(find_between(message, "\"light\":", ","))
        list.append(find_between(message, "\"pressure\":", ","))
        list.append(find_between(message, "\"temperature\":", "}"))
    print(list)
    for x in list:
        if isinstance(x, bytes):
            x = x.decode()
            print("caca")

<<<<<<< HEAD

def returnMessage(message):
    list = []

    list.append(find_between(message, "\"device_id\":\"", "\",\"application_ids\""))
    if message.__contains__(bytes("packetbroker", 'utf-8')):
        list.append(find_between(message, "\"gateway_id\":\"", "\"},"))
    else:
        list.append(find_between(message, "\"gateway_id\":\"", "\",\"eui\":"))

    list.append(find_between(message, "\"time\":\"", "T"))
    time = find_between(message, "\"time\":\"", "\",\"")
    list.append(find_between(time, "T", "Z"))
    if message.__contains__(bytes("BatV", 'utf-8')):
        list.append(find_between(message, "\"ILL_lmessage\":", ","))
        list.append("NaN")
        list.append(find_between(message, "\"Hum_SHT\":", ","))
        list.append(find_between(message, "\"TempC_SHT\":", ","))
        list.append(find_between(message, "\"BatV\":", ","))
        list.append(find_between(message, "Work_mode\":\"", "\""))
    else:
        list.append(find_between(message, "\"light\":", ","))
        list.append(find_between(message, "\"pressure\":", ","))
        list.append("NaN")
        list.append(find_between(message, "\"temperature\":", "}"))
        list.append("inf")
        list.append("Temperature Sensor")
    return list
=======
    print(list)
>>>>>>> 269565f3df681a833c68c378961043c2335e53e3
