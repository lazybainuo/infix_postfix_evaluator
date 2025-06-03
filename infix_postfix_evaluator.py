"""
表达式求值计算器

该程序实现了中缀表达式的求值，支持以下功能：
1. 支持中英文括号：() 和 （）
2. 支持基本运算符：+、-、*、/
3. 支持多位数运算
4. 支持空格输入
5. 支持前缀表达式和后缀表达式转换
6. 支持调试模式
7. 支持负号处理
8. 支持表达式历史记录

作者：白诺
日期：2024-05-28
"""

import logging
import time
from datetime import datetime
from typing import List


class Colors:
    """
    ANSI颜色代码类，用于控制终端输出颜色
    """
    RED = '\033[91m'      # 红色，用于错误信息
    GREEN = '\033[92m'    # 绿色，用于成功信息
    YELLOW = '\033[93m'   # 黄色，用于警告信息
    BLUE = '\033[94m'     # 蓝色，用于调试信息
    MAGENTA = '\033[95m'  # 品红色，用于标题
    CYAN = '\033[96m'     # 青色，用于时间戳
    ENDC = '\033[0m'      # 结束颜色


class CustomFormatter(logging.Formatter):
    """
    自定义日志格式化器，用于添加颜色和时间戳
    
    功能：
    1. 为不同级别的日志添加不同的颜色
    2. 添加时间戳
    3. 格式化日志消息
    """
    def __init__(self):
        """初始化格式化器"""
        super().__init__()
        self.counter = 0  # 日志计数器

    def format(self, record):
        """
        格式化日志记录，添加颜色和时间戳
        
        @param record: 日志记录对象
        @return: 格式化后的日志消息
        """
        self.counter += 1
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        
        # 根据日志级别设置不同的颜色
        if record.levelno == logging.DEBUG:
            record.msg = f"{Colors.CYAN}[{timestamp}] [DEBUG]{Colors.ENDC} {Colors.BLUE}{record.msg}{Colors.ENDC}"
        elif record.levelno == logging.WARNING:
            record.msg = f"{Colors.YELLOW}[{timestamp}] [WARNING]{Colors.ENDC} {Colors.YELLOW}{record.msg}{Colors.ENDC}"
        elif record.levelno == logging.ERROR:
            record.msg = f"{Colors.RED}[{timestamp}] [ERROR]{Colors.ENDC} {Colors.RED}{record.msg}{Colors.ENDC}"
        return super().format(record)


class DebugHandler(logging.Handler):
    """
    自定义日志处理器，用于收集调试信息
    
    功能：
    1. 收集日志消息
    2. 提供消息获取和清理功能
    3. 支持按时间戳排序
    """
    def __init__(self):
        """初始化处理器"""
        super().__init__()
        self.messages = []  # 存储日志消息的列表

    def emit(self, record):
        """
        处理日志记录
        
        @param record: 日志记录对象
        """
        msg = self.format(record)
        self.messages.append(msg)

    def get_messages(self):
        """
        获取所有收集的日志消息
        
        @return: 日志消息列表
        """
        return self.messages

    def clear(self):
        """清空日志消息列表"""
        self.messages = []


class Stack:
    """
    栈的实现类，用于模拟栈的基本操作
    
    功能：
    1. 基本的栈操作（入栈、出栈、查看栈顶）
    2. 栈状态查询（是否为空、大小）
    3. 操作次数统计
    """
    def __init__(self):
        """初始化栈"""
        self.items = []  # 存储栈元素的列表
        self.operations = 0  # 记录操作次数

    def push(self, item):
        """
        入栈操作
        
        @param item: 要入栈的元素
        """
        self.items.append(item)
        self.operations += 1

    def pop(self):
        """
        出栈操作

        @return: 栈顶元素
        @raises IndexError: 如果栈为空，则抛出异常
        """
        if not self.is_empty():
            self.operations += 1
            return self.items.pop()
        raise IndexError("空栈无法执行出栈操作")

    def peek(self):
        """
        查看栈顶元素，但不移除它

        @return: 栈顶元素，如果栈为空则返回 None
        """
        return self.items[-1] if self.items else None

    def is_empty(self):
        """
        判断栈是否为空
        
        @return: 如果栈为空返回 True，否则返回 False
        """
        return len(self.items) == 0

    def size(self):
        """
        返回栈的大小
        
        @return: 栈中元素的数量
        """
        return len(self.items)

    def get_operations_count(self):
        """
        获取操作次数
        
        @return: 栈操作的总次数
        """
        return self.operations


# 配置日志系统
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False  # 防止日志传播到根日志器

# 创建并配置调试信息收集器
debug_handler = DebugHandler()
debug_handler.setFormatter(CustomFormatter())
logger.addHandler(debug_handler)


def log_debug(message):
    """
    统一的调试日志输出函数
    
    @param message: 要记录的调试信息
    """
    logger.debug(message)


def print_debug_info():
    """
    打印收集的调试信息，按时间戳排序
    
    功能：
    1. 获取所有日志消息
    2. 按时间戳排序
    3. 格式化输出
    4. 清空消息列表
    """
    messages = debug_handler.get_messages()
    if messages:
        print(f"\n{Colors.MAGENTA}调试信息:{Colors.ENDC}")
        # 按时间戳排序
        messages.sort(key=lambda x: x.split(']')[0].split('[')[1])
        for msg in messages:
            print(msg)
        debug_handler.clear()


