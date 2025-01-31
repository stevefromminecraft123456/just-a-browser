import sys
import torch
import torch.nn as nn
import torch.optim as optim
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction, QLineEdit
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QPalette, QColor

# Example PyTorch model for URL classification
class SimpleURLClassifier(nn.Module):
    def __init__(self):
        super(SimpleURLClassifier, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(100, 50),
            nn.ReLU(),
            nn.Linear(50, 2),  # Binary classification (e.g., safe vs. unsafe URL)
            nn.Softmax(dim=1)
        )

    def forward(self, x):
        return self.fc(x)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Setup browser
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://google.com'))
        self.setCentralWidget(self.browser)
        self.setWindowTitle('My Cool Browser')
        self.showMaximized()

        # Load PyTorch model
        self.model = self.load_model()

        # Apply dark mode
        self.apply_dark_mode()

        # Create navigation bar
        self.create_navbar()

    def create_navbar(self):
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Back button
        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        # Forward button
        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        # Reload button
        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        # Home button
        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText('Enter URL and press Enter...')
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Update URL bar when the browser URL changes
        self.browser.urlChanged.connect(self.update_url_bar)

    def apply_dark_mode(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
        dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        QApplication.setPalette(dark_palette)

    def load_model(self):
        # Initialize and load a dummy model (replace with real training/loading code)
        model = SimpleURLClassifier()
        model.eval()  # Set to evaluation mode
        return model

    def navigate_home(self):
        self.browser.setUrl(QUrl('http://programming-hero.com'))

    def navigate_to_url(self):
        url = self.url_bar.text()

        # Add 'http://' prefix if missing
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        # Dummy feature extraction for URL classification
        features = torch.randn(1, 100)  # Replace with real feature extraction
        prediction = self.model(features)
        predicted_label = torch.argmax(prediction, dim=1).item()

        if predicted_label == 1:
            print(f"Navigating to a safe URL: {url}")
        else:
            print(f"Warning: The URL may be unsafe: {url}")

        self.browser.setUrl(QUrl(url))

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Apply dark mode before creating the window
    app.setStyle('Fusion')

    window = MainWindow()
    sys.exit(app.exec_())
