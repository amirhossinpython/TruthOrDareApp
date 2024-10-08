from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase
from bidi.algorithm import get_display
import arabic_reshaper
import random

# بارگذاری فونت فارسی
LabelBase.register(name='Vazir', fn_regular='Vazirmatn-Bold.ttf')

# لیست سوالات حقیقت

truth_questions = [
    "آیا تا به حال دروغ بزرگی گفته‌ای؟",
    "بهترین خاطره دوران کودکی تو چیست؟",
    "اگر می‌توانستی یک روز از زندگی کسی دیگر را تجربه کنی، چه کسی را انتخاب می‌کردی؟",
    "بهترین دوستت کیست و چرا؟",
    ".کدوم کشور دلت میخاد بری؟",
    ".چند بار سوتی دادی؟",
    "مدرسه یا گوشی؟",
    ".بهترین اتفاق هفته گذشته ات چی بود؟",
    "تا به حال از چیزی ترسیده‌ای؟",
    "اگر یک قدرت فراطبیعی داشتی، چه بود؟",
    "آیا تا به حال به کسی حسادت کرده‌ای؟",
    "بهترین هدیه‌ای که تا به حال دریافت کرده‌ای چه بوده؟",
    "اگر یک هفته فرصت داشتی به هر جایی سفر کنی، کجا می‌رفتی؟",
    "بدترین عادتت چیست؟",
    "اگر می‌توانستی یک چیز را تغییر دهی، چه چیزی را تغییر می‌دادی؟",
    "آخرین باری که گریه کردی کی بود و چرا؟",
    "آیا تا به حال چیزی را دزدیده‌ای؟",
    "اگر می‌توانستی یک روز زندگی یک نفر دیگر را تجربه کنی، چه کسی را انتخاب می‌کردی؟",
    "چقدر به خودت اعتماد به نفس داری؟",
    "چه چیزی تو را بیشتر از همه شاد می‌کند؟",
    "چه چیزی تو را بیشتر از همه عصبانی می‌کند؟",
    "آیا تا به حال در موقعیت دشوار قرار گرفته‌ای که به نظر می‌رسید هیچ راهی برای فرار نداشتی؟",
    "چه چیزی در مورد خودت را بیشتر از همه دوست داری؟",
    "چه چیزی را بیشتر از همه در زندگی‌ات تغییر می‌دادی؟",
    "آیا تا به حال با کسی بر سر یک موضوع مهم اختلاف نظر داشته‌ای؟",
    "بهترین نصیحتی که تا به حال دریافت کرده‌ای چه بوده؟",
    "آیا تا به حال در زندگی‌ات به چیزی یا کسی که دوستش داری خیانت کرده‌ای؟",
    "چه آرزویی داری که هنوز نتوانسته‌ای به آن دست پیدا کنی؟",
    "اگر می‌توانستی با یک شخصیت تاریخی ملاقات کنی، با کی ملاقات می‌کردی؟",
    "چه چیزی در زندگی‌ات باعث افتخار تو است؟",
    "آیا تا به حال کاری کرده‌ای که بعداً از آن پشیمان شده‌ای؟",
    "چگونه با استرس و فشارهای زندگی کنار می‌آیی؟",
    "چه چیزی در مورد دوستانت را بیشتر از همه دوست داری؟",
    "چه احساسی داری وقتی به آینده فکر می‌کنی؟",
    "آیا تاکنون عاشق شده‌ای؟ اگر بله، چه چیزی را درباره آن تجربه کردی؟",
    "چه چیزی در زندگی‌ات تو را بیشتر از همه تحت تأثیر قرار داده است؟",
    "آیا تا به حال احساس کرده‌ای که کسی تو را به خوبی نمی‌شناسد؟",
    "آیا تا به حال در یک موقعیت عاشقانه یا احساسی بزرگترین اشتباه را کرده‌ای؟",
    "بهترین هدیه‌ای که تاکنون از کسی دریافت کرده‌ای چه بوده است؟",
    "اگر می‌توانستی یک روز به طور کامل از زندگی خود را تغییر دهی، چه می‌کردی؟",
    "تا به حال در استخر دستشویی کردی؟",
    "آیا تو دست توی دماغت می‌کنی؟",
    "آیا با خودت جلوی آینه صحبت می‌کنی؟",
    "جذابترین آدم توی این اتاق از نظر تو کیه؟",
    "آیا توی حمام دستشویی می‌کنی؟",
    "تا به حال راز دوستات رو به بقیه گفتی؟",
    "اگر مجبور باشی با یکی از دوستات قطع رابطه کنی، اون کیه؟",
    "کی‌بیشتر‌میخندونه‌تو‌رو؟",
    "عشق‌رو‌تجربه‌کردی؟",
    "در حال حاضر از کی خوشت میاد؟",
    "چندسالته",
    "زن داری؟",
    "بدترین دروغی که تا به حال گفته‌های چه بوده است؟",
    "عشق اولت چه کسی بود",
    "آیا تا به حال به کسی خیانت کرده‌ای؟ اگر بله، چرا",
    "آیا تا به حال قانون شکنی کرده است؟ اگر بله، چه چیزی؟ ",
    "دوباره  بزن",
    "پوچ",
    "رکب خوردی کیومرث",
    "تابحال عاشق دخترشدی ؟",
    "ـابحال گناه کردی؟",
    "تابحال زجه زدی ؟",
    "نام کسی که در مدرسه به او علاقه داشتی را بگو.",
    "چه کاری را هرگز انجام نمی‌دادی اما همیشه دوست داشتی؟",
    "آخرین باری که گریه کردی چه زمانی بود و چرا؟",
    "اگر می‌توانستی به هر جای دنیا سفر کنی، کجا می‌رفتی؟",
    "بزرگ‌ترین ترس تو چیست؟",
    "آیا تا به حال دروغ بزرگی گفته‌ای؟ چه بود؟",
    "کدام یک از دوستانت را بیشتر از همه دوست داری و چرا؟",
    "آخرین باری که بدون دلیل خوشحال بودی چه زمانی بود؟",
    "چه چیزی تو را واقعاً عصبی می‌کند؟",
    "تابحال فحاشی کردی؟",
    "عاشق شدی؟",
    "ی خاطره از بچگیت بگو؟ ",
    "اسمت چیه؟",
    "قدت؟",
    "وزنت؟",
    ".تاریخ تولدت؟",
    "ولین‌دعواتون‌با‌عشقت‌کی‌بود؟",
    "دل کسی رو شکوندی؟",
    "الان خوشحالی یا ناراحت؟ ",
    "غذای مورد علاقت؟",
    ".تاحالا بهم دروغ گفتی؟ ",
    "حموم که میری از شامپویی استفاده میکنی؟",
    "نوشابه مورد علاقت؟ ",
    ".ماشین مورد علاقت؟"

   
    
    
]


