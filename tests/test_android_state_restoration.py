from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "android" / "state-saving-restoration.html"
DATA = ROOT / "assets" / "patterns-data.js"
PROGRESS = ROOT / "learning-progress.md"


class AndroidStateRestorationPageTest(unittest.TestCase):
    def test_page_covers_android_state_restoration(self):
        html = PAGE.read_text(encoding="utf-8")
        required = [
            "Android 状态保存与恢复",
            "ViewModel",
            "SavedStateHandle",
            "rememberSaveable",
            "进程被系统回收",
            "配置变化",
            "数据分层",
            "速学路线",
            "Jetpack Compose",
            "协程与 Flow",
            "性能与 ANR",
        ]
        for phrase in required:
            self.assertIn(phrase, html)

    def test_page_is_registered_and_uses_shared_layout(self):
        html = PAGE.read_text(encoding="utf-8")
        self.assertIn('class="lead"', html)
        self.assertIn('class="meta"', html)
        self.assertIn('class="summary"', html)
        self.assertIn('../assets/tutorial.css', html)
        self.assertIn('state-saving-restoration.html', DATA.read_text(encoding="utf-8"))
        self.assertIn('state-saving-restoration.html', PROGRESS.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
