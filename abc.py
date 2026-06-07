import sys
import os
import json
import hashlib
import requests
from PyQt6.QtCore import Qt, QUrl, QSettings
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QStackedWidget, QListWidget, QListWidgetItem, QCheckBox,
                             QMessageBox, QTreeWidget, QTreeWidgetItem, QTextEdit,
                             QComboBox, QMenu, QSplitter, QInputDialog, QGraphicsDropShadowEffect)
from PyQt6.QtGui import QFont, QAction, QColor
from PyQt6.QtWebEngineWidgets import QWebEngineView

# 【当前软件源码版本】
# 如果你想给所有人更新代码，只需在 GitHub 网页上修改 version.json 里的版本号为 "v1.0.1"，
# 本地源码运行到第 42 行时就会自动触发无感下载，把最新的 main.py 替换到本地并自动重启！
CURRENT_VERSION = "v1.0.0"

# ==============================================================================
# ⚙️ 核心全网云同步配置区域 (请填写你在 GitHub 上准备好的信息)
# ==============================================================================
GITHUB_USER = "KEPMk47KHAM5532-DOT"
GITHUB_REPO = "luobotech-data"
GITHUB_TOKEN = "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"


# ==============================================================================

class LuoboStudentClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"萝卜科技 学生端 {CURRENT_VERSION}")
        self.setGeometry(100, 100, 1280, 850)

        # 数据持久化存储（本地记住密码与缓存配置）
        self.settings = QSettings("LuoboTech", "StudentClientStandard")
        self.is_online_mode = False

        # 全局大字体设置（全简体）
        self.global_font = QFont("Microsoft YaHei", 12)
        self.setFont(self.global_font)

        # 主层级堆栈
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 📥 【核心注入】启动时首要检查 GitHub 云端是否有更新的 Python 源码
        self.check_github_source_update()

        # 初始化页面
        self.init_mode_page()  # 0: 启动模式选择页
        self.init_login_reg_page()  # 1: 登录与注册卡片页
        self.init_main_page()  # 2: 统一主功能核心页

        self.stacked_widget.setCurrentIndex(0)
        self.load_saved_credentials()
        self.apply_perfect_styles()  # 注入像素级美化样式表

    # ---------------- 📥 核心算法：GitHub 源码全自动热更新 ----------------
    def check_github_source_update(self):
        """ 运行时自动检查云端代码，如果是新版，直接下载最新的 .py 源码覆盖自身并重启 """
        version_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/version.json"
        code_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/main.py"
        try:
            resp = requests.get(version_url, timeout=3)
            if resp.status_code == 200:
                cloud_data = resp.json()
                cloud_version = cloud_data.get("version", "v1.0.0")

                # 如果云端的版本号大于当前本地的版本号
                if cloud_version > CURRENT_VERSION:
                    print(f"检测到云端有更新的代码: {cloud_version}，正在全自动热更新源码...")
                    code_resp = requests.get(code_url, timeout=10)
                    if code_resp.status_code == 200:
                        # 核心跨平台操作：直接用新代码改写当前的 .py 源码文件
                        with open(__file__, "w", encoding="utf-8") as f:
                            f.write(code_resp.text)

                        QMessageBox.information(
                            self, "全自动更新完成",
                            f"客户端已成功热升级至 {cloud_version}！\n更新日志:\n{cloud_data.get('log', '优化系统稳定度')}\n\n程序将自动重启应用新代码！"
                        )
                        # 自动重启 Python 脚本
                        os.execv(sys.executable, ['python'] + sys.argv)
                        sys.exit()
        except Exception as e:
            print("检查更新跳过或暂无网络，原因:", e)

    # ---------------- 🔑 核心算法：基于 GitHub 仓库的全网账号云同步 ----------------
    def encrypt_password(self, password):
        """ sha256安全加密，绝对不让明文密码暴露在公开的 GitHub 仓库里 """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def fetch_cloud_users_db(self):
        """ 从 GitHub 动态拉取全网统一的用户数据库文件 """
        url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/users.json"
        try:
            resp = requests.get(url, timeout=4)
            if resp.status_code == 200:
                return resp.json()
        except:
            pass
        return {}

    def upload_users_db_to_cloud(self, data):
        """ 将新注册的用户追加写入 GitHub 仓库，覆盖原 users.json """
        url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/users.json"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

        # 获取最新文件的 sha 值，这是 GitHub API 覆盖写入的必须要求
        sha = None
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            sha = res.json().get("sha")

        payload = {
            "message": "更新全网用户数据库",
            "content": requests.utils.base64.b64encode(json.dumps(data, indent=4).encode('utf-8')).decode('utf-8')
        }
        if sha:
            payload["sha"] = sha

        return requests.put(url, headers=headers, json=payload).status_code in [200, 201]

    # ---------------- 🎨 UI 像素级美化样式 ----------------
    def apply_perfect_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-family: 'Microsoft YaHei', 'Segoe UI';
                color: #2c3e50;
            }
            QMainWindow {
                background-color: #eef3fa;
            }
            QLineEdit {
                border: 1px solid #dcdfe6;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 16px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #1e6fff;
            }
            QPushButton#blueBtn {
                background-color: #1e6fff;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 12px;
            }
            QPushButton#blueBtn:hover { background-color: #4085ff; }
            QPushButton#blueBtn:pressed { background-color: #0055dd; }

            QPushButton#linkBtn {
                background-color: transparent;
                color: #8a92a6;
                font-size: 14px;
                border: none;
            }
            QPushButton#linkBtn:hover { color: #1e6fff; }

            QListWidget#sidebarMenu {
                background-color: transparent;
                border: none;
            }
            QListWidget#sidebarMenu::item {
                height: 52px;
                color: #515a6e;
                padding-left: 20px;
                font-size: 16px;
                border-radius: 8px;
                margin-bottom: 4px;
            }
            QListWidget#sidebarMenu::item:hover {
                background-color: #e4e9f2;
            }
            QListWidget#sidebarMenu::item:selected {
                background-color: #e8f0fe;
                color: #1e6fff;
                font-weight: bold;
            }

            QTreeWidget {
                border: 1px solid #e4e7ed;
                border-radius: 6px;
                background-color: #ffffff;
                font-size: 15px;
            }
            QTextEdit {
                border: 1px solid #dcdfe6;
                border-radius: 8px;
                font-size: 16px;
                padding: 12px;
                background-color: #ffffff;
            }
        """)

    # ---------------- 1. 启动模式选择界面 ----------------
    def init_mode_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(25)

        logo_lbl = QLabel("📖")
        logo_lbl.setStyleSheet(
            "font-size: 42px; background-color: #1e6fff; color: white; padding: 15px; border-radius: 16px;")

        title = QLabel("萝卜科技 学生端")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #1c1f23; margin-top: 10px;")
        subtitle = QLabel(f"工作台就绪 • 当前代码版本 {CURRENT_VERSION}")
        subtitle.setStyleSheet("font-size: 16px; color: #8a92a6; margin-bottom: 20px;")

        layout.addWidget(logo_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_offline = QPushButton("离线模式\n无需登录，直接进入本地笔记本")
        btn_offline.setFixedSize(450, 95)
        btn_offline.setStyleSheet("""
            QPushButton {
                background-color: white; border: 2px solid #e4e7ed; border-radius: 12px;
                font-size: 18px; font-weight: bold; color: #2c3e50; text-align: left; padding-left: 30px;
            }
            QPushButton:hover { border-color: #1e6fff; background-color: #f8faff; }
        """)
        btn_offline.clicked.connect(self.enter_offline_mode)

        btn_online = QPushButton("在线模式\n多设备全网账号云端登录，同步数据")
        btn_online.setFixedSize(450, 95)
        btn_online.setStyleSheet("""
            QPushButton {
                background-color: white; border: 2px solid #e4e7ed; border-radius: 12px;
                font-size: 18px; font-weight: bold; color: #2c3e50; text-align: left; padding-left: 30px;
            }
            QPushButton:hover { border-color: #1e6fff; background-color: #f8faff; }
        """)
        btn_online.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        layout.addWidget(btn_offline)
        layout.addWidget(btn_online)
        self.stacked_widget.addWidget(page)

    # ---------------- 2. 登录与注册卡片界面（带大圆角阴影） ----------------
    def init_login_reg_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QWidget()
        card.setFixedSize(420, 480)
        card.setStyleSheet("background-color: #ffffff; border-radius: 16px;")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(35, 40, 35, 40)

        self.form_stack = QStackedWidget()

        # ----- 2A: 登录卡片 -----
        login_w = QWidget()
        login_l = QVBoxLayout(login_w)
        login_l.setContentsMargins(0, 0, 0, 0)
        login_l.setSpacing(15)

        lbl_l1 = QLabel("账号/手机号")
        lbl_l1.setStyleSheet("font-weight: bold; font-size: 15px; color: #515a6e;")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("输入手机号")

        lbl_l2 = QLabel("密码")
        lbl_l2.setStyleSheet("font-weight: bold; font-size: 15px; color: #515a6e;")
        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("输入密码")
        self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.remember_cb = QCheckBox("记住密码自动填")
        self.remember_cb.setStyleSheet("color: #7f8c8d; font-size: 14px;")

        btn_login = QPushButton("全网云端登录")
        btn_login.setObjectName("blueBtn")
        btn_login.clicked.connect(self.handle_login)

        bottom_links = QHBoxLayout()
        btn_back = QPushButton("← 返回首页", self)
        btn_back.setObjectName("linkBtn")
        btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        btn_go_reg = QPushButton("注册全网新账号", self)
        btn_go_reg.setObjectName("linkBtn")
        btn_go_reg.clicked.connect(lambda: self.form_stack.setCurrentIndex(1))
        bottom_links.addWidget(btn_back)
        bottom_links.addStretch()
        bottom_links.addWidget(btn_go_reg)

        login_l.addWidget(lbl_l1)
        login_l.addWidget(self.phone_input)
        login_l.addWidget(lbl_l2)
        login_l.addWidget(self.pwd_input)
        login_l.addWidget(self.remember_cb)
        login_l.addSpacing(5)
        login_l.addWidget(btn_login)
        login_l.addLayout(bottom_links)

        # ----- 2B: 注册卡片 -----
        reg_w = QWidget()
        reg_l = QVBoxLayout(reg_w)
        reg_l.setContentsMargins(0, 0, 0, 0)
        reg_l.setSpacing(12)

        lbl_r1 = QLabel("设置手机号/账号")
        lbl_r1.setStyleSheet("font-weight: bold; color: #515a6e;")
        self.reg_phone = QLineEdit()
        self.reg_phone.setPlaceholderText("作为后续跨设备登录账号")

        lbl_r2 = QLabel("设置密码")
        lbl_r2.setStyleSheet("font-weight: bold; color: #515a6e;")
        self.reg_pwd = QLineEdit()
        self.reg_pwd.setPlaceholderText("密码不少于6位")
        self.reg_pwd.setEchoMode(QLineEdit.EchoMode.Password)

        lbl_r3 = QLabel("确认密码")
        lbl_r3.setStyleSheet("font-weight: bold; color: #515a6e;")
        self.reg_pwd_confirm = QLineEdit()
        self.reg_pwd_confirm.setPlaceholderText("再次输入密码以验证")
        self.reg_pwd_confirm.setEchoMode(QLineEdit.EchoMode.Password)

        btn_reg_submit = QPushButton("注册并自动云同步")
        btn_reg_submit.setObjectName("blueBtn")
        btn_reg_submit.setStyleSheet("background-color: #2ed573;")
        btn_reg_submit.clicked.connect(self.handle_register)

        btn_to_login = QPushButton("已有账号？直接登录", self)
        btn_to_login.setObjectName("linkBtn")
        btn_to_login.clicked.connect(lambda: self.form_stack.setCurrentIndex(0))

        reg_l.addWidget(lbl_r1)
        reg_l.addWidget(self.reg_phone)
        reg_l.addWidget(lbl_r2)
        reg_l.addWidget(self.reg_pwd)
        reg_l.addWidget(lbl_r3)
        reg_l.addWidget(self.reg_pwd_confirm)
        reg_l.addSpacing(5)
        reg_l.addWidget(btn_reg_submit)
        reg_l.addWidget(btn_to_login, alignment=Qt.AlignmentFlag.AlignRight)

        self.form_stack.addWidget(login_w)
        self.form_stack.addWidget(reg_w)
        card_layout.addWidget(self.form_stack)

        layout.addWidget(card)
        self.stacked_widget.addWidget(page)

    # ---------------- 3. 统一主功能界面（左收纳侧边栏 + 右主工作区） ----------------
    def init_main_page(self):
        page = QWidget()
        layout = QHBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        sidebar = QWidget()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet("background-color: #ffffff; border-right: 1px solid #e4e7ed;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)

        logo_title = QLabel("萝卜科技")
        logo_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1e6fff; margin-bottom: 2px;")
        self.user_label = QLabel("")
        self.user_label.setStyleSheet("font-size: 14px; color: #7f8c8d; margin-bottom: 15px;")
        sidebar_layout.addWidget(logo_title)
        sidebar_layout.addWidget(self.user_label)

        self.sidebar_menu = QListWidget()
        self.sidebar_menu.setObjectName("sidebarMenu")
        sidebar_layout.addWidget(self.sidebar_menu)
        sidebar_layout.addStretch()

        # 【云同步版本检查控制块】
        btn_version_check = QPushButton("🚀 检查云端新源码")
        btn_version_check.setStyleSheet("""
            QPushButton { background-color: #ffa502; color: white; font-weight: bold; border-radius: 6px; padding: 8px; margin-bottom: 6px; }
            QPushButton:hover { background-color: #ffb123; }
        """)
        btn_version_check.clicked.connect(self.handle_one_click_update)
        sidebar_layout.addWidget(btn_version_check)

        btn_logout = QPushButton("↩ 退出当前模式")
        btn_logout.setStyleSheet("""
            QPushButton { background-color: #fdf0f0; color: #ff4d4f; border: 1px solid #ffa39e; border-radius: 6px; padding: 10px; font-weight: bold;}
            QPushButton:hover { background-color: #ff4d4f; color: white; }
        """)
        btn_logout.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        sidebar_layout.addWidget(btn_logout)

        self.content_stack = QStackedWidget()

        # 挂载三大功能板块
        self.create_notebook_module()  # 0: 笔记本
        self.create_webview_module()  # 1: GESP刷题网页
        self.create_compiler_module()  # 2: 独立多语种编译器环境

        layout.addWidget(sidebar)
        layout.addWidget(self.content_stack)
        self.stacked_widget.addWidget(page)

    # ------ 📁 功能子板块 A: 原版可双击改名笔记本 ------
    def create_notebook_module(self):
        main_w = QWidget()
        layout = QHBoxLayout(main_w)
        layout.setContentsMargins(15, 15, 15, 15)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        left_box = QWidget()
        left_vbox = QVBoxLayout(left_box)
        left_vbox.setContentsMargins(0, 0, 0, 0)

        bar_layout = QHBoxLayout()
        bar_title = QLabel("笔记本")
        bar_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1c1f23;")
        bar_layout.addWidget(bar_title)
        bar_layout.addStretch()

        btn_refresh = QPushButton("⟳")
        btn_new_folder = QPushButton("📁+")
        btn_new_file = QPushButton("📄+")

        mini_style = "QPushButton { background-color: transparent; font-size: 16px; color: #515a6e; max-width: 30px; padding: 2px; } QPushButton:hover { color: #1e6fff; }"
        for btn in [btn_refresh, btn_new_folder, btn_new_file]:
            btn.setStyleSheet(mini_style)

        btn_new_folder.clicked.connect(self.notebook_add_folder)
        btn_new_file.clicked.connect(self.notebook_add_file)

        bar_layout.addWidget(btn_refresh)
        bar_layout.addWidget(btn_new_folder)
        bar_layout.addWidget(btn_new_file)
        left_vbox.addLayout(bar_layout)

        self.note_tree = QTreeWidget()
        self.note_tree.setHeaderHidden(True)
        self.note_tree.setEditTriggers(QTreeWidget.EditTrigger.DoubleClicked)
        self.note_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.note_tree.customContextMenuRequested.connect(self.show_notebook_right_menu)
        self.note_tree.itemClicked.connect(self.handle_notebook_item_click)
        self.note_tree.itemChanged.connect(self.handle_notebook_rename_save)
        left_vbox.addWidget(self.note_tree)

        demo_dir = QTreeWidgetItem(self.note_tree, ["我的第一本错题集"])
        demo_dir.setFlags(demo_dir.flags() | Qt.ItemFlag.ItemIsEditable)
        demo_dir.setData(0, Qt.ItemDataRole.UserRole, "folder")

        right_box = QWidget()
        right_vbox = QVBoxLayout(right_box)
        right_vbox.setContentsMargins(0, 0, 0, 0)

        self.editor_header_lbl = QLabel("选择一篇本地笔记开始高效记录吧...")
        self.editor_header_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #1e6fff; padding-bottom: 5px;")

        self.note_editor = QTextEdit()
        self.note_editor.setPlaceholderText("在这里记录你的错题分析、核心思路或代码段...")
        self.note_editor.textChanged.connect(self.auto_save_note_typing)

        right_vbox.addWidget(self.editor_header_lbl)
        right_vbox.addWidget(self.note_editor)

        splitter.addWidget(left_box)
        splitter.addWidget(right_box)
        splitter.setSizes([320, 850])

        layout.addWidget(splitter)
        self.content_stack.addWidget(main_w)

    def show_notebook_right_menu(self, pos):
        item = self.note_tree.itemAt(pos)
        if not item: return
        menu = QMenu(self)
        act_rename = QAction("📝 重命名 (或双击名称)", self)
        act_delete = QAction("🗑️ 彻底删除", self)

        act_rename.triggered.connect(lambda: self.note_tree.editItem(item, 0))
        act_delete.triggered.connect(lambda: self.handle_notebook_delete(item))

        menu.addAction(act_rename)
        menu.addAction(act_delete)
        menu.exec(self.note_tree.mapToGlobal(pos))

    def notebook_add_folder(self):
        curr = self.note_tree.currentItem()
        parent = curr if curr and curr.data(0, Qt.ItemDataRole.UserRole) == "folder" else self.note_tree
        item = QTreeWidgetItem(parent, ["新文件夹"])
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        item.setData(0, Qt.ItemDataRole.UserRole, "folder")
        if curr: self.note_tree.expandItem(curr)

    def notebook_add_file(self):
        curr = self.note_tree.currentItem()
        parent = curr if curr and curr.data(0, Qt.ItemDataRole.UserRole) == "folder" else self.note_tree
        item = QTreeWidgetItem(parent, ["未命名笔记"])
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        item.setData(0, Qt.ItemDataRole.UserRole, "file")
        if curr: self.note_tree.expandItem(curr)
        self.note_tree.setCurrentItem(item)
        self.handle_notebook_item_click(item, 0)

    def handle_notebook_item_click(self, item, col):
        if item.data(0, Qt.ItemDataRole.UserRole) == "file":
            self.note_editor.setEnabled(True)
            self.editor_header_lbl.setText(f"📝 正在编辑: {item.text(0)}")
            data = self.settings.value(f"cloud_notes/{item.text(0)}", "", type=str)
            self.note_editor.blockSignals(True)
            self.note_editor.setHtml(data)
            self.note_editor.blockSignals(False)
            self.old_active_name = item.text(0)
        else:
            self.note_editor.setDisabled(True)
            self.editor_header_lbl.setText("📁 选中了目录树文件夹")

    def handle_notebook_rename_save(self, item, col):
        if item.data(0, Qt.ItemDataRole.UserRole) == "file" and hasattr(self, 'old_active_name'):
            new_name = item.text(0)
            if new_name != self.old_active_name:
                old_val = self.settings.value(f"cloud_notes/{self.old_active_name}", "", type=str)
                self.settings.setValue(f"cloud_notes/{new_name}", old_val)
                self.settings.remove(f"cloud_notes/{self.old_active_name}")
                self.old_active_name = new_name
                self.editor_header_lbl.setText(f"📝 正在编辑: {new_name}")

    def auto_save_note_typing(self):
        item = self.note_tree.currentItem()
        if item and item.data(0, Qt.ItemDataRole.UserRole) == "file":
            self.settings.setValue(f"cloud_notes/{item.text(0)}", self.note_editor.toHtml())

    def handle_notebook_delete(self, item):
        if item.data(0, Qt.ItemDataRole.UserRole) == "file":
            self.settings.remove(f"cloud_notes/{item.text(0)}")
        parent = item.parent()
        if parent:
            parent.removeChild(item)
        else:
            self.note_tree.takeTopLevelItem(self.note_tree.indexOfTopLevelItem(item))
        self.note_editor.clear()
        self.note_editor.setDisabled(True)

    # ------ 🏆 功能子板块 B: GESP 刷题 ------
    def create_webview_module(self):
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl("http://oj.quxuexi.club/home"))
        self.content_stack.addWidget(self.web_view)

        # ------ 💻 功能子板块 C: 我的项目开发环境 ------

    def create_compiler_module(self):
        main_w = QWidget()
        layout = QVBoxLayout(main_w)
        layout.setContentsMargins(10, 10, 10, 10)

        top_bar = QHBoxLayout()
        lbl_switch = QLabel("选择开发语言环境:")
        lbl_switch.setStyleSheet("font-weight: bold; font-size: 16px; color: #1e6fff;")

        self.lang_box = QComboBox()
        self.lang_box.addItems(["Scratch 编程内核", "Python 在线开发环境", "C++ 竞赛编译系统"])
        self.lang_box.setFixedWidth(280)
        self.lang_box.currentIndexChanged.connect(lambda idx: self.compiler_stack.setCurrentIndex(idx))

        top_bar.addWidget(lbl_switch)
        top_bar.addWidget(self.lang_box)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        self.compiler_stack = QStackedWidget()

        self.web_scratch = QWebEngineView()
        self.web_scratch.setUrl(QUrl("https://scratch.stem86.com/index.html"))

        self.web_python = QWebEngineView()
        self.web_python.setUrl(QUrl("https://python.stem86.com/"))

        self.web_cpp = QWebEngineView()
        self.web_cpp.setUrl(QUrl("https://ce.stem86.com/"))

        self.compiler_stack.addWidget(self.web_scratch)
        self.compiler_stack.addWidget(self.web_python)
        self.compiler_stack.addWidget(self.web_cpp)

        layout.addWidget(self.compiler_stack)
        self.content_stack.addWidget(main_w)

        # ---------------- 🚀 核心工作模式与业务引擎控制 ----------------

    def enter_offline_mode(self):
        self.is_online_mode = False
        self.user_label.setText("👤 模式: [本地离线访客]")

        self.sidebar_menu.blockSignals(True)
        self.sidebar_menu.clear()

        item_note = QListWidgetItem("📖 笔记本")
        item_note.setData(Qt.ItemDataRole.UserRole, 0)
        item_comp = QListWidgetItem("💻 我的项目")
        item_comp.setData(Qt.ItemDataRole.UserRole, 2)

        self.sidebar_menu.addItem(item_note)
        self.sidebar_menu.addItem(item_comp)
        self.sidebar_menu.blockSignals(False)

        try:
            self.sidebar_menu.currentRowChanged.disconnect()
        except:
            pass
        self.sidebar_menu.currentRowChanged.connect(self.handle_sidebar_switch)
        self.sidebar_menu.setCurrentRow(0)
        self.stacked_widget.setCurrentIndex(2)

    def enter_online_mode(self, account_phone):
        self.is_online_mode = True
        self.user_label.setText(f"🟢 云端已连接: @{account_phone}")

        self.sidebar_menu.blockSignals(True)
        self.sidebar_menu.clear()

        item_note = QListWidgetItem("📖 笔记本")
        item_note.setData(Qt.ItemDataRole.UserRole, 0)
        item_gesp = QListWidgetItem("🏆 GESP 刷题")
        item_gesp.setData(Qt.ItemDataRole.UserRole, 1)
        item_comp = QListWidgetItem("💻 我的项目")
        item_comp.setData(Qt.ItemDataRole.UserRole, 2)

        self.sidebar_menu.addItem(item_note)
        self.sidebar_menu.addItem(item_gesp)
        self.sidebar_menu.addItem(item_comp)
        self.sidebar_menu.blockSignals(False)

        try:
            self.sidebar_menu.currentRowChanged.disconnect()
        except:
            pass
        self.sidebar_menu.currentRowChanged.connect(self.handle_sidebar_switch)
        self.sidebar_menu.setCurrentRow(0)
        self.stacked_widget.setCurrentIndex(2)

    def handle_sidebar_switch(self, row):
        if row < 0: return
        target_idx = self.sidebar_menu.item(row).data(Qt.ItemDataRole.UserRole)
        self.content_stack.setCurrentIndex(target_idx)

    # 🔗 业务逻辑改写：对接 GitHub 实现全网云登录验证
    def handle_login(self):
        phone = self.phone_input.text().strip()
        pwd = self.pwd_input.text().strip()
        if not phone or not pwd:
            QMessageBox.warning(self, "信息提示", "手机号或验证密码不能为空！")
            return

        # 联网请求共享数据库
        cloud_db = self.fetch_cloud_users_db()
        encrypted_pwd = self.encrypt_password(pwd)

        if phone in cloud_db and cloud_db[phone] == encrypted_pwd:
            if self.remember_cb.isChecked():
                self.settings.setValue("user_p", phone)
                self.settings.setValue("user_w", pwd)
                self.settings.setValue("user_r", True)
            else:
                self.settings.remove("user_p")
                self.settings.remove("user_w")
                self.settings.setValue("user_r", False)
            self.enter_online_mode(phone)
        else:
            QMessageBox.critical(self, "登录失败",
                                 "该手机号未注册或密码不正确（由于您正处于在线模式，请确保您的GitHub配置与网络正常）。")

    # 🔗 业务逻辑改写：注册后直接安全推送到 GitHub 共享云端
    def handle_register(self):
        phone = self.reg_phone.text().strip()
        pwd = self.reg_pwd.text().strip()
        pwd_c = self.reg_pwd_confirm.text().strip()

        if len(phone) < 5:  # 允许字母或短数字账户
            QMessageBox.warning(self, "校验提示", "请输入有效的登录账号。")
            return
        if len(pwd) < 6:
            QMessageBox.warning(self, "校验提示", "为了安全，新密码长度请勿低于6位。")
            return
        if pwd != pwd_c:
            QMessageBox.warning(self, "校验提示", "两次输入的密码不一致，请核对。")
            return

        # 拉取当前云端最新的数据进行查重
        cloud_db = self.fetch_cloud_users_db()
        if phone in cloud_db:
            QMessageBox.warning(self, "校验提示", "该账号在全网已存在，无需重复注册。")
            return

        # 追加新用户数据
        cloud_db[phone] = self.encrypt_password(pwd)

        # 上传写回云端
        if self.upload_users_db_to_cloud(cloud_db):
            QMessageBox.information(self, "注册成功", "新用户已同步到全网云端数据库！系统已为您自动登录。")
            self.form_stack.setCurrentIndex(0)
            self.enter_online_mode(phone)
        else:
            QMessageBox.critical(self, "同步失败", "云端数据库写入失败，请检查您的 GitHub Token 是否具有 repo 读写权限。")

    # 🔗 业务逻辑改写：检查更新按钮同步接入 GitHub 真实环境
    def handle_one_click_update(self):
        version_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/version.json"
        try:
            resp = requests.get(version_url, timeout=4)
            if resp.status_code == 200:
                cloud_data = resp.json()
                cloud_version = cloud_data.get("version", "v1.0.0")
                if cloud_version > CURRENT_VERSION:
                    reply = QMessageBox.question(
                        self, "检测到新源码发布！",
                        f"当前代码版本: {CURRENT_VERSION}\n云端最新版本: {cloud_version}\n\n更新日志:\n{cloud_data.get('log', '无')}\n\n是否执行全自动源码热覆盖升级？",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    if reply == QMessageBox.StandardButton.Yes:
                        self.check_github_source_update()
                else:
                    QMessageBox.information(self, "检查更新", f"当前源码已是最新版本 ({CURRENT_VERSION})，无需更新。")
            else:
                QMessageBox.warning(self, "检查更新", "未能成功连接到 GitHub 获取版本文件，请检查您的仓库配置。")
        except Exception as e:
            QMessageBox.critical(self, "网络异常", f"无法连接到 GitHub：{e}")

    def load_saved_credentials(self):
        if self.settings.value("user_r", type=bool):
            self.phone_input.setText(self.settings.value("user_p", type=str))
            self.pwd_input.setText(self.settings.value("user_w", type=str))
            self.remember_cb.setChecked(True)


if __name__ == "__main__":
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    client = LuoboStudentClient()
    client.show()
    sys.exit(app.exec())