# لیست چالش‌های جرأت
dare_challenges = [
    "یک آهنگ بخوان.",
    "پیاز  خام و گاز بزن؟",
    "یک لطیفه بگو.",
    "یک دقیقه با صدای بلند بخند.",
    "یک حرکت ورزشی انجام بده.",
    "یک جمله عاشقانه به یکی از بازیکنان بگو.",
    "یک کار خنده‌دار انجام بده.",
    "برای یک دقیقه چشم‌هایت را ببند و چیزی بکش.",
    "یک حرکت رقص انجام بده.",
    "یک راز خنده‌دار از خودت بگو.",
    "با صدای بچه صحبت کن.",
    "یک پاراگراف با صدای بلند بخوان.",
    "یک حقیقت از زندگی‌ات بگو.",
    "یک داستان کوتاه برای دیگران بگو.",
    "یک نفر را در بازی به چالش بکش.",
    "یک چیزی را به زبان خارجی بگو.",
    "یک تصویر خنده‌دار از خودت بگیر و به اشتراک بگذار.",
    "یک دقیقه با یک قدم ثابت قدم بزن.",
    "یک رفتار خنده‌دار از خودت انجام بده.",
    "یک جمله به یک بازیکن بگو که همیشه دوست داری.",
    "در مقابل دوربین یک داستان خیالی بگو.",
    "یک نفر را به یک چالش جذاب دعوت کن.",
    "برای چند ثانیه به حالت ایستاده بمان و سپس به حالت نشسته برگرد.",
    "یک جمله را با زبان بدن به نمایش بگذار.",
    "یک حرکت ورزش یوگا انجام بده.",
    "یک شعر خنده‌دار بخوان.",
    "با صدای مختلفی برای چند ثانیه صحبت کن.",
    "یک حقیقت عجیب درباره خودت بگو.",
    "یک دایره با انگشتت روی میز بکش و آن را برای دیگران توضیح بده.",
    "یک تصویر از یک مدل خنده‌دار بساز و آن را به اشتراک بگذار.",
    "یک عاشقانه‌ترین جمله‌ای که تا به حال شنیده‌ای را بگو.",
    "یک کار غیرمعمول انجام بده که هیچ وقت قبلاً نکرده‌ای.",
    "یک پاراگراف عاشقانه برای یک بازیکن بنویس و آن را بخوان.",
    "یک داستان کوتاه احساسی درباره یک لحظه خاص از زندگیت بگو.",
    "با صدای خود یک قصه عاشقانه بخوان.",
    "یک چالش جذاب برای یکی از بازیکنان پیشنهاد کن.",
    "یک تصویر از یک لحظه ویژه از زندگیت به اشتراک بگذار.",
    "ده لیوان اب بخور",
    "ده بار بگو لبیک یاخامنه ای",
    "بگو من یک برانداز کسخلم",
    "به کسی که دوستش داری بگو که چقدر برایت مهم است.",
    "یک پیام عاشقانه به اولین نفری که در فهرست مخاطبان بفرست است",
    "لباس دخترانه بپوش",
    "صدای خر دربیار",
    "صدای بز دربیار",
    "بگو من یک اسکل هستم",
    "یک آهنگ بخوان که خیلی دوستش داری.",
    "به مدت ۳۰ ثانیه بر روی یک پای خود بایست.",
    "سعی کن یک لهجه خاص را تقلید کنی و دیگران حدس بزنند که کدام لهجه است.",
    "یک پیام خنده‌دار به کسی که در مخاطبین خود داری ارسال کن.",
    "یکی از حرکات رقص مورد علاقه‌ات را نشان بده.",
    "یک دقیقه بدون صحبت کردن فقط به شکل‌های خنده‌دار روی صورتت درست کن.",
    "به مدت ۱۵ ثانیه در یک نقطه بایست و هیچ حرکتی نکن.",
    "بگو که اگر می‌توانستی به هر موجوداتی (واقعی یا خیالی) تبدیل شوی، چه چیزی را انتخاب می‌کردی؟",
    "برو به پدر مادرت بگو زن میخام",
    "برو به پدرمادرت بگو شوهر میخام",
    "اسم عزیزترین فرد زندگیتو داد بزن؟ ",
    ""
    
    
    
    
    
    
    
]



