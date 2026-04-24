# 12D — First Live Source Implementation Plan v1

## Durum
- Status: Accepted Draft
- Amaç: 12C’de tanımlanan ilk canlı source mapping ve acceptance matrisini gerçek implementasyon adımlarına çevirmek
- Hedef: ilk canlı source adapter’ı için minimum kodlama sırası, dosya yerleşimi, test planı ve teslimat sınırını netleştirmek

## 1. Implementasyon hedefi

Bu fazın hedefi şudur:

tek bir gerçek press release/news-style source için çalışan bir ingestion adapter yazmak ve bunu mevcut scheduler -> worker -> db -> classification akışına bağlamak.

Bu fazın sonunda sistem şunları yapabilmelidir:

- gerçek source’tan item çekmek
- raw payload saklamak
- canonical ingestion record üretmek
- duplicate/stale/validation uygulamak
- classification’a handoff etmek

Bu fazın sonunda henüz “çok kaynaklı sistem” hedeflenmez.

---

## 2. V1 implementasyon sınırı

### In Scope
- tek source adapter
- polling tabanlı fetch
- raw record persistence
- canonical normalize
- duplicate detection
- stale detection
- validation status
- scheduler entegrasyonu
- classification handoff
- integration/acceptance test

### Out of Scope
- multi-source fan-in
- source ranking
- UI genişlemesi
- explainable commentary text
- cross-source clustering
- historical backfill engine
- admin panel
- source management UI

---

## 3. Dosya/dizin planı

V1 için önerilen minimum yerleşim:

- `src/app/services/ingestion/`
- `src/app/services/ingestion/adapters/`
- `src/app/services/ingestion/normalization.py`
- `src/app/services/ingestion/dedupe.py`
- `src/app/services/ingestion/validation.py`
- `src/app/services/ingestion/types.py`
- `src/app/services/ingestion/service.py`

Source adapter için:

- `src/app/services/ingestion/adapters/press_release_feed.py`

Scheduler bağlantısı için mevcut scheduler katmanında:

- source polling çağrısını buraya bağlayan minimal orchestration

Testler için:

- `tests/services/ingestion/test_press_release_feed_adapter.py`
- `tests/services/ingestion/test_ingestion_normalization.py`
- `tests/services/ingestion/test_ingestion_dedupe.py`
- `tests/integration/test_live_source_ingestion_flow.py`

---

## 4. Minimum veri modelleri

V1’de aşağıdaki mantıksal veri yapıları gerekir:

### 4.1 FetchRun
Alanlar:
- `fetch_run_id`
- `source_name`
- `run_started_at`
- `run_finished_at`
- `run_status`
- `records_fetched`
- `records_accepted`
- `records_rejected`
- `records_quarantined`
- `records_duplicated`
- `error_summary`

### 4.2 RawSourceRecord
Alanlar:
- `raw_record_id`
- `source_name`
- `source_record_id`
- `fetch_run_id`
- `fetched_at`
- `source_url`
- `raw_payload`
- `content_hash`
- `adapter_version`

### 4.3 CanonicalIngestionRecord
Alanlar:
- `record_id`
- `source_name`
- `source_record_id`
- `source_url`
- `title`
- `body_text`
- `published_at`
- `ingested_at`
- `processed_at`
- `primary_ticker`
- `company_name`
- `language`
- `content_hash`
- `dedupe_key`
- `is_duplicate`
- `is_stale`
- `validation_status`
- `quality_flags`
- `raw_record_ref`
- `normalization_version`

---

## 5. Adapter sınıfı / fonksiyon sınırı

Adapter şu minimal fonksiyonları sunmalıdır:

- `fetch_since(cursor_or_time)`
- `parse_feed(response_text)`
- `extract_items(parsed_feed)`
- `compute_source_record_id(item)`
- `build_raw_record(item, fetch_run_id, fetched_at)`
- `normalize_item(item, fetched_at)`
- `compute_content_hash(normalized)`
- `compute_dedupe_key(normalized)`
- `classify_validation_status(normalized)`

Bu fonksiyonlar tek dosyada başlayabilir; erken abstraction zorunlu değildir. Ancak adapter mantığı worker içinden ayrılmış olmalıdır.

---

## 6. Implementasyon sırası

### Adım 1 — Types / contracts
Önce ingestion types yazılır:
- raw record tipi
- canonical record tipi
- validation status enum/constant set
- quality flags standardı

### Adım 2 — Feed parser
Seçilen source için:
- HTTP fetch
- RSS/Atom parse
- item extraction

### Adım 3 — Raw persistence
Her item için raw record oluşturulup saklanır.

### Adım 4 — Normalization
Source item -> canonical ingestion record mapping yapılır.

