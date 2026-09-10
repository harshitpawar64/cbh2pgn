from enum import IntEnum
from typing import Any


class Piece(IntEnum):
    NONE = 0
    W_QUEEN = 1
    W_KNIGHT = 2
    W_BISHOP = 3
    W_ROOK = 4
    B_QUEEN = 5
    B_KNIGHT = 6
    B_BISHOP = 7
    B_ROOK = 8
    W_KING = 9
    B_KING = 10
    W_PAWN = 11
    B_PAWN = 12


BoardGrid = list[list[Any]]
PieceLocations = list[list[Any]]

MASK_START_WITH_INITIAL = 0x40000000
MASK_IS_ENCODED = 0x80000000
MASK_SPECIAL_ENCODING = 0x04000000
MASK_GAME_LENGTH = 0x00FFFFFF
MASK_IS_960 = 0x00A00000
MASK_EN_PASSANT_FILE = 0x7
MASK_TURN = 0x10
MASK_WHITE_CASTLE_LONG = 1
MASK_WHITE_CASTLE_SHORT = 2
MASK_BLACK_CASTLE_LONG = 4
MASK_BLACK_CASTLE_SHORT = 8

ABS_TO_XY = tuple((file, rank) for file in range(8) for rank in range(8))

# fmt: off
DEOBFUSCATE_2B = [
    0xA2, 0x95, 0x43, 0xF5, 0xC1, 0x3D, 0x4A, 0x6C, 0x53, 0x83, 0xCC, 0x7C, 0xFF, 0xAE, 0x68, 0xAD,
    0xD1, 0x92, 0x8B, 0x8D, 0x35, 0x81, 0x5E, 0x74, 0x26, 0x8E, 0xAB, 0xCA, 0xFD, 0x9A, 0xF3, 0xA0,
    0xA5, 0x15, 0xFC, 0xB1, 0x1E, 0xED, 0x30, 0xEA, 0x22, 0xEB, 0xA7, 0xCD, 0x4E, 0x6F, 0x2E, 0x24,
    0x32, 0x94, 0x41, 0x8C, 0x6E, 0x58, 0x82, 0x50, 0xBB, 0x02, 0x8A, 0xD8, 0xFA, 0x60, 0xDE, 0x52,
    0xBA, 0x46, 0xAC, 0x29, 0x9D, 0xD7, 0xDF, 0x08, 0x21, 0x01, 0x66, 0xA3, 0xF1, 0x19, 0x27, 0xB5,
    0x91, 0xD5, 0x42, 0x0E, 0xB4, 0x4C, 0xD9, 0x18, 0x5F, 0xBC, 0x25, 0xA6, 0x96, 0x04, 0x56, 0x6A,
    0xAA, 0x33, 0x1C, 0x2B, 0x73, 0xF0, 0xDD, 0xA4, 0x37, 0xD3, 0xC5, 0x10, 0xBF, 0x5A, 0x23, 0x34,
    0x75, 0x5B, 0xB8, 0x55, 0xD2, 0x6B, 0x09, 0x3A, 0x57, 0x12, 0xB3, 0x77, 0x48, 0x85, 0x9B, 0x0F,
    0x9E, 0xC7, 0xC8, 0xA1, 0x7F, 0x7A, 0xC0, 0xBD, 0x31, 0x6D, 0xF6, 0x3E, 0xC3, 0x11, 0x71, 0xCE,
    0x7D, 0xDA, 0xA8, 0x54, 0x90, 0x97, 0x1F, 0x44, 0x40, 0x16, 0xC9, 0xE3, 0x2C, 0xCB, 0x84, 0xEC,
    0x9F, 0x3F, 0x5C, 0xE6, 0x76, 0x0B, 0x3C, 0x20, 0xB7, 0x36, 0x00, 0xDC, 0xE7, 0xF9, 0x4F, 0xF7,
    0xAF, 0x06, 0x07, 0xE0, 0x1A, 0x0A, 0xA9, 0x4B, 0x0C, 0xD6, 0x63, 0x87, 0x89, 0x1D, 0x13, 0x1B,
    0xE4, 0x70, 0x05, 0x47, 0x67, 0x7B, 0x2F, 0xEE, 0xE2, 0xE8, 0x98, 0x0D, 0xEF, 0xCF, 0xC4, 0xF4,
    0xFB, 0xB0, 0x17, 0x99, 0x64, 0xF2, 0xD4, 0x2A, 0x03, 0x4D, 0x78, 0xC6, 0xFE, 0x65, 0x86, 0x88,
    0x79, 0x45, 0x3B, 0xE5, 0x49, 0x8F, 0x2D, 0xB9, 0xBE, 0x62, 0x93, 0x14, 0xE9, 0xD0, 0x38, 0x9C,
    0xB2, 0xC2, 0x59, 0x5D, 0xB6, 0x72, 0x51, 0xF8, 0x28, 0x7E, 0x61, 0x39, 0xE1, 0xDB, 0x69, 0x80,
]
# fmt: on

