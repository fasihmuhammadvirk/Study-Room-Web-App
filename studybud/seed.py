"""
Seed script: clears all Rooms, Messages, Topics, and JoinRequests,
then creates fresh study rooms and conversations using existing users
plus a new user Shiza Batool.

Run with:
    python seed.py
"""

import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studybud.settings')
django.setup()

from mainapp.models import Room, Message, Topic, JoinRequest, User

# ─── 1. CLEAR ROOMS, MESSAGES, TOPICS, JOIN REQUESTS ───────────────────────
print("Clearing existing rooms, messages, topics and join requests...")
JoinRequest.objects.all().delete()
Message.objects.all().delete()
Room.objects.all().delete()
Topic.objects.all().delete()
print("Done clearing.\n")

# ─── 2. GET OR CREATE SHIZA ─────────────────────────────────────────────────
shiza, created = User.objects.get_or_create(
    email='shiza@gmail.com',
    defaults={
        'username': 'shizabatool',
        'name': 'Shiza Batool',
    }
)
if created:
    shiza.set_password('shiza1234')
    shiza.save()
    print("Created new user: Shiza Batool (shiza@gmail.com / shiza1234)")
else:
    print("User Shiza Batool already exists.")

# ─── 3. LOAD ALL USERS ──────────────────────────────────────────────────────
users = list(User.objects.all())
print(f"\nAll users: {[u.email for u in users]}\n")

# Assign aliases
u0 = User.objects.filter(email='fasih@gmail.com').first() or users[0]
u1 = User.objects.filter(email='fasihmuhammad.virk@gmail.com').first() or users[1]
u2 = User.objects.filter(email='admin@gmail.com').first() or users[2 % len(users)]
u3 = shiza

# ─── 4. CREATE TOPICS ───────────────────────────────────────────────────────
topics_data = [
    "Python Programming",
    "Data Structures & Algorithms",
    "Machine Learning",
    "Web Development",
    "Mathematics",
    "Database Systems",
]
topic_objs = {name: Topic.objects.create(name=name) for name in topics_data}
print(f"Created topics: {list(topic_objs.keys())}\n")

