from settings import PATH_FILE
from json_saver import JSONSaver
from main_utils import get_selected_platforms, get_vacancies, \
    get_search_query_and_area, print_vacancies, delete_vacancies, \
    sort_vacancies, load_area_dicts


json_saver = JSONSaver(PATH_FILE)
PLATFORMS = ['HeadHunter', 'headhunter', 'hh', 'SuperJob', 'superjob', 'sj']


def user_inter():
    """
    Функция работы с пользователем по вакансиям
    """
    # Вспомогательная переменная для цикла while
    program_exit = False

    # Цикл while с флагом program_exit принимает значение False до тех пор, пока пользователь не введет команду 'нет'
    while not program_exit:
        # Создание списка с выбранной платформой, на которой будем осуществляться поиск
        api_list = get_selected_platforms(PLATFORMS)

        # Создание переменной для выбранного пользователем города
        area_hh, area_sj = load_area_dicts()
        # Создание переменной с поиском запроса и городом запроса, поиск вакансий по этим критериям
        search_query, search_area_hh, search_area_sj = \
            get_search_query_and_area(area_hh, area_sj)

        # Передача созданных переменных в функцию, которая создает экземпляры вакансий и добавляет их в список
        # Обращение к функциям, которые запрашивают у пользователя данные для фильтрации по зарплате и требованиям.
        get_vacancies(json_saver, api_list, search_query,
                      search_area_hh, search_area_sj)

        # Установка переменной для списка
        filtered_vacancies = json_saver.data

        # Запрос о сортировке.
        if filtered_vacancies:
            choice = input("Хотите отсортировать вакансии по зарплате? "
                           "(да/нет): ")
            if choice.lower() == 'да':
                order = input("Введите порядок сортировки "
                              "(возрастание - 1/убывание - 2): ")
                # Значение top_n может быть больше,
                # чем количество отфильтрованных вакансий
                top_n = (input("Введите количество вакансий для вывода: "))
                sorted_vacancies = sort_vacancies(filtered_vacancies,
                                                  order, top_n)

                if sorted_vacancies:
                    print_vacancies(sorted_vacancies)
                    delete_vacancies(json_saver, sorted_vacancies)
            else:
                print("Вы отказались от сортировки.")
                # Значение top_n может быть больше,
                # чем количество отфильтрованных вакансий
                top_n = (input("Введите количество вакансий для вывода: "))
                filtered_vacancies = filtered_vacancies[:int(top_n)] \
                    if top_n else filtered_vacancies
                if filtered_vacancies:
                    print_vacancies(filtered_vacancies)
                    delete_vacancies(json_saver, filtered_vacancies)
                else:
                    print("Нет вакансий, соответствующих заданным критериям.")

        # Выход из программы
        exit_or_not = input("Хотите начать поиск заново? (да/нет): ")
        if exit_or_not.lower() == 'нет':
            program_exit = True
            delete_vacancies(json_saver, filtered_vacancies)
        delete_vacancies(json_saver, filtered_vacancies)


if __name__ == "__main__":
    user_inter()