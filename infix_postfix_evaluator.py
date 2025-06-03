import logging
import time
from datetime import datetime


# ANSI颜色代码
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'

# 配置日志
class CustomFormatter(logging.Formatter):
    """自定义日志格式化器"""
    def __init__(self):
        super().__init__()
        self.counter = 0

    def format(self, record):
        self.counter += 1
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        
        if record.levelno == logging.DEBUG:
            record.msg = f"{Colors.CYAN}[{timestamp}] [DEBUG] [{self.counter}]{Colors.ENDC} {Colors.BLUE}{record.msg}{Colors.ENDC}"
        elif record.levelno == logging.WARNING:
            record.msg = f"{Colors.YELLOW}[{timestamp}] [WARNING] [{self.counter}]{Colors.ENDC} {Colors.YELLOW}{record.msg}{Colors.ENDC}"
        elif record.levelno == logging.ERROR:
            record.msg = f"{Colors.RED}[{timestamp}] [ERROR] [{self.counter}]{Colors.ENDC} {Colors.RED}{record.msg}{Colors.ENDC}"
        return super().format(record)

# 创建日志处理器
class DebugHandler(logging.Handler):
    """自定义日志处理器，用于收集调试信息"""
    def __init__(self):
        super().__init__()
        self.messages = []

    def emit(self, record):
        msg = self.format(record)
        self.messages.append(msg)

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages = []

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False  # 防止日志传播到根日志器

# 创建并配置调试信息收集器
debug_handler = DebugHandler()
debug_handler.setFormatter(CustomFormatter())
logger.addHandler(debug_handler)

def log_debug(message):
    """统一的调试日志输出函数"""
    logger.debug(message)

def print_debug_info():
    """打印收集的调试信息"""
    messages = debug_handler.get_messages()
    if messages:
        print(f"\n{Colors.MAGENTA}调试信息:{Colors.ENDC}")
        # 按时间戳排序
        messages.sort(key=lambda x: x.split(']')[0].split('[')[1])
        for msg in messages:
            print(msg)
        debug_handler.clear()

class Stack:
    """
    栈的实现类，用于模拟栈的基本操作。
    """

    def __init__(self):
        """
        初始化栈，使用一个空列表来存储栈中的元素。
        """
        self.items = []
        self.operations = 0  # 记录操作次数

    def push(self, item):
        """
        入栈操作，将一个元素添加到栈顶。
        :param item: 要入栈的元素
        """
        self.items.append(item)
        self.operations += 1

    def pop(self):
        """
        出栈操作，移除并返回栈顶元素。
        :return: 栈顶元素
        :raises IndexError: 如果栈为空，则抛出异常
        """
        if not self.is_empty():
            self.operations += 1
            return self.items.pop()
        raise IndexError("空栈无法执行出栈操作")

    def peek(self):
        """
        查看栈顶元素，但不移除它。
        :return: 栈顶元素，如果栈为空则返回 None
        """
        if not self.is_empty():
            self.operations += 1
            return self.items[-1]
        return None

    def is_empty(self):
        """
        判断栈是否为空。
        :return: 如果栈为空返回 True，否则返回 False
        """
        self.operations += 1
        return len(self.items) == 0

    def size(self):
        """
        返回栈的大小，即栈中元素的数量。
        :return: 栈的大小
        """
        self.operations += 1
        return len(self.items)

    def get_operations_count(self):
        """获取操作次数"""
        return self.operations


def tokenize(expression):
    """
    分词函数，将输入的中缀表达式字符串转换为标记列表。
    处理多位数、空格和中英文括号。
    :param expression: 中缀表达式字符串
    :return: 标记列表
    """
    start_time = time.time()
    tokens = []  # 用于存储分词结果
    num_buffer = []  # 用于暂存多位数的数字字符
    expression = expression.replace(' ', '')  # 移除所有空格

    # 定义括号映射，将中英文括号统一为英文括号
    bracket_map = {'（': '(', '）': ')', '(': '(', ')': ')'}
    valid_operators = {'+', '-', '*', '/'}

    for char in expression:
        if char.isdigit():
            # 如果字符是数字，则加入数字缓冲区
            num_buffer.append(char)
        else:
            if num_buffer:
                # 如果数字缓冲区不为空，则将缓冲区中的数字加入标记列表
                tokens.append(''.join(num_buffer))
                num_buffer = []
            # 处理中英文括号
            if char in bracket_map:
                tokens.append(bracket_map[char])
            elif char in valid_operators:
                tokens.append(char)
            else:
                logger.error(f"发现无效字符: '{char}'")
                raise ValueError(f"表达式包含无效字符: '{char}'")

    if num_buffer:  # 处理最后一个数字
        tokens.append(''.join(num_buffer))

    end_time = time.time()
    log_debug(f"分词耗时: {(end_time - start_time)*1000:.2f}ms")
    log_debug(f"分词结果: {tokens}")
    return tokens


