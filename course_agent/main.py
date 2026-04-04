import json
import time
import threading
from datetime import datetime

# 课程数据文件
DATA_FILE = "courses.json"

# 周几映射
WEEKDAY_MAP = {
    "周一": 0, "一": 0,
    "周二": 1, "二": 1,
    "周三": 2, "三": 2,
    "周四": 3, "四": 3,
    "周五": 4, "五": 4,
    "周六": 5, "六": 5,
    "周日": 6, "日": 6,
    "monday": 0, "mon": 0,
    "tuesday": 1, "tue": 1,
    "wednesday": 2, "wed": 2,
    "thursday": 3, "thu": 3,
    "friday": 4, "fri": 4,
    "saturday": 5, "sat": 5,
    "sunday": 6, "sun": 6
}

WEEKDAY_LIST = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

# 加载课程
def load_courses():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

# 保存课程
def save_courses(courses):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)

# 添加课程
def add_course(name, time_str, place):
    courses = load_courses()
    courses.append({
        "name": name,
        "time": time_str,
        "place": place
    })
    save_courses(courses)
    return True

# 查询所有课程
def query_courses(day=None):
    courses = load_courses()
    if day:
        day = day.strip()
        return [c for c in courses if day in c["time"]]
    return courses

# 删除课程
def delete_course(name):
    courses = load_courses()
    new_courses = [c for c in courses if c["name"] != name]
    save_courses(new_courses)
    return len(new_courses) < len(courses)

# 提醒线程
def remind_task(course_name, course_time, course_place):
    print(f"[提醒已设置] {course_name} | {course_time} | {course_place}")
    while True:
        now = datetime.now().strftime("%H:%M")
        if now in course_time:
            print(f"\n==================================================")
            print(f"🔔 课程提醒：{course_name} 即将开始！")
            print(f"   时间：{course_time}")
            print(f"   地点：{course_place}")
            print(f"==================================================\n")
            break
        time.sleep(60)

# 设置提醒
def set_remind(name, time_str, place):
    threading.Thread(target=remind_task, args=(name, time_str, place), daemon=True).start()

# 获取今天是周几
def get_today_weekday():
    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    return weekday[datetime.now().weekday()]

# 从文本中提取周几信息
def extract_weekday_from_text(text):
    """从用户输入文本中提取周几信息"""
    for key in WEEKDAY_MAP.keys():
        if key in text:
            return WEEKDAY_LIST[WEEKDAY_MAP[key]]
    return None

# 查询指定周几的课程
def query_courses_by_weekday(weekday):
    """查询指定周几的所有课程"""
    courses = load_courses()
    weekday_courses = []
    for c in courses:
        if weekday in c["time"]:
            weekday_courses.append(c)
    return sorted(weekday_courses, key=lambda x: x["time"])

# 获取今天是周几
def get_today_weekday():
    return WEEKDAY_LIST[datetime.now().weekday()]

# 获取当前时间
def get_now_time():
    return datetime.now().strftime("%H:%M")

# 自动查询今天的课表
def get_today_courses():
    today = get_today_weekday()
    courses = load_courses()
    today_courses = []
    for c in courses:
        if today in c["time"]:
            today_courses.append(c)
    today_courses.sort(key=lambda x: x["time"])
    return today_courses

# 简易意图识别（模拟AI）
def intent_recognize(text):
    """识别用户的意图"""
    # 检查是否是查询某周课程的问题（优先级最高）
    weekday = extract_weekday_from_text(text)
    if weekday and any(word in text for word in ["有课", "有没有", "几点", "什么", "吗", "课"]):
        return "ask_weekday"
    
    text_lower = text.replace(" ", "").lower()
    
    # 添加课程
    if any(word in text for word in ["添加", "新增"]) or "add" in text_lower:
        return "add"
    # 查询全部课程
    elif any(word in text for word in ["查询", "看", "全部", "列表"]) or "query" in text_lower or "all" in text_lower:
        return "query"
    # 删除课程
    elif any(word in text for word in ["删除", "移除"]) or "delete" in text_lower or "remove" in text_lower:
        return "delete"
    else:
        return "unknown"

# 主程序
def main():
    # 自动获取时间、周几、今日课表
    now_time = get_now_time()
    today = get_today_weekday()
    today_courses = get_today_courses()

    print("=" * 50)
    print("        课程智能提醒助手 Agent（能说会做）")
    print("=" * 50)
    print(f"📅 当前日期：{today}    🕒 当前时间：{now_time}")
    print("=" * 50)

    # 自动展示今日课表
    print(f"📚【{today} 今日课表】")
    if not today_courses:
        print("   今天没有课！🎉")
    else:
        for i, c in enumerate(today_courses, 1):
            print(f"   {i}. {c['name']} | {c['time']} | {c['place']}")
    print("=" * 50)
    print("支持指令：添加课程 | 查询课程 | 删除课程")
    print("=" * 50)
    
    while True:
        user_input = input("\n你：")
        intent = intent_recognize(user_input)

        # 处理查询某周课程的请求
        if intent == "ask_weekday":
            weekday = extract_weekday_from_text(user_input)
            if weekday:
                courses = query_courses_by_weekday(weekday)
                if courses:
                    print(f"\nAI：有啦！😊 {weekday}有以下课程：")
                    for i, c in enumerate(courses, 1):
                        print(f"   {i}. {c['name']} | {c['time']} | {c['place']}")
                else:
                    print(f"\nAI：没有呢~😆 {weekday}没有课！")
            continue

        elif intent == "add":
            print("\nAI：请输入 课程名 时间 地点（空格分隔）")
            info = input("格式示例：高数 周一08:00 A302：").strip().split()
            if len(info) >= 3:
                course_name = info[0]
                course_time = info[1]
                course_place = info[2]
                add_course(course_name, course_time, course_place)
                set_remind(course_name, course_time, course_place)
                print(f"AI：✅ 添加成功：{course_name}")
            continue

        elif intent == "query":
            courses = query_courses()
            if not courses:
                print("AI：📭 暂无课程")
            else:
                print("\nAI：📚 全部课程列表：")
                for i, c in enumerate(courses, 1):
                    print(f"{i}. {c['name']} | {c['time']} | {c['place']}")
            continue

        elif intent == "delete":
            print("\nAI：请输入要删除的课程名称：")
            name = input().strip()
            if delete_course(name):
                print(f"AI：🗑️ 已删除课程：{name}")
            else:
                print(f"AI：❌ 未找到课程：{name}")
            continue

        else:
            print("\nAI：不明白这个指令呢 😅 请试试：")
            print("   • 「周二有课吗」-> 查询周二的课程")
            print("   • 「添加课程」-> 添加新课程")
            print("   • 「查询课程」-> 查看全部课程")
            print("   • 「删除课程」-> 删除指定课程")

if __name__ == "__main__":
    main()