# opcode: (white_type, black_type, piece_index, dx, dy, is_pawn)
OPCODE_MAP = {
    0x00: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 6, 6, False),
    0x01: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 0, 7, False),
    0x02: (Piece.W_BISHOP, Piece.B_BISHOP, 0, 1, 1, False),
    0x04: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 2, 6, False),
    0x05: (Piece.W_ROOK, Piece.B_ROOK, 1, 2, 0, False),
    0x06: (Piece.W_BISHOP, Piece.B_BISHOP, 0, 1, 7, False),
    0x07: (Piece.W_KNIGHT, Piece.B_KNIGHT, 1, -1, -2, False),
    0x08: (Piece.W_BISHOP, Piece.B_BISHOP, 1, 3, 3, False),
    0x09: (Piece.W_PAWN, Piece.B_PAWN, 5, 0, 1, True),
    0x0A: (Piece.W_ROOK, Piece.B_ROOK, 2, 0, 6, False),
    0x0B: (Piece.W_PAWN, Piece.B_PAWN, 3, 0, 2, True),
    0x0D: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 0, 4, False),
    0x0E: (Piece.W_KNIGHT, Piece.B_KNIGHT, 1, 1, 2, False),
    0x0F: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 0, 3, False),
    0x10: (Piece.W_ROOK, Piece.B_ROOK, 2, 4, 0, False),
    0x11: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 0, 4, False),
    0x12: (Piece.W_PAWN, Piece.B_PAWN, 7, 0, 1, True),
    0x13: (Piece.W_PAWN, Piece.B_PAWN, 7, 1, 1, True),
    0x14: (Piece.W_ROOK, Piece.B_ROOK, 1, 0, 1, False),
    0x15: (Piece.W_PAWN, Piece.B_PAWN, 4, 1, 1, True),
    0x16: (Piece.W_BISHOP, Piece.B_BISHOP, 1, 7, 1, False),
    0x17: (Piece.W_PAWN, Piece.B_PAWN, 1, 0, 2, True),
    0x18: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 7, 1, False),
    0x19: (Piece.W_PAWN, Piece.B_PAWN, 7, -1, 1, True),
    0x1A: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 0, 1, False),
    0x1B: (Piece.W_ROOK, Piece.B_ROOK, 2, 0, 4, False),
    0x1D: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 5, 0, False),
    0x1F: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 4, 4, False),
    0x20: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 2, 6, False),
    0x21: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 4, 0, False),
    0x23: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 0, 7, False),
    0x24: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 6, 6, False),
    0x26: (Piece.W_ROOK, Piece.B_ROOK, 0, 3, 0, False),
    0x27: (Piece.W_KNIGHT, Piece.B_KNIGHT, 2, 2, -1, False),
    0x28: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 3, 5, False),
    0x2A: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 4, 4, False),
    0x2B: (Piece.W_ROOK, Piece.B_ROOK, 2, 0, 7, False),
    0x2C: (Piece.W_BISHOP, Piece.B_BISHOP, 0, 5, 3, False),
    0x2D: (Piece.W_PAWN, Piece.B_PAWN, 0, 0, 1, True),
    0x2E: (Piece.W_ROOK, Piece.B_ROOK, 0, 1, 0, False),
    0x2F: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 5, 3, False),
    0x30: (Piece.W_ROOK, Piece.B_ROOK, 0, 5, 0, False),
    0x31: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 0, 6, False),
    0x32: (Piece.W_ROOK, Piece.B_ROOK, 1, 6, 0, False),
    0x33: (Piece.W_PAWN, Piece.B_PAWN, 7, 0, 2, True),
    0x34: (Piece.W_KNIGHT, Piece.B_KNIGHT, 1, 2, -1, False),
    0x35: (Piece.W_BISHOP, Piece.B_BISHOP, 1, 1, 7, False),
    0x36: (Piece.W_PAWN, Piece.B_PAWN, 4, -1, 1, True),
    0x37: (Piece.W_BISHOP, Piece.B_BISHOP, 0, 7, 1, False),
    0x38: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 3, 3, False),
    0x39: (Piece.W_KING, Piece.B_KING, 0, 1, 1, False),
    0x3A: (Piece.W_PAWN, Piece.B_PAWN, 6, -1, 1, True),
    0x3B: (Piece.W_BISHOP, Piece.B_BISHOP, 2, 4, 4, False),
    0x3D: (Piece.W_KNIGHT, Piece.B_KNIGHT, 0, 1, 2, False),
    0x3E: (Piece.W_BISHOP, Piece.B_BISHOP, 2, 3, 5, False),
    0x3F: (Piece.W_BISHOP, Piece.B_BISHOP, 1, 2, 2, False),
    0x40: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 2, 2, False),
    0x41: (Piece.W_BISHOP, Piece.B_BISHOP, 0, 4, 4, False),
    0x42: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 0, 2, False),
    0x43: (Piece.W_ROOK, Piece.B_ROOK, 0, 0, 3, False),
    0x44: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 1, 1, False),
    0x45: (Piece.W_BISHOP, Piece.B_BISHOP, 2, 3, 3, False),
    0x46: (Piece.W_BISHOP, Piece.B_BISHOP, 2, 4, 4, False),
    0x47: (Piece.W_KING, Piece.B_KING, 0, 7, 1, False),
    0x48: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 2, 6, False),
    0x49: (Piece.W_KING, Piece.B_KING, 0, 0, 1, False),
    0x4A: (Piece.W_KNIGHT, Piece.B_KNIGHT, 0, 2, -1, False),
    0x4B: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 7, 7, False),
    0x4D: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 1, 1, False),
    0x4E: (Piece.W_ROOK, Piece.B_ROOK, 0, 0, 1, False),
    0x4F: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 4, 0, False),
    0x50: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 0, 3, False),
    0x51: (Piece.W_BISHOP, Piece.B_BISHOP, 2, 1, 1, False),
    0x52: (Piece.W_ROOK, Piece.B_ROOK, 1, 7, 0, False),
    0x53: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 0, 4, False),
    0x54: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 3, 0, False),
    0x55: (Piece.W_BISHOP, Piece.B_BISHOP, 0, 3, 5, False),
    0x56: (Piece.W_BISHOP, Piece.B_BISHOP, 2, 5, 5, False),
    0x57: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 7, 0, False),
    0x58: (Piece.W_KNIGHT, Piece.B_KNIGHT, 0, 2, 1, False),
    0x59: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 4, 4, False),
    0x5A: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 6, 2, False),
    0x5B: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 3, 5, False),
    0x5C: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 1, 0, False),
    0x5D: (Piece.W_KING, Piece.B_KING, 0, 1, 7, False),
    0x5E: (Piece.W_BISHOP, Piece.B_BISHOP, 1, 6, 6, False),
    0x5F: (Piece.W_KNIGHT, Piece.B_KNIGHT, 1, -2, 1, False),
    0x60: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 7, 1, False),
    0x61: (Piece.W_ROOK, Piece.B_ROOK, 0, 6, 0, False),
    0x62: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 4, 4, False),
    0x63: (Piece.W_ROOK, Piece.B_ROOK, 0, 0, 5, False),
    0x64: (Piece.W_PAWN, Piece.B_PAWN, 1, 0, 1, True),
    0x66: (Piece.W_BISHOP, Piece.B_BISHOP, 2, 2, 6, False),
    0x67: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 1, 7, False),
    0x68: (Piece.W_ROOK, Piece.B_ROOK, 1, 0, 3, False),
    0x69: (Piece.W_ROOK, Piece.B_ROOK, 2, 6, 0, False),
    0x6A: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 6, 2, False),
    0x6B: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 0, 6, False),
    0x6C: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 7, 7, False),
    0x6D: (Piece.W_BISHOP, Piece.B_BISHOP, 1, 3, 5, False),
    0x6E: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 4, 4, False),
    0x6F: (Piece.W_ROOK, Piece.B_ROOK, 0, 7, 0, False),
    0x70: (Piece.W_PAWN, Piece.B_PAWN, 1, 1, 1, True),
    0x71: (Piece.W_BISHOP, Piece.B_BISHOP, 1, 4, 4, False),
    0x72: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 7, 0, False),
    0x73: (Piece.W_BISHOP, Piece.B_BISHOP, 1, 5, 5, False),
    0x74: (Piece.W_ROOK, Piece.B_ROOK, 2, 5, 0, False),
    0x75: (Piece.W_KNIGHT, Piece.B_KNIGHT, 1, -2, -1, False),
    0x76: (Piece.W_KING, Piece.B_KING, 0, 2, 0, False),
    0x77: (Piece.W_ROOK, Piece.B_ROOK, 1, 0, 6, False),
    0x78: (Piece.W_BISHOP, Piece.B_BISHOP, 1, 7, 7, False),
    0x79: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 1, 0, False),
    0x7A: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 2, 0, False),
    0x7B: (Piece.W_PAWN, Piece.B_PAWN, 2, 0, 1, True),
    0x7C: (Piece.W_BISHOP, Piece.B_BISHOP, 0, 6, 6, False),
    0x7D: (Piece.W_PAWN, Piece.B_PAWN, 5, 1, 1, True),
    0x7E: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 6, 0, False),
    0x7F: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 0, 5, False),
    0x80: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 2, 2, False),
    0x81: (Piece.W_ROOK, Piece.B_ROOK, 2, 0, 1, False),
    0x82: (Piece.W_ROOK, Piece.B_ROOK, 2, 0, 2, False),
    0x83: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 5, 5, False),
    0x84: (Piece.W_PAWN, Piece.B_PAWN, 4, 0, 1, True),
    0x85: (Piece.W_PAWN, Piece.B_PAWN, 2, -1, 1, True),
    0x86: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 1, 7, False),
    0x87: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 5, 5, False),
    0x88: (Piece.W_ROOK, Piece.B_ROOK, 0, 4, 0, False),
    0x89: (Piece.W_KNIGHT, Piece.B_KNIGHT, 1, 1, -2, False),
    0x8B: (Piece.W_ROOK, Piece.B_ROOK, 1, 3, 0, False),
    0x8C: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 4, 4, False),
    0x8D: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 0, 7, False),
    0x8E: (Piece.W_PAWN, Piece.B_PAWN, 0, 1, 1, True),
    0x8F: (Piece.W_ROOK, Piece.B_ROOK, 2, 1, 0, False),
    0x90: (Piece.W_PAWN, Piece.B_PAWN, 3, 1, 1, True),
    0x91: (Piece.W_BISHOP, Piece.B_BISHOP, 2, 6, 6, False),
    0x92: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 5, 3, False),
    0x93: (Piece.W_BISHOP, Piece.B_BISHOP, 1, 4, 4, False),
    0x94: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 0, 2, False),
    0x95: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 2, 0, False),
    0x96: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 7, 7, False),
    0x97: (Piece.W_BISHOP, Piece.B_BISHOP, 0, 2, 2, False),
    0x98: (Piece.W_ROOK, Piece.B_ROOK, 1, 5, 0, False),
    0x99: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 5, 0, False),
    0x9A: (Piece.W_ROOK, Piece.B_ROOK, 2, 0, 3, False),
    0x9B: (Piece.W_KNIGHT, Piece.B_KNIGHT, 2, 2, 1, False),
    0x9C: (Piece.W_ROOK, Piece.B_ROOK, 0, 0, 6, False),
    0x9D: (Piece.W_ROOK, Piece.B_ROOK, 2, 0, 5, False),
    0x9E: (Piece.W_PAWN, Piece.B_PAWN, 5, 0, 2, True),
    0xA0: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 3, 3, False),
    0xA1: (Piece.W_ROOK, Piece.B_ROOK, 1, 4, 0, False),
    0xA2: (Piece.W_BISHOP, Piece.B_BISHOP, 1, 5, 3, False),
    0xA3: (Piece.W_KNIGHT, Piece.B_KNIGHT, 2, -2, 1, False),
    0xA4: (Piece.W_PAWN, Piece.B_PAWN, 1, -1, 1, True),
    0xA5: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 0, 1, False),
    0xA6: (Piece.W_ROOK, Piece.B_ROOK, 1, 1, 0, False),
    0xA7: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 1, 7, False),
    0xA8: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 6, 0, False),
    0xA9: (Piece.W_ROOK, Piece.B_ROOK, 1, 0, 2, False),
    0xAB: (Piece.W_BISHOP, Piece.B_BISHOP, 2, 1, 7, False),
    0xAC: (Piece.W_KNIGHT, Piece.B_KNIGHT, 2, -2, -1, False),
    0xAE: (Piece.W_BISHOP, Piece.B_BISHOP, 0, 6, 2, False),
    0xB0: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 0, 5, False),
    0xB1: (Piece.W_KING, Piece.B_KING, 0, 7, 7, False),
    0xB2: (Piece.W_KING, Piece.B_KING, 0, 7, 0, False),
    0xB3: (Piece.W_BISHOP, Piece.B_BISHOP, 2, 5, 3, False),
    0xB4: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 2, 2, False),
    0xB5: (Piece.W_KING, Piece.B_KING, 0, -2, 0, False),
    0xB6: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 6, 2, False),
    0xB7: (Piece.W_BISHOP, Piece.B_BISHOP, 0, 2, 6, False),
    0xB8: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 0, 2, False),
    0xB9: (Piece.W_BISHOP, Piece.B_BISHOP, 2, 2, 2, False),
    0xBA: (Piece.W_KNIGHT, Piece.B_KNIGHT, 0, -2, -1, False),
    0xBB: (Piece.W_PAWN, Piece.B_PAWN, 6, 0, 1, True),
    0xBC: (Piece.W_PAWN, Piece.B_PAWN, 6, 1, 1, True),
    0xBD: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 5, 5, False),
    0xBE: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 2, 0, False),
    0xBF: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 3, 3, False),
    0xC0: (Piece.W_KNIGHT, Piece.B_KNIGHT, 2, 1, 2, False),
    0xC1: (Piece.W_PAWN, Piece.B_PAWN, 0, 0, 2, True),
    0xC2: (Piece.W_KING, Piece.B_KING, 0, 0, 7, False),
    0xC3: (Piece.W_BISHOP, Piece.B_BISHOP, 0, 5, 5, False),
    0xC4: (Piece.W_KNIGHT, Piece.B_KNIGHT, 1, 2, 1, False),
    0xC5: (Piece.W_PAWN, Piece.B_PAWN, 3, 0, 1, True),
    0xC6: (Piece.W_ROOK, Piece.B_ROOK, 0, 2, 0, False),
    0xC8: (Piece.W_BISHOP, Piece.B_BISHOP, 2, 7, 1, False),
    0xC9: (Piece.W_KNIGHT, Piece.B_KNIGHT, 2, -1, -2, False),
    0xCA: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 3, 0, False),
    0xCB: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 0, 3, False),
    0xCD: (Piece.W_ROOK, Piece.B_ROOK, 2, 2, 0, False),
    0xCE: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 5, 3, False),
    0xD1: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 0, 6, False),
    0xD2: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 6, 0, False),
    0xD3: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 4, 0, False),
    0xD4: (Piece.W_KNIGHT, Piece.B_KNIGHT, 0, -1, -2, False),
    0xD6: (Piece.W_ROOK, Piece.B_ROOK, 2, 7, 0, False),
    0xD7: (Piece.W_ROOK, Piece.B_ROOK, 0, 0, 4, False),
    0xD8: (Piece.W_KING, Piece.B_KING, 0, 1, 0, False),
    0xD9: (Piece.W_BISHOP, Piece.B_BISHOP, 0, 4, 4, False),
    0xDA: (Piece.W_PAWN, Piece.B_PAWN, 2, 0, 2, True),
    0xDB: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 7, 1, False),
    0xDD: (Piece.W_KNIGHT, Piece.B_KNIGHT, 0, 1, -2, False),
    0xDE: (Piece.W_PAWN, Piece.B_PAWN, 5, -1, 1, True),
    0xDF: (Piece.W_PAWN, Piece.B_PAWN, 6, 0, 2, True),
    0xE0: (Piece.W_PAWN, Piece.B_PAWN, 2, 1, 1, True),
    0xE1: (Piece.W_BISHOP, Piece.B_BISHOP, 0, 3, 3, False),
    0xE2: (Piece.W_ROOK, Piece.B_ROOK, 1, 0, 7, False),
    0xE3: (Piece.W_KNIGHT, Piece.B_KNIGHT, 2, -1, 2, False),
    0xE4: (Piece.W_BISHOP, Piece.B_BISHOP, 0, 7, 7, False),
    0xE5: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 0, 1, False),
    0xE6: (Piece.W_ROOK, Piece.B_ROOK, 0, 0, 7, False),
    0xE7: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 1, 1, False),
    0xE8: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 6, 6, False),
    0xE9: (Piece.W_KNIGHT, Piece.B_KNIGHT, 0, -2, 1, False),
    0xEA: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 0, 5, False),
    0xEB: (Piece.W_QUEEN, Piece.B_QUEEN, 0, 3, 0, False),
    0xEC: (Piece.W_KNIGHT, Piece.B_KNIGHT, 2, 1, -2, False),
    0xED: (Piece.W_ROOK, Piece.B_ROOK, 2, 3, 0, False),
    0xEE: (Piece.W_ROOK, Piece.B_ROOK, 1, 0, 4, False),
    0xEF: (Piece.W_QUEEN, Piece.B_QUEEN, 1, 7, 0, False),
    0xF0: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 1, 0, False),
    0xF1: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 3, 5, False),
    0xF2: (Piece.W_BISHOP, Piece.B_BISHOP, 1, 2, 6, False),
    0xF3: (Piece.W_BISHOP, Piece.B_BISHOP, 1, 6, 2, False),
    0xF4: (Piece.W_QUEEN, Piece.B_QUEEN, 2, 5, 0, False),
    0xF5: (Piece.W_PAWN, Piece.B_PAWN, 0, -1, 1, True),
    0xF6: (Piece.W_BISHOP, Piece.B_BISHOP, 1, 1, 1, False),
    0xF8: (Piece.W_ROOK, Piece.B_ROOK, 0, 0, 2, False),
    0xF9: (Piece.W_PAWN, Piece.B_PAWN, 3, -1, 1, True),
    0xFA: (Piece.W_KNIGHT, Piece.B_KNIGHT, 0, -1, 2, False),
    0xFB: (Piece.W_ROOK, Piece.B_ROOK, 1, 0, 5, False),
    0xFC: (Piece.W_BISHOP, Piece.B_BISHOP, 2, 6, 2, False),
    0xFD: (Piece.W_BISHOP, Piece.B_BISHOP, 2, 7, 7, False),
    0xFE: (Piece.W_KNIGHT, Piece.B_KNIGHT, 1, -1, 2, False),
    0xFF: (Piece.W_PAWN, Piece.B_PAWN, 4, 0, 2, True),
}

