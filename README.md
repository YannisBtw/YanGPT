# YanGPT

## Обзор
YanGPT - это Телеграм бот, созданный для общения и помощи в повседневных задачах. Он может стать вашим помощником по домашним заданиям, поддержать беседу о личных переживаниях или помочь с любыми другими вопросами.

## Алгоритм работы
1. Бот принимает текстовое или голосовое сообщение.
2. Если это текст, он отправляется в YandexGPT.
3. Если это голосовое сообщение:
   - Оно преобразуется в текст с помощью SpeechKit.
   - Текст отправляется в YandexGPT.
   - Ответ от YandexGPT преобразуется обратно в голос через SpeechKit.
4. Бот отправляет ответ пользователю в том же формате, в котором был получен запрос.

## Дополнительные функции
- Контроль расходов и ограничение пользователя по токенам и аудиоблокам.

## Ошибки и журналирование
- Все ошибки записываются в файл `bot.log`.
- При ошибке подключения к API GPT, бот уведомляет пользователя.
- Если запрос слишком длинный, бот попросит его укоротить.

## Контакты
- **Telegram**: https://t.me/GPTbyYannis_bot или @GPTbyYannis_bot
- **Telegram автора**: https://t.me/yanniskekw или @yanniskekw

## Заметки разработчика
Это проект был сложным, но интересным вызовом. Я работал над ним много и надеюсь, что он принесет пользу пользователям. Спасибо за поддержку и понимание!
