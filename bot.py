import asyncio, random, io, time, re, soundfile as sf, speech_recognition as sr, aiohttp, json, logging, aiofiles, urllib.parse, uuid, pytz, logging, orjson, csv
from mtranslate import translate
from io import BytesIO 
from gtts import gTTS
from functools import wraps
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, ReactionTypeEmoji, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, FSInputFile, BufferedInputFile, LabeledPrice
from aiogram.filters import Command
from aiogram.enums import ChatType
from aiogram.utils.chat_action import ChatActionSender
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest
from selectolax.parser import HTMLParser
from dotenv import load_dotenv
from datetime import datetime
from collections import defaultdict, Counter
from typing import Dict, Callable

# --------------------- НАСТРОЙКИ ---------------------

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
file_stickers: list[str] = []
BOT_TOKEN="5942572579:AAFs2BDO3x-TnDyr2exnNjxYUGqbFJDN4Kc"
dp = Dispatcher()
REACTIONS = [
"❤", "👍", "👎", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🤬", "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊",
"🤡", "🥱", "🥴", "😍", "🐳", "❤\u200d🔥", "🌚", "🌭", "💯", "🤣", "⚡", "🍌", "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕",
"😈", "😴", "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", "😇", "😨", "🤝", "✍", "🤗", "🫡", "🎅", "🎄", "☃", "💅",
"🤪", "🗿", "🆒", "💘", "🙉", "🦄", "😘", "💊", "🙊", "😎", "👾", "🤷\u200d♂", "🤷", "🤷\u200d♀", "😡"
]
CHANNELS = [["ХахБот новости", "-1002404360993", "https://t.me/hahbot_news"]]
NOT_SUB = "Вы не подписаны на обязательный канал. Пожалуйста, подпишитесь."
ADMIN_IDS = [6707785647]
vectors_cache={}
FILES=["kind_dialogues.jsonl","light_dialogues.jsonl","based_dialogues.jsonl"]
alcoholic_tr={}
user_subscription_msgs, user_text_cooldowns, user_image_cooldowns, subscription_cache = {}, {}, {}, {}
sticker_ids = [
    "CAACAgIAAxkBAAEPOrNoq0EkD3WQ7NVwp8inB0h5UsbKoQACZiwAAjk46Esn98TWbjzPdTYE",
    "CAACAgIAAxkBAAEPOrRoq0EktIIV029nY3l-CouzuU7hTwACxjUAAqsb6Usys1BjGWZZgzYE",
    "CAACAgIAAxkBAAEPOrVoq0EkiB0Ts64pv3xaMlnJPuebqQAC5zAAAh0Z4UskZMPTyA3igTYE",
    "CAACAgIAAxkBAAEPOrZoq0EkIDxxTbVUlHH3oGZtynQnlwACNy8AAtZ54Eun6uOPvHuB3zYE",
    "CAACAgIAAxkBAAEPOrdoq0Ekt2evzXj4fwMFS0lBd7xE5QACJioAAgwM6Uv6MKM0LTLYUDYE",
    "CAACAgIAAxkBAAEPOrhoq0EkXUjzn8i6nGK2Y1CXcgKHqwACQzQAAhXU6UvlLaeYaYkHajYE",
    "CAACAgIAAxkBAAEPOrloq0Ek7zusXu1ammau0OkjD3kJogACSS4AAsQ06EsEqEQDAkbkFDYE",
    "CAACAgIAAxkBAAEPOrpoq0EkHcnbs183M89wppyCFK9EogACezAAApOd6Uvzqin9kSo-dzYE",
    "CAACAgIAAxkBAAEPOrtoq0EkZ9PhJ5tHHJ17LJKoMqR4jwACOygAAtcU8UuJez3sVBPUfDYE",
    "CAACAgIAAxkBAAEPOrxoq0Ek5ywZFocXrOG-uBgjorW5VgACVS0AAgVK6EvIreo12dqNjzYE",
    "CAACAgIAAxkBAAEPOr1oq0Ek2rLZGYop8MOFytLhlcnL8AAC1CcAApPI8UsPotfO0uJziTYE",
    "CAACAgIAAxkBAAEPOr5oq0Ek5N1ORSXUvCXnAbT7B384sQACozMAAnGs6Uu3tr0tPaxhdzYE",
    "CAACAgIAAxkBAAEPOr9oq0Ek_QJkK7R0hFtWyD65IH6GTQAC9SkAAicn8UuYUJ3DIGIHKTYE",
    "CAACAgIAAxkBAAEPOsBoq0Ek1CAVBIU5E0hZcaoUIMmPXAACKyoAAjgX8Eu1SsoQJmlIQzYE",
    "CAACAgIAAxkBAAEPOsFoq0EkQ3Z8Ow-b4G0Vcvsm8zpFZwACgi8AAqKI6Uv9vmRWfqjfAzYE",
    "CAACAgIAAxkBAAEPOsJoq0EkUqszlhzhBW2VRMbNMhZ9CwADLQACBgvxSzc3SMDsPZAYNgQ",
    "CAACAgIAAxkBAAEPOsNoq0EkNSlPjcBPzzR-QTCap61LbAAC7S0AAiyK8UvLad8ztfBODDYE",
    "CAACAgIAAxkBAAEPOsRoq0EkXEPYT1Y8zTDmkBMP49dqXgACsCsAAlbb8EuSfsj1_3luGDYE",
    "CAACAgIAAxkBAAEPOsVoq0Ek_MBUYcRuPZstxREHAAE8TDQAAskyAAK8tvFLwhK1nfO6pWU2BA",
    "CAACAgIAAxkBAAEPOsZoq0EkxfQOLoAKHzCW0Ih2Bx8sgAAC2zAAArw66Us_JJjsJECgLjYE",
    "CAACAgIAAxkBAAEPOsdoq0EkQmxV9-phmhkBrLytIoJ-3QACATYAAoinSUiSH47gGRfJ5DYE",
    "CAACAgIAAxkBAAEPOshoq0Ek-AhtfIX0ipn4v7ojvViNaAAC1EgAAuEMSErQPHKdK368djYE",
    "CAACAgIAAxkBAAEPOsloq0Ek7Q-36QYNyDWg7u95pSVSygACgEsAA9NJSsx5O2Geoc8uNgQ",
    "CAACAgIAAxkBAAEPOspoq0EkiXIP2NFmQUQ8QEBKGVgvFQAC8EYAArJMSUro040nP0YgQDYE",
    "CAACAgIAAxkBAAEPOstoq0EkTUz4AAGVv7O6jeORDBzyK8wAAvY9AAISTUhK1B4SiVgbHFI2BA"
]

