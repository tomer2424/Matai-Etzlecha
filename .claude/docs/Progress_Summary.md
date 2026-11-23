# סיכום התקדמות: שף נגד ג'אנק פוד (לשעבר "מתי אצלך?")
*עודכן: 23.11.2026 · שינויי המבנה בקוד הושלמו (`PlayerStats`, `WeaponBase`/`WeaponData`, `EnemyData`, `WaveDirector`). **הנושא הוחלף למסעדה:** שף, פיצה ב-3 טעמים, סכין ומטבע בתוך המשחק. הבא: Animator, נשק שני, אויב שני, המפה.*

> **לשיחה חדשה עם Claude:** `.claude/CLAUDE.md` נטען אוטומטית. הוא מפנה לקובץ הזה ול-`.claude/docs/GDD.md`.

---

## כללי עבודה עם Claude (חובה!)
1. **Git: אני עושה commit ו-push בעצמי.** Claude מציע שם ותיאור לקומיט.
2. **Claude לא משנה ולא כותב שום דבר בתיקיית הפרויקט** אלא אם ביקשתי במפורש.
   - **חריג: גרפיקה.** בגרפיקה Claude עובד כ"מעצב ספרייטים מקצועי" ומכין את הקבצים בעצמו. אני ממקם אותם בסצנה.
3. **מצב מנטור (לקוד של המשחק):** כשאני מבקש עזרה, רק הכוונה, רמזים ושאלות, לא פתרון ישיר. חריג: כשאני כותב "תגיד לי" / "תגיד לי מה הפתרון" / "תכתוב לי", מקבלים תשובה ישירה.
4. **"תבדוק אותי" / "תסתכל":** Claude קורא את הקבצים (סקריפטים, סצנה, פריפאבים) ומעיר. זה מותר תמיד.
5. **צעדים קטנים.** כשיש הרבה בבת אחת אני מתבלבל. מושג חדש: להסביר מאפס, עם דוגמה פשוטה או משל.
6. דברים יכולים להשתנות. אני מעדכן מה עשיתי ומתי עוברים נושא.
- שיחה בעברית, הערות בקוד באנגלית. כשמבקשים הערות, רק על מה שביקשתי.
- כשאני מבקש "תרשום לנו" משהו לעתיד, לשמור אותו כאן ולהזכיר אותו בזמן המתאים.

---

## הפרויקט
- **Unity 6000.3.26f1, 2D URP.** פרויקט סיום בקורס, עבודה לבד. **הגשה: בערך אמצע דצמבר 2026.**
- 🆕 Survivors-like: **שף במסעדה ענקית נגד ג'אנק פוד שקם לתחייה.** זורק כלי מטבח, האוכל מוותר ומשאיר מטבעות (XP), שורדים 15 דקות. **שם המשחק עוד לא נבחר.**
- מסמך העיצוב: `.claude/docs/GDD.md` (גרסה 3.0: נושא המסעדה).
- טבלת איזון: `.claude/docs/Balance.md` (מספרי התחלה, עוד לא נבדקו במשחק).
- סצנה: `Assets/Scenes/Prototype.unity`. סקריפטים: `Assets/Scripts/<תיקייה>/`. נתונים: `Assets/Data/`.

---

## ✅ מה בנוי (הכל עובד ונבדק)

### 🆕 מבנה התיקיות של הסקריפטים (22.11)
`Player/`, `Enemies/`, `Weapons/`, `Pickups/`, `Systems/`, `UI/`, `Debug/`. הזזה ושינוי שם **רק בתוך Unity** (שומר את ה-GUID).

