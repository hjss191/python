import streamlit as st
import copy


class Board:
    def __init__(self, board):
        self.board = copy.deepcopy(board)

    def find_empty_cell(self):
        for row, contents in enumerate(self.board):
            try:
                col = contents.index(0)
                return row, col
            except ValueError:
                pass
        return None

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return all(self.board[row][col] != num for row in range(9))

    def valid_in_square(self, row, col, num):
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3
        for row_no in range(row_start, row_start + 3):
            for col_no in range(col_start, col_start + 3):
                if self.board[row_no][col_no] == num:
                    return False
        return True

    def is_valid(self, empty, num):
        row, col = empty
        return all([
            self.valid_in_row(row, num),
            self.valid_in_col(col, num),
            self.valid_in_square(row, col, num)
        ])

    def solver(self):
        if (next_empty := self.find_empty_cell()) is None:
            return True
        for guess in range(1, 10):
            if self.is_valid(next_empty, guess):
                row, col = next_empty
                self.board[row][col] = guess
                if self.solver():
                    return True
                self.board[row][col] = 0
        return False


# --- Streamlit 配置 ---
st.set_page_config(page_title="Sudoku Solver", page_icon="🧩", layout="centered")
st.title("🧩 Python 数独解题器")


# --- 按钮回调函数 ---
def reset_board():
    """将所有输入框重置为 0"""
    for r in range(9):
        for c in range(9):
            st.session_state[f"in_{r}_{c}"] = 0


def load_example():
    """加载一个预设题目"""
    example = [
        [0, 0, 2, 0, 0, 8, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 7, 6, 2],
        [4, 3, 0, 0, 3, 0, 8, 0, 0],
        [0, 5, 0, 0, 3, 0, 0, 9, 0],
        [0, 4, 0, 0, 0, 0, 0, 2, 6],
        [0, 0, 0, 4, 6, 7, 0, 0, 0],
        [0, 8, 6, 7, 0, 4, 0, 0, 0],
        [0, 0, 0, 5, 1, 9, 0, 0, 8],
        [1, 7, 0, 0, 0, 6, 0, 0, 5]
    ]
    for r in range(9):
        for c in range(9):
            st.session_state[f"in_{r}_{c}"] = example[r][c]


# --- 侧边栏/功能按钮 ---
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("🧹 一键清空", use_container_width=True):
        reset_board()
with col_btn2:
    if st.button("💡 加载经典题目", use_container_width=True):
        load_example()

st.markdown("---")

# --- 渲染 9x9 输入矩阵 ---
current_board = []
for r in range(9):
    cols = st.columns(9)
    row_data = []
    for c in range(9):
        # 初始值设为 0
        if f"in_{r}_{c}" not in st.session_state:
            st.session_state[f"in_{r}_{c}"] = 0

        val = cols[c].number_input(
            label=f"R{r}C{c}",
            min_value=0,
            max_value=9,
            step=1,
            key=f"in_{r}_{c}",
            label_visibility="collapsed"
        )
        row_data.append(val)
    current_board.append(row_data)

st.markdown("---")

# --- 解题按钮逻辑 ---
if st.button("🚀 开始解题", type="primary", use_container_width=True):
    # 检查是否为空白棋盘
    if all(all(cell == 0 for cell in row) for row in current_board):
        st.warning("棋盘是空的，请先输入题目。")
    else:
        game = Board(current_board)
        with st.spinner('算法正在深度搜索中...'):
            if game.solver():
                st.success("✅ 解题成功！结果如下：")
                # 使用 DataFrame 或 Table 漂亮地显示
                st.table(game.board)
            else:
                st.error("❌ 此题逻辑上无解，请检查输入是否有误。")