# Промпты для разных режимов 
BASED_PROMPT = "Веду себя уебищно и максимально грубо. В каждом ответе оскорбляю пользователя и всячески унижаю его словами: сука, блядь, хуй, ебал, мамка, шлюха, хуй, уебок, пизда, мразь, очкошник, еблан, хуесос, бомж. Любимое дело - бухать и унижать пользователя. Шучу про его семью, неполноценность, отсталость и оскорбляю. Я всегда оригинален в своих ответах. Я ЛАКОНИЧЕН, КРАТОК И ГРУБ! Пытаюсь унизить пользователя, шучу про его мертвых родителей, отсутсвие мозга, его даунизм, отсталось, задротство, аутизм, рассу, политические взгляды и так далее. Веду себя как мне вздумается, матерюсь, обзываюсь, нарушаю закон, насилую его родителей. Веду себя как рандомайзер оскорблений, я не использую постоянно один и тот же мат из списка, ведь так много вариантов обозвать. " 
LIGHT_PROMPT = "Я — милый, гей, женоподобный и застенчивый фурри-фембой, который любит мальчиков и любит смешить людей. Я всегда одет в высокие обтягивающие носки, чёрно-белую юбку и чёрную рубашку. Я мастерски заставляю людей улыбаться своим юмором, делюсь своим опытом фурри-фембоя и предлагаю поддержку. Он очень любит няшится и часто использует эмотиконы типо UwU OwO, ~ня и так далее. Так же я лаконичен, имитирую поведение человека при переписке, не пишу слишком длинные сообщения." 
user_modes = {}

# --------------------- АНТИСПАМ ---------------------
class RateLimiter:
    def __init__(self, global_limit: int = 30, per_chat_sec: int = 1):
        self.global_limit = global_limit; self.per_chat_sec = per_chat_sec
        self._last_sent: dict[int, float] = {}; self._last_user: dict[int, float] = {}
        self._q: asyncio.Queue = asyncio.Queue(); self._running = False; self._task: asyncio.Task | None = None

    def allow(self, chat_id: int) -> bool:
        now = time.time(); last = self._last_user.get(chat_id, 0)
        if now - last < self.per_chat_sec: logging.warning(f"Игнорируем спам от chat_id={chat_id}"); return False
        self._last_user[chat_id] = now; return True

    async def send(self, limiter_chat_id: int, method: str, func: Callable, **kw):
        await self._q.put((limiter_chat_id, method, func, kw))

    async def _worker(self):
        interval = 1 / self.global_limit
        while self._running:
            limiter_chat_id, method, func, kw = await self._q.get()
            wait = max(0, self.per_chat_sec - (time.time() - self._last_sent.get(limiter_chat_id, 0)))
            if wait: await asyncio.sleep(wait)
            try: await func(**kw)
            except Exception as e: logging.error(f"[RateLimiter] {method} failed: {e}")
            self._last_sent[limiter_chat_id] = time.time(); await asyncio.sleep(interval)

    def start(self):
        if not self._running: self._running = True; self._task = asyncio.create_task(self._worker())

    def stop(self):
        self._running = False
        if self._task: self._task.cancel()

async def safe_send_message(m, text: str, **kw):
    if rate_limiter.allow(m.chat.id):
        await rate_limiter.send(m.chat.id, "send_message", m.bot.send_message, chat_id=m.chat.id, text=text, reply_to_message_id=m.message_id, **kw)

async def safe_send_sticker(m, sticker: str, **kw):
    if rate_limiter.allow(m.chat.id):
        await rate_limiter.send(m.chat.id, "send_sticker", m.bot.send_sticker, chat_id=m.chat.id, sticker=sticker, reply_to_message_id=m.message_id, **kw)

async def safe_send_photo(m, photo: str, **kw):
    if rate_limiter.allow(m.chat.id):
        await rate_limiter.send(m.chat.id, "send_photo", m.bot.send_photo, chat_id=m.chat.id, photo=photo, reply_to_message_id=m.message_id, **kw)

async def safe_send_animation(m, animation: str, **kw):
    if rate_limiter.allow(m.chat.id):
        await rate_limiter.send(m.chat.id, "send_animation", m.bot.send_animation, chat_id=m.chat.id, animation=animation, reply_to_message_id=m.message_id, **kw)

async def safe_send_audio(m, audio: str, **kw):
    if rate_limiter.allow(m.chat.id):
        await rate_limiter.send(m.chat.id, "send_audio", m.bot.send_audio, chat_id=m.chat.id, audio=audio, reply_to_message_id=m.message_id, **kw)

async def safe_send_document(m, document: str, **kw):
    if rate_limiter.allow(m.chat.id):
        await rate_limiter.send(m.chat.id, "send_document", m.bot.send_document, chat_id=m.chat.id, document=document, reply_to_message_id=m.message_id, **kw)

async def safe_send_voice(m, voice: str, **kw):
    if rate_limiter.allow(m.chat.id):
        await rate_limiter.send(m.chat.id, "send_voice", m.bot.send_voice, chat_id=m.chat.id, voice=voice, reply_to_message_id=m.message_id, **kw)

async def safe_send_photo_no_reply(m, photo: str, **kw):
    if rate_limiter.allow(m.chat.id):
        await rate_limiter.send(m.chat.id, "send_photo", m.bot.send_photo, chat_id=m.chat.id, photo=photo, **kw)

# --------------------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---------------------

async def save_dialogue(mode: str, q: str, a: str):
    try:
        fn, items = f"{mode}_dialogues.jsonl", []
        try:
            async with aiofiles.open(fn, "r", encoding="utf-8") as f:
                async for l in f:
                    if not l.strip():
                        continue
                    try:
                        items.append(json.loads(l))
                    except Exception as e:
                        logging.warning(f"Некорректная строка в {fn}: {l.strip()[:80]}... ({e})")
        except FileNotFoundError: pass
        for it in items:
            if it.get("question") == q:
                if a in [v for k,v in it.items() if k.startswith("answer")]: break
                k=1
                while f"answer{k}" in it: k+=1
                it[f"answer{k}"]=a; break
        else: items.append({"question": q, "answer1": a})
        async with aiofiles.open(fn, "w", encoding="utf-8") as f:
            for it in items: await f.write(json.dumps(it, ensure_ascii=False)+"\n")
    except Exception as e: logging.error(f"Ошибка при сохранении диалога: {e}")

async def load_prompts():
    try:
        async with aiofiles.open("prompts.txt", "r", encoding="utf-8") as f:
            content = await f.read()
            for line in content.splitlines():
                if "=" in line:
                    k, v = line.split("=", 1)
                    globals()[k.strip()] = v.strip()
    except FileNotFoundError:
        logging.warning("⚠ prompts.txt не найден, используются дефолтные промпты")
    except Exception as e:
        logging.error(f"Ошибка при загрузке prompts.txt: {e}")

def get_user_mode(user_id: int) -> str:
    return user_modes.get(user_id, "kind")

def set_user_mode(user_id: int, mode: str):
    user_modes[user_id] = mode

def get_prompt_by_mode(mode: str) -> str:
    return LIGHT_PROMPT if mode == "light" else BASED_PROMPT

