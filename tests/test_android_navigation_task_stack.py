from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "android" / "activity-navigation-task-stack-launch-modes.html"
DATA = ROOT / "assets" / "patterns-data.js"
PROGRESS = ROOT / "learning-progress.md"


class AndroidNavigationTaskStackPageTest(unittest.TestCase):
    def test_page_covers_task_stack_and_launch_modes(self):
        html = PAGE.read_text(encoding="utf-8")
        required = [
            "页面导航、任务栈与 Activity 启动模式",
            "任务栈",
            "系统维护的一条用户任务与返回路径",
            "通常包含一个或多个按栈管理的 Activity",
            "一个 Task 也可以只有一个 Activity",
            "单 Activity + Navigation",
            "standard",
            "singleTop",
            "singleTask",
            "singleInstance",
            "singleInstancePerTask",
            "onNewIntent",
            "FLAG_ACTIVITY_CLEAR_TOP",
            "FLAG_ACTIVITY_NEW_TASK",
            "单 Activity",
        ]
        for phrase in required:
            self.assertIn(phrase, html)

    def test_page_uses_shared_layout_and_is_registered(self):
        html = PAGE.read_text(encoding="utf-8")
        self.assertIn('class="lead"', html)
        self.assertIn('class="meta"', html)
        self.assertIn('class="summary"', html)
        self.assertIn('../assets/tutorial.css', html)
        self.assertIn('activity-navigation-task-stack-launch-modes.html', DATA.read_text(encoding="utf-8"))
        self.assertIn('activity-navigation-task-stack-launch-modes.html', PROGRESS.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
