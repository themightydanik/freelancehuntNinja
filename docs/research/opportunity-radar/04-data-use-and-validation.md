# Правила использования данных и контакта

## Границы пилота

Только три источника в коде: Find a Tender и TED (реальные API-снимки), Companies House (synthetic fixture). Документационные страницы и конкурентные pricing pages — исследовательские источники, не дополнительные feeds пилота. Без scraping магазинов, авторизации в чужих аккаунтах, CAPTCHA/anti-bot обходов, маркетинговых сообщений или email enrichment.

FTS JSON сам содержит [OGL v3](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/): указывать Cabinet Office / Find a Tender, не подразумевать endorsement; personal data и сторонние права не становятся свободными от ограничений. TED документация прямо предусматривает commercial reuse опубликованных notices; [legal notice](https://ted.europa.eu/en/legal-notice) нужно повторно проверить для будущего продукта и вложений третьих сторон. Подробные вложения и контакты в этот публичный PR не включены. Полный TED legal notice вернул anti-bot страницу, OGL page — 403 в web-инструменте; обходов не было. Разрешение TED на commercial analysis/reuse подтверждено доступной официальной API-документацией; детальные ограничения legal notice остаются gate коммерческого распространения. OGL URL и версия подтверждены самим FTS payload, не успешной загрузкой текста лицензии.

Сохранены: organisation name, notice ID, title, date, stage, доступные value/deadline, source link. Исключены personal names, emails, phones, street addresses и полные описания. Прототип не запрашивает и не хранит ключи. CH fixture не является настоящей компанией; никогда не смешивать её с real opportunity count.

SHA-256 в журнале относится к исходному HTTP body, который намеренно не закоммичен из-за минимизации. Это контрольная сумма, а не возможность восстановить body или доказательство независимой верификации. JSON-снимки минимизированы и воспроизводимы offline; source URL и время запросов позволяют повторно проверить факт, пока ресурс доступен. Источники могут обновиться.

## Policy gate перед будущим контактом

Обязательные поля: страна отправителя и получателя, legal entity/subscriber type, platform/channel, цель и основание обработки, основание отправки, evidence URL/time, deadline, scope, роль контактного адреса, suppression status. Пока хотя бы одно неизвестно, `outreach_ready=false`. Опубликованный email, API scope и legitimate interest по GDPR не заменяют отдельные правила электронного маркетинга.

| Страна / канал | Рабочее правило для отдельного эксперимента | Первичный источник |
|---|---|---|
| UK / tender portal | Только действующая закупка и указанный submission/clarification process; не использовать buyer email для сторонней рекламы. Проверить документы, supplier eligibility и portal terms | [Find a Tender](https://www.find-tender.service.gov.uk/Developer/Documentation) и конкретный notice |
| UK / корпоративный email | ICO различает corporate и individual subscribers. Для corporate electronic mail PECR consent обычно не требуется, но необходимо установить тип, учитывать UK GDPR при personal data, идентифицировать отправителя, дать opt-out и вести suppression. Sole traders/некоторые partnerships — другой режим; при неизвестном типе только consent/применимая законная оговорка | [ICO B2B](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/business-to-business-marketing/) |
| Польша / email, сообщения, звонки | Консервативный эксперимент: предварительное согласие на direct marketing по PKE art. 398; B2B/публичный адрес не считать общим исключением. Запросить актуальный consolidated text перед отправкой | [PKE, закон 12.07.2024](https://isap.sejm.gov.pl/isap.nsf/download.xsp/WDU20240001221/O/D20241221.pdf), art. 398 |
| Германия / email | Предварительное express consent, кроме узкого existing-customer exception с выполнением всех условий §7(3). Для холодного B2B email не использовать blanket legitimate-interest разрешение | [UWG §7](https://www.gesetze-im-internet.de/uwg_2004/__7.html) |
| Остальные страны / любые marketing channels | **Не допущены к этому эксперименту**, пока не проверены местные правила и трансграничная применимость. US SAM — исследованный источник, не разрешение на сообщения в США | Отдельная проверка перед включением |
| Allegro/Amazon/Etsy/eBay / seller messaging | Не использовать buyer/seller communications для рекламы агентства; доступ к API/аккаунту не разрешает это автоматически. Нужны прямое соответствие platform terms и основание на сообщение | Официальные platform API/terms из `01-marketplaces.md` |
| Shopify/Woo / merchant | Только согласившиеся владельцы или отдельно одобренный корпоративный канал; технически открытый storefront не приглашение к рекламе | Merchant agreement + применимое право |

Отправитель может находиться в другой стране; нужно проверить оба применимых режима. Этот документ не объявляет единые «правила для всей Европы». Любой эксперимент остаётся отдельным и не был проведён здесь.

## Хранение и последующие права

Для будущего операционного пилота: хранить только нужные company/task fields, ограничить доступ, назначить ответственного, установить 30-дневный review/delete срок для неквалифицированных событий (проектное решение, не универсальный statutory срок). Для возражений — минимальный suppression record, который предотвращает повторные обращения. Правила исправления/удаления personal data, attribution и licensing проверять до переноса в коммерческий продукт. Публичный Git PR неизменяемо распространяет данные через clones, поэтому контакты в него не помещать.

Companies House: [API guidelines](https://developer.company-information.service.gov.uk/developer-guidelines/) и [data products](https://www.gov.uk/guidance/companies-house-data-products); получать ключ штатно. Границы OGL и privacy повторно проверить прежде, чем делать живой company-registration radar.