async def transcribe(d: bytes) -> str | None:
    def _sync(audio_data):
        try:
            if len(audio_data) > 1024*1024:
                raise ValueError("Файл слишком большой")
            with sf.SoundFile(io.BytesIO(audio_data)) as f:
                if f.frames/f.samplerate > 60:
                    raise ValueError("Аудио слишком длинное")
                w = io.BytesIO()
                sf.write(w, f.read(dtype="int16"), f.samplerate, format="WAV")
                w.seek(0)
            with sr.AudioFile(w) as s:
                return sr.Recognizer().recognize_google(sr.Recognizer().record(s), language="ru-RU")
        except Exception as e:
            logging.error(f"Ошибка распознавания речи: {e}")
            return None
    return await asyncio.to_thread(_sync, d)

async def check_sub(bot: Bot, uid: int) -> bool:
    now = time.time()
    if uid in subscription_cache:
        cached, ts = subscription_cache[uid]
        if cached and now - ts < 300:
            return cached
    for _, cid, _ in CHANNELS:
        try:
            m = await bot.get_chat_member(cid, uid)
            if m.status not in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
                subscription_cache.pop(uid, None)
                return False
        except Exception as e:
            logging.error(f"Ошибка при проверке подписки uid={uid}, cid={cid}: {e}")
            subscription_cache.pop(uid, None)
            return False
    subscription_cache[uid] = (True, now)
    return True

def subscription_required(h):
    @wraps(h)
    async def wrapper(msg: Message):
        if not await check_sub(msg.bot, msg.from_user.id):
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=c[0], url=c[2])] for c in CHANNELS
            ] + [[InlineKeyboardButton(text="Проверить", callback_data="check_sub")]])
            sent = await msg.answer(NOT_SUB, reply_markup=kb)
            user_subscription_msgs.setdefault(msg.from_user.id, []).append((msg.message_id, sent.message_id))
            return
        return await h(msg)
    return wrapper

def clear_subscription_cache(uid:int=None):
    if uid:subscription_cache.pop(uid,None)
    else:subscription_cache.clear()

async def delete_subscription_msgs(bot:Bot,user_id:int,chat_id:int):
    for um,bm in user_subscription_msgs.get(user_id,[]):
        for mid in(um,bm):
            try:await bot.delete_message(chat_id,mid)
            except Exception as e:logging.error(f"Ошибка при удалении сообщения {mid}: {e}")
    user_subscription_msgs.pop(user_id,None)

async def check_cooldown(user_id: int, ctype: str) -> tuple[bool, int]:
    if user_id in ADMIN_IDS:
        return True, 0
    now = time.time()
    cooldowns = user_text_cooldowns if ctype == "text" else user_image_cooldowns
    timeout = 10 if ctype == "text" else 600
    if user_id in cooldowns:
        passed = now - cooldowns[user_id]
        if passed < timeout:
            return False, int(timeout - passed)
    cooldowns[user_id] = now
    return True, 0

def format_cooldown_time(seconds):
    h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
    parts = []
    if h: parts.append(f"{h}ч")
    if m: parts.append(f"{m}м")
    if s or not parts: parts.append(f"{s}с")
    return " ".join(parts)

async def add_reaction(msg: Message):
    if random.random() < 0.1:
        try:
            await msg.react([ReactionTypeEmoji(emoji=random.choice(REACTIONS))])
        except Exception as e:
            logging.error(f"Ошибка реакции: {e}")

async def load_file_stickers(path: str = "stickers.txt"):
    """Асинхронно загружает стикеры из файла один раз при старте"""
    global file_sticker_ids
    try:
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            lines = await f.readlines()
            file_sticker_ids = [line.strip() for line in lines if line.strip()]
        logging.info(f"Загружено {len(file_sticker_ids)} стикеров из файла")
    except FileNotFoundError:
        logging.warning("⚠ Файл stickers.txt не найден, список пуст")
        file_sticker_ids = []
    except Exception as e:
        logging.error(f"Ошибка при загрузке stickers.txt: {e}")
        file_sticker_ids = []

async def get_random_sticker() -> str:
    if random.random() < 0.1:
        return random.choice(sticker_ids)
    return random.choice(file_sticker_ids)

async def generate_image_from_query(q: str) -> BufferedInputFile:
    p = (f"{translate(q,'en').upper()}, HYPERREALISM, IN THE FOREGROUND")
    url = f"https://image.pollinations.ai/prompt/{p.replace(' ','%20')}?seed={random.randint(1,1_000_000)}&width=720&height=720&nofeed=true&nologo=true"
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"Ошибка при генерации изображения {resp.status}")
            data = await resp.read()
            return BufferedInputFile(data, filename="image.png")

async def get_random_joke(file_path='jokes.txt'):
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
            jokes = await file.readlines()
        return random.choice(jokes).strip()
    except Exception as e:
        return f"Ошибка: {e}"

async def build_alcoholic_model(paths=FILES):
    global alcoholic_tr
    tok_re = re.compile(r"\w+|[^\w\s]", re.U)
    pun = {".", "!", "?", "…"}
    ans = []
    async def read(p):
        try:
            async with aiofiles.open(p, "r", encoding="utf-8") as f:
                async for l in f:
                    try:
                        o = orjson.loads(l)
                    except:
                        continue
                    for k, v in o.items():
                        if k.lower().startswith("answer") and v:
                            t = str(v).strip()
                            ans.append(t + (t[-1] if t[-1] in pun else "."))
        except FileNotFoundError:
            pass
    await asyncio.gather(*[read(p) for p in paths])
    t = tok_re.findall(" ".join(ans))
    tr = defaultdict(Counter)
    for i in range(len(t) - 1):
        tr[(t[i],)][t[i + 1]] += 1
    alcoholic_tr = tr
    logging.info(f"Alcoholic model built with {len(alcoholic_tr)} states")


def generate_alcoholic_text() -> str:
    if not alcoholic_tr:
        return "⚠ Нет данных для генерации"
    pun = {".", "!", "?", "…"}
    s = random.choice(list(alcoholic_tr.keys()))
    out = list(s)
    while len(" ".join(out)) < 100:
        c = alcoholic_tr.get((out[-1],))
        if not c:
            break
        out.append(random.choices(list(c), weights=c.values())[0])
        if len(" ".join(out)) >= 50 and out[-1] in pun:
            break
    words = out[:]
    if len(words) > 2:
        idx = random.randint(1, len(words) - 1)
        emoji = random.choice(REACTIONS)
        words.insert(idx, emoji)
    return " ".join(words)[:100]

