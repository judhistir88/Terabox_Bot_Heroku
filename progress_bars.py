import random

progress_bars = [
    "█████-----",  # Example: Filled: █, Empty: -
    "✅✅✅🟩🟩🟩🟩🟩🟩🟩",  # Example: Filled: ✅, Empty: 🟩
    "★★★------",  # Example: Filled: ★, Empty: -
    "###......",  # Example: Filled: #, Empty: .
    "[=====-----]",  # Example: Filled: =, Empty: -
    "●●●○○○○○○○",  # Example: Filled: ●, Empty: ○
    "♥♥♥-------",  # Example: Filled: ♥, Empty: -
    "+++------",  # Example: Filled: +, Empty: -
    "■■■□□□□□□□",  # Example: Filled: ■, Empty: □
    "➤➤➤------",  # Example: Filled: ➤, Empty: -
    "▓▓▓▓▓     ",  # Example: Filled: ▓, Empty:  
    "🐟🐟🐟🌊🌊🌊🌊🌊🌊🌊",  # Example: Filled: 🐟, Empty: 🌊
    "🍕🍕🍕🧀🧀🧀🧀🧀🧀🧀",  # Example: Filled: 🍕, Empty: 🧀
    "👽👽👽🚀🚀🚀🚀🚀🚀🚀",  # Example: Filled: 👽, Empty: 🚀
    "🐱🐱🐱🐭🐭🐭🐭🐭🐭🐭",  # Example: Filled: 🐱, Empty: 🐭
    "❤️❤️❤️💔💔💔💔💔💔💔",  # Example: Filled: ❤️, Empty: 💔
    "☀️☀️☀️☁️☁️☁️☁️☁️☁️☁️",  # Example: Filled: ☀️, Empty: ☁️
    "🎵🎵🎵🎶🎶🎶🎶🎶🎶🎶",  # Example: Filled: 🎵, Empty: 🎶
    "📚📚📚📜📜📜📜📜📜📜",  # Example: Filled: 📚, Empty: 📜
    "⭐️⭐️⭐️🌙🌙🌙🌙🌙🌙🌙",  # Example: Filled: ⭐, Empty: 🌙
    "🌳🌳🌳🍂🍂🍂🍂🍂🍂🍂",  # Example: Filled: 🌳, Empty: 🍂
    "👻👻👻🎃🎃🎃🎃🎃🎃🎃",  # Example: Filled: 👻, Empty: 🎃
    "🎈🎈🎈🎉🎉🎉🎉🎉🎉🎉",  # Example: Filled: 🎈, Empty: 🎉
    "🐉🐉🐉🔥🔥🔥🔥🔥🔥🔥",  # Example: Filled: 🐉, Empty: 🔥
    "⚔️⚔️⚔️🛡️🛡️🛡️🛡️🛡️🛡️",  # Example: Filled: ⚔️, Empty: 🛡️
    "🚗🚗🚗🏁🏁🏁🏁🏁🏁🏁",  # Example: Filled: 🚗, Empty: 🏁
    "🍭🍭🍭🍬🍬🍬🍬🍬🍬🍬",  # Example: Filled: 🍭, Empty: 🍬
    "🚂🚂🚂🛤️🛤️🛤️🛤️🛤️🛤️",  # Example: Filled: 🚂, Empty: 🛤️
    "❄️❄️❄️⛄⛄⛄⛄⛄⛄⛄",  # Example: Filled: ❄️, Empty: ⛄
    "🏈🏈🏈🥅🥅🥅🥅🥅🥅🥅",  # Example: Filled: 🏈, Empty: 🥅
    "🍎🍎🍎📚📚📚📚📚📚📚",  # Example: Filled: 🍎, Empty: 📚
    "🍌🍌🍌🐒🐒🐒🐒🐒🐒🐒",  # Example: Filled: 🍌, Empty: 🐒
    "🐧🐧🐧❄️❄️❄️❄️❄️❄️❄️",  # Example: Filled: 🐧, Empty: ❄️
    "🐔🐔🐔🥚🥚🥚🥚🥚🥚🥚",  # Example: Filled: 🐔, Empty: 🥚
    "🚢🚢🚢⚓⚓⚓⚓⚓⚓⚓",  # Example: Filled: 🚢, Empty: ⚓
    "🍔🍔🍔🍟🍟🍟🍟🍟🍟🍟",  # Example: Filled: 🍔, Empty: 🍟
    "🐝🐝🐝🌸🌸🌸🌸🌸🌸🌸",  # Example: Filled: 🐝, Empty: 🌸
    "🦀🦀🦀🐚🐚🐚🐚🐚🐚🐚",  # Example: Filled: 🦀, Empty: 🐚
    "🦉🦉🦉🌳🌳🌳🌳🌳🌳🌳",  # Example: Filled: 🦉, Empty: 🌳
    "🌍🌍🌍⭐⭐⭐⭐⭐⭐⭐",  # Example: Filled: 🌍, Empty: ⭐
    "🦋🦋🦋🌺🌺🌺🌺🌺🌺🌺"  # Example: Filled: 🦋, Empty: 🌺
]

def get_random_progress_bar():
    return random.choice(progress_bars)
