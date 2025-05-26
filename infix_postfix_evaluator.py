class Stack:
    """栈的实现类"""

    def __init__(self):
        self.items = []

    def push(self, item):
        """入栈操作"""
        self.items.append(item)

    def pop(self):
        """出栈操作"""
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("空栈无法执行出栈操作")

    def peek(self):
        """查看栈顶元素"""
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        """判断栈是否为空"""
        return len(self.items) == 0

    def size(self):
        """返回栈的大小"""
        return len(self.items)


def tokenize(expression):
    """
    分词函数，将输入字符串转换为标记列表
    处理多位数、空格和中英文括号
    """
    tokens = []
    num_buffer = []
    expression = expression.replace(' ', '')  # 移除所有空格
    
    # 定义括号映射
    bracket_map = {'（': '(', '）': ')', '(': '(', ')': ')'}

    for char in expression:
        if char.isdigit():
            num_buffer.append(char)
        else:
            if num_buffer:
                tokens.append(''.join(num_buffer))
                num_buffer = []
            # 处理中英文括号
            if char in bracket_map:
                tokens.append(bracket_map[char])
            else:
                tokens.append(char)

    if num_buffer:  # 处理最后一个数字
        tokens.append(''.join(num_buffer))

    return tokens


def infix_to_postfix(infix_expr):
    """
    中缀表达式转后缀表达式
    :param infix_expr: 中缀表达式字符串
    :return: 后缀表达式字符串
    """
    precedence = {'+': 2, '-': 2, '*': 3, '/': 3, '(': 1}
    op_stack = Stack()
    postfix = []

    try:
        tokens = tokenize(infix_expr)
    except:
        raise ValueError("表达式格式无效")

    for token in tokens:
        if token.isdigit():
            postfix.append(token)
        elif token == '(':
            op_stack.push(token)
        elif token == ')':
            try:
                top = op_stack.pop()
                while top != '(':
                    postfix.append(top)
                    top = op_stack.pop()
            except IndexError:
                raise ValueError("括号不匹配")
        else:
            while (not op_stack.is_empty()) and \
                    (precedence[op_stack.peek()] >= precedence[token]):
                postfix.append(op_stack.pop())
            op_stack.push(token)

    while not op_stack.is_empty():
        postfix.append(op_stack.pop())

    return ' '.join(postfix)


def infix_to_prefix(infix_expr):
    """
    中缀表达式转前缀表达式
    :param infix_expr: 中缀表达式字符串
    :return: 前缀表达式字符串
    """
    precedence = {'+': 2, '-': 2, '*': 3, '/': 3, '(': 1}
    op_stack = Stack()
    prefix = []
    
    try:
        tokens = tokenize(infix_expr)
        # 反转表达式以便处理前缀
        tokens.reverse()
    except:
        raise ValueError("表达式格式无效")

    for token in tokens:
        if token.isdigit():
            prefix.append(token)
        elif token == ')':  # 注意：由于反转了表达式，括号也要反转
            op_stack.push(token)
        elif token == '(':
            try:
                top = op_stack.pop()
                while top != ')':
                    prefix.append(top)
                    top = op_stack.pop()
            except IndexError:
                raise ValueError("括号不匹配")
        else:
            while (not op_stack.is_empty()) and \
                    (precedence[op_stack.peek()] > precedence[token]):
                prefix.append(op_stack.pop())
            op_stack.push(token)

    while not op_stack.is_empty():
        prefix.append(op_stack.pop())

    # 反转结果得到前缀表达式
    prefix.reverse()
    return ' '.join(prefix)


def evaluate_postfix(postfix_expr):
    """
    后缀表达式求值
    :param postfix_expr: 空格分隔的后缀表达式
    :return: 计算结果
    """
    operand_stack = Stack()
    tokens = postfix_expr.split()

    for token in tokens:
        if token.isdigit():
            operand_stack.push(int(token))
        else:
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

            operand_stack.push(result)

    if operand_stack.size() != 1:
        raise ValueError("后缀表达式格式无效")

    return operand_stack.pop()


def evaluate_prefix(prefix_expr):
    """
    前缀表达式求值
    :param prefix_expr: 空格分隔的前缀表达式
    :return: 计算结果
    """
    operand_stack = Stack()
    tokens = prefix_expr.split()
    # 反转tokens以便从右向左处理
    tokens.reverse()

    for token in tokens:
        if token.isdigit():
            operand_stack.push(int(token))
        else:
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

            operand_stack.push(result)

    if operand_stack.size() != 1:
        raise ValueError("前缀表达式格式无效")

    return operand_stack.pop()


def main():
    """主程序交互界面"""
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