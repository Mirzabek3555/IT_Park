# Tuproqqal'a IT Park Web Sayti

Tuproqqal'a tumani IT Parki uchun zamonaviy, mobil moslashuvchan web-sayt. Bu loyiha Django framework da yaratilgan va test tizimi, foydalanuvchilar reytingi va admin panelini o'z ichiga oladi.

## Asosiy xususiyatlar

### 🏠 Bosh sahifa
- IT Park haqida umumiy ma'lumot
- Logotip va rasm
- So'nggi yangiliklar
- Eng yaxshi o'quvchilar reytingi

### 📚 Yo'nalishlar
- IT Park faoliyat yo'nalishlari
- Dasturlash, dizayn, sun'iy intellekt
- Kibermuhofaza, robototexnika va boshqalar
- Har yo'nalish uchun alohida sahifa

### 🧪 Test tizimi
- Foydalanuvchilar ro'yxatdan o'tish va login
- Dasturlash, matematika, informatika, fizika fanlaridan testlar
- Turli formatdagi testlar:
  - 4 variantli savollar
  - Kod yozish testlari
  - Mantiqiy masalalar
- Har testdan keyin ball hisoblash
- Foydalanuvchilar reytingi

### 🏆 Reyting sahifasi
- Eng yuqori ball to'plagan o'quvchilar ro'yxati
- O'rtacha ball va testlar soni bo'yicha reyting

### 📞 Kontakt
- Manzil, telefon, email
- Xaritada ko'rsatish
- Bog'lanish formasi

### 👤 Foydalanuvchi profili
- Shaxsiy ma'lumotlar
- Test natijalari tarixi
- Statistika va reyting

## Texnik talablar

### Frontend
- HTML5, CSS3
- Bootstrap 5 (responsive dizayn)
- JavaScript (Vue.js o'rniga oddiy JS)
- Font Awesome ikonlari

### Backend
- Python 3.11+
- Django 5.2.5
- SQLite ma'lumotlar bazasi

### Qo'shimcha kutubxonalar
- Pillow (rasm ishlash uchun)

## O'rnatish va ishga tushirish

### 1. Loyihani klonlash
```bash
git clone <repository-url>
cd Tuproqqala_ITPARK
```

### 2. Virtual environment yaratish
```bash
python -m venv venv
venv\Scripts\activate  # Windows uchun
source venv/bin/activate  # Linux/Mac uchun
```

### 3. Kerakli kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. Ma'lumotlar bazasini yaratish
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Superuser yaratish
```bash
python manage.py createsuperuser
```

### 6. Server ishga tushirish
```bash
python manage.py runserver
```

### 7. Brauzerda ochish
```
http://127.0.0.1:8000/
```

## Admin panel

Admin panelga kirish uchun:
```
http://127.0.0.1:8000/admin/
```

Admin panel orqali:
- Testlar qo'shish va tahrirlash
- Foydalanuvchilarni boshqarish
- Yangiliklar qo'shish
- Yo'nalishlar boshqarish
- Reytingni ko'rish

## Loyiha strukturasi

```
Tuproqqala_ITPARK/
├── itpark_project/          # Asosiy Django loyiha
├── main/                    # Asosiy app (bosh sahifa, yangiliklar, yo'nalishlar)
├── tests/                   # Test tizimi app
├── users/                   # Foydalanuvchilar app
├── templates/               # HTML shablonlar
│   ├── base.html
│   ├── main/
│   ├── tests/
│   └── users/
├── static/                  # Statik fayllar
│   ├── css/
│   ├── js/
│   └── images/
├── media/                   # Foydalanuvchi yuklangan fayllar
├── manage.py
└── README.md
```

## Ma'lumotlar bazasi modellari

### Users app
- **User**: Foydalanuvchi ma'lumotlari
- **Profile**: Foydalanuvchi profili va statistikasi

### Tests app
- **Category**: Test kategoriyalari
- **Test**: Test ma'lumotlari
- **Question**: Savollar
- **Answer**: Javoblar
- **TestResult**: Test natijalari
- **UserAnswer**: Foydalanuvchi javoblari

### Main app
- **News**: Yangiliklar
- **Direction**: Yo'nalishlar
- **Contact**: Kontakt ma'lumotlari
- **About**: IT Park haqida ma'lumot

## Xususiyatlar

### Responsive dizayn
- Mobil qurilmalarga moslashuvchan
- Bootstrap 5 grid tizimi
- Zamonaviy UI/UX

### Xavfsizlik
- Django CSRF himoyasi
- XSS va SQL injection himoyasi
- Foydalanuvchi autentifikatsiyasi

### Tezlik
- Ma'lumotlar bazasi optimizatsiyasi
- Statik fayllar caching
- Responsive rasm formatlari

## Rivojlantirish

### Yangi xususiyatlar qo'shish
1. Yangi app yarating: `python manage.py startapp app_name`
2. `settings.py` ga qo'shing
3. Modellar yarating
4. Views va templates yarating
5. URL patterns qo'shing

### Test yaratish
1. Admin panelga kiring
2. Category yarating
3. Test qo'shing
4. Savollar va javoblarni kiritng

## Yordam

Agar savollaringiz bo'lsa:
- Email: admin@example.com
- Telegram: @itpark_support

## Litsenziya

Bu loyiha MIT litsenziyasi ostida tarqatiladi.

## Muallif

Tuproqqal'a IT Park jamoasi