OPCODE_TABLE = tuple(OPCODE_MAP.get(opcode) for opcode in range(256))
SPECIAL_CODES = {0x29, 0xDC, 0x9F}

PIECE_TO_FEN_CHAR = {
    Piece.W_KING: "K",
    Piece.W_QUEEN: "Q",
    Piece.W_ROOK: "R",
    Piece.W_BISHOP: "B",
    Piece.W_KNIGHT: "N",
    Piece.W_PAWN: "P",
    Piece.B_KING: "k",
    Piece.B_QUEEN: "q",
    Piece.B_ROOK: "r",
    Piece.B_BISHOP: "b",
    Piece.B_KNIGHT: "n",
    Piece.B_PAWN: "p",
}

# (king, opcode): (rook_piece, from_file, to_file, rank)
CASTLING_ROOKS = {
    (Piece.W_KING, 0x76): (Piece.W_ROOK, 7, 5, 0),
    (Piece.B_KING, 0x76): (Piece.B_ROOK, 7, 5, 7),
    (Piece.W_KING, 0xB5): (Piece.W_ROOK, 0, 3, 0),
    (Piece.B_KING, 0xB5): (Piece.B_ROOK, 0, 3, 7),
}

# (pawn, target_rank): (queen, rook, bishop, knight)
PROMOTION_MAP = {
    (Piece.W_PAWN, 7): (Piece.W_QUEEN, Piece.W_ROOK, Piece.W_BISHOP, Piece.W_KNIGHT),
    (Piece.B_PAWN, 0): (Piece.B_QUEEN, Piece.B_ROOK, Piece.B_BISHOP, Piece.B_KNIGHT),
}

