# ShoppingWithAI
AI导购（Shopping Assistant）项目：用户输入 → LangGraph(agent) → (RAG/价格查询/直接回答) → 输出。

## Features (MVP)
- 路由：根据用户问题简单判断走 RAG /价格查询 /直接回答
- RAG：本地 `data/docs.txt` + 向量检索（自动构建索引）
-价格查询：mock价格（可重复，用于演示）
-机型推荐：设备库 + embedding 检索
-直接回答：Qwen `qwen3.5-plus`（DashScope OpenAI兼容接口）

## Environment Setup

###1) Create venv

```bash
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

###2) Install dependencies

```bash
python -m pip install -r requirements.txt
# (optional) editable install for module import
python -m pip install -e .
```

###3) Configure API key

Create `.env` in project root:

```env
DASHSCOPE_API_KEY=你的key
```

## Run

```bash
# CLI
python scripts/run_cli.py
```

## Streamlit UI

```bash
python -m streamlit run app_streamlit.py
```

## Import as module

如果遇到 `ModuleNotFoundError: shopping_with_ai`，请确认已在项目根目录执行：

```bash
python -m pip install -e .
```

然后在代码里这样导入：

```python
from shopping_with_ai.app import run_once
```

## Project Log (from note.md)

### Day1
- Created Spring Boot project with dependencies: Spring Web, Spring Data JPA, MySQL driver, Lombok
- Installed MySQL, created database `mysql94` (password `12356`)
- Tried MySQL Workbench, uninstalled due to UI
- Connected DB via IntelliJ built‑in database tool
- Created DB `myschool`, linked to project
- Created `TestUser` entity, generated table
- Fixed dialect configuration error by removing the line

### Day2
- Removed `TestUser`, created entities: User / Student / Instructor / Course / CourseSection / Enrollment
- Hibernate auto‑created tables and FK relationships
- Viewed tables in IntelliJ DB tool

### Day3
- Added User repository + service (CRUD + business separation)
- Built GUI class with constructor injection and buttons calling services
- Fixed empty table issue by inserting3 test users
- Init GUI in main class with startup logs
- MVC mapping: GUI=View, Service=Controller, Repository=Model

### Day4
- Learned ON DELETE CASCADE + JOIN
- Added cascade annotations on Course / CourseSection / Student / Instructor

### Day5
- Added repositories + services for each entity
- Added GUI screens for enroll/withdraw/view courses, add/delete courses
- Added navigation GUI
- Fixed bugs (typos/imports)
- Added `data` class to reset test data on startup

### Day6
- Added FlatLaf for dark mode UI; fixed theme switch bug via UIManager
- Refactored to Pet School domain:
 - Entities: Pet / Owner / PetInstructor / PetCourse / PetCourseSection / PetEnrollment
 - Rebuilt repositories, services, GUI screens
- Fixed multiple bugs (imports/method changes/typos)
- Cleared residual DB data, re‑seeded clean data

### Day7
- Added Achievements wall + Pet profile
- Added login & role‑based permissions (config + service validation)
- Default entry is login screen
- Fixed guest permission bug in service validation

### Day8
- Translated UI to English
- Added3 images
- Updated `petprofile` and `data.sql` to load images

## Notes
-价格查询为 mock 实现（不依赖外部价格API）：基于 query生成**可重复**的演示价格。
- 向量索引缓存文件会自动生成（已在 .gitignore 中忽略）。
