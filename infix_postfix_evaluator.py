class Stack:
    """
    栈的实现类，用于模拟栈的基本操作。
    """

    def __init__(self):
        """
        初始化栈，使用一个空列表来存储栈中的元素。
        """
        self.items = []

    def push(self, item):
        """
        入栈操作，将一个元素添加到栈顶。
        :param item: 要入栈的元素
        """
        self.items.append(item)

    def pop(self):
        """
        出栈操作，移除并返回栈顶元素。
        :return: 栈顶元素
        :raises IndexError: 如果栈为空，则抛出异常
        """
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("空栈无法执行出栈操作")

    def peek(self):
        """
        查看栈顶元素，但不移除它。
        :return: 栈顶元素，如果栈为空则返回 None
        """
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        """
        判断栈是否为空。
        :return: 如果栈为空返回 True，否则返回 False
        """
        return len(self.items) == 0

    def size(self):
        """
        返回栈的大小，即栈中元素的数量。
        :return: 栈的大小
        """
        return len(self.items)


def tokenize(expression):
    """
    分词函数，将输入的中缀表达式字符串转换为标记列表。
    处理多位数、空格和中英文括号。
    :param expression: 中缀表达式字符串
    :return: 标记列表
    """
    tokens = []  # 用于存储分词结果
    num_buffer = []  # 用于暂存多位数的数字字符
    expression = expression.replace(' ', '')  # 移除所有空格

    # 定义括号映射，将中英文括号统一为英文括号
    bracket_map = {'（': '(', '）': ')', '(': '(', ')': ')'}

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
            else:
                # 其他字符直接加入标记列表
                tokens.append(char)

    if num_buffer:  # 处理最后一个数字
        tokens.append(''.join(num_buffer))

    return tokens


def infix_to_postfix(infix_expr):
    """
    将中缀表达式转换为后缀表达式。
    :param infix_expr: 中缀表达式字符串
    :return: 后缀表达式字符串
    """
    # 定义运算符优先级
    precedence = {'+': 2, '-': 2, '*': 3, '/': 3, '(': 1}
    op_stack = Stack()  # 运算符栈
    postfix = []  # 后缀表达式列表

    try:
        tokens = tokenize(infix_expr)  # 对中缀表达式进行分词
    except:
        raise ValueError("表达式格式无效")

    for token in tokens:
        if token.isdigit():
            # 如果是数字，直接加入后缀表达式
            postfix.append(token)
        elif token == '(':
            # 如果是左括号，入栈
            op_stack.push(token)
        elif token == ')':
            # 如果是右括号，弹出栈顶元素直到遇到左括号
            try:
                top = op_stack.pop()
                while top != '(':
                    postfix.append(top)
                    top = op_stack.pop()
            except IndexError:
                raise ValueError("括号不匹配")
        else:
            # 如果是运算符，根据优先级处理
            while (not op_stack.is_empty()) and \
                    (precedence[op_stack.peek()] >= precedence[token]):
                postfix.append(op_stack.pop())
            op_stack.push(token)

    # 将剩余的运算符加入后缀表达式
    while not op_stack.is_empty():
        postfix.append(op_stack.pop())

    return ' '.join(postfix)  # 返回后缀表达式字符串


def infix_to_prefix(infix_expr):
    """
    将中缀表达式转换为前缀表达式。
    :param infix_expr: 中缀表达式字符串
    :return: 前缀表达式字符串
    """
    # 定义运算符优先级
    precedence = {'+': 2, '-': 2, '*': 3, '/': 3, '(': 1}
    op_stack = Stack()  # 运算符栈
    prefix = []  # 前缀表达式列表

    try:
        tokens = tokenize(infix_expr)  # 对中缀表达式进行分词
        # 反转表达式以便处理前缀
        tokens.reverse()
    except:
        raise ValueError("表达式格式无效")

    for token in tokens:
        if token.isdigit():
            # 如果是数字，直接加入前缀表达式
            prefix.append(token)
        elif token == ')':  # 注意：由于反转了表达式，括号也要反转
            # 如果是右括号，入栈
            op_stack.push(token)
        elif token == '(':
            # 如果是左括号，弹出栈顶元素直到遇到右括号
            try:
                top = op_stack.pop()
                while top != ')':
                    prefix.append(top)
                    top = op_stack.pop()
            except IndexError:
                raise ValueError("括号不匹配")
        else:
            # 如果是运算符，根据优先级处理
            while (not op_stack.is_empty()) and \
                    (precedence[op_stack.peek()] > precedence[token]):
                prefix.append(op_stack.pop())
            op_stack.push(token)

    # 将剩余的运算符加入前缀表达式
    while not op_stack.is_empty():
        prefix.append(op_stack.pop())

    # 反转结果得到前缀表达式
    prefix.reverse()
    return ' '.join(prefix)  # 返回前缀表达式字符串


def evaluate_postfix(postfix_expr):
    """
    后缀表达式求值。
    :param postfix_expr: 空格分隔的后缀表达式字符串
    :return: 计算结果
    """
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

    return operand_stack.pop()  # 返回最终结果


def evaluate_prefix(prefix_expr):
    """
    前缀表达式求值。
    :param prefix_expr: 空格分隔的前缀表达式字符串
    :return: 计算结果
    """
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
    print("=" * 50)
    print("输入 'exit' 或 'quit' 退出程序")

    while True:
        try:
            input_expr = input("\n请输入表达式：").strip()

            if input_expr.lower() in ['exit', 'quit']:
                print("程序已退出")
                break

            # 转换中缀表达式为前缀表达式
            prefix = infix_to_prefix(input_expr)
            print(f"前缀表达式: {prefix}")

            # 转换中缀表达式为后缀表达式
            postfix = infix_to_postfix(input_expr)
            print(f"后缀表达式: {postfix}")

            # 计算后缀表达式
            result = evaluate_postfix(postfix)
            print(f"后缀表达式计算结果: {result}")

            # 计算前缀表达式
            result = evaluate_prefix(prefix)
            print(f"前缀表达式计算结果: {result}")

        except ValueError as ve:
            print(f"输入错误：{str(ve)}")
        except ZeroDivisionError as zde:
            print(f"计算错误：{str(zde)}")
        except Exception as e:
            print(f"发生未知错误：{str(e)}")


if __name__ == "__main__":
    main()