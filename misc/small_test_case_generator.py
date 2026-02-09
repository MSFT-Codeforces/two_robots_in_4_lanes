
def build_input(testcases):
    """
    testcases: list of (n, rows_top_to_bottom)
    returns full input string with leading t.
    """
    out = [str(len(testcases))]
    for n, rows in testcases:
        assert n == len(rows)
        for r in rows:
            assert len(r) == 4 and set(r) <= {'.', '#'}
        out.append(str(n))
        out.extend(rows)
    return "\n".join(out)

inputs = []

# Input 1: минимальный, пустой ряд (|S|=0)
inputs.append(build_input([
    (1, ["...."])
]))

# Input 2: минимальный, один артефакт в колонке 1 (|S|=1)
inputs.append(build_input([
    (1, ["#..."])
]))

# Input 3: минимальный, один артефакт в колонке 3 (|S|=1), проверка стартовой стоимости
inputs.append(build_input([
    (1, ["..#."])
]))

# Input 4: минимальный, два артефакта (1,4) (|S|=2), совпадает со стартовыми позициями
inputs.append(build_input([
    (1, ["#..#"])
]))

# Input 5: минимальный, два артефакта (2,3) (|S|=2), нужны движения обоих
inputs.append(build_input([
    (1, [".##."])
]))

# Input 6: минимальный невозможный (|S|=3)
inputs.append(build_input([
    (1, ["###."])
]))

# Input 7: все ряды пустые (проверка, что ответ 0 и нет лишних переходов)
inputs.append(build_input([
    (5, ["....", "....", "....", "....", "...."])
]))

# Input 8: одинаковые ряды с одиночным '#', столбец 2
inputs.append(build_input([
    (4, [".#..", ".#..", ".#..", ".#.."])
]))

# Input 9: одинаковые ряды с парой '#', столбцы 3 и 4
inputs.append(build_input([
    (3, ["..##", "..##", "..##"])
]))

# Input 10: чувствительность к порядку обработки (ввод сверху-вниз, обработка снизу-вверх)
# Top: #..#, Bottom: .##.
inputs.append(build_input([
    (2, ["#..#", ".##."])
]))

# Input 11: пустые ряды между ограниченными (проверка корректной обработки |S|=0)
inputs.append(build_input([
    (5, ["....", "..#.", "....", "....", ".#.."])
]))

# Input 12: стресс для перебора назначений при |S|=2 (чередование пар, ближние/дальние)
inputs.append(build_input([
    (6, [".#.#", "#.#.", "..##", "##..", ".##.", "#..#"])
]))

# Input 13: невозможность на последнем обрабатываемом ярусе (самая верхняя строка ввода)
inputs.append(build_input([
    (4, ["####", "....", ".##.", "...."])
]))

# Input 14: много тестов в одном вводе (проверка сброса DP между тестами)
inputs.append(build_input([
    (1, ["...."]),            # trivial
    (1, ["####"]),            # impossible
    (2, ["#...", "...."]),    # mix with empty
    (2, [".##.", "#..#"]),    # order sensitivity inside a multi-row test
    (3, ["....", ".#..", "..##"])  # mixed constraints
]))

# Input 15: одиночные '#' заставляют роботов часто перестраиваться (общая проверка DP)
inputs.append(build_input([
    (6, ["..#.", "#...", "...#", "#...", "...#", ".#.."])
]))

print("Test Cases: ")
for i, s in enumerate(inputs, 1):
    print(f"Input {i}:")
    print(s)
    if i != len(inputs):
        print()