FILES = ("a", "b", "c", "d", "e", "f", "g", "h")
RANKS = ("1", "2", "3", "4", "5", "6", "7", "8")
SAN_PROMOTION_CHARS = ("Q", "R", "B", "N")
SAN_PIECE_CHARS = {
    Piece.W_QUEEN: "Q",
    Piece.B_QUEEN: "Q",
    Piece.W_ROOK: "R",
    Piece.B_ROOK: "R",
    Piece.W_BISHOP: "B",
    Piece.B_BISHOP: "B",
    Piece.W_KNIGHT: "N",
    Piece.B_KNIGHT: "N",
    Piece.W_KING: "K",
    Piece.B_KING: "K",
}

BIT_CODE_TO_PIECE = {
    "10001": Piece.W_KING,
    "10010": Piece.W_QUEEN,
    "10011": Piece.W_KNIGHT,
    "10100": Piece.W_BISHOP,
    "10101": Piece.W_ROOK,
    "10110": Piece.W_PAWN,
    "11001": Piece.B_KING,
    "11010": Piece.B_QUEEN,
    "11011": Piece.B_KNIGHT,
    "11100": Piece.B_BISHOP,
    "11101": Piece.B_ROOK,
    "11110": Piece.B_PAWN,
}


def create_empty_board() -> BoardGrid:
    return [[(Piece.NONE, None) for _ in range(8)] for _ in range(8)]


