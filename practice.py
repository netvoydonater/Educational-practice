import csv
from typing import List, Optional

MAX_CRYPTOS = 100

class Cryptocurrency:
    def __init__(self, name: str, symbol: str, price: float, market_cap: float, circulating_supply: float):
        self.Name = name
        self.Symbol = symbol
        self.Price = price
        self.Market_cap = market_cap
        self.Circulating_supply = circulating_supply

class ListNode:
    def __init__(self, data: Cryptocurrency, next_node=None):
        self.data = data
        self.next = next_node

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

def replace_comma_with_dot(input_str: str) -> str:
    return input_str.replace(',', '.')

def remove_quotes(input_str: str) -> str:
    return input_str.replace('"', '')

def load_from_file(crypto_list: LinkedList) -> None:
    try:
        with open('currencies25.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Пропускаем заголовок
            
            for row in reader:
                if not row:
                    continue
                
                try:
                    name = remove_quotes(row[0])
                    symbol = remove_quotes(row[1])
                    price = float(replace_comma_with_dot(remove_quotes(row[2])))
                    market_cap = float(replace_comma_with_dot(remove_quotes(row[3])))
                    circulating_supply = float(replace_comma_with_dot(remove_quotes(row[4])))
                    
                    crypto = Cryptocurrency(name, symbol, price, market_cap, circulating_supply)
                    new_node = ListNode(crypto)
                    
                    if not crypto_list.head:
                        crypto_list.head = crypto_list.tail = new_node
                    else:
                        crypto_list.tail.next = new_node
                        crypto_list.tail = new_node
                        
                except (IndexError, ValueError) as e:
                    print(f"Ошибка при парсинге строки: {row}\nПричина: {e}")
                    continue
                    
    except FileNotFoundError:
        print("Ошибка в открытии файла!")
        return

def print_crypto(crypto: Cryptocurrency) -> None:
    print(f"Название: {crypto.Name}")
    print(f"Символ: {crypto.Symbol}")
    print(f"Цена: {crypto.Price:.2f} USD")
    print(f"Рыночная капитализация: {crypto.Market_cap:.2f}")
    print(f"Оборот: {crypto.Circulating_supply:.2f} токенов\n")

def print_all_cryptos(crypto_arr: List[ListNode], size: int) -> None:
    print(f"=== Все криптовалюты ({size} шт.) ===")
    for i in range(size):
        print_crypto(crypto_arr[i].data)
    print("=======================")

def fill_array(crypto_list: LinkedList, arr: List[Optional[ListNode]], max_count: int) -> int:
    count = 0
    current = crypto_list.head
    while current and count < max_count:
        arr[count] = current
        count += 1
        current = current.next
    return count

def sort_cryptos(arr: List[ListNode], size: int) -> None:
    for i in range(size - 1):
        for j in range(size - i - 1):
            if arr[j].data.Name > arr[j + 1].data.Name:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def sort_quick_v2(arr: List[ListNode], left: int, right: int) -> None:
    if left >= right:
        return
    pivot = arr[(left + right) // 2].data.Name
    i, j = left, right

    while i <= j:
        while arr[i].data.Name < pivot:
            i += 1
        while arr[j].data.Name > pivot:
            j -= 1
        if i <= j:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1
    
    if j - left < right - i:
        sort_quick_v2(arr, left, j)
        left = i
    else:
        sort_quick_v2(arr, i, right)
        right = j
    
    if left < right:
        sort_quick_v2(arr, left, right)

def binary_search_by_name(arr: List[ListNode], size: int, target: str) -> int:
    left, right = 0, size - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid].data.Name == target:
            return mid
        elif arr[mid].data.Name < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def free_list(crypto_list: LinkedList) -> None:
    current = crypto_list.head
    while current:
        next_node = current.next
        del current
        current = next_node
    crypto_list.head = crypto_list.tail = None

def main():
    crypto_list = LinkedList()
    load_from_file(crypto_list)

    ptr_arr = [None] * MAX_CRYPTOS
    count = fill_array(crypto_list, ptr_arr, MAX_CRYPTOS)
    
    if count == 0:
        print("Данные не загружены. Проверьте содержимое файла.")
        return

    # Выберите метод сортировки (раскомментируйте нужный)
    sort_cryptos(ptr_arr, count)
    # sort_quick_v2(ptr_arr, 0, count - 1)

    while True:
        print("\n1. Поиск по названию")
        print("2. Вывести все криптовалюты")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            query = input("Введите название криптовалюты: ").strip()
            index = binary_search_by_name(ptr_arr, count, query)
            if index != -1:
                print_crypto(ptr_arr[index].data)
            else:
                print("Криптовалюта не найдена!")
        elif choice == "2":
            print_all_cryptos(ptr_arr, count)
        else:
            print("Неверный ввод!")

    free_list(crypto_list)

if __name__ == "__main__":
    main()