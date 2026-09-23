from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "android" / "android-platform-features.html"


class AndroidPlatformFeaturesPageTest(unittest.TestCase):
    def test_page_covers_ten_android_platform_features(self):
        html = PAGE.read_text(encoding="utf-8")
        required = [
            "Android 平台核心特性",
            "Activity 生命周期",
            "进程与任务",
            "配置变化",
            "四大组件",
            "Intent",
            "权限模型",
            "主线程与 ANR",
            "资源与屏幕适配",
            "应用沙箱",
            "设备碎片化",
            "onRestart",
            "onResume",
        ]
        for phrase in required:
            self.assertIn(phrase, html)

    def test_page_uses_the_shared_tutorial_layout(self):
        html = PAGE.read_text(encoding="utf-8")
        self.assertIn('class="lead"', html)
        self.assertIn('class="meta"', html)
        self.assertIn('class="summary"', html)
        self.assertIn('../assets/tutorial.css', html)


if __name__ == "__main__":
    unittest.main()
