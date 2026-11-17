# מתי אצלך? – סיכום התקדמות (אב טיפוס)
*עודכן: 11.11.2026 · סוף שלב 5, תחילת שלב 6*

> **לשיחה חדשה:** להדביק את הקובץ הזה ולצרף את `Mati_Etzlecha_GDD.md`. אחר כך לכתוב "בוא נמשיך משלב 6".

---

## כללי עבודה עם Claude (חובה!)
1. **Git נעשה בסוף.**
2. **Claude לא משנה ולא כותב שום דבר בתיקיית הפרויקט** אלא אם ביקשתי במפורש.
3. **מצב מנטור:** כשאני מבקש עזרה, רק הכוונה, רמזים ושאלות, לא פתרון ישיר. חריג: כשאני כותב "תגיד לי" / "תגיד לי את התשובה", מקבלים תשובה ישירה.
4. דברים יכולים להשתנות, ואני מעדכן מה עשיתי ומתי עוברים נושא.
- שיחה בעברית, הערות בקוד באנגלית. כשמבקשים הערות, רק על מה שביקשתי.
- כשאני מבקש "תרשום לנו" משהו לעתיד, לשמור אותו ולהזכיר אותו בזמן המתאים.

---

## הפרויקט
- **Unity 6000.3.26f1, 2D URP**, פרויקט סיום בקורס, עבודה לבד.
- Survivors-like: רווק בחתונה בורח מדודות, "תירוצים" נורים אוטומטית, פתקים בטלפון נותנים XP.
- מסמך העיצוב: `Mati_Etzlecha_GDD.md`. היעד הנוכחי הוא האב טיפוס (סעיף 12 במסמך).
  - ⚠️ במסמך עדיין כתובים Dash וחצים, אבל **שניהם הוסרו** (החלטה שלי).
- סצנה: `Assets/Scenes/Prototype.unity`. סקריפטים: `Assets/Scripts/`.

---

## מה בנוי

### ✅ שלב 1: תזוזה ומצלמה (`PlayerMovement.cs`, `SmoothCameraFollow.cs`)
- WASD דרך Input System, בלי חצים. הוקטור מנורמל באלכסון. קלט ב-`Update`, `rb.linearVelocity` ב-`FixedUpdate`. מהירות 4.
- **בלי Dash.**
- **מוסכמת כיוון:** כל הספרייטים מצוירים **פונים שמאלה**. `facingRight` מתחיל ב-`false`, וההיפוך רק דרך `sr.flipX = facingRight` (לא `Rotate` ולא `scale`).
- המצלמה ב-**`LateUpdate`** עם `SmoothDamp`. לשחקן יש Rigidbody עם Interpolate ו-Continuous.

### ✅ שלב 2: דודה רודפת ושולחנות (`EnemyMovement.cs`, `Doda.prefab`, `Table.prefab`)
- הדודה תמיד הולכת ישר לשחקן (נרמול, ואז `linearVelocity`). מהירות 2.5. מוצאת את השחקן לפי Tag "Player". **בלי מרחק עצירה.**
- התנגשויות פיזיקליות. **Mass של השחקן = 100**, כך שהדודות לא מזיזות אותו.
- **קולידרים בחצי התחתון** ("רגליים"). **מיון לפי Y:** Custom Axis (0,1,0) ב-`Renderer2D.asset`.
- Layers: Player (6), Enemy (7). **אין Tag בשם Enemy**, רק Layer.
- הדודות על **Collision Detection: Discrete** (עם Continuous ה-FPS ירד ל-10–40 ב-130 דודות. עכשיו 300 דודות ב-בערך 220 FPS).

### ✅ שלב 3: Spawner (`EnemySpawner.cs`)
- `HandleSpawning()`: טיימר שיורד, `while` שיוצר דודות, ו-`timer += interval` (שומר שארית).
- `HandleSpawnRate()`: `globalTimer` מתחילת המשחק, ו-`spawnInterval = Mathf.Max(curve.Evaluate(globalTimer), 0.5f)`.
- **`AnimationCurve`:** מ-**(0, 2)** עד **(300, 0.5)**, קו ישר. בדקה הראשונה בערך 5 דודות על המסך (המסמך: 5–10).
- `timerToNextSpawn` מתחיל ב-1.5, כלומר שקט קצר בהתחלה.
- `GetSpawnLocation()`: נקודה אקראית על מעגל סביב **המצלמה**. הרדיוס הוא מהמרכז לפינת המסך ועוד `spawnMargin`. `z = 0`.

### ✅ שלב 4: תירוץ ראשון, "יש לי משמרת מחר!"
- **`ShiftExcuse.cs`** (על **child של השחקן**):
  - `HandleFiring()`: ירייה כל `fireInterval = 1`. **"ירייה טעונה":** אם אין דודה בטווח, הטיימר לא מתאפס ומחכה, וברגע שדודה נכנסת היא חוטפת מיד. האיפוס הוא עם `=` ולא `+=`, כדי שלא יהיה מטח של יריות אחרי המתנה.
  - `GetClosestDoda()`: `Physics2D.OverlapCircleAll(pos, range, whatIsEnemy)`, ואז לולאה עם `sqrMagnitude` שמתחילה מ-`Mathf.Infinity`. הפיזיקה מחליטה מי בטווח, והלולאה מחליטה מי הכי קרובה.
  - `Fire()`: הכיוון הוא "יעד פחות מקור", הקליע נלקח מהמאגר לתיקיית קליעים (לא child של השחקן!), ואז `LaunchBullet(direction, position)`.
  - `OnDrawGizmos` מצייר את הטווח.