# 8 files x 8 ranks: (piece_type, piece_index)
INITIAL_BOARD_GRID = (
    (
        (Piece.W_ROOK, 0),
        (Piece.W_PAWN, 0),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.B_PAWN, 0),
        (Piece.B_ROOK, 0),
    ),
    (
        (Piece.W_KNIGHT, 0),
        (Piece.W_PAWN, 1),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.B_PAWN, 1),
        (Piece.B_KNIGHT, 0),
    ),
    (
        (Piece.W_BISHOP, 0),
        (Piece.W_PAWN, 2),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.B_PAWN, 2),
        (Piece.B_BISHOP, 0),
    ),
    (
        (Piece.W_QUEEN, 0),
        (Piece.W_PAWN, 3),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.B_PAWN, 3),
        (Piece.B_QUEEN, 0),
    ),
    (
        (Piece.W_KING, 0),
        (Piece.W_PAWN, 4),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.B_PAWN, 4),
        (Piece.B_KING, 0),
    ),
    (
        (Piece.W_BISHOP, 1),
        (Piece.W_PAWN, 5),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.B_PAWN, 5),
        (Piece.B_BISHOP, 1),
    ),
    (
        (Piece.W_KNIGHT, 1),
        (Piece.W_PAWN, 6),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.B_PAWN, 6),
        (Piece.B_KNIGHT, 1),
    ),
    (
        (Piece.W_ROOK, 1),
        (Piece.W_PAWN, 7),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.NONE, None),
        (Piece.B_PAWN, 7),
        (Piece.B_ROOK, 1),
    ),
)

