# 05. Каналы дистрибуции: 36 проверенных адресов, admission gates открыты

**Дата проверки: 2026-11-13 (Europe/Kyiv).** Метки: VERIFIED — первичный документ или воспроизводимый тест; OBSERVED — ограниченная выборка; ESTIMATED — расчёт; ASSUMED — допущение; UNKNOWN — данных недостаточно. HTTP 200 сам по себе не подтверждает API, спрос или право автоматизации.

[distribution_channels.csv](../../data/distribution_channels.csv) содержит 15 запрошенных характеристик для 36 кандидатов. «Проверен» в заголовке означает проверенный публичный адрес/ответ/часть политики, **не** подтверждённые регистрацию, выплаты, индексацию или заявки. Не создавались аккаунты и не проверялись выплаты. UNKNOWN не означает запрет Украине; но и не разрешение. Конкретная территория проживания, bank/PayPal availability, sanctions, tax status и KYC могут изменить ответ.

| ID | Канал | Тип | HTTP | Украина / ограничения | Стоимость по проверенной странице или UNKNOWN |
| --- | --- | --- | --- | --- | --- |
| D01 | Freelancehunt | freelance | 404 | conditional; regional platform; payout/KYC not tested | UNKNOWN current fee; service URL 404 |
| D02 | Upwork Project Catalog | fixed service | 200 | conditional; official excludes Crimea/DPR/LPR and sanctioned regions; other UA subject KYC | UNKNOWN current fee/Connects; pricing blocked |
| D03 | Fiverr | fixed service | 404 | UNKNOWN UA payout; moved help page | UNKNOWN fee until current terms verified |
| D04 | Contra | service portfolio | 200 | UNKNOWN UA payout rails; commission-free not eligibility proof | OBSERVED 0% freelancer commission claim; processor/platform costs separate |
| D05 | Freelancer | freelance | 200 | UNKNOWN UA KYC and payout route | OBSERVED 10% or $5 fixed fee minimum; hourly 10%; other costs possible |
| D06 | PeoplePerHour | offers | 200 | UNKNOWN UA admission/payout | UNKNOWN current tier fees; terms retrieved; withdrawal delay applies |
| D07 | Guru | freelance | 403 | UNKNOWN UA payout; pricing 403 | UNKNOWN current fees |
| D08 | Toptal | vetted talent | 200 | UNKNOWN UA admission and legal eligibility | Application available; terms/price UNKNOWN |
| D09 | Codeable | WP expert network | 404 | UNKNOWN admission; apply URL moved | UNKNOWN fee and current intake |
| D10 | Codementor | mentoring | 200 | UNKNOWN UA payout and acceptance | UNKNOWN current take rate |
| D11 | Lemon.io | vetted developers | 200 | UNKNOWN actual acceptance and payout contract | UNKNOWN rate/margin |
| D12 | Clutch | agency directory | 200 | Profile likely international; Ukraine eligibility UNKNOWN pending terms | Listing entry retrieved; paid promotion quote UNKNOWN |
| D13 | GoodFirms | agency directory | 200 | UNKNOWN specific UA restrictions | UNKNOWN free listing terms/current promotion fee |
| D14 | DesignRush | agency directory | 200 | UNKNOWN UA terms and verification | UNKNOWN free/paid admission |
| D15 | WooCommerce partners | expert ecosystem | 200 | UNKNOWN UA partner acceptance | UNKNOWN partner tiers/fees |
| D16 | Shopify partners | ecosystem | 200 | UNKNOWN UA merchant/payout route by program | Program-specific app/partner fees UNKNOWN |
| D17 | Zapier experts | integration partner | 404 | UNKNOWN UA admission; retrieved URL 404 | UNKNOWN partner requirements/fees |
| D18 | Make partners | integration partner | 200 | UNKNOWN UA admission | UNKNOWN program fee |
| D19 | n8n templates | workflow distribution | 200 | No payout needed for OSS discovery; UA program eligibility UNKNOWN | Free public templates candidate; license/creator terms verify |
| D20 | WordPress.org | plugin distribution | 200 | No payout in free directory; UA account eligibility not explicitly checked | No listing fee established by retrieved developer guide; paid features via separate offer subject rules |
| D21 | Chrome Web Store | extension | 200 | OBSERVED Ukraine listed for developer registration; payout not tested | Registration fee required; amount UNKNOWN from current extract |
| D22 | GitHub Marketplace | developer apps | 200 | UA payout UNKNOWN; public OSS repo does not require app marketplace | Free listing vs paid app financial checks differ |
| D23 | npm | OSS package | 200 | Registry publication eligibility UNKNOWN; no built-in product payout | Public-package distribution candidate; terms apply |
| D24 | PyPI | OSS package | 404 | No payout needed; current terms URL 404 | UNKNOWN current terms; public packages not lead marketplace |
| D25 | Gumroad | digital storefront | 200 | UNKNOWN UA payout; payout page rendered shell only | OBSERVED direct 10%+$0.50; Discover 30% |
| D26 | Lemon Squeezy | digital checkout | 200 | UNKNOWN UA payout: country page fetched but list not rendered | OBSERVED 5%+$0.50 base; extras possible |
| D27 | Paddle | MoR checkout | 404 | UNKNOWN current UA support; help URL 404 | UNKNOWN current fee and approval |
| D28 | Envato CodeCanyon | code marketplace | 200 | UNKNOWN current Ukraine payout/intake | UNKNOWN current author fee; author page shell |
| D29 | Product Hunt | launch community | 200 | Account eligibility UNKNOWN; no native payout needed | Launch page retrieved; paid promotions optional; terms verify |
| D30 | Indie Hackers | community | 200 | Account eligibility UNKNOWN; no payout | Community contribution; exact promotion rules verify per area |
| D31 | Reddit niche communities | community | 200 | Account access UNKNOWN; no payout needed | No listing purchase planned; subreddit-specific rules |
| D32 | AlternativeTo | software directory | 200 | UA submission eligibility UNKNOWN; no payout | Submission terms UNKNOWN; page truncated |
| D33 | G2 | B2B directory | 200 | UA listing eligibility UNKNOWN | Profile entry retrieved; exact free plan eligibility UNKNOWN |
| D34 | DEV Community | technical content | 200 | UA account eligibility UNKNOWN; no native payout required | Terms retrieved; no paid promotion planned |
| D35 | SourceForge | OSS directory | 200 | UA eligibility UNKNOWN; no direct payout assumed | Project creation page retrieved; terms review pending |
| D36 | Malt | freelance network | 200 | UNKNOWN UA contracting and country support; do not prioritize | UNKNOWN fees and supported residence |

