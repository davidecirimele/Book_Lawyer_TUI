from dataclasses import field, InitVar, dataclass
from typing import Callable, List, Dict, Optional, Any

from typeguard import typechecked
from valid8 import validate

from validation.regex import pattern


@typechecked
@dataclass(order=True, frozen=True)
class Description:
    value: str

    def __post_init__(self):
        validate('Description.value', self.value, min_len=1, max_len=1000, custom=pattern(r'[0-9A-Za-z ;.,_-]*'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(order=True, frozen=True)
class Key:
    value: str

    def __post_init__(self):
        validate('Key.value', self.value, min_len=1, max_len=10, custom=pattern(r'[0-9A-Za-z_-]*'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True)
class Entry:
    key: Key
    description: Description
    on_selected: Callable[[], None] = field(default=lambda: None)
    is_exit: bool = field(default=False)
    is_visible_by_anyone: bool = field(default=False)

    @staticmethod
    def create(key: str, description: str, on_selected: Callable[[], None] = lambda: None,
               is_exit: bool = False) -> 'Entry':
        return Entry(Key(key), Description(description), on_selected, is_exit)


@typechecked
@dataclass(frozen=True)
class Menu:
    description: Description

    auto_select: Callable[[], None] = field(default=lambda: None)
    __entries: List[Entry] = field(default_factory=list, repr=False, init=False)
    __key2entry: Dict[Key, Entry] = field(default_factory=dict, repr=False, init=False)
    create_key: InitVar[Any] = field(default='None')

    def __post_init__(self, create_key: Any):
        validate('create_key', create_key, custom=Menu.Builder.is_valid_key)

    def _add_entry(self, value: Entry, create_key: Any) -> None:
        validate('create_key', create_key, custom=Menu.Builder.is_valid_key)
        validate('value.key', value.key, custom=lambda v: v not in self.__key2entry)
        self.__entries.append(value)
        self.__key2entry[value.key] = value

    def _has_exit(self) -> bool:
        return bool(list(filter(lambda e: e.is_exit, self.__entries)))

    def __print(self) -> None:
        length = len(str(self.description))

        fmt = '***{}{}{}***'
        print(fmt.format('*', '*' * length, '*'))
        print(fmt.format(' ', self.description.value, ' '))
        print(fmt.format('*', '*' * length, '*'))
        self.auto_select()
        for entry in self.__entries:
            print(f'{entry.key}:\t{entry.description}')

    def __select_from_input(self) -> bool:
        while True:
            try:
                line = input("What do you want to do? ")

                key = Key(line.strip())
                entry = self.__key2entry[key]
                entry.on_selected()
                return entry.is_exit
            except (KeyError, TypeError, ValueError) as e:
                print('Invalid selection. Please, try again...')

    def run(self) -> None:
        while True:
            self.__print()
            is_exit = self.__select_from_input()
            if is_exit:
                return
    @typechecked
    @dataclass()
    class Builder:
        __menu: Optional['Menu']
        __create_key = object()

        def __init__(self, description: Description, auto_select: Callable[[], None] = lambda: None):
            self.__menu = Menu(description, auto_select, self.__create_key)

        @staticmethod
        def is_valid_key(key: Any) -> bool:
            return key == Menu.Builder.__create_key

        def with_entry(self, value: Entry) -> 'Menu.Builder':
            validate('menu', self.__menu)
            self.__menu._add_entry(value, self.__create_key)
            return self

        def build(self) -> 'Menu':
            validate('menu', self.__menu)
            validate('menu.entries', self.__menu._has_exit(), equals=True)
            res, self.__menu = self.__menu, None
            return res