def infix_to_postfix(tokens):
    """
    将中缀表达式转换为后缀表达式。
    :param tokens: 已分词的标记列表
    :return: 后缀表达式字符串
    """
    start_time = time.time()
    # 定义运算符优先级，括号优先级最低
    precedence = {'+': 2, '-': 2, '*': 3, '/': 3, '(': 0, ')': 0}
    op_stack = Stack()  # 运算符栈
    postfix = []  # 后缀表达式列表

    for token in tokens:
        if token.isdigit():
            # 如果是数字，直接加入后缀表达式
            postfix.append(token)
        elif token == '(':
            # 如果是左括号，入栈
            op_stack.push(token)
        elif token == ')':
            # 如果是右括号，弹出栈顶元素直到遇到左括号
            while not op_stack.is_empty() and op_stack.peek() != '(':
                postfix.append(op_stack.pop())
            if op_stack.is_empty():
                raise ValueError("括号不匹配")
            op_stack.pop()  # 弹出左括号
        else:
            # 如果是运算符，根据优先级处理
            while (not op_stack.is_empty()) and \
                    (precedence[op_stack.peek()] >= precedence[token]):
                postfix.append(op_stack.pop())
            op_stack.push(token)

    # 将剩余的运算符加入后缀表达式
    while not op_stack.is_empty():
        if op_stack.peek() == '(':
            raise ValueError("括号不匹配")
        postfix.append(op_stack.pop())

    end_time = time.time()
    log_debug(f"中缀转后缀耗时: {(end_time - start_time)*1000:.2f}ms")
    log_debug(f"栈操作次数: {op_stack.get_operations_count()}")
    return ' '.join(postfix)  # 返回后缀表达式字符串


def infix_to_prefix(tokens):
    """
    将中缀表达式转换为前缀表达式。
    :param tokens: 已分词的标记列表
    :return: 前缀表达式字符串
    """
    start_time = time.time()
    # 定义运算符优先级，括号优先级最低
    precedence = {'+': 2, '-': 2, '*': 3, '/': 3, '(': 0, ')': 0}
    op_stack = Stack()  # 运算符栈
    prefix = []  # 前缀表达式列表

    # 反转表达式以便处理前缀
    tokens = tokens.copy()
    tokens.reverse()

    for token in tokens:
        if token.isdigit():
            # 如果是数字，直接加入前缀表达式
            prefix.append(token)
        elif token == ')':  # 注意：由于反转了表达式，括号也要反转
            # 如果是右括号，入栈
            op_stack.push(token)
        elif token == '(':
            # 如果是左括号，弹出栈顶元素直到遇到右括号
            while not op_stack.is_empty() and op_stack.peek() != ')':
                prefix.append(op_stack.pop())
            if op_stack.is_empty():
                raise ValueError("括号不匹配")
            op_stack.pop()  # 弹出右括号
        else:
            # 如果是运算符，根据优先级处理
            while (not op_stack.is_empty()) and \
                    (precedence[op_stack.peek()] > precedence[token]):
                prefix.append(op_stack.pop())
            op_stack.push(token)

    # 将剩余的运算符加入前缀表达式
    while not op_stack.is_empty():
        if op_stack.peek() == ')':
            raise ValueError("括号不匹配")
        prefix.append(op_stack.pop())

    # 反转结果得到前缀表达式
    prefix.reverse()
    end_time = time.time()
    log_debug(f"中缀转前缀耗时: {(end_time - start_time)*1000:.2f}ms")
    log_debug(f"栈操作次数: {op_stack.get_operations_count()}")
    return ' '.join(prefix)  # 返回前缀表达式字符串


def evaluate_postfix(postfix_expr):
    """
    后缀表达式求值。
    :param postfix_expr: 空格分隔的后缀表达式字符串
    :return: 计算结果
    """
    start_time = time.time()
    operand_stack = Stack()  # 操作数栈
    tokens = postfix_expr.split()  # 将后缀表达式分割为标记列表

    for token in tokens:
        if token.isdigit():
            # 如果是数字，入栈
            operand_stack.push(int(token))
        else:
            # 如果是运算符，弹出两个操作数并进行计算
            try:
                b = operand_stack.pop()
                a = operand_stack.pop()
            except IndexError:
                raise ValueError("后缀表达式格式无效")

            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("除数不能为零")
                result = a / b  # 使用浮点除法
                result = round(result, 6)  # 保留6位小数
            else:
                raise ValueError("无效的运算符")

            operand_stack.push(result)  # 将计算结果入栈

    if operand_stack.size() != 1:
        raise ValueError("后缀表达式格式无效")

    end_time = time.time()
    log_debug(f"后缀表达式计算耗时: {(end_time - start_time)*1000:.2f}ms")
    log_debug(f"栈操作次数: {operand_stack.get_operations_count()}")
    return operand_stack.pop()  # 返回最终结果


