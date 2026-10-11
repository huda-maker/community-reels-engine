# ريل هوزن قو: «خل عميلك عميلك» (مُسلَّم 2026-10-11)

ملفات المشروع محفوظة هنا حتى يمكن تعديل الريل لاحقًا بدون البدء من الصفر. لا يوجد أي مفتاح API في هذه الملفات.

## ما المعتمد من صاحبة المشروع (هدى)
- **الجمهور:** أصحاب المطاعم والكافيهات ومتخذو القرار فيها.
- **الفكرة:** «عميلك ليس عميلك فعلًا، إذا كان يطلب منك عبر تطبيق غيرك.»
- **اللهجة والنبرة:** سعودية بيضاء، عفوية وواثقة.
- **الدعوة:** واتساب 920033443، على الشاشة فقط. (يجب التأكد أن الرقم يستقبل واتساب.)
- **المنصات والمدة:** ريلز وتيك توك وسناب، مقاس 9:16، مدة 30 ثانية.
- **الصوت:** Gemini TTS (`gemini-3.8-flash-tts`)، صوت Charon، التسجيل الرابع بعد تعديلات النطق، النص في `work/script-v3.txt`.
- **التصميم:** رسوم مسطّحة على خلفية كريمي مع مصابيح، ونصوص الكلام في إطارات بيضاء بحدود برتقالية، وخط Cairo، وألوان الشعار.
- **ممنوع:** أي شعار لعلامة أخرى، فلقطة «دوّار السعادة» حُذفت بطلبها. وممنوع شعار صغير أعلى الشاشة.
- **المؤثرات الصوتية:** 50 مؤثرًا مولّدة برمجيًا في `build_flat.py`، بمستوى 0.55 تحت صوت المعلّق.
- **تكلفة Google:** ‏0.0513$ (التفاصيل في `work/api-usage.json`).

## المحتويات
- `work/hwzngo-reel-final.mp4`: الريل النهائي المُسلَّم.
- `work/build_flat.py`: يبني التصميم والمؤثرات من الصفر.
- `work/narration-Charon-4.wav`: التسجيل المعتمد. `narration-final-30s.wav` هو نفس التسجيل مع صمت لبطاقة النهاية.
- `project/`: مشروع المحرك (`story` و`captions` واعتماد الكابشن) ومجلد التصميم `style-hwzngo-flat`.
- `work/assets/`: الشعار ولقطات التطبيق التي قدمتها هدى.

## الاستعادة في جلسة جديدة (من جذر المستودع)
```sh
npm ci
mkdir -p projects work
cp -r client-projects/hwzngo-direct-channel/project projects/hwzngo-direct-channel
cp -r client-projects/hwzngo-direct-channel/work work/hwzngo-direct-channel
python3 -I work/hwzngo-direct-channel/build_flat.py          # يعيد بناء التصميم وsfx.wav
O=projects/hwzngo-direct-channel/style-hwzngo-flat
HYPERFRAMES_NO_TELEMETRY=1 node_modules/.bin/hyperframes check $O
HYPERFRAMES_NO_TELEMETRY=1 node_modules/.bin/hyperframes render $O --output $O/picture.mp4 --fps 30 --quality high --workers 4 --no-best-effort
ffmpeg -i $O/picture.mp4 -i projects/hwzngo-direct-channel/clean.mp4 -i $O/sfx.wav \
  -filter_complex "[1:a]aresample=48000,aformat=channel_layouts=stereo[n];[2:a]aresample=48000,volume=0.55,aformat=channel_layouts=stereo[s];[n][s]amix=inputs=2:normalize=0:duration=first[a]" \
  -map 0:v:0 -map "[a]" -c:v copy -c:a aac -b:a 192k -ar 48000 -t 30 -movflags +faststart hwzngo-reel-v2.mp4
```

**قواعد التعديل:**
- أي تعديل على **الكلام** يعني تسجيلًا صوتيًا جديدًا، ويحتاج موافقة على النص والتكلفة، ثم قياس التوقيت من جديد واعتماد جديد.
- تعديل **الشكل فقط** يكون في `build_flat.py`، ثم يُعاد التصدير.
- عند توليد صوت جديد، يُضاف المفتاح عبر Network secrets (الترويسة `x-goog-api-key`، والموقع `generativelanguage.googleapis.com`)، ويُشغَّل الأمر مع `GEMINI_KEY_SOURCE=network-secret`. التفاصيل في `docs/gemini-setup.md`.
