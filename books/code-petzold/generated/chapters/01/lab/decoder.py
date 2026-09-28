"""Original exact-timing teaching model; not a physical Morse receiver."""
CODES = {'E': '.', 'T': '-', 'A': '.-', 'N': '-.'}
LETTERS = {value: key for key, value in CODES.items()}
PREFIXES = {code[:i] for code in LETTERS for i in range(1, len(code) + 1)}


def check_tau(tau):
    if type(tau) is not int or tau <= 0:
        raise ValueError('tau must be a positive integer')


def encode(text, tau=1):
    """Return alternating (ON=1/OFF=0, duration) events, with implicit EOF."""
    check_tau(tau)
    if not isinstance(text, str):
        raise ValueError('text must be a string')
    if text == '':
        return []
    if text.startswith(' ') or text.endswith(' ') or '  ' in text:
        raise ValueError('use one space only between nonempty words')
    if any(char not in CODES and char != ' ' for char in text):
        raise ValueError('only uppercase E, T, A, N and spaces are supported')
    events = []
    previous = None
    for char in text:
        if char == ' ':
            previous = ' '
            continue
        if events:
            events.append((0, (6 if previous == ' ' else 3) * tau))
        for index, mark in enumerate(CODES[char]):
            if index:
                events.append((0, tau))
            events.append((1, (1 if mark == '.' else 3) * tau))
        previous = char
    return events


def decode(events, tau=1):
    """Validate an iterable of exact events; return text or raise ValueError."""
    check_tau(tau)
    output = []
    pending = ''
    expected = 1
    seen = False

    def close():
        nonlocal pending
        if pending not in LETTERS:
            raise ValueError('unknown completed pattern')
        output.append(LETTERS[pending])
        pending = ''

    for event in events:
        if not isinstance(event, (list, tuple)) or len(event) != 2:
            raise ValueError('each event must have level and duration')
        level, duration = event
        if type(level) is not int or level not in (0, 1) or level != expected:
            raise ValueError('events must alternate, starting ON')
        if type(duration) is not int or duration <= 0 or duration % tau:
            raise ValueError('duration must be a positive integer multiple of tau')
        ratio = duration // tau
        if level == 1:
            if ratio not in (1, 3):
                raise ValueError('invalid ON duration')
            pending += '.' if ratio == 1 else '-'
            if pending not in PREFIXES:
                raise ValueError('pattern cannot match the restricted alphabet')
        else:
            if ratio not in (1, 3, 6):
                raise ValueError('invalid OFF duration')
            if ratio in (3, 6):
                close()
                if ratio == 6:
                    output.append(' ')
        expected = 1 - level
        seen = True
    if not seen:
        return ''
    if expected == 1:
        raise ValueError('frame must end ON; EOF closes the final character')
    close()
    return ''.join(output)
