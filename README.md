# Python-projects-hackathon-2021
Project for hackathon`21, "Keyboard trainer" game

## "Игра 'Клавиатурный тренажер'."

![Интерфейс](/forms/light.png)

Игра содержит 8 уровней:
*	с 1 по 5 уровень - случайный набор символов,
*	6, 7 уровни - случайный выбор слова из списка слов,
*	8 уровень - предложение.

На каждом уровне предлагается по 10 наборов символов / слов / предложений.
Уровни предполагают как регистрозависимый ввод (фиолетовый фон поля), так и игнорирование регистра при вводе (зеленый фон поля).
Доступна регистрация с последующим сохранением результатов в базе и авторизация.
Зарегистрированным пользователям также доступны настройки:
•	выбор уровня (1-8);
•	языка набота символов / слов / предложений (английский (EN), русский (RU));
•	ориентация окна (горизонтально (H), вертикально (V));
•	выбор темы (светлая (light), темная (dark));
•	отображение предупреждений при новой игре и регистрозависимых уровнях.

В игре реализован редактор тем оформления, где пользователь может изменить существующие темы оформления, и на их основе создать свою, особенную, для последующего использования.
Зарегистрированный пользователь может сохранить темы в файл .json и при следующем запуске файл подгрузится в список тем. Обычный пользователь может пользоваться темами и изменять существующие, но только в рамках текущего запуска.

ВНИМАНИЕ! Если вы создаете свою тему - обязательно меняйте название и псевдоним темы.

Пользователь Anonymous - зарезервирован.

После прохождения каждого уровня предлагается продолжить игру.
Если пользователь не продолжает - ставится пауза и при следующем старте игра продолжится с этого места.

При проигрыше у зарегистрированного пользователя игра возобновляется с текущего уровня, незарегистрированный пользователь начинает с 1 уровня.

#### Ограничение на длину логина - 12 символов.
#### Ограничение на длину пароля  - 32 символа.
#### Ограничение на длину названия темы / псевдонима темы - 25 символов.

#### Команда "ПНЗКН Хакатон'21".
#### [@Prospero2005](https://t.me/prospero2005) (Идея, логика, сборка)
#### [@Posegrey](https://t.me/Posegrey) (База данных)
#### [@Lenz_Gardfild](https://t.me/Lenz_Gardfild) (Подбор данных, тесты)
#### [@quqpup](https://t.me/quqpup) (Интерфейс, отладка)