### Player
- **`PlayerMovement`:** WASD דרך Input System (בלי חצים, בלי Dash). קלט ב-`Update`, `rb.linearVelocity = movementVector * playerStats.GetMoveSpeed()` ב-`FixedUpdate`.
- **מוסכמת כיוון:** כל הדמויות מצוירות **פונות שמאלה**. `facingRight` מתחיל ב-`false`, ההיפוך רק דרך `sr.flipX`.
- 🆕 **`PlayerStats`:** ‏`baseMoveSpeed` 4, ומכפילים שמתחילים ב-1: `moveSpeedMultiplier`, ‏`damageMultiplier`, ‏`fireIntervalMultiplier`. כמה כל שדרוג מוסיף: ‏0.08 / ‏0.1 / ‏0.08 (באינספקטור). מתודות: `GetMoveSpeed()`, ‏`GetDamageMultiplier()`, ‏`GetFireIntervalMultiplier()`, ‏`IncreaseMoveSpeed()`, ‏`IncreaseDamage()`, ‏`DecreaseFireInterval()`. **"בסיס × מכפיל":** המכפילים מוחלים ברגע השימוש, לא משנים את הנשק.
- **`PlayerPatience`:** 100, חסינות 0.5 שנ' אחרי מכה, `isDead`, `ReducePatience(float)`, `OnCollisionStay2D` עם `EnemyDamage`. אירועים: `onPatienceChanged(float)`, `onDeath`. 🆕 `DebugToggleInvincible()`.
- **השף בסצנה:** `Chef_sheet_0`. CapsuleCollider2D ‏0.43×0.77 (הרגליים והגוף, בלי הראש). Mass 100, Interpolate.

### Enemies
- 🆕 **`EnemyData`** (ScriptableObject, "כרטיס"): `enemyName`, ‏`maxInsistence`, ‏`moveSpeed`, ‏`damage`, ‏`xpDropped` (int), ‏`hitLineChance` (Range 0–1), ‏`hitLines`, ‏`giveUpLines`. בראש הקובץ: הערה **למה אין `EnemyBase`** (מספרים שונים ← כרטיס, התנהגות שונה ← רכיב נוסף).
  - **`Pizza.asset`:** 10 / 2.5 / 5 / 1 XP / 0.3, ומשפטים של פיצה.
- **שלושת הרכיבים קוראים מהכרטיס ב-`Awake`** (לכל אחד הפניה משלו, `[SerializeField] EnemyData`):
  - **`EnemyMovement`:** הולך ישר לשחקן (Tag "Player"). 🆕 `SetEnemyPosition(pos)` (היה `SetDodaPosition`).
  - **`EnemyInsistence`:** `ReduceInsistence`, `GiveUp()` (מטבע עם ה-XP מהכרטיס, משפט ויתור, `Release`). `OnEnable` מאפס (`insistence = maxInsistence`). 🆕 `ApplyInsistenceMultiplier(float)`: ‏`insistence = maxInsistence × מכפיל` (לא משנה את `maxInsistence`!).
  - **`EnemyDamage`:** `Damage =>`.
- **`EnemySpawner`:** `ObjectPool<EnemyMovement> enemyPool`. ‏`CreateNewEnemy` מעביר לאויב את ה-Pool, את `NotesSpawner` ואת `FloatingTextManager`. יצירה על מעגל סביב המצלמה, מחוץ למסך.
  - 🆕 המרווח מגיע מ-`WaveDirector.GetSpawnInterval()` (העקומה וה-`globalTimer` נמחקו).
  - 🆕 **אחרי `Get()`:** מבקש מ-`WaveDirector` את מכפיל ההתעקשות ומעביר אותו לאויב (`OnEnable` כבר רץ ואיפס, אז הסדר נכון).
  - 🆕 **תקרה:** `maxEnemyAmount` = 250 (`CountActive`). הבדיקה בתוך ה-`while`, והטיימר גדל תמיד, אז אין לולאה אינסופית. יצירה שמגיעה בתקרה **מדלגת**.
- 🆕 **`WaveDirector`** ("המנצח", על אובייקט בסצנה): `GameTimer` (מקור זמן אחד), `SpawnWave[] spawnWaveList` באינספקטור (9 שורות מ-`Balance.md`: ‏0, 60, 120, 240, 360, 480, 600, 720, 840).
  - `GetSpawnInterval()`: השורה **האחרונה** שזמן ההתחלה שלה עבר (`<=`, ‏`break` בשורה הראשונה שעוד לא התחילה). רשת ביטחון: אם אין שורה, `LogWarning` ומחזיר 1.
  - `GetInsistenceMultiplier()`: ‏`1 + insistenceIncreasePerMinute (0.1) × Mathf.FloorToInt(דקות)`. **דקות שלמות** כדי שבדקה הראשונה יהיו בדיוק 2 סכינים לפיצה.