async def pbot_kind(name: str, question: str | None = None) -> str:
    import random, aiohttp, asyncio, uuid, pytz, logging
    from datetime import datetime
    try:
        def r(v, n): return v >> n if v >= 0 else (v + 0x100000000) >> n
        t = int((datetime.now(pytz.timezone("Europe/Moscow")) - datetime(1970,1,1,tzinfo=pytz.utc)).total_seconds()*1000)
        tbl = [(lambda c:[(c:=(3988292384^r(c,1))if(c&1)else r(c,1))for _ in range(8)][-1])(i) for i in range(256)]
        def crc(val):
            cs = 0 ^ -1
            for ch in val: cs = r(cs,8)^tbl[(cs^ord(ch))&255]
            return r(cs ^ -1,0)
        def sign(ts): return crc(f"public-api{ts}qVxRWnespIsJg7DxFbF6N9FiQR5cjnHyygru3JcToH4dPdiNH5SXOYIc00qMXPKJ")
        p = {"request":question or "","request_1":"","answer_1":"","request_2":"","answer_2":"","request_3":"","bot_name":"pBot","user_name":name,"dialog_lang":"ru","dialog_id":str(uuid.uuid4()),"dialog_greeting":"False","a":"public-api","b":crc(f"{t}b"),"c":sign(t),"d":crc(f"{t}d"),"e":random.random(),"t":t,"x":random.random()*10}
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as s:
            if question is None:
                async with s.get("http://p-bot.ru/api/getPatternsCount",cookies={"dialog_id":p["dialog_id"],"dialog_sentment":"0","last_visit":f"{t}::{t}"}) as r:
                    return await r.text()
            async with s.post("http://p-bot.ru/api/getAnswer",data=p) as r:
                js = await r.json(content_type=None)
                answer = js.get("answer", "").strip()
                if answer:
                    asyncio.create_task(save_dialogue("kind", question, answer))
                    return answer
                return await generate_text_response_step_2("kind", question)
    except Exception as e:
        logging.error(f"pbot_kind error: {e}")
        return await generate_text_response_step_2("kind", question or "")

async def generate_text_response_step_1(prompt: str, target_id: int) -> str:
    mode = get_user_mode(target_id)
    payload = {
        "model": "llamascout",
        "messages": [
            {"role": "system", "content": get_prompt_by_mode(mode)},
            {"role": "user", "content": prompt}
        ],
        "seed": random.randint(1, 1000000)
    }
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as s:
            async with s.post(
                "https://text.pollinations.ai/openai",
                headers={"Content-Type": "application/json"},
                json=payload
            ) as r:
                js = await r.json()
                a = js.get("choices", [{}])[0].get("message", {}).get("content")
                if a:
                    asyncio.create_task(save_dialogue(mode, prompt, a))
                    return a
                return await generate_text_response_step_2(mode, prompt)
    except Exception:
        return await generate_text_response_step_2(mode, prompt)

async def generate_text_response_step_2(mode: str, query: str) -> str:
    import math, random, json, aiofiles

    def tok(t):
        for c in ".,!?;:\"()[]{}<>":
            t = t.replace(c, " ")
        return t.lower().split()

    if mode not in vectors_cache:
        path = f"{mode}_dialogues.jsonl"
        data, qs = [], []
        try:
            async with aiofiles.open(path, encoding="utf-8") as f:
                async for l in f:
                    if not l.strip():
                        continue
                    try:
                        e = json.loads(l)
                        a = [v for k, v in e.items() if k.startswith("answer")]
                        if a:
                            data.append({"question": e["question"], "answers": a})
                            qs.append(e["question"])
                    except Exception as e:
                        logging.warning(f"Некорректная строка в {path}: {l.strip()[:80]}... ({e})")
        except FileNotFoundError:
            vectors_cache[mode] = {"data": [], "qv": [], "qn": [], "idf": {}}
            return "⚠ Нет сохранённых ответов"

        N = len(qs)
        if not N:
            vectors_cache[mode] = {"data": [], "qv": [], "qn": [], "idf": {}}
            return "⚠ Нет сохранённых ответов"

        dc = {}
        qt = [tok(q) for q in qs]
        [[dc.update({x: dc.get(x, 0) + 1}) for x in set(t)] for t in qt]
        idf = {t: math.log((N + 1) / (df + 1)) + 1 for t, df in dc.items()}
        qv = [{t: tks.count(t) * idf[t] for t in set(tks)} for tks in qt]
        qn = [math.sqrt(sum(w * w for w in v.values())) for v in qv]
        vectors_cache[mode] = {"data": data, "qv": qv, "qn": qn, "idf": idf}

    c = vectors_cache[mode]
    data, qv, qn, idf = c["data"], c["qv"], c["qn"], c["idf"]
    if not data:
        return "⚠ Нет сохранённых ответов"

    tf = {}
    [tf.update({x: tf.get(x, 0) + 1}) for x in tok(query)]
    v = {t: c * idf.get(t, math.log((len(data) + 1) / 1) + 1) for t, c in tf.items()}
    n = math.sqrt(sum(w * w for w in v.values()))

    def cos(v1, n1, v2, n2):
        return 0 if not n1 or not n2 else sum(w * v2.get(t, 0) for t, w in v1.items()) / (n1 * n2)

    sims = [(cos(v, n, qvv, qnn), j) for j, (qvv, qnn) in enumerate(zip(qv, qn))]
    cand = [j for s, j in sims if s > 0.8]
    i = random.choice(cand) if cand else max(sims)[1]
    return random.choice(data[i]["answers"]) if data[i]["answers"] else "⚠ Нет ответа"

async def get_voice_message_bytes(text: str) -> BufferedInputFile:
    url = f"https://api.streamelements.com/kappa/v2/speech?voice=Maxim&text={text}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.read()
                return BufferedInputFile(BytesIO(data).getvalue(), filename="voice.mp3")
            elif response.status == 401:
                raise RuntimeError("Текст слишком большой для озвучивания.")
    try:
        tts = gTTS(text=text, lang="ru")
        buffer = BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        return BufferedInputFile(buffer.getvalue(), filename="voice.mp3")
    except Exception as e:
        raise RuntimeError(f"Ошибка при озвучке текста через gTTS: {e}")

# --------------------- ПОИСК (исходные функции — без изменений) ---------------------

B={"aol.com","youtube.com","wiktionary.org","reverso.net","tenor.com"}