# ─── 5. ROOMS + CONVERSATIONS ───────────────────────────────────────────────
rooms_config = [
    # ── PUBLIC ROOMS ──────────────────────────────────────────────────────────
    {
        "host": u0,
        "topic": "Python Programming",
        "name": "Python Beginners Hub",
        "description": "A welcoming space for Python beginners to ask questions and share resources.",
        "is_private": False,
        "messages": [
            (u0,  "Hey everyone! Welcome to the Python Beginners Hub 🐍 Feel free to ask anything!"),
            (u3,  "Hi! I'm Shiza. I just started learning Python last week and I'm already loving it!"),
            (u1,  "Welcome Shiza! It gets even better. What are you working on right now?"),
            (u3,  "I'm trying to understand list comprehensions. They look really clean but confuse me a bit."),
            (u2,  "List comprehensions are awesome! Try this: `[x**2 for x in range(10)]`"),
            (u3,  "Oh wow that's so much shorter than a for loop. What about filtering?"),
            (u2,  "Add an `if` at the end: `[x for x in range(20) if x % 2 == 0]` — only even numbers!"),
            (u0,  "Exactly! Also check out https://docs.python.org/3/tutorial/datastructures.html"),
            (u3,  "This is so helpful, thank you all! 😊 Can we also cover functions next time?"),
            (u0,  "Absolutely! Drop your questions anytime."),
        ],
    },
    {
        "host": u3,
        "topic": "Data Structures & Algorithms",
        "name": "DSA Grind Room",
        "description": "Daily LeetCode and HackerRank problem solving. Share solutions, discuss approaches.",
        "is_private": False,
        "messages": [
            (u3,  "Good morning everyone! I created this room for daily DSA practice 💪"),
            (u0,  "Great idea Shiza! What's today's problem?"),
            (u3,  "Two Sum on LeetCode — classic one. Anyone solve it already?"),
            (u1,  "Yes! O(n) using a hashmap — store complement as you iterate through the array."),
            (u2,  "I did brute force O(n²) first then optimised. Hashmap is definitely the way to go."),
            (u3,  "I tried brute force too 😅 Can you walk through the hashmap approach?"),
            (u1,  "Sure! For each number, check if `target - num` is already in your map. If yes, return indices. If no, add `num` to map."),
            (u3,  "Ohh that makes it so clear. I'll implement it now!"),
            (u0,  "Don't forget edge cases — like negative numbers and zeros."),
            (u3,  "Good point! I'll add test cases for those. Tomorrow let's do Binary Search?"),
            (u1,  "I'm in! I always mess up the `left <= right` vs `left < right` boundary."),
        ],
    },
    {
        "host": u1,
        "topic": "Machine Learning",
        "name": "ML Paper Reading Club",
        "description": "We read and discuss one ML paper per week. This week: Attention Is All You Need.",
        "is_private": False,
        "messages": [
            (u1,  "This week we're reading 'Attention Is All You Need' 📄 https://arxiv.org/abs/1706.03762"),
            (u3,  "I've heard about Transformers but never read the original paper. Excited!"),
            (u2,  "The idea of replacing RNNs entirely with attention is wild when you first see it."),
            (u3,  "Can someone explain the multi-head attention part? I read it twice and still feel lost."),
            (u0,  "Think of it like looking at a sentence from multiple perspectives simultaneously — each 'head' captures different types of relationships."),
            (u3,  "Oh that's a great analogy! So one head might focus on grammar and another on context?"),
            (u1,  "Exactly! That's the intuition."),
            (u2,  "What about positional encoding? Why do we need it?"),
            (u3,  "I was going to ask that too!"),
            (u0,  "Because attention is permutation-invariant — it has no sense of word order by default. Positional encoding injects position info."),
            (u3,  "So without it 'cat sat on mat' and 'mat on sat cat' look identical to the model? 😂"),
            (u1,  "Haha exactly! Great insight Shiza. Next week: BERT!"),
        ],
    },
    {
        "host": u2,
        "topic": "Web Development",
        "name": "Full Stack Study Group",
        "description": "Learning React, Django REST, and deployment. Beginners to intermediate welcome.",
        "is_private": False,
        "messages": [
            (u2,  "Welcome to the Full Stack Study Group! Who's working on what this week?"),
            (u3,  "I'm building a personal portfolio with React. First time using it!"),
            (u0,  "Nice! Are you using Create React App or Vite?"),
            (u3,  "Create React App for now. Should I switch?"),
            (u1,  "Vite is much faster for dev builds. Worth switching early before your project gets big."),
            (u3,  "I'll try Vite for my next project then. Also, I'm confused by useEffect — when does it run?"),
            (u0,  "It runs after every render by default. Pass `[]` as second arg to run only on mount."),
            (u3,  "That makes sense! And cleanup — I keep getting memory leak warnings."),
            (u2,  "Return a function from useEffect: `return () => clearInterval(timer);`"),
            (u3,  "Ohh! That's what the cleanup function is for. Thank you Fasih!"),
            (u0,  "On the backend side, are you using Django REST Framework or something else?"),
            (u3,  "We're using Django for our university project — StudyBuddy actually!"),
        ],
    },
    {
        "host": u0,
        "topic": "Mathematics",
        "name": "Linear Algebra for ML",
        "description": "Reviewing vectors, matrices, eigenvalues and their applications in machine learning.",
        "is_private": False,
        "messages": [
            (u0,  "Today: matrix multiplication and why it matters for ML. Let's start with the basics."),
            (u3,  "I struggle with matrices so much in my Linear Algebra course 😭 glad this room exists."),
            (u1,  "Same! Can you explain why AB ≠ BA in general?"),
            (u2,  "Think geometrically — rotate then scale gives a different result than scale then rotate."),
            (u3,  "Oh! So order of transformation matters. That's a great way to think about it."),
            (u0,  "Exactly. Now eigenvalues — who can explain them intuitively?"),
            (u3,  "I know eigenvalues from class but I don't really *get* them."),
            (u2,  "An eigenvector is a direction that doesn't change when a transformation is applied — it only gets scaled by the eigenvalue."),
            (u3,  "So eigenvalue = how much stretching happens in that direction?"),
            (u1,  "Yes! And PCA uses this to find directions of maximum variance in your data."),
            (u3,  "This is finally clicking 🧠 Thank you everyone!"),
        ],
    },
    # ── PRIVATE ROOM ──────────────────────────────────────────────────────────
    {
        "host": u3,
        "topic": "Database Systems",
        "name": "DB Final Exam Prep (Private)",
        "description": "Private group for our class preparing for the Database Systems final. Members only.",
        "is_private": True,
        "messages": [
            (u3,  "Hey team! I created this private room for our DB final exam prep 🗂️"),
            (u0,  "Great idea Shiza! When is the exam?"),
            (u3,  "Two weeks from now. I'll share my normalization notes here today."),
            (u1,  "Can we cover indexing and query optimization? That's always heavy in the exam."),
            (u3,  "Definitely adding that to the list. Also ACID properties — prof loves asking about those."),
            (u2,  "I have a cheat sheet for ACID. Will post it tomorrow."),
            (u0,  "Also the difference between clustered vs non-clustered indexes is a common exam question."),
            (u3,  "Adding that too! I'll put together a practice question set by Thursday."),
            (u1,  "Perfect. Should we do a group study session on Sunday?"),
            (u3,  "Sunday at 3pm works for me! I'll prepare the SQL query optimization section."),
            (u2,  "I'm in. See everyone then 🙌"),
            (u0,  "Same. Good luck everyone! We've got this 💪"),
        ],
    },
]

# ─── 6. INSERT ───────────────────────────────────────────────────────────────
for cfg in rooms_config:
    topic = topic_objs[cfg["topic"]]
    room = Room.objects.create(
        host=cfg["host"],
        topic=topic,
        name=cfg["name"],
        description=cfg["description"],
        is_private=cfg["is_private"],
    )
    privacy_label = "🔒 PRIVATE" if cfg["is_private"] else "🌐 PUBLIC"
    print(f"  [{privacy_label}] {room.name}")

    for author, body in cfg["messages"]:
        Message.objects.create(user=author, room=room, body=body)
        room.participants.add(author)

    print(f"    → {len(cfg['messages'])} messages, {room.participants.count()} participants")

print("\n✅ Seeding complete!")
print(f"   Rooms:    {Room.objects.count()}")
print(f"   Topics:   {Topic.objects.count()}")
print(f"   Messages: {Message.objects.count()}")
print(f"   Users:    {User.objects.count()}")
