import struct

from .header import *
from funcutils import match, OfType
from clformat import clformat


@match(s=OfType(bool))
def iso_str(s):
    return int(s)

@match(s=OfType(int))
def iso_str(s):
    return s

@match(s=OfType(float))
def iso_str(s):
    """Interpret IEEE-754 floating-point value as signed integer."""
    return struct.unpack('i', struct.pack('f', s))[0]

@match(s=OfType(str))
def iso_str(s):
    return s


def translator(seq=1, msg=''):
    return lambda cmd=None, *args, **kwargs: at(seq, msg, cmd, *args, **kwargs)


@match(cmd=OfType(str))
def at(seq, msg, cmd=None, *args, **kwargs):
    """Push a new command"""
    return translator(seq + 1, msg + clformat("AT*~a=~s,~{~s~^,~}\r",
        cmd, seq, map(iso_str, globals()[cmd.lower()](*args, **kwargs))))

@match(msg='', cmd=None)
def at(seq, msg, cmd=None, *args, **kwargs):
    """Output the comwdg"""
    return translator(seq)(*COMWDG_CMD)()

@match(msg=OfType(str), cmd=None)
def at(seq, msg, cmd=None, *args, **kwargs):
    """Output the result"""
    return translator(seq), msg


def ref(takeoff, emergency=False):
    """
    Basic behaviour of the drone: take-off/landing, emergency stop/reset

    Parameters:
    takeoff -- True: Takeoff / False: Land
    emergency -- True: Turn of the engines
    """
    assert type(takeoff) == bool
    assert type(emergency) == bool
    return 0b10001010101000000000000000000 | (emergency << 8) | (takeoff << 9),


def pcmd(progressive, lr, fb, vv, va):
    """
    Makes the drone move (translate/rotate).

    Parameters:
    progressive -- True: enable progressive commands, False: disable (i.e.
        enable hovering mode)
    lr -- left-right tilt: float [-1..1] negative: left, positive: right
    rb -- front-back tilt: float [-1..1] negative: forwards, positive:
        backwards
    vv -- vertical speed: float [-1..1] negative: go down, positive: rise
    va -- angular speed: float [-1..1] negative: spin left, positive: spin 
        right

    The above float values are a percentage of the maximum speed.
    """
    assert type(progressive) == bool
    assert all(map(lambda x: abs(x) <= 1, (lr, fb, vv, va)))
    return progressive, float(lr), float(fb), float(vv), float(va)


def ftrim():
    """
    Tell the drone it's lying horizontally.

    Parameters:
    """
    return ()


def config(option, value):
    """
    Set configuration parameters of the drone.

    Parameters:
    option -- the name of the option to set (byte with hex.value 22h)
    value -- the option value
    """
    return str(option), str(value)


def config_ids(sid, uid, aid):
    """
    Identifiers for the next AT*CONFIG command

    Parameters:
    sid -- current session id
    uid -- current user id
    aid -- current application id
    """
    assert all(map(lambda x: type(x) == int, (sid, uid, aid)))
    return sid, uid, aid


def comwdg():
    """
    Reset communication watchdog.

    Parameters:
    """
    # OPTIONAL: no sequence number
    return ()


def led(anim, freq, duration):
    """
    Control the drones LED.

    Parameters:
    anim --integer: animation to play
    freq -- float: frequence in HZ of the animation
    duration -- integer: total duration in seconds of the animation (animation is
        played (duration*frequence times))
    """
    assert type(anim) == int
    assert type(freq) == float
    assert type(duration) == int
    return anim, freq, duration


def anim(anim, duration):
    """
    Makes the drone execute a predefined movement (animation).

    Parameters:
    anim -- integer: animation to play
    duration -- integer: total duration in sections of the animation
    """
    assert type(anim) == int
    assert type(duration) == int
    return anim, duration