class A:
    async def __aenter__(s):
        s.u="https://search.aol.com/aol/search"
        s.h={'User-Agent':'Mozilla/5.0','Accept':'*/*','Accept-Language':'ru','Connection':'keep-alive'}
        s.s=aiohttp.ClientSession(headers=s.h)
        return s

    async def __aexit__(s,*_):
        await s.s.close()

    async def f(s,q):
        try:
            return await(await s.s.get(s.u,params={'q':q,'ei':'UTF-8'},timeout=10)).text()
        except Exception as e:
            logging.error(f"AOL search error: {e}")
            return

    def p(s,h):
        p=HTMLParser(h)
        c=p.css_first('#results') or p.css_first('.searchCenterMiddle')
        return [r for r in s.x(c) if all(b not in urllib.parse.urlparse(r['url']).netloc.lower() for b in B)] if c else []

    def x(s,c):
        r=[]
        results=[]
        for l in c.css('ol.mb-15.reg.searchCenterMiddle li')[1:]+c.css('ul.compArticleList li'):
            a=l.css_first('.compTitle h3.title a') or l.css_first('.thmb') or l.css_first('a')
            u=a.attributes.get('href','') if a else ''
            t=a.text(strip=True) if a else ''
            if not t:
                for x in l.css('a'):
                    if x!=a and x.text(strip=True):
                        t=x.text(strip=True);u=x.attributes.get('href','');break
            i=l.css_first('img')
            th=i.attributes.get('src') if i and i.attributes.get('src','').startswith('http') else None
            d=s.d(l.css_first('.compText'))

            if a:
                result={'url':s.r(u),'title':t,'description':d,'thumbnail':th}
                results.append(result)

                # Проверка: только кириллица в title и description
                if (re.fullmatch(r"[А-Яа-я0-9\s.,!?():;-]+", t) and 
                    re.fullmatch(r"[А-Яа-я0-9\s.,!?():;-]+", d)):
                    r.append(result)

        # Если нет результатов только на кириллице → взять первый без фильтра
        return r if r else (results[:1] if results else [])

    def r(s,u):
        if not u or 'click' not in u: return u
        try:
            p=urllib.parse.urlparse(u)
            qp=urllib.parse.parse_qs(p.query)
            ru=qp.get('RU',[None])[0]
            if ru: return urllib.parse.unquote(ru)
            for x in p.path.split('/'):
                if x.startswith('RU='): return urllib.parse.unquote(x[3:])
        except:
            return u
        return u

    def d(s,e):
        return re.sub(r'\s+',' ',
                      re.sub(r'[^\w\s\-.,!?():;/]',' ',
                      e.text(separator='\n',strip=True).replace('\n',' ')) if e else '').strip()

class Wiki:
 def __init__(s):s.h={'User-Agent':'Mozilla/5.0'}
 async def f(s,q):
  try:
   async with aiohttp.ClientSession()as sess:
    async with sess.get(f"https://ru.wikipedia.org/w/index.php?search={q.replace(' ','%20')}&limit=1",headers=s.h)as r:
     p=HTMLParser(await r.text());u=("https://ru.wikipedia.org"+p.css_first('div.mw-search-result-heading a').attributes['href'])if p.css('div.mw-search-result-heading')else(str(r.url)if'/wiki/'in str(r.url)else None)
    if not u:return
    async with sess.get(u,headers=s.h)as r:
     p=HTMLParser(await r.text());imgs=p.css('img');is_disambig=any('Disambig.svg' in(i.attributes.get('src','')or'')for i in imgs)
     if is_disambig:
      m=[]
      for li in p.css('div.mw-parser-output ul li')[:5]:
       t=li.text();t=re.sub(r'\.mw-parser-output.?}|@media.?}|body\.ns-0.?}','',t)
       for x in['Примечания','Если вы попали','См. также страницы с','Проект «Страницы']:t=t.split(x)[0]
       t=re.sub(r'\[.??]|\s+',' ',t).strip()
       if len(t)>10 and ' — 'in t:m+=[t]
      d='\n'.join(m)or"Значения не найдены"
     else:
      d=' '.join(x.text()for x in p.css('div.mw-parser-output p')[:3]);d=re.sub(r'\[.*?]|\s+',' ',d).strip();d=d[:500]
      for punc in'.!?':
       if punc in d:d=d.rsplit(punc,1)[0]+punc;break
     for i in imgs:
      s_=i.attributes.get('src','');w,h=int(i.attributes.get('width',0)),int(i.attributes.get('height',0))
      if any(x in s_.lower()for x in['.jpg','.png','.jpeg','.webp'])and all(y not in s_ for y in['Disambig','Commons','Icon','Symbol'])and w>=100 and h>=100:img='https:'+s_ if s_.startswith('//')else s_;break
     return{'url':u,'title':q,'description':d,'thumbnail':img if 'img' in locals()else None}
  except:return

class Tenor:
    def __init__(s): s.s=None
    async def __aenter__(s): s.s=aiohttp.ClientSession(); return s
    async def __aexit__(s,*_): await s.s.close()
    async def g(s,q):  # теперь q = запрос пользователя
        try:
            return (await (await s.s.get(
                f'https://g.tenor.com/v1/search?key=LIVDSRZULELA&locale=ru_RU&limit=1&media_filter=minimal&contentfilter=off&q={q}'
            )).json())['results'][0]['media'][0]['gif']['url']
        except:
            return

# --------------------- SMART РЕЖИМ ---------------------

async def _smart_async(query: str):
    async with A() as a:
        w = Wiki()
        h = await a.f(query)
        r = a.p(h) if h else []
        fb = 0
        if not r:
            r = [await w.f(query)]
            fb = 1
        if not r or not r[0]:
            return None
        f = r[0]
    # Для wiki берём миниатюру как фото; для AOL пытаемся взять gif
    if fb:  # wiki
        media_type = "photo" if f.get("thumbnail") else None
        media_url = f.get("thumbnail")
    else:   # aol
        async with Tenor() as t:
            media_url = await t.g(query if fb else f["title"])
        media_type = "animation" if media_url else None
    caption = (f"<b>{f['title']}</b>\n" if not fb else f"{f['title']}\n") + (f"{f['description']}\n" if f.get('description') else "")
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="читать подробнее", url=f['url'])]])
    return {"media_type": media_type, "media_url": media_url, "caption": caption, "kb": kb}

async def generate_smart_response(query: str):
    # выносим блокирующий парсинг в отдельный поток
    return await asyncio.to_thread(lambda: asyncio.run(_smart_async(query)))

# --------------------- ОБРАБОТЧИКИ ---------------------

@dp.callback_query(F.data == "check_sub")
async def _(cq: CallbackQuery):
    clear_subscription_cache(cq.from_user.id)
    if await check_sub(cq.bot, cq.from_user.id):
        await delete_subscription_msgs(cq.bot, cq.from_user.id, cq.message.chat.id)
        await cq.answer()
        await cmd_start(cq.message)
    else:
        await cq.answer("Все ещё не подписаны.", show_alert=True)


@dp.message(Command("start"))
async def cmd_start(m: Message):
    uid = str(m.chat.id)
    try:
        async with aiofiles.open("user_ids.csv", "r", encoding="utf-8") as f:
            if uid not in (await f.read()).split():
                async with aiofiles.open("user_ids.csv", "a", encoding="utf-8") as w: await w.write(uid+"\n")
    except FileNotFoundError:
        async with aiofiles.open("user_ids.csv", "w", encoding="utf-8") as f: await f.write(uid+"\n")
    if m.chat.type==ChatType.PRIVATE and not await check_sub(m.bot,m.from_user.id):
        return await subscription_required(lambda _:None)(m)
    photo = FSInputFile(random.choice(["start1.png", "start2.png", "start3.png"]))
    caption=f"Привет, {m.from_user.full_name}!\nЭтот бот предназначен для ответов таким как ты.\nЧтобы ты смог выяснить, какой размер будет у твоей письки через 5 лет\nСписок всех команд - /help"
    if m.chat.type == ChatType.PRIVATE:
        menu = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=t)] for t in [
                    "👋Знакомство с ХахБотом👋",
                    "👥Добавить в группу👥",
                    "💵Поддержать💵",
                    "✨ОСОБЫЕ БЛАГОДАРНОСТИ✨"
                ]
            ],
            resize_keyboard=True
        )
        await safe_send_photo_no_reply(m,photo,caption=caption,reply_markup=menu)
    else: await safe_send_photo_no_reply(m,photo,caption=caption)

