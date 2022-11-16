from typing import List, Iterable, Iterator, TypeVar
from config import FULL_KOLODA, SLICE_WO_VISIBLE, LEN_BIN_QTY, MASTI

T = TypeVar('T')

def circle_generator (iter_obj: Iterable[T]) -> Iterator[T]:
    """ круговой итератор """
    while True:
        for iter in iter_obj:
            yield iter

def circle_gen_with_first (iter_obj: Iterable[int], first_returned: int = 0) -> Iterator[int]:
    gen = circle_generator (iter_obj)
    for i in range(first_returned):
        next(gen)
    return gen

def convert_int_to_list_bin (int_val: int, len_str: int = LEN_BIN_QTY) -> List[int]:
    ''' convert int to string of bin '''
    bin_val = bin(int_val).replace('0b','')
    sss = ''.join(['0' for _ in range(len_str - len(bin_val))]) + bin_val
    return [int(s) for s in sss]

def convert_listcard_to_binlist (listcard: List[str]) -> List[int]:
    ''' convert list of card to binary list '''
    ls = [c[SLICE_WO_VISIBLE] for c in listcard] # удаляем признак видимости карт
    bin_list = [1 if k in ls else 0 for k in FULL_KOLODA]
    assert len(ls) == sum(bin_list)
    return bin_list

def convert_mastcard_to_binlist (card: str) -> List[int]:
    ''' convert mast of card to bin list [0,0,0,0] '''
    return [1 if m == card[0] else 0 for m in MASTI]