- 🆕 **`SpawnWave`** (`[System.Serializable]`): `startTimeSeconds`, ‏`spawnInterval`. אין זמן סיום: שורה נגמרת כשהבאה מתחילה.
- 🆕 **`RandomLook`:** `Sprite[] sprites`, בוחר ספרייט אקראי ב-`OnEnable` (3 טעמי פיצה).
- **`Pizza.prefab`** (היה `Doda.prefab`, אותו GUID): `Pizza_pepperoni_sheet_0`, CapsuleCollider2D, Offset y ‏0.55, Size ‏0.7×0.5 (על הקרום). Collision Detection **Discrete**.
- **Layers:** Player (6), Enemy (7), Pickup (8, מתנגש רק עם Player).

### Weapons
- 🆕 **`WeaponBase`** (abstract, על ה-child של השחקן):
  - `playerStats = GetComponentInParent<PlayerStats>()`. מעתיק מ-`WeaponData` ב-`Awake`: `fireInterval`, ‏`minFireInterval`, ‏`damage`, ‏`projectileCount`. ‏`maxLevel = weaponLevelUpgradeList.Count + 1`.
  - `Update` ← `HandleFiring()`: הטיימר יורד, וכשהוא ב-0 ו-`TryAttack()` מחזיר `true`, מתאפס ל-`Mathf.Max(minFireInterval, fireInterval × GetFireIntervalMultiplier())`. אם אין יעד, ההתקפה נשארת "טעונה".
  - `protected abstract bool TryAttack()`: הבסיס מחליט **מתי**, הילד מחליט **איך**.
  - `LevelUp()` (ציבורי, לקלף): `currentLevel` מתחיל ב-1, עד `maxLevel`, וקורא ל-`ApplyLevel(level)` (`virtual`): שורה `level - 2` בטבלה מוסיפה נזק וקליעים ומכפילה את הטעינה.
  - ⚠️ **ילד לא כותב `Update`/`Awake` פרטי משלו** (זה מסתיר את של הבסיס). ‏`protected override void Awake() { base.Awake(); ... }`.
- 🆕 **`WeaponData`** (ScriptableObject): `weaponName`, ‏`description`, ‏`fireInterval`, ‏`minFireInterval`, ‏`damage`, ‏`projectileCount`, ‏`List<WeaponLevelUpgrade>`. **`WeaponLevelUpgrade`** (`[System.Serializable]`): `damageToAdd`, ‏`projectilesToAdd`, ‏`fireIntervalMultiplier`.
  - **`Knife.asset`** (היה `Meatballs.asset`): 1 / 0.4 / 5 / 1. שורות: (0,1,1), (5,0,1), (0,1,1), (5,0,0.8).
- 🆕 **`KnifeWeapon`** (היה `ShiftExcuse` ← `MeatballsWeapon`, אותו GUID): `GetClosestEnemies()` מחזיר עד `projectileCount` אויבים **שונים**, מהקרוב (לולאה לכל סכין, `!targetList.Contains`, ‏`break` כשאין עוד). ‏`TryAttack` זורק לפי `i % targetList.Count`. טווח 6. הנזק: `damage × GetDamageMultiplier()`. Pool של סכינים בתוך `KnifeWeaponFolder` (בשורש הסצנה, לא בתוך השחקן!).
- **`BulletBehaviour`:** Kinematic + Trigger, `hasHit`, חוזר ל-Pool בפגיעה או אחרי `maxAliveTime`. 🆕 `LaunchBullet` **מסובב את הקליע לכיוון התעופה**: `Mathf.Atan2(y, x) * Mathf.Rad2Deg` ל-`rb.rotation` ול-`transform.rotation`.
- **`KnifeProjectile.prefab`** (היה `MeatballProjectile`): ספרייט `Knife`, CircleCollider2D רדיוס 0.22, IsTrigger.