### Adım 5 — Validation / dedupe / staleness
Canonical kayıt üstünde:
- duplicate
- stale
- validation status
hesaplanır.

### Adım 6 — DB persist
Canonical kayıtlar kaydedilir.

### Adım 7 — Classification handoff
Accepted veya accepted_with_flags kayıtlar classification pipeline’a verilir.

### Adım 8 — Scheduler integration
Polling run scheduler’dan tetiklenir.

### Adım 9 — Integration test
Raw -> canonical -> handoff zinciri test edilir.

---

## 7. Scheduler entegrasyon planı

Scheduler tarafında ayrı orchestration fonksiyonu olmalıdır.

Örnek mantık:
- scheduler tick
- source enabled mi kontrol et
- fetch run başlat
- adapter fetch etsin
- batch işlensin
- fetch run result yazılsın

### Kural
Scheduler business parsing yapmaz.  
Yalnızca run tetikler ve sonucu kaydeder.

---

## 8. Worker / service akışı

Worker/service içinde minimum akış:

1. fetch run başlat
2. source’tan item’ları al
3. her item için raw record oluştur
4. normalize et
5. validation/dedupe/staleness hesapla
6. persist et
7. classification handoff yap
8. run summary üret

### Kural
Bir item bozuldu diye tüm batch çökmez.  
Per-item resilience korunur.

---

## 9. Dedupe implementasyon planı

İlk sürümde dedupe şu sırayla uygulanır:

1. `source_name + source_record_id`
2. `content_hash`

Near duplicate heuristic ilk implementasyonda opsiyoneldir.  
Varsa sadece flag üretir, ana drop kararı exact duplicate kadar sert olmaz.

---

## 10. Validation implementasyon planı

Validation minimum şu kararları verir:

- `accepted`
- `accepted_with_flags`
- `quarantined`
- `rejected`

Kontroller:
- source identity var mı
- title usable mı
- body usable mı
- published_at parse edildi mi
- payload normalize edilebildi mi

---

## 11. Config planı

Yeni config alanları:

- `LIVE_SOURCE_ENABLED`
- `LIVE_SOURCE_URL`
- `LIVE_SOURCE_POLL_INTERVAL_SECONDS`
- `LIVE_SOURCE_TIMEOUT_SECONDS`
- `LIVE_SOURCE_MAX_ITEMS_PER_RUN`
- `LIVE_SOURCE_STALENESS_THRESHOLD_SECONDS`

### Kural
Source URL ve polling değerleri kod içine gömülmez.

---

## 12. Test planı

### Unit test
- source_record_id üretimi
- title/body normalize
- published_at parse
- content_hash üretimi
- dedupe key üretimi

### Service test
- duplicate item skip
- stale item flag
- missing ticker accepted_with_flags
- invalid timestamp quarantine/reject

### Integration test
- gerçekçi örnek feed payload
- fetch -> raw -> canonical -> handoff
- batch partial failure davranışı

---

## 13. Minimum acceptance test listesi

Aşağıdaki senaryolar yeşil olmalıdır:

1. normal yeni PR item accepted
2. exact duplicate item downstream’e tekrar gitmez
3. ticker missing item reject olmaz
4. invalid timestamp item quarantine/reject olur
5. stale item doğru flag alır
6. description-only item accepted_with_flags olabilir
7. partial batch failure iyi item’ları düşürmez

---

## 14. Done criteria

Bu implementasyon ancak şu durumda done sayılır:

- gerçek source’tan veri çekiliyor
- raw persistence çalışıyor
- canonical ingestion record oluşuyor
- duplicate çalışıyor
- stale çalışıyor
- validation status çalışıyor
- classification handoff çalışıyor
- en az bir integration test geçiyor
- scheduler run summary gözlenebiliyor

---

## 15. İlk teslimat stratejisi

İlk PR/commit serisi şu sırayla gitmelidir:

1. ingestion types + basic models
2. feed adapter + parser
3. normalization + validation + dedupe
4. persistence + scheduler integration
5. integration tests
6. acceptance hardening / cleanup

### Kural
Tek dev commit yerine küçük ama çalışan slice’lar tercih edilir.

---

## 16. Sonraki adım

Bu plan onaylandıktan sonraki doğrudan uygulama adımı:

**13A — First Live Source Adapter Coding Slice v1**

İlk kod slice’ının hedefi:
- adapter iskeleti
- config alanları
- basic fetch/parse
- raw record üretimi

## Kısa sonuç

Bu plan, ilk canlı source adapter’ın hangi dosyalarda, hangi sırayla ve hangi kabul kapılarıyla implement edileceğini netleştirir. V1 hedefi, çalışan tek-source canlı ingestion omurgasıdır.