def validate_expression(tokens: List[str]) -> None:
    """
    验证表达式基本结构
    
    功能：
    1. 检查括号匹配
    2. 验证运算符位置
    3. 确保表达式结构有效
    
    @param tokens: 标记列表
    @raises ValueError: 如果表达式结构无效
    """
    stack = Stack()
    for i, token in enumerate(tokens):
        if token == '(':
            stack.push((token, i))
        elif token == ')':
            if stack.is_empty():
                raise ValueError(f"位置 {i+1}: 多余的右括号")
            stack.pop()
    
    if not stack.is_empty():
        _, pos = stack.peek()
        raise ValueError(f"位置 {pos+1}: 缺少右括号")
    
    # 检查运算符位置
    for i in range(1, len(tokens)):
        if tokens[i] in '+-*/' and tokens[i-1] in '+-*/(':
            raise ValueError(f"位置 {i+1}: 运算符 {tokens[i-1]} 后不能直接跟 {tokens[i]}")


def tokenize(expression: str) -> List[str]:
    """
    分词函数，将输入的中缀表达式字符串转换为标记列表
    
    功能：
    1. 处理多位数
    2. 处理空格
    3. 处理中英文括号
    4. 处理负号
    5. 验证字符有效性
    
    @param expression: 中缀表达式字符串
    @return: 标记列表
    @raises ValueError: 如果表达式包含无效字符
    """
    start_time = time.time()
    tokens = []  # 用于存储分词结果
    num_buffer = []  # 用于暂存多位数的数字字符
    expression = expression.replace(' ', '')  # 移除所有空格

    # 定义括号映射，将中英文括号统一为英文括号
    bracket_map = {'（': '(', '）': ')', '(': '(', ')': ')'}
    valid_operators = {'+', '-', '*', '/'}

    for i, char in enumerate(expression):
        if char.isdigit():
            # 如果字符是数字，则加入数字缓冲区
            num_buffer.append(char)
        else:
            # 处理负号（一元运算符）
            if char == '-' and (i == 0 or not num_buffer and (tokens and tokens[-1] in '(+' or not tokens)):
                tokens.append('0')  # 添加0使其成为二元操作
            
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
                logger.error(f"位置 {i+1} 发现无效字符: '{char}'")
                raise ValueError(f"位置 {i+1}: 无效字符 '{char}'")

    if num_buffer:  # 处理最后一个数字
        tokens.append(''.join(num_buffer))

    end_time = time.time()
    log_debug(f"分词耗时: {(end_time - start_time)*1000:.2f}ms")
    log_debug(f"分词结果: {tokens}")
    return tokens


def infix_to_postfix(tokens: List[str]) -> str:
    """
    将中缀表达式转换为后缀表达式
    
    功能：
    1. 使用调度场算法转换表达式
    2. 处理运算符优先级
    3. 处理括号匹配
    
    @param tokens: 已分词的标记列表
    @return: 后缀表达式字符串
    @raises ValueError: 如果表达式格式无效
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


def infix_to_prefix(tokens: List[str]) -> str:
    """
    将中缀表达式转换为前缀表达式
    
    功能：
    1. 反转表达式
    2. 使用调度场算法转换表达式
    3. 处理运算符优先级
    4. 处理括号匹配
    
    @param tokens: 已分词的标记列表
    @return: 前缀表达式字符串
    @raises ValueError: 如果表达式格式无效
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


def evaluate_postfix(postfix_expr: str) -> float:
    """
    后缀表达式求值
    
    功能：
    1. 使用栈计算后缀表达式
    2. 处理基本运算
    3. 处理除零错误
    4. 保留6位小数
    
    @param postfix_expr: 空格分隔的后缀表达式字符串
    @return: 计算结果
    @raises ValueError: 如果表达式格式无效
    @raises ZeroDivisionError: 如果除数为零
    """
    start_time = time.time()
    log_debug(f"开始计算后缀表达式: {postfix_expr}")
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

    result = operand_stack.pop()
    end_time = time.time()
    log_debug(f"计算结果: {result}")
    log_debug(f"后缀表达式计算耗时: {(end_time - start_time)*1000:.2f}ms")
    log_debug(f"栈操作次数: {operand_stack.get_operations_count()}")
    return result


def evaluate_prefix(prefix_expr: str) -> float:
    """
    前缀表达式求值
    
    功能：
    1. 使用栈计算前缀表达式
    2. 处理基本运算
    3. 处理除零错误
    4. 保留6位小数
    
    @param prefix_expr: 空格分隔的前缀表达式字符串
    @return: 计算结果
    @raises ValueError: 如果表达式格式无效
    @raises ZeroDivisionError: 如果除数为零
    """
    start_time = time.time()
    log_debug(f"开始计算前缀表达式: {prefix_expr}")
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

    result = operand_stack.pop()
    end_time = time.time()
    log_debug(f"计算结果: {result}")
    log_debug(f"前缀表达式计算耗时: {(end_time - start_time)*1000:.2f}ms")
    log_debug(f"栈操作次数: {operand_stack.get_operations_count()}")
    return result


def main():
    """
    主程序交互界面，提供用户输入表达式并进行转换和求值的功能
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
    print("7. 支持负号处理")
    print("8. 支持表达式历史记录")
    print("=" * 50)
    print("输入 'exit' 或 'quit' 退出程序")
    print("输入 'debug' 开启/关闭调试模式")
    print("输入 'history' 查看历史记录")

    debug_mode = False
    expression_history = []  # 存储表达式历史记录

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

            if input_expr.lower() == 'history':
                if not expression_history:
                    print(f"{Colors.YELLOW}暂无历史记录{Colors.ENDC}")
                else:
                    print(f"\n{Colors.MAGENTA}历史记录:{Colors.ENDC}")
                    for i, expr in enumerate(expression_history, 1):
                        print(f"{i}. {expr}")
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
                
                # 验证表达式结构
                validate_expression(tokens)
                
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

                # 记录历史
                expression_history.append(input_expr)
                if len(expression_history) > 10:  # 只保留最近10条记录
                    expression_history.pop(0)

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