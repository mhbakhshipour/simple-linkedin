import random

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import User
from messaging.models import Conversation, Message
from posts.models import Post
from profiles.models import Profile
from relationships.models import Follow


class Command(BaseCommand):
    help = "Seed database with Persian demo data"

    @transaction.atomic
    def handle(self, *args, **options):
        Follow.objects.all().delete()
        Message.objects.all().delete()
        Conversation.objects.all().delete()
        Post.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()

        first_names = [
            "علی",
            "مهدی",
            "زهرا",
            "فاطمه",
            "محمد",
            "سارا",
            "رضا",
            "نگار",
            "حسین",
            "مریم",
        ]
        last_names = [
            "رضایی",
            "احمدی",
            "کریمی",
            "حسینی",
            "مرادی",
            "قاسمی",
            "کاظمی",
            "جلالی",
            "محمدی",
            "رحیمی",
        ]
        headlines = [
            "توسعه‌دهنده جنگو",
            "مهندس نرم‌افزار",
            "طراح رابط کاربری",
            "مدیر محصول",
            "برنامه‌نویس پایتون",
            "کارشناس داده",
            "توسعه‌دهنده فرانت‌اند",
            "توسعه‌دهنده بک‌اند",
            "کارآفرین",
            "دانشجوی کامپیوتر",
        ]
        bios = [
            "علاقه‌مند به توسعه وب و یادگیری تکنولوژی‌های جدید.",
            "روی پروژه‌های متن‌باز کار می‌کنم و از همکاری استقبال می‌کنم.",
            "تجربه چند ساله در توسعه نرم‌افزارهای سازمانی.",
            "علاقه‌مند به استارتاپ‌ها و دنیای محصول.",
            "تمرکز روی توسعه با پایتون و جنگو.",
        ]
        post_texts = [
            "امروز روی یک ویژگی جدید در پروژه جنگو کار کردم.",
            "بهترین راه یادگیری برنامه‌نویسی، انجام پروژه‌های واقعی است.",
            "کتابخانه‌های پایتون برای علم داده فوق‌العاده هستند.",
            "امروز یک باگ سخت را بعد از چند ساعت دیباگ کردن پیدا کردم.",
            "به نظر شما آینده توسعه وب به چه سمتی می‌رود؟",
            "از کار با تیم‌های ریموت خیلی لذت می‌برم.",
            "به‌تازگی یک دوره جدید آنلاین را به پایان رساندم.",
            "استفاده از تست خودکار باعث افزایش کیفیت کد می‌شود.",
            "امروز در مورد معماری سرویس‌گرا مطالعه کردم.",
            "آیا شما هم از جنگو در پروژه‌های تولیدی استفاده می‌کنید؟",
        ]
        message_texts = [
            "سلام، حالت چطوره؟",
            "می‌خواستم در مورد پروژه‌ات بیشتر بدونم.",
            "اگر فرصت داشتی خوشحال می‌شم گپی بزنیم.",
            "آیا روی این موضوع تجربه‌ای داری؟",
            "مرسی از اینکه تجربه‌ات را به اشتراک گذاشتی.",
            "این پستت خیلی جالب بود.",
            "در مورد این تکنولوژی چه نظری داری؟",
            "اگر منبع خوبی داری معرفی کن.",
            "موفق باشی.",
            "امیدوارم روز خوبی داشته باشی.",
        ]

        users = []
        for i in range(10):
            email = f"user{i + 1}@user.com"
            user = User.objects.create_user(
                email=email,
                password="1234",
                first_name=first_names[i],
                last_name=last_names[i],
            )
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    "headline": headlines[i],
                    "bio": random.choice(bios),
                },
            )
            users.append(user)

        for user in users:
            count = random.randint(3, 7)
            for _ in range(count):
                Post.objects.create(
                    author=user,
                    body=random.choice(post_texts),
                )

        for follower in users:
            others = [u for u in users if u != follower]
            following_sample = random.sample(others, k=random.randint(2, len(others)))
            for target in following_sample:
                Follow.objects.get_or_create(follower=follower, following=target)

        conversations = []
        for i in range(len(users)):
            for j in range(i + 1, len(users)):
                if random.random() < 0.4:
                    conversation = Conversation.objects.create(
                        user1=users[i],
                        user2=users[j],
                    )
                    conversations.append(conversation)

        for conversation in conversations:
            participants = conversation.participants()
            count = random.randint(3, 8)
            for _ in range(count):
                sender = random.choice(participants)
                Message.objects.create(
                    conversation=conversation,
                    sender=sender,
                    body=random.choice(message_texts),
                )
