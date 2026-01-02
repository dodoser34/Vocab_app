from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QConicalGradient
from project.app.logic.stats_logic import get_training_stats, get_streaks
from project.app.logic.settings_logic import get_settings
from project.app.logic.translations.translations import t

# ------------------ Круговой прогресс с плавным градиентом ------------------
class CircularProgress(QWidget):
    def __init__(self, value=0, size=150):
        super().__init__()
        self.value = max(0, min(100, value))
        self.size = size
        self.setFixedSize(self.size, self.size)

    def setValue(self, value):
        self.value = max(0, min(100, value))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        thickness = 15
        rect = self.rect().adjusted(thickness//2, thickness//2, -thickness//2, -thickness//2)

        # фон круга
        painter.setPen(QPen(QColor("#1f1f1f"), thickness))
        painter.drawEllipse(rect)

        # градиент от красного -> желтый -> зеленый
        center = QPointF(rect.center().x(), rect.center().y())
        gradient = QConicalGradient(center, -90)

        # Пропорции цвета по значению
        val_ratio = self.value / 100
        # градиент плавно от красного через желтый к зеленому
        gradient.setColorAt(0.0, QColor(255, 0, 0))
        gradient.setColorAt(0.5, QColor(255, 255, 0))
        gradient.setColorAt(1.0, QColor(0, 255, 0))

        pen = QPen()
        pen.setWidth(thickness)
        pen.setBrush(gradient)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        span_angle = int(-self.value * 16 * 3.6)
        painter.drawArc(rect, 90 * 16, span_angle)

        # текст в центре
        painter.setPen(QColor("white"))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{self.value}%")

# ------------------ Визуализатор стрика ------------------
class StreakVisualizer(QWidget):
    def __init__(self, current=0, max_streak=10, size=20, spacing=5):
        super().__init__()
        self.current = current
        self.max_streak = max_streak
        self.size = size
        self.spacing = spacing
        self.setFixedHeight(self.size + 10)

    def setStreak(self, current, max_streak=None):
        self.current = current
        if max_streak:
            self.max_streak = max_streak
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        total_width = self.max_streak * self.size + (self.max_streak - 1) * self.spacing
        start_x = (self.width() - total_width) / 2

        for i in range(self.max_streak):
            if i < self.current:
                factor = (i + 1) / max(1, self.max_streak)
                # градиент плавный от красного -> желтый -> зеленый
                if factor < 0.5:
                    r = 255
                    g = int(255 * (factor / 0.5))
                else:
                    r = int(255 * (1 - (factor - 0.5)/0.5))
                    g = 255
                color = QColor(r, g, 0)
            else:
                color = QColor(60, 60, 60)
            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)
            x = start_x + i * (self.size + self.spacing)
            painter.drawRoundedRect(int(x), 0, self.size, self.size, 5, 5)

# ------------------ Экран статистики ------------------
class StatsScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setStyleSheet("background:#232323; color:white;")
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # заголовок
        self.title = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size:28px; background:#2b2b2b; padding:15px; border-radius:20px;")
        self.layout.addWidget(self.title)

        # средняя точность
        self.avg_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.avg_label.setStyleSheet("font-size:22px; padding:10px;")
        self.layout.addWidget(self.avg_label)
        self.avg_progress = CircularProgress()
        self.layout.addWidget(self.avg_progress, alignment=Qt.AlignmentFlag.AlignCenter)

        # стрик
        self.streak_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.streak_label.setStyleSheet("font-size:22px; padding:10px;")
        self.layout.addWidget(self.streak_label)
        self.streak_visual = StreakVisualizer()
        self.layout.addWidget(self.streak_visual)

        # всего дней
        self.total_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.total_label.setStyleSheet("font-size:22px; padding:10px;")
        self.layout.addWidget(self.total_label)
        self.total_progress = CircularProgress(size=120)
        self.layout.addWidget(self.total_progress, alignment=Qt.AlignmentFlag.AlignCenter)

        # кнопка назад
        self.back_btn = QPushButton()
        self.back_btn.setStyleSheet("background:#7b2f2f; border-radius:25px; font-size:22px; color:white; padding:12px;")
        self.back_btn.clicked.connect(self.main.show_menu)
        self.layout.addWidget(self.back_btn)

        self.refresh_ui()
        self.refresh()

    def refresh_ui(self):
        lang = get_settings().get("language", "en")
        self.STRINGS = {
            "title": t(lang, "stats", "title"),
            "average_accuracy": t(lang, "stats", "average_accuracy"),
            "current_streak": t(lang, "stats", "current_streak"),
            "total_days": t(lang, "stats", "total_days"),
            "back": t(lang, "stats", "back"),
        }
        self.title.setText(self.STRINGS["title"])
        self.back_btn.setText(self.STRINGS["back"])

    def refresh(self):
        stats = get_training_stats()
        streaks = get_streaks()

        # средняя точность
        self.avg_label.setText(
            f"{self.STRINGS['average_accuracy']}: {stats['average_percent']}% "
            f"({stats['correct']} ✅ / {stats['incorrect']} ❌)"
        )
        self.avg_progress.setValue(stats['average_percent'])

        # стрик
        current = streaks.get('current_streak', 0)
        streak_history = streaks.get('streak_history') or [current]
        max_streak = max(streak_history)
        self.streak_label.setText(f"{self.STRINGS['current_streak']}: {current}")
        self.streak_visual.setStreak(current, max_streak)

        # всего дней
        total_days = streaks.get('total_days', 0)
        self.total_label.setText(f"{self.STRINGS['total_days']}: {total_days}")
        self.total_progress.setValue(min(total_days, 100))
