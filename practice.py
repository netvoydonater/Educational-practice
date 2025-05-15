import csv

class Cryptocurrency:
    def __init__(self, name: str, symbol: str, price: float, market_cap: float, circulating_supply: float):
        self.name = name
        self.symbol = symbol
        self.price = price
        self.market_cap = market_cap
        self.circulating_supply = circulating_supply

def clean_string(value: str) -> str:
    return value.replace('"', '').replace(',', '.')

def load_cryptos(filename: str) -> list[Cryptocurrency]:
    cryptos = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            
            for row in reader:
                try:
                    cryptos.append(Cryptocurrency(
                        name=clean_string(row[0]),
                        symbol=clean_string(row[1]),
                        price=float(clean_string(row[2])),
                        market_cap=float(clean_string(row[3])),
                        circulating_supply=float(clean_string(row[4]))
                    ))
                except (IndexError, ValueError) as e:
                    print(f"Ошибка в строке: {row} - {e}")
    except FileNotFoundError:
        print("Файл не найден!")
    return cryptos

def print_crypto(crypto: Cryptocurrency) -> None:
    print(f"\nНазвание: {crypto.name}")
    print(f"Символ: {crypto.symbol}")
    print(f"Цена: {crypto.price:.2f} USD")
    print(f"Капитализация: {crypto.market_cap:.2f}")
    print(f"Оборот: {crypto.circulating_supply:.2f}")

def main():
    cryptos = load_cryptos('currencies25.csv')
    if not cryptos:
        return

    # Сортируем по имени для бинарного поиска
    cryptos.sort(key=lambda x: x.name)

    while True:
        print("\n1. Поиск по названию")
        print("2. Показать все")
        print("0. Выход")
        choice = input("Выберите: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            query = input("Название: ").strip()
            # Бинарный поиск
            left, right = 0, len(cryptos) - 1
            found = None
            while left <= right:
                mid = (left + right) // 2
                if cryptos[mid].name.lower() == query.lower():
                    found = cryptos[mid]
                    break
                elif cryptos[mid].name.lower() < query.lower():
                    left = mid + 1
                else:
                    right = mid - 1
            
            print_crypto(found) if found else print("Не найдено!")
        elif choice == "2":
            for crypto in cryptos:
                print_crypto(crypto)
        else:
            print("Неверный ввод!")

if __name__ == "__main__":
    main()