## TOP-7 кандидатов, а не семь доказанно доступных каналов

| Приоритет | Канал | Роль | Доказательство и blocker | Go/no-go |
| --- | --- | --- | --- | --- |
| 1 | D01 Freelancehunt | Intent capture для P01/P09 | Активные technical requests OBSERVED; fees/KYC/payout не проверены | Согласовать аккаунт/тариф и цену; не строить на 2 000 UAH budget чек $500 |
| 2 | D04 Contra | Один англоязычный case/offer | Official commission-free page; UA payouts UNKNOWN | Проверить реальные processor/platform charges и payout route |
| 3 | D02 Upwork Project Catalog | Buyer search для scoped package | Official eligibility допускает не все территории; pricing заблокирован | Ручная актуальная fee/Connects/KYC проверка владельцем |
| 4 | D34 DEV | Technical explanation → demo → inquiry | Terms page retrieved; нет встроенного потока покупателей | Один качественный tutorial, UTM и только добровольная заявка |
| 5 | D19 n8n templates | Implementation proof/discovery | Template directory retrieved; creator/commercial terms ещё gate | Убедиться в license; один полезный credential-free artifact |
| 6 | D18 Make partner path | Agency referrals позже | Partners page retrieved; approval UNKNOWN | Не тратить на сертификацию до двух кейсов и подтверждения admission |
| 7 | D15 WooCommerce ecosystem | P02 agency specialization | Partner page retrieved; acceptance UNKNOWN | Подтвердить WP competence, review requirements и country eligibility |

Замена D02 при платном входе/непройденном KYC — D03 только после проверки payouts; не обещаем бесплатные bids/traffic. D12 Clutch — позже с реальными кейсами/отзывами, а не как источник первых быстрых заявок. D25–D27 MoR/checkout — **не acquisition channels по умолчанию**; Gumroad Discover — отдельный 30% fee без гарантированного показа. npm/PyPI — distribution кода, не merchant checkout. Product Hunt — launch event, не recurrent demand engine.

## Первые клиенты без отзывов (план, не действие)

Нужен честный transferable proof: synthetic broken→recovered scenario, видео ≤90s, acceptance checklist, clear fixed scope, публичный executable fixture, English/Ukrainian copy и explicit limitations. Не приписывать client names/logos/revenue; помечать demo как synthetic. Первый pilot можно предложить по ограниченной экспериментальной цене, не в обмен на fake review и не с обещанием любого результата.

Начать с **двух** каналов максимум: один buyer-intent marketplace после eligibility gate + один контент/портфель. Owner разрешает публикации отдельно. 12–16h на assets/первые профили — ASSUMED; дальше недельный budget 4–6h. Совокупные profile-hours из CSV не план к выполнению: десятки регистраций расходуют всю мощность.

Измерения: exposure → click → qualified inquiry → meeting → scope accepted → paid → accepted → repeat. Qualified = проблема в scope, есть полномочный buyer, ориентир бюджета и срок, client grants access. Канал без impression analytics: считать tracked visits и inquiries, **не придумывать** impressions. UTM source + pseudonymous lead ID, consented minimal contact отдельно. Цена, страна, слова запроса, listing age и response time — экспериментальные факторы.

## Время и материалы

Для каждого канала CSV задаёт ASSUMED часы создания профиля, материалы/verification, допустимые типы офферов, automation gate, measurement/duplication plan. Оценки не включают ожидание approval, KYC, ревью приложения, сроки выплат и создание самого продукта. Один canonical offer + локализованная copy; не 36 одинаковых profiles. Не автоматизировать регистрации, публикации, offers, proposals, reviews, voting и сообщения без отдельного разрешения и проверки правил.

## Неподтверждённые страны/выплаты

Chrome Web Store registration page явно перечисляет Ukraine (OBSERVED); это не подтверждает коммерческий payout. Upwork eligibility явно исключает отдельные территории и sanctioned regions; это не blanket ban всей Украине. Lemon Squeezy countries page загрузилась, но список payouts не извлёкся; Gumroad payout page — shell; Paddle URL 404. Не обходить challenge и не выводить положительное eligibility заключение из пустой страницы. До paid product launch владелец должен проверить страну/банк/юридический статус в официальном merchant onboarding и предоставить **статус**, а не секреты.