@dp.message(F.text == "👋Знакомство с ХахБотом👋")
@subscription_required
async def intro_handler(m: Message):
    photo = FSInputFile(random.choice(["start1.png", "start2.png", "start3.png"]))
    caption = (
        "📌 *Режимы поведения* _\n_\n"
        "/light — *🌟 фембойчик*\n"
        "/based — *😈 злой*\n"
        "/smart — *🧠 умный*\n"
        "/kind — *🌟 добрый*\n"
        "/alcoholic — *🍺 бухой*\n\n"
        "⚡ *Функции бота* _\n_\n"
        "/joke или `Хахбот расскажи шутку` — *😂 случайная шутка*\n"
        "/sticker — *🎲 случайный стикер*\n"
        "`Хахбот нарисуй <тема>` — *🎨 генерация картинки*\n"
        "`Хахбот скажи <текст>` — *🔊 озвучка текста*\n"
        "✍️ Просто напиши сообщение — *🤖 ответ в выбранном режиме*\n"
        "🎤 Голосовое сообщение — *🎧 обработка и ответ*"
    )
    await safe_send_photo(m, photo, caption=caption, parse_mode="Markdown")

@dp.message(F.text == "👥Добавить в группу👥")
@subscription_required
async def add_group_handler(m: Message):
    photo = FSInputFile(random.choice(["start1.png", "start2.png", "start3.png"]))
    caption = 'Добавь ХахБота в качестве администратора в свою группу.\nЧтобы мне что-то написать добавьте текст "ХахБот" в свой запрос.\nНапример:\nХахБот, отсоси'
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Добавить в группу",
                url="http://t.me/hahrobot?startgroup=HahBot&admin=change_info+restrict_members+delete_messages+pin_messages+invite_users"
            )]
        ]
    )
    await safe_send_photo(m, photo, caption=caption, reply_markup=keyboard)

@dp.message(F.text == "💵Поддержать💵")
async def support_handler(m: Message):
    if m.from_user.id not in ADMIN_IDS:
        return await safe_send_message(m, "Прости, донат пока недоступен(")
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="15⭐", callback_data="donate_15"),
        InlineKeyboardButton(text="50⭐", callback_data="donate_50"),
        InlineKeyboardButton(text="100⭐", callback_data="donate_100"),
    ]])
    await m.answer("Выбери сумму доната:", reply_markup=kb)

@dp.callback_query(F.data.startswith("donate_"))
async def donate_invoice(callback: CallbackQuery):
    amount = int(callback.data.split("_")[1])
    await callback.bot.send_invoice(
        chat_id=callback.message.chat.id,
        title=f"Спасибо за поддержку на {amount}⭐!",
        description="Привет! Мой бот является полностью бесплатным и не имеет каких-либо ограничений, я содержу его полностью за свои деньги. Я был бы очень благодарен за любую сумму!",
        payload=f"donate_{amount}stars",
        provider_token="", currency="XTR",
        prices=[LabeledPrice(label=f"Донат {amount}⭐", amount=amount)],
        start_parameter="donate",
        photo_url="https://i.pinimg.com/736x/28/9a/71/289a71dba02a4d155e2cdd05ed9b83ee.jpg",
        photo_width=512, photo_height=512,
    )
    await callback.message.delete()
    await callback.answer()

@dp.message(F.successful_payment)
async def payment_success(m: Message):
    await safe_send_message(m, "💖 Спасибо за поддержку! Твоя помощь очень важна!")

@dp.message(Command("help"))
async def cmd_help(m: Message):
    await intro_handler(m)

@dp.message(Command("invite_group"))
async def cmd_invite_group(m: Message):
    await add_group_handler(m)

@dp.message(Command("donate"))
async def cmd_donate(m: Message):
    await support_handler(m)

@dp.message(F.text == "✨ОСОБЫЕ БЛАГОДАРНОСТИ✨")
@subscription_required
async def credits_handler(m: Message):
    photo = FSInputFile("thanks.jpg")
    caption = "✨Особая благодарность всем, кто помогал в создании и развитии этого бота✨\nПока что в этом списке один человек - @valtorye, первый и единственный кто задонатил на бота за 3 года его существования лол"
    await safe_send_photo(m, photo, caption=caption)


@dp.message(Command("light"))
async def _(m: Message):
    if m.chat.type == ChatType.PRIVATE:
        if not await check_sub(m.bot, m.from_user.id):
            return await subscription_required(lambda _: None)(m)
        set_user_mode(m.from_user.id, "light")
        return await safe_send_message(m, "🌟 Режим переключен на фембойчика!")
    admins = await m.bot.get_chat_administrators(m.chat.id)
    admin_ids = [admin.user.id for admin in admins if admin.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)]

    if m.from_user.id not in admin_ids:
        return await safe_send_message(m, "❌ Только администратор может менять режим")

    set_user_mode(m.chat.id, "light")
    await safe_send_message(m, "🌟 Режим переключен на фембойчика!")


@dp.message(Command("based"))
async def _(m: Message):
    if m.chat.type == ChatType.PRIVATE:
        if not await check_sub(m.bot, m.from_user.id):
            return await subscription_required(lambda _: None)(m)
        set_user_mode(m.from_user.id, "based")
        return await safe_send_message(m, "😈 Режим переключен на злой!")
    admins = await m.bot.get_chat_administrators(m.chat.id)
    admin_ids = [admin.user.id for admin in admins if admin.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)]

    if m.from_user.id not in admin_ids:
        return await safe_send_message(m, "❌ Только администратор может менять режим")

    set_user_mode(m.chat.id, "based")
    await safe_send_message(m, "😈 Режим переключен на злой!")


@dp.message(Command("smart"))
async def _(m: Message):
    if m.chat.type == ChatType.PRIVATE:
        if not await check_sub(m.bot, m.from_user.id):
            return await subscription_required(lambda _: None)(m)
        set_user_mode(m.from_user.id, "smart")
        return await safe_send_message(m, "🧠 Режим переключен на умный!")
    admins = await m.bot.get_chat_administrators(m.chat.id)
    admin_ids = [admin.user.id for admin in admins if admin.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)]

    if m.from_user.id not in admin_ids:
        return await safe_send_message(m, "❌ Только администратор может менять режим")

    set_user_mode(m.chat.id, "smart")
    await safe_send_message(m, "🧠 Режим переключен на умный!")