# piece: ((file, rank), ...)
INITIAL_PIECE_LOCATIONS = {
    Piece.NONE: (),
    Piece.W_QUEEN: ((3, 0), None, None, None, None, None, None, None),
    Piece.W_KNIGHT: ((1, 0), (6, 0), None, None, None, None, None, None),
    Piece.W_BISHOP: ((2, 0), (5, 0), None, None, None, None, None, None),
    Piece.W_ROOK: ((0, 0), (7, 0), None, None, None, None, None, None),
    Piece.B_QUEEN: ((3, 7), None, None, None, None, None, None, None),
    Piece.B_KNIGHT: ((1, 7), (6, 7), None, None, None, None, None, None),
    Piece.B_BISHOP: ((2, 7), (5, 7), None, None, None, None, None, None),
    Piece.B_ROOK: ((0, 7), (7, 7), None, None, None, None, None, None),
    Piece.W_KING: ((4, 0),),
    Piece.B_KING: ((4, 7),),
    Piece.W_PAWN: tuple((file, 1) for file in range(8)),
    Piece.B_PAWN: tuple((file, 6) for file in range(8)),
}

_INITIAL_PIECE_LOCATIONS_TUPLE = tuple(
    INITIAL_PIECE_LOCATIONS[Piece(piece)] for piece in range(len(Piece))
)


