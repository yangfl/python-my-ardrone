import inspect
import types
import dis
from time import sleep

from .header import *

from ebc import iter_disassemble, assemble


def init(interface):
    inspect.stack()[2][0].f_locals.update({name: getattr(interface, method) for name, method in SHORTHAND_COMMAND.items()})


def use_ardrone(interface, co_stacksize=16):
    def wrapper(func):
        code_obj = func.__code__
        code = assemble(
            _get_literal_expression(code_obj, interface),
            co_argcount=code_obj.co_argcount, co_stacksize=co_stacksize,
            co_flags=code_obj.co_flags, co_filename=code_obj.co_filename,
            co_name=code_obj.co_name, co_firstlineno=code_obj.co_firstlineno,
            co_freevars=code_obj.co_freevars, co_cellvars=code_obj.co_cellvars)
        return types.FunctionType(
            code,
            func.__globals__,
            func.__name__,
            func.__defaults__,
            func.__closure__)
    return wrapper


def _get_literal_expression(code, interface):
    tape = []
    iter_code = iter_disassemble(code)
    command_buffer = []
    for op, arg in iter_code:
        if op == dis.opmap['LOAD_GLOBAL'] and arg in SHORTHAND_COMMAND:
            while op != dis.opmap['POP_TOP']:
                if op == dis.opmap['LOAD_ATTR'] or op == dis.opmap['LOAD_GLOBAL']:
                    command_buffer.append(arg)
                elif op == dis.opmap['LOAD_CONST'] or op == dis.opmap['LOAD_FAST']:
                    command_buffer.append(arg)
                    next(iter_code)
                op, arg = next(iter_code)
            tape.extend(_combine(command_buffer, interface))
            command_buffer = []
        else:
            tape.append((op, arg))
    return tape


def _combine(command_buffer, interface):
    result = []
    stack = []
    move = [(0, 0.0)] * 4
    movep = False
    pos = 0
    while pos < len(command_buffer):
        op = command_buffer[pos]
        pos += 1
        stack.append(op)
        if op in (
                'l',  # move_left
                'r',  # move_right
                'f',  # move_forward
                'b',  # move_backward
                'u',  # move_up
                'd',  # move_down
                'p',  # turn_left
                'n',  # turn_right
                ):
            arg = command_buffer[pos] if pos < len(command_buffer) else ''
            pos += 1
            if arg in SHORTHAND_COMMAND or arg == '':
                pos -= 1
                arg = 1.0
            movep = True
            if op == 'l':
                move[0] = _get_neg(1, arg)
            elif op == 'r':
                move[0] = _get_neg(0, arg)
            elif op == 'f':
                move[1] = _get_neg(1, arg)
            elif op == 'b':
                move[1] = _get_neg(0, arg)
            elif op == 'u':
                move[2] = _get_neg(0, arg)
            elif op == 'd':
                move[2] = _get_neg(1, arg)
            elif op == 'p':
                move[3] = _get_neg(1, arg)
            elif op == 'n':
                move[3] = _get_neg(0, arg)
            continue
        if movep:
            result.extend(_asm_call_attr(interface, 'move', *move))
            result.extend(_asm_call_sleep(0.4))
            move = [(0, 0.0)] * 4
            movep = False
        if op in (
                'y',  # land
                't',  # takeoff
                'h',  # hover
                'z',  # reset
                ):
            result.extend(_asm_call_attr(interface, SHORTHAND_COMMAND[op]))
            if op == 'h':
                result.extend(_asm_call_sleep(2))
        elif op in (
                's',  # sleep
                ):
            arg = command_buffer[pos]
            pos += 1
            result.extend(_asm_call_sleep(arg))
    if movep:
        result.extend(_asm_call_attr(interface, 'move', *move))
        result.extend(_asm_call_sleep(0.4))
    return result

def _get_neg(neg_p, arg):
    if neg_p:
        if type(arg) in (int, float):
            return (0, -arg)
        else:
            return (1, arg)
    else:
        return (0, arg)

def _asm_call_attr(interface, attr, *opn):
    asm_opn = []
    for neg_p, arg in opn:
        if type(arg) in (int, float):
            asm_opn.append(('LOAD_CONST', arg))
        else:
            asm_opn.append(('LOAD_FAST', arg))
        if neg_p:
            asm_opn.append(('UNARY_NEGATIVE', None))
    return [
        ('LOAD_CONST', interface),
        ('LOAD_ATTR', attr)] + asm_opn + [
        ('CALL_FUNCTION', len(opn)),
        ('POP_TOP', None)]

def _asm_call_sleep(time):
    return (
        ('LOAD_CONST', sleep),
        ('LOAD_CONST' if type(time) in (int, float) else 'LOAD_FAST', time),
        ('CALL_FUNCTION', 1),
        ('POP_TOP', None))