def reshape_text(text):
    """این تابع متن را برای نمایش صحیح به صورت راست به چپ پردازش می‌کند."""
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

class TruthOrDareApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.result_label = Label(
            text=reshape_text('انتخاب کنید "جرأت" یا "حقیقت"'),
            font_name='Vazir',
            font_size='20sp',
            size_hint=(1, 0.2),
            halign='right',
            valign='middle'
        )
        layout.add_widget(self.result_label)

        button_layout = BoxLayout(orientation='horizontal', spacing=10)

        truth_button = Button(
            text=reshape_text('حقیقت'),
            font_name='Vazir',
            font_size='18sp',
            on_press=self.show_truth
        )
        dare_button = Button(
            text=reshape_text('جرأت'),
            font_name='Vazir',
            font_size='18sp',
            on_press=self.show_dare
        )

        button_layout.add_widget(truth_button)
        button_layout.add_widget(dare_button)

        layout.add_widget(button_layout)

        return layout

    def show_truth(self, instance):
        question = random.choice(truth_questions)
        
        self.show_popup("Truth Question", reshape_text(question))  # تغییر تایتل به انگلیسی

      
    def show_dare(self, instance):
        
        challenge = random.choice(dare_challenges)
        self.show_popup("Dare Challenge", reshape_text(challenge)) 
    def show_popup(self, title, content):
        """این تابع یک Popup با عنوان و محتوای پردازش‌شده ایجاد و نمایش می‌دهد."""
        content_label = Label(
            text=content,
            font_name='Vazir',
            font_size='16sp',
            halign='right',
            valign='middle',
            text_size=(None, None)
        )
        content_label.bind(size=self.update_text_size)

        popup = Popup(
            title=title,
            title_align='right',
            content=content_label,
            size_hint=(0.8, 0.4)
        )
        popup.title = reshape_text(title)  # تنظیم عنوان پردازش‌شده
        popup.open()

    def update_text_size(self, instance, value):
        """این تابع برای تنظیم اندازه متن درون Label استفاده می‌شود."""
        instance.text_size = (instance.width * 0.9, None)

if __name__ == '__main__':
    TruthOrDareApp().run()


