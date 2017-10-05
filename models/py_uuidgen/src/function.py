from generator import generate_uuid
import shortuuid


def execute(data: list, **kwargs):
    for row in data:
        alphabet = row.get('alphabet', shortuuid.get_alphabet())
        length = int(row.get('length', 12))
        row['uuid'] = generate_uuid(alphabet, length)
    return data

# test
# if __name__ == '__main__':
#     data = [
#         {
#             'length': 10
#         },
#         {
#             'alphabet': 'qwerty',
#             'length': 2
#         },
#         {}
#     ]
#     print(main(data))