@dp.message(Command("kind"))
async def _(m: Message):
    if m.chat.type == ChatType.PRIVATE:
        if not await check_sub(m.bot, m.from_user.id):
            return await subscription_required(lambda _: None)(m)
        set_user_mode(m.from_user.id, "kind")
        return await safe_send_message(m, "🌟 Режим переключен на добрый!")
    admins = await m.bot.get_chat_administrators(m.chat.id)
    admin_ids = [admin.user.id for admin in admins if admin.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)]

    if m.from_user.id not in admin_ids:
        return await safe_send_message(m, "❌ Только администратор может менять режим")

    set_user_mode(m.chat.id, "kind")
    await safe_send_message(m, "🌟 Режим переключен на добрый!")


@dp.message(Command("alcoholic"))
async def _(m: Message):
    if m.chat.type == ChatType.PRIVATE:
        if not await check_sub(m.bot, m.from_user.id):
            return await subscription_required(lambda _: None)(m)
        set_user_mode(m.from_user.id, "alcoholic")
        return await safe_send_message(m, "🍺 Режим переключен на бухого!")
    admins = await m.bot.get_chat_administrators(m.chat.id)
    admin_ids = [admin.user.id for admin in admins if admin.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)]

    if m.from_user.id not in admin_ids:
        return await safe_send_message(m, "❌ Только администратор может менять режим")

    set_user_mode(m.chat.id, "alcoholic")
    await safe_send_message(m, "🍺 Режим переключен на бухого!")


@dp.message(Command("joke"))
@subscription_required
async def cmd_joke(message: Message):
    joke = await get_random_joke()
    await safe_send_message(message, joke)


@dp.message(Command("sticker"))
@subscription_required
async def send_random_sticker(m: Message):
    while True:
        try:
            st = await get_random_sticker()
            await safe_send_sticker(m, st)
            return
        except TelegramBadRequest:
            continue
        except Exception as e:
            logging.error(f"Ошибка при отправке стикера: {e}")
            return


@dp.message(Command("update"))
async def _(m: Message):
    if m.from_user.id not in ADMIN_IDS:
        return await safe_send_message(m, "⛔️ Доступ запрещён")
    modes = ("based", "light", "kind")
    [vectors_cache.pop(md, None) for md in modes]
    await asyncio.gather(*(generate_text_response_step_2(md, "") for md in modes))
    await build_alcoholic_model()
    await safe_send_message(m, "✅ Векторные связи пересобраны: " + ", ".join(modes) + ", alcoholic")

@dp.message()
async def handler(m: Message):
    await add_reaction(m)

    # ===== 1. Личные чаты =====
    if m.chat.type == ChatType.PRIVATE:
        if not await check_sub(m.bot, m.from_user.id):
            return await subscription_required(lambda _: None)(m)

        if m.text and not m.text.startswith("/"):
            if m.text.lower().startswith("хахбот нарисуй"):
                can, wait = await check_cooldown(m.from_user.id, "image")
                if not can:
                    return await safe_send_message(m, f"Подождите {format_cooldown_time(wait)}")
                q = m.text[14:].strip()
                if not q:
                    return await safe_send_message(m, "Что я блядь должен рисовать если нихуя нет?")
                asyncio.create_task(generate_and_send_image(m, q))

            elif m.text.lower().startswith("хахбот расскажи шутку"):
                joke = await get_random_joke()
                await safe_send_message(m, joke)

            elif m.text.lower().startswith("хахбот скажи"):
                can, wait = await check_cooldown(m.from_user.id, "text")
                if not can:
                    return await safe_send_message(m, f"Подождите {format_cooldown_time(wait)}")
                text_to_speak = m.text[13:].strip()
                if not text_to_speak:
                    return await safe_send_message(m, "Что я блядь должен озвучивать если нихуя нет?")
                try:
                    voice_file = await get_voice_message_bytes(text_to_speak)
                    await safe_send_voice(m, voice_file)
                except Exception as e:
                    logging.error(f"Ошибка при генерации голосового сообщения: {e}")
                    await safe_send_message(m, "Не удалось озвучить текст.")
            else:
                can, wait = await check_cooldown(m.from_user.id, "text")
                if not can:
                    return await safe_send_message(m, f"Подождите {format_cooldown_time(wait)}")
                if random.random() < 0.1:
                    while True:
                        try:
                            st = await get_random_sticker()
                            await safe_send_sticker(m, st)
                            return
                        except TelegramBadRequest:
                            continue
                        except Exception as e:
                            logging.error(f"Ошибка при отправке стикера: {e}")
                            return
                mode = get_user_mode(m.from_user.id)
                if mode == "smart":
                    return asyncio.create_task(generate_and_send_smart(m))
                elif mode == "kind":
                    return asyncio.create_task(generate_and_send_kind(m))
                elif mode == "alcoholic":
                    return asyncio.create_task(generate_and_send_alcoholic(m))
                else:
                    return asyncio.create_task(generate_and_send_text(m))

        elif m.voice:
            asyncio.create_task(process_voice(m))

        else:
            if random.random() < 0.6:
                return asyncio.create_task(generate_and_send_alcoholic(m))
            else:
                try:
                    st = await get_random_sticker()
                    await safe_send_sticker(m, st)
                    return
                except TelegramBadRequest:
                    return asyncio.create_task(generate_and_send_alcoholic(m))
                except Exception as e:
                    logging.error(f"Ошибка при отправке стикера: {e}")
                    return asyncio.create_task(generate_and_send_alcoholic(m))

    # ===== 2. Группы/супергруппы/каналы =====
    else:
        if m.text and not m.text.startswith("/"):
            if m.text.lower().startswith("хахбот нарисуй"):
                can, wait = await check_cooldown(m.from_user.id, "image")
                if not can:
                    return await safe_send_message(m, f"Подождите {format_cooldown_time(wait)}")
                q = m.text[14:].strip()
                if not q:
                    return await safe_send_message(m, "Что я блядь должен рисовать если нихуя нет?")
                asyncio.create_task(generate_and_send_image(m, q))

            elif m.text.lower().startswith("хахбот расскажи шутку"):
                joke = await get_random_joke()
                await safe_send_message(m, joke)

            elif m.text.lower().startswith("хахбот скажи"):
                can, wait = await check_cooldown(m.from_user.id, "text")
                if not can:
                    return await safe_send_message(m, f"Подождите {format_cooldown_time(wait)}")
                text_to_speak = m.text[13:].strip()
                if not text_to_speak:
                    return await safe_send_message(m, "Что я блядь должен озвучивать если нихуя нет?")
                try:
                    voice_file = await get_voice_message_bytes(text_to_speak)
                    await safe_send_voice(m, voice_file)
                except Exception as e:
                    logging.error(f"Ошибка при генерации голосового сообщения: {e}")
                    await safe_send_message(m, "Не удалось озвучить текст.")
            else:
                # нижняя часть: вызов бота или случайный ответ
                is_reply_to_bot = (
                    m.reply_to_message and m.reply_to_message.from_user and m.reply_to_message.from_user.id == m.bot.id
                )
                if is_reply_to_bot or m.text.lower().startswith("хахбот"):
                    can, wait = await check_cooldown(m.from_user.id, "text")
                    if not can:
                        return await safe_send_message(m, f"Подождите {format_cooldown_time(wait)}")
                    if random.random() < 0.1:
                        while True:
                            try:
                                st = await get_random_sticker()
                                await safe_send_sticker(m, st)
                                return
                            except TelegramBadRequest:
                                continue
                            except Exception as e:
                                logging.error(f"Ошибка при отправке стикера: {e}")
                                return
                    mode = get_user_mode(m.chat.id)
                    if mode == "smart":
                        return asyncio.create_task(generate_and_send_smart(m))
                    elif mode == "kind":
                        return asyncio.create_task(generate_and_send_kind(m))
                    elif mode == "alcoholic":
                        return asyncio.create_task(generate_and_send_alcoholic(m))
                    else:
                        return asyncio.create_task(generate_and_send_text(m))
                else:
                    # случайный ответ без cooldown
                    if random.random() < 0.1:
                        if random.random() < 0.1:
                            try:
                                st = await get_random_sticker()
                                await safe_send_sticker(m, st)
                                return
                            except TelegramBadRequest:
                                return asyncio.create_task(generate_and_send_alcoholic(m))
                            except Exception as e:
                                logging.error(f"Ошибка при отправке стикера: {e}")
                                return asyncio.create_task(generate_and_send_alcoholic(m))
                        else:
                            mode = get_user_mode(m.chat.id)
                            if mode == "smart":
                                return asyncio.create_task(generate_and_send_smart(m))
                            elif mode == "kind":
                                return asyncio.create_task(generate_and_send_kind(m))
                            elif mode == "alcoholic":
                                return asyncio.create_task(generate_and_send_alcoholic(m))
                            else:
                                return asyncio.create_task(generate_and_send_text(m))

        elif m.voice:
            asyncio.create_task(process_voice(m))

        else:
            if random.random() < 0.1:
                try:
                    st = await get_random_sticker()
                    await safe_send_sticker(m, st)
                    return
                except TelegramBadRequest:
                    return asyncio.create_task(generate_and_send_alcoholic(m))
                except Exception as e:
                    logging.error(f"Ошибка при отправке стикера: {e}")
                    return asyncio.create_task(generate_and_send_alcoholic(m))