### Pickups
- **`NotesSpawner` + `NoteBehaviour`** (השמות נשארו מהפתקים): Pool. 🆕 `SpawnNote(position, xpAmount)` ← `note.SetXPAmount(xp)` מיד אחרי `Get()`. איסוף ב-`OnTriggerEnter2D` עם `TryGetComponent(out LevelSystem)`, ‏`wasCollected` מתאפס ב-`OnEnable`.
- 🆕 **`Coin.prefab`** (היה `Note.prefab`, אותו GUID): ספרייט `Coin`, צבע לבן, Scale 1, CircleCollider2D רדיוס 0.22, IsTrigger.

### Systems
- **`GameTimer`:** שעון יורד, `gameDuration` (**900 בסצנה**, ‏300 כברירת מחדל בקוד), `OnSecondsLeftChanged(int)` רק כשהשנייה משתנה, `OnTimeUp` פעם אחת. 🆕 `GetTimePassed()`, ‏`DebugSkipTime(float)`.
- **`LevelSystem`:** `AddXP` עם `while`. 🆕 `GetXPToLevelUp()` = `xpRequiredPerLevel (10) × currentLevel`. אירועים: `OnXPChanged(float)`, `OnLevelUp`. 🆕 `DebugSkipLevel()`.
- **`SmoothCameraFollow`:** `SmoothDamp` ב-`LateUpdate`.
- **Pixel Perfect Camera:** PPU 16, ‏Reference 480×270, ‏Crop Frame None, ‏Grid Snapping None. Game view ‏1920×1080.

### UI
- **`CardSelectScreen` + `UpgradeOption`** (`[System.Serializable]`: שם, תיאור, `UnityEvent`): `pendingChoices`, הגרלה בלי חזרות, `OnCardButtonPress(int)`. בעצירה: `timeScale = 0` ו-`PlayerMovement.enabled = false`.
  - 🆕 **הקלפים היום:** "Knife / Upgrade knife" ← `KnifeWeapon.LevelUp`, ‏"Quick Escape / +8% move speed" ← `PlayerStats.IncreaseMoveSpeed`, ‏"Increase Base Damage / +10% damage" ← `PlayerStats.IncreaseDamage`.
- **`ProgressBar`** (מדי XP וסבלנות, עם `Bar background.png`), **`TimerText`** (m:ss), **`EndScreen`** (`ShowEndScreen(string)`, "You Died !" / "You Win !", טעינה מחדש).
- **`FloatingTextManager` + `FloatingText`:** Pool, `ShowRandomText(string[], pos)`. הטקסטים באנגלית.

### Debug
- 🆕 **`DebugKeys`** (רק בעורך, `#if UNITY_EDITOR` **בתוך** `Update`): F1 = ‏`DebugSkipTime(60)`, F2 = ‏`DebugSkipLevel()`, F3 = ‏`DebugToggleInvincible()`.

### מיון לפי Y
- `Renderer2D.asset`: Transparency Sort Mode = Custom Axis (0, 1, 0). Sprite Sort Point = **Pivot**, Pivot ברגליים.

---

## 🆕 הנושא החדש: מסעדה (22–23.11.2026)
**הוחלט 23.11:** במקום חתונה, **שף במסעדה ענקית נגד ג'אנק פוד שקם לתחייה**. כלי מטבח במקום אוכל, מטבעות (טיפים) במקום פתקי טלפון. **הקוד והמכניקות לא השתנו**, רק המראה, השמות והמשפטים (בזכות `EnemyData` ו-`WeaponData`).
- **סופי:** שף (שחקן), פיצה (האויב הבסיסי, במקום הדודה), סכין (הנשק הראשון, במקום הקציצות), מטבע (XP).
- **הצעות** (ב-GDD סעיף 4, עם השם הקודם מהחתונה): המבורגר, פחית, צ'יפס, דונאט, קרטון פיצה, בוס "מגה קומבו". מחבת, סיר, מלחייה, מערוך, סכין קצבים. בר סלטים (במקום בופה), ארגזי ירקות (במקום מתנות).
- **המפה לא השתנתה ברעיון:** אולם ענק ופתוח (בערך 200×200), **בלי קירות פנימיים**, איים קבועים (מטבח פתוח, ברי סלטים, בר...) ופיזור אקראי פעם אחת.
- **שינוי שמות:** שמות של **תוכן** הוחלפו (`Pizza`, ‏`Knife`, ‏`Coin`). שמות של **מערכות** נשארו (`EnemyInsistence`, ‏`PlayerPatience`, ‏`NoteBehaviour`).

