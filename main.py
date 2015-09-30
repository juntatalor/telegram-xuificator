
from tornado import gen, ioloop
from telezombie import api
import re
from random import choice


def make_x(s):
    vocals = 'аеёиоуыэюя'
    for i, l in enumerate(s):
        if l in vocals and i != len(s) - 1:
            if l == 'о':
                l1 = 'е'
            elif l == 'а':
                l1 = 'я'
            elif l == 'у':
                l1 = 'ю'
            elif l == 'ы':
                l1 = 'и'
            else:
                l1 = l
            return 'ху' + l1 + s[i + 1:]
    return s


class Xuificator(api.TeleLich):
    XUI_PHRASES = ['Ну же, пиши хуй, не стесняйся!',
                   'Че цензуришь? Не четкий чель?',
                   'В жопу себе звездочки поставь',
                   'Орел комнатный? Без цензуры не можешь?',
                   'Раз, два, три... Звездочки нахуй убери!']

    RUDE_PHRASES = ['ПВП или зассал?',
                    'Тебя мама по губам отшлепает',
                    'Я не буду больше с тобой разговаривать',
                    'Тебе не надоело?',
                    'Не приставай ко мне',
                    'Заебываешь, блять!',
                    'Я тебя по IP вычислю!',
                    'Я если я тебя в реале найду?',
		    'Нахуй иди',
                    'Иди нахуй',
                    'Поешь говна, грубиян-хуиян']

    def __init__(self, api_token):
        super(Xuificator, self).__init__(api_token)

    @gen.coroutine
    def on_text(self, message):
        chat = message.chat

        lt = message.text.lower()

        # Не надо цензуры!
        p = re.compile(r'х[!@#$%^&*()]+[йяюи]')
        if p.search(lt):
            yield self.send_message(chat.id_, choice(self.XUI_PHRASES))
            return

        # Не надо обижать бота!
#        p = re.compile(
#            r'(х(у+)(й|и|ю|я|е))|(дурак)|(идиот)|(лох)|(лош(о|а))|(пид(о|р))|(педик)|(г(о|а)ндон)|с(у+)(к|ч|(чк))(а+)|(муд(о|а))')
	p = re.compile(
             r'((сам)? ?(ты)? ?(сам)?|((по)?сл(у|ы)ш(ай)?)) ?,? (х(у+)(й|и|ю|я|е))|(дурак)|(идиот)|(лох)|(лош(о|а))|(пид(о|р))|(педик)|(г(о|а)ндон)|с(у+)(к|ч|(чк))(а+)|(муд(о|а))')
        if p.search(lt):
            yield self.send_message(chat.id_, choice(self.RUDE_PHRASES))
            return

        text = lt.split(' ')

        if text[0][0] == '/':
            # Не обрабатываем команды. Особенно от сторонних ботов.
            return

        text = [make_x(x) for x in text if x != '@xuifikatorbot' and x[0] != '/']

        res = ' '.join(text)
        if res[-1:] == '?':
            res = res[:-1] + ', блять!'

        yield self.send_message(chat.id_, res)


@gen.coroutine
def forever():
    api_token = ''
    proc = Xuificator(api_token)

    yield proc.poll()


if __name__ == "__main__":
    main_loop = ioloop.IOLoop.instance()
    main_loop.run_sync(forever)