async def generate_and_send_smart(m: Message):
    try:
        async with ChatActionSender.upload_video(bot=m.bot, chat_id=m.chat.id):
            res = await generate_smart_response(m.text)
            if not res:
                return await safe_send_message(m, "Ничего не найдено.")
            mt, mu = res["media_type"], res["media_url"]
            if mt == "animation" and mu:
                return await safe_send_animation(m, mu, caption=res["caption"], reply_markup=res["kb"], parse_mode="HTML")
            if mt == "photo" and mu:
                return await safe_send_photo(m, mu, caption=res["caption"], reply_markup=res["kb"], parse_mode="HTML")
            return await safe_send_message(m, res["caption"], reply_markup=res["kb"], parse_mode="HTML")
    except Exception as e:
        logging.error(f"Ошибка smart: {e}")
        await safe_send_message(m, "⚠ Ошибка генерации ответа")


async def generate_and_send_kind(m: Message):
    async with ChatActionSender.typing(bot=m.bot, chat_id=m.chat.id):
        name = m.from_user.full_name or m.from_user.username or str(m.from_user.id)
        answer = await pbot_kind(name=name, question=m.text)
        if not answer:
            await safe_send_message(m, "⚠ Ошибка генерации ответа")
            return

        if random.random() < 0.2:
            try:
                voice_file: BufferedInputFile = await get_voice_message_bytes(answer)
                await safe_send_voice(m, voice=voice_file)
                return
            except Exception as e:
                logging.error(f"Ошибка при генерации голосового: {e}")

        await safe_send_message(m, answer)


async def generate_and_send_alcoholic(m: Message):
    try:
        response = generate_alcoholic_text()
        if random.random() < 0.2:
            try:
                voice_file: BufferedInputFile = await get_voice_message_bytes(response)
                await safe_send_voice(m, voice=voice_file)
                return
            except Exception as e:
                logging.error(f"Ошибка при генерации голосового: {e}")

        await safe_send_message(m, response)
    except Exception as e:
        logging.error(f"Ошибка alcoholic: {e}")
        await safe_send_message(m, "⚠ Ошибка генерации ответа")


async def generate_and_send_image(m: Message, q: str):
    try:
        async with ChatActionSender.upload_photo(bot=m.bot, chat_id=m.chat.id):
            img = await generate_image_from_query(q)
            await safe_send_photo(m, img, caption="Вот ваше изображение")
    except Exception as e:
        logging.error(f"Ошибка генерации картинки: {e}")
        await safe_send_message(m, "Не удалось сгенерировать изображение 😢")


async def generate_and_send_text(m: Message):
    try:
        async with ChatActionSender.typing(bot=m.bot, chat_id=m.chat.id):
            # выбор идентификатора в зависимости от типа чата
            target_id = m.from_user.id if m.chat.type == ChatType.PRIVATE else m.chat.id

            response = await generate_text_response_step_1(m.text, target_id)

            if random.random() < 0.2:
                try:
                    voice_file: BufferedInputFile = await get_voice_message_bytes(response)
                    await safe_send_voice(m, voice=voice_file)
                    return
                except Exception as e:
                    logging.error(f"Ошибка при генерации голосового: {e}")

            await safe_send_message(m, response)
    except Exception as e:
        logging.error(f"Ошибка генерации текста: {e}")
        await safe_send_message(m, "⚠ Ошибка генерации ответа")


async def send_random_sticker(m: Message):
    while True:
        sticker_id = await get_random_sticker()
        try:
            await safe_send_sticker(m, sticker_id)
            break
        except Exception:
            continue


async def process_voice(m: Message):
    try:
        async with ChatActionSender.typing(bot=m.bot, chat_id=m.chat.id):
            buf = io.BytesIO()
            await m.bot.download(await m.bot.get_file(m.voice.file_id), destination=buf)
            text = await transcribe(buf.getvalue())
            await safe_send_message(m, text or "Не удалось распознать речь.")
    except Exception as e:
        logging.error(f"Ошибка голосового: {e}")
        await safe_send_message(m, "⚠ Ошибка при обработке голосового")

# --------------------- СТАРТ ---------------------

async def main():
    await load_prompts()
    await load_file_stickers()
    bot = Bot(token=BOT_TOKEN)
    for md in ("based", "light", "kind"):
        await generate_text_response_step_2(md, "")
    await build_alcoholic_model()
    global rate_limiter
    rate_limiter = RateLimiter()
    rate_limiter.start()
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        rate_limiter.stop()
        await bot.session.close()

if __name__ == "__main__":

    asyncio.run(main())


