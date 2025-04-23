#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iomanip>
#include <algorithm>

const int MAX_CRYPTOS = 100;

using namespace std;

struct Cryptocurrency
{
    string Name;
    string Symbol;
    double Price;
    double Market_cap;
    double Circulating_supply;
};

struct ListNode
{
    Cryptocurrency data;
    ListNode *next;
};

struct LinkedList
{
    ListNode *head = nullptr;
    ListNode *tail = nullptr;
};

string replace_comma_with_dot(const string &input)
{
    string result = input;
    replace(result.begin(), result.end(), ',', '.');
    return result;
}

string remove_quotes(const string &input)
{
    string result = input;
    result.erase(remove(result.begin(), result.end(), '\"'), result.end());
    return result;
}

void load_from_file(LinkedList &list)
{
    ifstream file("currencies25.csv");
    if (!file.is_open())
    {
        cout << "Ошибка в открытии файла!" << endl;
        return;
    }

    string line;
    // Пропускаем только строку заголовка
    if (!getline(file, line))
    {
        cerr << "Ошибка: файл пуст!" << endl;
        return;
    }

    while (getline(file, line))
    {
        if (line.empty())
            continue;

        stringstream ss(line);
        Cryptocurrency crypto;

        try
        {
            // Name
            string field;
            getline(ss, field, ',');
            crypto.Name = remove_quotes(field);

            // Symbol
            getline(ss, field, ',');
            crypto.Symbol = remove_quotes(field);

            // Price
            getline(ss, field, ',');
            crypto.Price = stod(replace_comma_with_dot(remove_quotes(field)));

            // Market Cap
            getline(ss, field, ',');
            crypto.Market_cap = stod(replace_comma_with_dot(remove_quotes(field)));

            // Circulating Supply
            getline(ss, field);
            crypto.Circulating_supply = stod(replace_comma_with_dot(remove_quotes(field)));
        }
        catch (const exception &e)
        {
            cerr << "Ошибка при парсинге строки: " << line << "\nПричина: " << e.what() << endl;
            continue;
        }

        ListNode *newNode = new ListNode{crypto, nullptr};
        if (!list.head)
            list.head = list.tail = newNode;
        else
        {
            list.tail->next = newNode;
            list.tail = newNode;
        }
    }
    file.close();
}

void print(const Cryptocurrency &crypto)
{
    cout << fixed << setprecision(2);
    cout << "Название: " << crypto.Name << "\n"
         << "Символ: " << crypto.Symbol << "\n"
         << "Цена: " << crypto.Price << " USD\n"
         << "Рыночная капитализация: " << crypto.Market_cap << "\n"
         << "Оборот: " << crypto.Circulating_supply << " токенов\n\n";
    cout << defaultfloat;
}

void print_all_cryptos(ListNode *arr[], int size)
{
    cout << "=== Все криптовалюты (" << size << " шт.) ===\n";
    for (int i = 0; i < size; i++)
    {
        print(arr[i]->data);
    }
    cout << "=======================\n";
}

int fill_array(LinkedList &list, ListNode *arr[], int max_count)
{
    int count = 0;
    ListNode *current = list.head;
    while (current && count < max_count)
    {
        arr[count++] = current;
        current = current->next;
    }
    return count;
}

void sort_cryptos(ListNode *arr[], int size)
{
    for (int i = 0; i < size - 1; i++)
    {
        for (int j = 0; j < size - i - 1; j++)
        {
            if (arr[j]->data.Name > arr[j + 1]->data.Name)
                swap(arr[j], arr[j + 1]);
        }
    }
}

void sort_quick_v2(ListNode *arr[], int left, int right)
{
    if (left >= right)
        return;
    string pivot = arr[(left + right) / 2]->data.Name;
    int i = left, j = right;

    while (i <= j)
    {
        while (arr[i]->data.Name < pivot)
        {
            i++;
        }
        while (arr[i]->data.Name > pivot)
        {
            j--;
        }
        if (i <= j)
        {
            swap(arr[i], arr[j]);
            i++;
            j--;
        }
    }
    if (j - left < right - i)
    {
        sort_quick_v2(arr, left, j);
        left = i;
    }
    else
    {
        sort_quick_v2(arr, i, right);
        right = j;
    }
    if (left < right)
        sort_quick_v2(arr, left, right);
}

int binary_search_by_name(ListNode *arr[], int size, const string &target)
{
    int left = 1;
    int right = size - 1;

    while (left < right)
    {
        int mid = left + (right - left) / 2;
        if (arr[mid]->data.Name == target)
            return mid;
        else if (arr[mid]->data.Name < target)
            left = mid + 1;
        else
            right = mid;
    }
    return -1;
}

void free_list(LinkedList &list)
{
    ListNode *current = list.head;
    while (current)
    {
        ListNode *next = current->next;
        delete current;
        current = next;
    }
    list.head = list.tail = nullptr;
}

int main()
{
    setlocale(LC_ALL, "ru");
    LinkedList cryptoList;
    load_from_file(cryptoList);

    ListNode *ptrArr[MAX_CRYPTOS];
    int count = fill_array(cryptoList, ptrArr, MAX_CRYPTOS);
    if (count == 0)
    {
        cerr << "Данные не загружены. Проверьте содержимое файла." << endl;
        return 1;
    }

    sort_cryptos(ptrArr, count);
    // sort_quick_v2(ptrArr, 0, count - 1);

    string query;
    while (true)
    {
        cout << "1. Поиск по названию\n"
             << "2. Вывести все криптовалюты\n"
             << "0. Выход\n"
             << "Выберите действие: ";

        getline(cin, query);

        if (query == "0")
            break;
        else if (query == "1")
        {
            cout << "Введите название криптовалюты: ";
            getline(cin, query);
            int index = binary_search_by_name(ptrArr, count, query);
            if (index != -1)
                print(ptrArr[index]->data);
            else
                cout << "Криптовалюта не найдена!\n";
        }
        else if (query == "2")
            print_all_cryptos(ptrArr, count);
        else
            cout << "Неверный ввод!\n";
    }

    free_list(cryptoList);
    return 0;
}