### היסטוריה קצרה של הכיוון
- **16.11:** אחרי אב הטיפוס: 15 דקות, מפה גדולה עם אזורים, אויבים חדשים לאורך הזמן, עמדות ריפוי, זריקת חפצים, פיקסל ארט 3/4.
- **17.11:** מפה סגורה עם בניין ← עולם אינסופי ← **מפה סופית ענקית בלי בניין, עם איים** (סופי).
- **23.11:** חתונה ← **מסעדה**.

---

## 🎨 גרפיקה: מה קיים

### 🆕 נושא המסעדה (בשימוש)
- **סקריפט:** `.claude/art/PixelArt/make_restaurant.py`. פלט: `.claude/art/PixelArt/restaurant/`.
- **בתוך המשחק** (`Assets/Sprites/Restaurant/`):
  - `Chef_sheet.png` ו-`Pizza_pepperoni/margherita/veggie_sheet.png`: 4 פריימים של 16×24 (עמידה, הליכה 1, הליכה 2, נפגע / מוותרת). Multiple, PPU 16, Point, None, Grid 16×24, Pivot Bottom.
  - `Knife.png` (15×6, **פונה ימינה**) ו-`Coin.png` (7×7): Single, PPU 16, Point, None, Pivot Center.
  - **הפיצה: הקצה למעלה, הקרום הרחב למטה** (שונה לבקשתי, בשביל הקוליידר).
- **דוגמת סגנון (אושרה):** `restaurant_sample_x4.png` (מסך אחד: פרקט, משבצות במטבח, אי מטבח, בר סלטים עם "+" ירוקים, שולחנות עם מפה משובצת, עציצים) ו-`restaurant_characters_x8.png`.
- **הליכה בקליפ (ל-Animator):** הליכה 1 ← עמידה ← הליכה 2 ← עמידה, בבערך 8 FPS.

### ישן (חתונה, לא בשימוש)
- `.claude/art/PixelArt/make_characters.py` (בחור בחליפה + 4 דודות), `make_meatball.py`, `make_buffet.py`, `make_style_sample.py`, `make_map_plan.py`. נשארים לעיון.
- `.claude/art/VectorSprites/` ו-`.claude/art/Venue/`: סגנון וקטורי ישן.
- **נמחקו מ-`Assets` (23.11):** `Player_sheet`, ‏`Aunt_yellow_sheet`, ‏`Meatball_7`, ותמונה ישנה בלי שם.
- **עוד בשימוש:** `RoundTable.png` (ב-`Table.prefab`, שולחנות מאב הטיפוס בסצנה) ו-`Bar background.png` (מדי ה-UI).

- הסקריפטים בפייתון צריכים `pip install pillow`. מריצים: `python make_xxx.py <תיקיית פלט>`.

---