def evaluate_prefix(prefix_expr):
    """
    前缀表达式求值。
    :param prefix_expr: 空格分隔的前缀表达式字符串
    :return: 计算结果
    """
    start_time = time.time()
    operand_stack = Stack()  # 操作数栈
    tokens = prefix_expr.split()  # 将前缀表达式分割为标记列表
    # 反转tokens以便从右向左处理
    tokens.reverse()

    for token in tokens:
        if token.isdigit():
            # 如果是数字，入栈
            operand_stack.push(int(token))
        else:
            # 如果是运算符，弹出两个操作数并进行计算
            try:
                a = operand_stack.pop()
                b = operand_stack.pop()
            except IndexError:
                raise ValueError("前缀表达式格式无效")

            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("除数不能为零")
                result = a / b
                result = round(result, 6)
            else:
                raise ValueError("无效的运算符")

            operand_stack.push(result)  # 将计算结果入栈

    if operand_stack.size() != 1:
        raise ValueError("前缀表达式格式无效")

    end_time = time.time()
    log_debug(f"前缀表达式计算耗时: {(end_time - start_time)*1000:.2f}ms")
    log_debug(f"栈操作次数: {operand_stack.get_operations_count()}")
    return operand_stack.pop()  # 返回最终结果


def main():
    """
    主程序交互界面，提供用户输入表达式并进行转换和求值的功能。
    """
    print("=" * 50)
    print("表达式求值程序")
    print("支持功能：")
    print("1. 支持中英文括号：() 和 （）")
    print("2. 支持基本运算符：+、-、*、/")
    print("3. 支持多位数运算")
    print("4. 支持空格输入")
    print("5. 支持前缀表达式和后缀表达式转换")
    print("6. 支持调试模式（输入 'debug' 开启/关闭）")
    print("=" * 50)
    print("输入 'exit' 或 'quit' 退出程序")
    print("输入 'debug' 开启/关闭调试模式")

    debug_mode = False

    while True:
        try:
            # 清空之前的日志消息
            debug_handler.clear()
            
            input_expr = input("\n请输入表达式：").strip()
            
            if not input_expr:
                logger.warning("输入为空")
                print(f"{Colors.YELLOW}请输入有效的表达式{Colors.ENDC}")
                continue

            if input_expr.lower() == 'debug':
                debug_mode = not debug_mode
                logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)
                print(f"调试模式已{'开启' if debug_mode else '关闭'}")
                continue

            if input_expr.lower() in ['exit', 'quit']:
                print("程序已退出")
                break

            # 记录开始时间
            start_time = time.time()
            log_debug(f"开始处理表达式: {input_expr}")

            try:
                # 先进行分词，只记录一次分词结果
                tokens = tokenize(input_expr)
                
                # 转换中缀表达式为前缀表达式
                prefix = infix_to_prefix(tokens)
                print(f"前缀表达式: {prefix}")

                # 转换中缀表达式为后缀表达式
                postfix = infix_to_postfix(tokens)
                print(f"后缀表达式: {postfix}")

                # 计算后缀表达式
                result = evaluate_postfix(postfix)
                print(f"后缀表达式计算结果: {result}")

                # 计算前缀表达式
                result = evaluate_prefix(prefix)
                print(f"前缀表达式计算结果: {result}")

            except Exception as e:
                # 即使发生错误，也显示调试信息
                if debug_mode:
                    logger.error(f"发生错误: {str(e)}")
                    print_debug_info()
                raise  # 重新抛出异常，让外层处理

            # 记录结束时间
            end_time = time.time()
            if debug_mode:
                log_debug(f"总耗时: {(end_time - start_time)*1000:.2f}ms")
                print_debug_info()

        except ValueError as ve:
            logger.error(f"输入错误：{str(ve)}")
            print(f"{Colors.RED}输入错误：{str(ve)}{Colors.ENDC}")
        except ZeroDivisionError as zde:
            logger.error(f"计算错误：{str(zde)}")
            print(f"{Colors.RED}计算错误：{str(zde)}{Colors.ENDC}")
        except Exception as e:
            logger.error(f"发生未知错误：{str(e)}")
            print(f"{Colors.RED}发生未知错误：{str(e)}{Colors.ENDC}")
            print(f"{Colors.YELLOW}请检查表达式格式是否正确{Colors.ENDC}")


if __name__ == "__main__":
    main()