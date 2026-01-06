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
            "امروز روی یک ویژگی جدید در پروژه جنگو کار کردم\nو بعد از چند ساعت بهینه‌سازی، عملکرد بخش گزارش‌گیری خیلی بهتر شد.\nاین تغییر را مستند کردم تا تیم هم بتواند از آن استفاده کند.",
            "چند روز اخیر زمان زیادی را صرف بازنویسی کدهای قدیمی کردم\nتا ساختار پروژه تمیزتر و قابل نگهداری‌تر شود.\nحالا خواندن و توسعه دادن بخش‌های مختلف نرم‌افزار بسیار ساده‌تر است.",
            "در این هفته روی طراحی معماری سرویس‌گرا برای یک محصول جدید کار کردم.\nسرویس‌ها را به شکل مستقل پیاده‌سازی کردیم و ارتباط بین آن‌ها را با پیام‌رسان مدیریت کردیم.\nاین ساختار کمک می‌کند تا در آینده مقیاس‌پذیری به شکل بهتری انجام شود.",
            "امروز چند تست خودکار جدید برای بخش احراز هویت اضافه کردم\nتا مطمئن شوم تغییرات آینده روی ورود و ثبت‌نام کاربران تاثیری منفی نگذارد.\nداشتن پوشش تست مناسب باعث می‌شود با خیال راحت‌تری کد را توسعه بدهم.",
            "در طول روز روی بهینه‌سازی کوئری‌های پایگاه داده کار کردم\nو با استفاده از ابزار پروفایلینگ متوجه چند نقطه کند در سیستم شدم.\nبعد از اعمال تغییرات، زمان پاسخ‌گویی چند endpoint به شکل چشم‌گیری کاهش پیدا کرد.",
            "بعد از پایان ساعت کاری کمی روی پروژه شخصی خودم کار کردم\nکه شامل ساخت یک داشبورد ساده با جنگو و قالب‌بندی داده‌ها برای نمایش بهتر بود.\nاین پروژه برای من فرصتی است تا ایده‌های جدید را بدون محدودیت امتحان کنم.",
            "در تیم تصمیم گرفتیم مستندات پروژه را به‌روزرسانی کنیم\nو هر قابلیت جدید را همراه با مثال و توضیح کامل ثبت کنیم.\nاین کار کمک می‌کند اعضای جدید تیم سریع‌تر با پروژه آشنا شوند.",
            "امروز بخشی از زمانم را به کد ریویو اختصاص دادم\nو چند پیشنهاد برای ساده‌تر شدن توابع پیچیده ارائه کردم.\nهمکاری روی بازبینی کد باعث شده کیفیت کلی پروژه در طول زمان بهتر شود.",
            "برای بهبود تجربه کاربری، استایل‌های رابط کاربری را بازنگری کردم\nو چند جزئیات کوچک مثل فاصله‌ها و اندازه فونت‌ها را تنظیم کردم.\nنتیجه کار یک رابط تمیزتر و خواناتر برای کاربران نهایی بود.",
            "در پایان روز گزارشی از پیشرفت کارهای انجام‌شده آماده کردم\nو در برد پروژه وضعیت تسک‌ها را به‌روزرسانی کردم.\nاین شفافیت کمک می‌کند کل تیم تصویر دقیق‌تری از وضعیت فعلی محصول داشته باشد.",
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
