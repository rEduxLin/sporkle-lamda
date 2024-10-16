from enum import IntFlag

class Permissions(IntFlag):
    ADMINISTRATOR = 0x8
    MANAGE_CHANNELS = 0x10
    SEND_MESSAGES = 0x800
    MANAGE_ROLES = 0x10000000
    MANAGE_THREADS = 0X400000000
    SEND_MESSAGES_IN_THREADS = 0x4000000000