- **`BulletBehaviour.cs`** (ה-Prefab של הקליע: **Kinematic**, Collider **Is Trigger**):
  - `LaunchBullet(dir, pos)`: נרמול תמיד, מיקום, ואז `linearVelocity`. חוזר למאגר אחרי 5 שניות.
  - `OnTriggerEnter2D`: `!hasHit && TryGetComponent(out EnemyInsistence)`, ואז `ReduceInsistence(bulletDamage = 5)` וחוזר למאגר. ה-`hasHit` מונע פגיעה כפולה באותו צעד.
- **`EnemyInsistence.cs`** (על הדודה): `insistence = 10`. `ReduceInsistence(amount)`: אם לא ויתרה, מורידים, ואם `<= 0` קוראים ל-`GiveUp()`. `GiveUp()` מסמן `isDead = true` ומחזיר למאגר. כל דרך לוויתור עוברת דרך `GiveUp`.
- **מבחן משחק:** "מרגיש שיכול להיות כיף עם שדרוגים וגרפיקה". בלי שדרוגים, כל עקומה עולה תקבור את השחקן בסוף. זה צפוי, ושלב 6 סוגר את הפער.

---

### ✅ שלב 5: Object Pooling (`UnityEngine.Pool.ObjectPool<T>`)
- **הכלל:** מי שיוצר את האובייקט מחזיק את המאגר. המאגר מועבר לאובייקט **פעם אחת**, בפונקציית היצירה, ומי שמחליט "למות" קורא ל-`Release`.
- **קליעים:** המאגר ב-`ShiftExcuse` (`ObjectPool<BulletBehaviour>`).
  - `CreateNewBullet`: `Instantiate` לתיקייה ואז `SetPool`. Taken/Returned: `SetActive(true/false)`.
  - `Fire`: `Get()` ואז `LaunchBullet(direction, position)`.
  - `LaunchBullet` קובע גם `rb.position` וגם `transform.position`. עם `rb.position` לבד היה הבהוב של פריים אחד במיקום הישן.
  - `OnEnable` מאפס `hasHit` ו-`timeAlive`. `Release` בפגיעה או אחרי `maxAliveTime`.
  - Order in Layer של הקליע = 1, של השולחן = 0, כדי שהקליע תמיד יהיה מעל.
- **דודות:** המאגר ב-`EnemySpawner` (`ObjectPool<EnemyMovement>`).
  - `CreateNewDoda`: `Instantiate` לתיקייה (בלי מיקום), ואז `newDoda.GetComponent<EnemyInsistence>().SetPool(...)`.
  - `SpawnEnemy`: `Get()` ואז `SetDodaPosition(spawnLocation)`, שקובעת `rb.position` ו-`transform.position`. המיקום נקבע **בכל לקיחה**, לא ביצירה.
  - `EnemyInsistence`: שומר `EnemyMovement` ב-`Awake`. `GiveUp` עושה `isDead = true` ואז `pool.Release(enemyMovement)`. `OnEnable` מאפס `isDead = false` ו-`insistence = maxInsistence` (ערך התחלה נפרד מהמונה, אותו לקח כמו `timeAlive`/`maxAliveTime`).
- **נבדק:** הכל עובד, רק כמה אובייקטים נוצרים בתיקיות ומשתמשים בהם שוב, הדודה שחוזרת צריכה בדיוק 2 פגיעות.

## 📝 דברים שביקשתי לזכור לעתיד
- **`ShiftExcuse`:** כשאין דודה בטווח, הטיימר נשאר מתחת ל-0, ולכן `OverlapCircleAll` רצה **בכל פריים** ויוצרת מערך חדש. **נמדד ב-Profiler (11.11):** 32 B לפריים כשאין דודה בטווח, 0 B בפריים רגיל כשיש דודה, ו-0.4% מהפריים. זניח, אז נשאר למעבר ביצועים בסוף. זה יחשוב יותר אם יהיו כמה תירוצים שכל אחד מחפש בכל פריים. אם צריך, לעבור לגרסה עם `List<Collider2D>` שמשתמשים בה שוב (`OverlapCircle` עם `ContactFilter2D`), או לחפש בתדירות נמוכה יותר.

---

## ⬜ מה הלאה
- **שלב 6:** פתקים, XP ובחירת 1 מתוך 3 קלפים. דודה שמוותרת תשאיר פתק, ובשביל זה `GiveUp` כבר מוכנה.
- **שלב 7:** סבלנות (`Patience`), נזק במגע והפסד. עם התנגשות פיזיקלית: `OnCollisionStay2D` (`Enter` לבד לא מספיק לנזק "כל עוד נוגעים").
- **שלב 8:** טקסט צף.
- **Git בסוף.**

## שיפורים אופציונליים שנשארו פתוחים
- Sprite Sort Point: להחליף מ-Center ל-Pivot שממוקם ברגליים
- PolygonCollider2D: אפשר להחליף ב-Circle עם Offset
- הערות ב-`EnemyMovement.cs`, והערה על "ירייה טעונה" ב-`ShiftExcuse`
- קיבוץ השדות ב-`ShiftExcuse` עם `[Header]`
- ה-Spawner יכול להעביר לדודה את ה-reference לשחקן, במקום `FindGameObjectWithTag`
- דודות יכולות להיווצר בתוך שולחנות (מקובל לאב טיפוס)
- מסמך העיצוב לא עודכן לגבי: הסרת ה-Dash, בלי חצים