def create_initial_board() -> tuple[BoardGrid, PieceLocations]:
    return [list(column) for column in INITIAL_BOARD_GRID], [
        list(slots) for slots in _INITIAL_PIECE_LOCATIONS_TUPLE
    ]


def decode_piece_locations(bit_string: str) -> tuple[BoardGrid, PieceLocations]:
    bit_index, square_index = 0, 0
    piece_locations = [[] for _ in range(len(Piece))]
    piece_locations[Piece.W_KING], piece_locations[Piece.B_KING] = [None], [None]
    board_grid = create_empty_board()

    while bit_index < len(bit_string) and square_index < 64:
        if bit_string[bit_index] == "0":
            bit_index += 1
            square_index += 1
            continue
        if len(bit_string) - bit_index < 5:
            break
        code = bit_string[bit_index : bit_index + 5]
        file_index, rank_index = ABS_TO_XY[square_index]
        if piece_type := BIT_CODE_TO_PIECE.get(code):
            if piece_type in (Piece.W_KING, Piece.B_KING):
                board_grid[file_index][rank_index] = (piece_type, 0)
                piece_locations[piece_type][0] = (file_index, rank_index)
            else:
                pieces = piece_locations[piece_type]
                slot = len(pieces)
                board_grid[file_index][rank_index] = (piece_type, slot)
                pieces.append((file_index, rank_index))
        bit_index += 5
        square_index += 1

    for piece_type in range(1, len(Piece)):
        if piece_type in (Piece.W_KING, Piece.B_KING):
            continue
        if (current_count := len(piece_locations[piece_type])) < 8:
            piece_locations[piece_type].extend([None] * (8 - current_count))
    return board_grid, piece_locations


def board_to_fen(
    board_grid: BoardGrid,
    en_passant_file: int,
    is_black_turn: int,
    white_castle_long: int,
    white_castle_short: int,
    black_castle_long: int,
    black_castle_short: int,
    fullmove_number: int,
) -> str:
    ranks = []
    for rank in reversed(range(8)):
        rank_string, empty_count = "", 0
        for file in range(8):
            piece_type, _ = board_grid[file][rank]
            if piece_type == Piece.NONE:
                empty_count += 1
            else:
                rank_string += (
                    str(empty_count) if empty_count else ""
                ) + PIECE_TO_FEN_CHAR.get(piece_type, "")
                empty_count = 0
        ranks.append(rank_string + (str(empty_count) if empty_count else ""))
    castle_string = (
        ("K" if white_castle_short else "")
        + ("Q" if white_castle_long else "")
        + ("k" if black_castle_short else "")
        + ("q" if black_castle_long else "")
    )
    en_passant_target = (
        f"{chr(ord('a') + en_passant_file - 1)}{3 if is_black_turn else 6} "
        if en_passant_file
        else "- "
    )
    return (
        f"{'/'.join(ranks)} "
        f"{'b' if is_black_turn else 'w'} "
        f"{castle_string or '-'} "
        f"{en_passant_target}0 {fullmove_number}"
    )


def decode_custom_position(
    data: memoryview | bytes, moves_offset: int
) -> tuple[BoardGrid, PieceLocations, str, bool, int]:
    en_passant_file = data[moves_offset + 5] & MASK_EN_PASSANT_FILE
    black_to_move = (data[moves_offset + 5] & MASK_TURN) >> 4
    castling_flags = data[moves_offset + 6]
    white_castle_long = castling_flags & MASK_WHITE_CASTLE_LONG
    white_castle_short = (castling_flags & MASK_WHITE_CASTLE_SHORT) >> 1
    black_castle_long = (castling_flags & MASK_BLACK_CASTLE_LONG) >> 2
    black_castle_short = (castling_flags & MASK_BLACK_CASTLE_SHORT) >> 3
    fullmove_number = data[moves_offset + 7]
    bit_string = "".join(
        f"{byte:08b}" for byte in data[moves_offset + 8 : moves_offset + 32]
    )
    board_grid, piece_locations = decode_piece_locations(bit_string)
    fen = board_to_fen(
        board_grid,
        en_passant_file,
        black_to_move,
        white_castle_long,
        white_castle_short,
        black_castle_long,
        black_castle_short,
        fullmove_number,
    )
    return (board_grid, piece_locations, fen, not bool(black_to_move), fullmove_number)


