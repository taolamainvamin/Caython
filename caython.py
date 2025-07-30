import re
import subprocess
import sys
import os

variables = {}
functions = {}

def run_block(block):
    run_code('\n'.join(block))

def run_line(line, lines_iter=None):
    line = line.strip()

    # Lệnh joke
    if line == "joke":
        print("😂 Caython sinh ra từ sự nghiêm túc quá mức của Python!")
        print("🤖 'kaatos' là lời nguyền cổ xưa từ một dòng code sai cú pháp.")
        print("🎭 'kayka' nghe như khai báo, nhưng là tên của con vẹt AI.")
        print("🚀 'TungSad' thật ra là tên bài hát của một mạng nơ-ron thất bại.")

    # Biến
    elif line.startswith("kayka "):
        match = re.match(r'kayka \[(.+?)\] = "(.*?)"', line)
        if match:
            var, val = match.groups()
            variables[var] = val
        else:
            print("Lỗi cú pháp khi khai báo biến:", line)

    # In chuỗi
    elif line.startswith("kaatos "):
        print(line[7:].strip('"'))

    # In biến
    elif line.startswith("+blua echive "):
        var = line[14:].strip("[] \n")
        print(variables.get(var, f"[Không tìm thấy bientro {var}]"))

    # AI huấn luyện
    elif line.startswith("+TungSad "):
        match = re.match(r"\+TungSad <(.+?)> -> (.+)", line)
        if match:
            data, output = match.groups()
            print(f"[AI] Đang huấn luyện từ {data} -> create {output}")
        else:
            print("Lỗi cú pháp khi hiểu AI:", line)

    # Shell
    elif line.startswith("!"):
        try:
            result = subprocess.run(line[1:], shell=True, capture_output=True, text=True)
            print(result.stdout if result.stdout else result.stderr)
        except Exception as e:
            print(f"Lỗi khi gọi shell: {e}")

    # include file
    elif line.startswith("include <") and line.endswith(">"):
        filename = line[9:-1]
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                run_code(f.read())
        else:
            print(f"[Lỗi] File không tồn tại: {filename}")

    # right? điều kiện
    elif line.startswith("right? "):
        match = re.match(r'right\? \[(.+?)\] = "(.*?)" {', line)
        if match and lines_iter:
            varname, expect_val = match.groups()
            block = []
            for subline in lines_iter:
                if subline.strip() == "}":
                    break
                block.append(subline)
            if variables.get(varname) == expect_val:
                run_block(block)

    # vòng lặp Inside
    elif line.startswith("Inside ") and " times {" in line and lines_iter:
        match = re.match(r'Inside (\d+) times {', line)
        if match:
            count = int(match.group(1))
            block = []
            for subline in lines_iter:
                if subline.strip() == "}":
                    break
                block.append(subline)
            for _ in range(count):
                run_block(block)

    # định nghĩa hàm
    elif line.startswith("@") and line.endswith("{") and lines_iter:
        fname = line[1:-1].strip()
        block = []
        for subline in lines_iter:
            if subline.strip() == "}":
                break
            block.append(subline)
        functions[fname] = block

    # gọi hàm
    elif line.startswith("@call "):  # ← dùng lại cú pháp gốc
        fname = line[6:].strip()
        if fname in functions:
            run_block(functions[fname])
        else:
            print(f"[Lỗi] Hàm '{fname}' chưa được định nghĩa")

    else:
        print(f"[Lỗi] Lệnh không hợp lệ hoặc không được hỗ trợ: {line}")

def run_code(code):
    lines = code.strip().split('\n')
    lines_iter = iter(lines)
    for line in lines_iter:
        run_line(line, lines_iter)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cách dùng: python3 caython.py <file.kayka>")
        exit()

    with open(sys.argv[1], 'r') as f:
        code = f.read()
        run_code(code)


def run_code(code):
    for line in code.strip().split('\n'):
        run_line(line)


