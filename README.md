# telegram_v2ray_sub

این پروژه به شما یک لینک سابسکریپشن برای استفاده در کلاینت های v2ray میدهد.

## نحوه کار پروژه
این پروژه از کانالهای تلگرامی کانفیگ v2ray را جمع آوری میکند و آنها را در قالب یک لینک سابسکریپشن در اختیار شما قرار میدهد.

## نحوه اجرا
1. پروژه را دانلود و یا clone کنید.
2. با اجرای دستور `pip install -r requirements.txt` پیش نیازهای پروژه را نصب کنید:
3. پروژه را با دستور `python telegram_v2ray_sub.py` اجرا کنید.
* برای اینکه با بستن ترمینال، همچنان لینک سابسکریپشن در دسترس باشد، میتوانید از ابزارهایی مانند tmux و یا pm2 استفاده کنید.

## نحوه استفاده
پس از اجرای پروژه، آدرس زیر در دسترس قرار دارد:

`http://<server ip>:5000/sub`

پارامترهای زیر برای این آدرس در دسترس هستند:
* channel:

آدرس کانال تلگرامی است که کانفیگ ها از آن کراول خواهند شد. در فایل `settings.py` میتوانید کانال پیشفرض را تنظیم کنید تا در صورتی که این پارامتر ارسال نشد، از آن کانال کراول انجام شود.
* count:

تعداد کانفیگ هایی که برای شما ارسال خواهد شد. مقدار پیشفرض این متغیر در فایل `settings.py` قابل تغییر است.
* protocols:

فقط کانفیگ هایی که اینجا تنظیم شوند ارسال خواهند شد. همچنین میتوانید چند پروتکل را با `,` ارسال کنید. در صورتی که این متغیر ارسال نشود، همه کانفیگ های استاندارد ارسال خواهند شد.
* توجه: در فایل تنظیمات متغیر دیگری به نام `POST_COUNT` قرار دارد که مشخص کننده حداکثر پست های کانال تلگرام برای کراول است.

### مثال
`http://<server ip>:5000/sub?channel=sample&count=25&protocols=ss,vmess`

حداکثر ۲۵ کانفیگ با پروتکل های shadow socks و vmess از کانال sample کراول و ارسال میکند.

_مشارکت شما، حس خوب برای ادامه را تزریق میکند._