def decrease_piece_index(
    piece_locations: PieceLocations,
    board_grid: BoardGrid,
    target_type: Piece | int,
    target_piece_index: int,
) -> None:
    locations = piece_locations[target_type]
    for slot in range(target_piece_index, len(locations) - 1):
        coord = locations[slot + 1]
        locations[slot] = coord
        if coord is not None:
            board_grid[coord[0]][coord[1]] = (target_type, slot)
    locations[-1] = None


def handle_capture(
    piece_locations: PieceLocations,
    board_grid: BoardGrid,
    moving_piece_type: Piece | int,
    from_file: int,
    from_rank: int,
    to_file: int,
    target_type: Piece | int,
    target_piece_index: int | None,
) -> None:
    if (
        moving_piece_type in (Piece.W_PAWN, Piece.B_PAWN)
        and from_file != to_file
        and target_type == Piece.NONE
    ):
        enemy_pawn_type, enemy_pawn_index = board_grid[to_file][from_rank]
        board_grid[to_file][from_rank] = (Piece.NONE, None)
        if enemy_pawn_index is not None:
            piece_locations[enemy_pawn_type][enemy_pawn_index] = None
    elif target_type in (Piece.W_PAWN, Piece.B_PAWN):
        if target_piece_index is not None:
            piece_locations[target_type][target_piece_index] = None
    elif (
        target_type not in (Piece.NONE, Piece.W_KING, Piece.B_KING)
        and target_piece_index is not None
    ):
        decrease_piece_index(
            piece_locations, board_grid, target_type, target_piece_index
        )


def update_castled_rook(
    piece_locations: PieceLocations,
    board_grid: BoardGrid,
    rook_type: Piece | int,
    src_file: int,
    dst_file: int,
    rank: int,
) -> None:
    _, slot = board_grid[src_file][rank]
    board_grid[src_file][rank] = (Piece.NONE, None)
    board_grid[dst_file][rank] = (rook_type, slot)
    if slot is not None:
        piece_locations[rook_type][slot] = (dst_file, rank)


def is_path_clear(
    board_grid: BoardGrid, from_file: int, from_rank: int, to_file: int, to_rank: int
) -> bool:
    delta_file = 0 if from_file == to_file else (1 if to_file > from_file else -1)
    delta_rank = 0 if from_rank == to_rank else (1 if to_rank > from_rank else -1)
    current_file, current_rank = from_file + delta_file, from_rank + delta_rank
    while current_file != to_file or current_rank != to_rank:
        if board_grid[current_file][current_rank][0] != Piece.NONE:
            return False
        current_file += delta_file
        current_rank += delta_rank
    return True


def can_reach(
    board_grid: BoardGrid,
    piece_type: Piece | int,
    from_file: int,
    from_rank: int,
    to_file: int,
    to_rank: int,
) -> bool:
    delta_file = abs(to_file - from_file)
    delta_rank = abs(to_rank - from_rank)
    if piece_type in (Piece.W_KNIGHT, Piece.B_KNIGHT):
        return (delta_file == 1 and delta_rank == 2) or (
            delta_file == 2 and delta_rank == 1
        )
    if piece_type in (Piece.W_BISHOP, Piece.B_BISHOP):
        return (
            delta_file == delta_rank
            and delta_file > 0
            and is_path_clear(board_grid, from_file, from_rank, to_file, to_rank)
        )
    if piece_type in (Piece.W_ROOK, Piece.B_ROOK):
        return (
            (delta_file == 0 or delta_rank == 0)
            and (delta_file + delta_rank > 0)
            and is_path_clear(board_grid, from_file, from_rank, to_file, to_rank)
        )
    if piece_type in (Piece.W_QUEEN, Piece.B_QUEEN):
        return (
            (delta_file == delta_rank and delta_file > 0)
            or ((delta_file == 0 or delta_rank == 0) and delta_file + delta_rank > 0)
        ) and is_path_clear(board_grid, from_file, from_rank, to_file, to_rank)
    return False


def get_disambiguation(
    board_grid: BoardGrid,
    piece_locations: PieceLocations,
    piece_type: Piece | int,
    moving_index: int | None,
    from_file: int,
    from_rank: int,
    to_file: int,
    to_rank: int,
) -> str:
    locations = piece_locations[piece_type]
    candidates: list[tuple[int, int]] = []
    for index, coords in enumerate(locations):
        if index != moving_index and coords is not None:
            candidate_file, candidate_rank = coords
            if can_reach(
                board_grid, piece_type, candidate_file, candidate_rank, to_file, to_rank
            ):
                candidates.append((candidate_file, candidate_rank))
    if not candidates:
        return ""
    if not any(candidate_file == from_file for candidate_file, _ in candidates):
        return FILES[from_file]
    if not any(candidate_rank == from_rank for _, candidate_rank in candidates):
        return RANKS[from_rank]
    return f"{FILES[from_file]}{RANKS[from_rank]}"