## 📝 דברים שביקשתי לזכור לעתיד
- **מסך Pause:** לרכז את העצירה במקום אחד (`Pause()`/`Resume()` + אירועים), במקום שכל מסך יכבה את `PlayerMovement` בעצמו. היום גם `CardSelectScreen` וגם `EndScreen` עושים את זה.
- **`OverlapCircleAll` ב-`KnifeWeapon`:** כשאין אויב בטווח, רצה בכל פריים ויוצרת מערך חדש (32 B לפריים, 0.4%). למעבר ביצועים בסוף: `OverlapCircle` עם `ContactFilter2D` ו-`List<Collider2D>`, או חיפוש בתדירות נמוכה יותר. (גם `GetComponent<EnemyInsistence>` בכל יצירה ב-Spawner.)
- **ליטוש מטבעות (לא נעשה):** מגנט (נמשכים לשחקן) ונעלמים אחרי 30 שניות. ספרייטים למטבע כסוף וזהב.
- **עברית או אנגלית:** להחליט. עברית = פונט עברי ל-TextMeshPro + RTL (למשל RTLTMPro).
- **גודל הדמויות: 16×24** (1×1.5 יחידות). צ'יפס קטן יותר, המבורגר נמוך ורחב, הבוס גדול יותר (בערך 20×30).
- **נשקים, דוגמאות מ-Vampire Survivors:** טעינה ארוכה = נזק גבוה. כל רמה משפרת דבר אחד, ו"עוד קליע" רק כל כמה רמות. 3 נשקים שונים מאוד: סכין (לקרוב), מחבת (מסתובבת), סיר (אזור).
- **פסיבי "ידיים מהירות"** (−8% טעינה): הקוד קיים (`PlayerStats.DecreaseFireInterval`), עוד אין לו קלף.
- **קלפים של נשק ברמה מקסימלית (18.11):** בסכין ברמה 5 הקלף עדיין מופיע, והלחיצה לא עושה כלום. במערכת הקלפים המלאה: להוציא מההגרלה פריטים שהגיעו למקסימום.
- **סכין אחת מעל אחרת:** כשיש יעד אחד וכמה סכינים, הן עפות אחת על השנייה. ליטוש: עיכוב קטן או זווית.
- 🆕 **`RandomLook` + Animator:** ה-Animator יקבע את הספרייט בכל פריים וידרוס את הבחירה. כשמוסיפים Animator: לבחור באקראי **בקר אנימציה** (`AnimatorOverrideController`) במקום ספרייט.
- 🆕 **`RandomLook` עם רשימה ריקה:** `Random.Range(0, 0)` מחזיר 0, ואז `sprites[0]` זורק שגיאה. כדאי בדיקה (ולא `sprite = null`, שהופך את האויב לשקוף).
- 🆕 **`KnifeProjectile`:** ב-`Rigidbody2D` מסומן Freeze Rotation Z. אם הסכין "קופצת" חזרה לשכיבה, להוריד את הסימון (הקליע Kinematic, אז זה בטוח).
- 🆕 **`GameTimer`:** ברירת המחדל בקוד היא 300, ובסצנה 900. אפשר לעדכן את הקוד ל-900.
- 🆕 **`WaveDirector`:** אסור 0 או מספר שלילי במרווח (אין רצפה בקוד).
- **אחרי ה-Pixel Perfect Camera, לבדוק:** גודל הטקסט הצף ביחס לדמויות (Font Size בפריפאב `Floating Text`). אם הספרייטים רועדים כשהמצלמה זזה: Grid Snapping = Pixel Snapping.
- 🆕 **פתוח:** שם המשחק, האם צריך אישור מהמרצה על החלפת הנושא, והסיפור.
- **Git:** commit בסוף כל שלב, push בסוף היום. `.claude/` נמצא ב-Git. (במחשב הזה Git לפעמים מתלונן על "dubious ownership"; ה-push לפעמים "נתקע" בסוף למרות שהצליח: `git fetch` ואז `git status`.)

---

## 🗓️ יומן קומיטים (18–23.11)
מקשי דיבאג ← `PlayerStats` ← `WeaponBase` ← רמות ← כמה קליעים ← `WeaponData` ← טבלת רמות ← קציצות ← סידור תיקיות ← `EnemyData` ← XP מהכרטיס ← נוסחת XP ← `WaveDirector` ← Spawner מ-`WaveDirector` ← התחזקות לפי דקה ← תקרת 250 ← שף ופיצה ← סכין ומטבע ← טעמי פיצה.

---

## ⬜ מה הלאה
**ההמלצה של Claude לסדר (23.11):**
1. **Animator** לשף ולפיצה (חובה בקורס): כבר יש 4 פריימים. כולל המעבר של `RandomLook` לבקרי אנימציה.
2. **נשק שני: מחבת מסתובבת.** הבדיקה האמיתית של `WeaponBase` עם התנהגות שונה. אחר כך סיר.
3. **אויב שני: המבורגר.** כאן בונים סוגים ואחוזים ב-`WaveDirector`, ו-Pool לכל סוג.
4. **מערכת קלפים מלאה** (נשק חדש / שדרוג / פסיבי, בלי פריטים ברמה מקסימלית).
5. **המפה** (שבוע 2–3): רצפה, גבולות, איים קבועים, פיזור אקראי, ארגזים, בר סלטים.
6. **גרפיקה** (Claude, במקביל): המבורגר, מחבת, רצפה וחפצים למפה.
7. לפי תוכנית ההפקה (GDD סעיף 13).
