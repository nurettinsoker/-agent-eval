# Agent-Eval Tanıtım Sayfası / Landing Page

## 🇹🇷 TÜRKÇE

---

## **Agent-Eval Nedir?**

**Agent-Eval**, yapay zeka ajanlarınızın (AI agents) performansını test etmek ve değerlendirmek için tasarlanmış açık kaynak bir platformdur.

### **Basit Deyişle:**
Eğer ChatGPT, Claude veya OpenAI API kullanan bir AI uygulaması geliştiriyorsanız, Agent-Eval size bu uygulamayı **otomatik olarak test etme** ve **sonuçlarını görselleştirme** imkanı verir.

---

## **Nasıl Çalışır?**

### **1. Test Hazırlama**
Bir YAML veya JSON dosyasında test sorularınızı yazarsınız:
```yaml
test_cases:
  - name: math_test
    input: "2 + 2 kaça eşittir?"
    expected_output: "4"
```

### **2. AI Ajanını Çalıştırma**
Agent-Eval CLI aracını kullanarak:
- AI ajandan soruyu sorar
- Cevabı kaydeder
- Birden fazla test sorusunu otomatik olarak çalıştırır

### **3. Cevapları Değerlendirme**
Cevapları 5 farklı metotla kontrol eder:

| Metot | Ne İşe Yarar | Örnek |
|-------|-------------|-------|
| **Tam Eşleşme** | Cevap tamamen aynı mı? | "Paris" == "Paris" ✅ |
| **Anlamsal Benzerlik** | Cevaplar anlam olarak benzer mi? | "Fransa'nın başkenti" ≈ "Paris" ✅ |
| **LLM Hakim** | Başka bir AI ile değerlendir | Başka AI: "Cevap doğru" ✅ |
| **Regex** | Kalıp eşleştirmesi | Cevap formata uyuyor mu? |
| **Kod Yürütme** | Kod çalıştırılabilir mi? | Python kodu doğru çalışıyor mu? |

### **4. Sonuçları Görüntüleme**
Web dashboard'da:
- ✅ Başarılı testler
- ❌ Başarısız testler
- 📊 Başarı yüzdesi
- 📈 Performans grafikleri

---

## **Neden Kullanmalısınız?**

**Örnek Senaryo:**
Bir customer support chatbot geliştiriyorsunuz:

```
1️⃣ 100 test sorusu hazırlarsınız
2️⃣ Agent-Eval'i çalıştırırsınız (1 komut ile)
3️⃣ Tüm sorulara verilen cevapları otomatik değerlendirir
4️⃣ Hangi sorularda başarısız olduğunu görebilirsiniz
5️⃣ Model değiştirir, tekrar test edersiniz
6️⃣ En iyi performans gösteren modeli seçersiniz
```

---

## **Temel Özellikler**

| Özellik | Açıklama |
|---------|----------|
| **CLI Motoru** | Komut satırından testleri çalıştır |
| **Çok Sağlayıcı Desteği** | OpenAI, Anthropic, kendi API'n, test modu |
| **5 Değerlendirme Tipi** | Farklı kontrol yöntemleri |
| **Web Dashboard** | Sonuçları güzel bir arayüzde gör |
| **Toplu Kontrol** | 100-1000 testleri hızlı çalıştır |
| **JSON Dışa Aktarma** | Sonuçları kaydet, analiz et |
| **Mock Agent** | API key olmadan test et |

---

## **Pratik Kullanım Örnekleri**

### **1. Chatbot Test Etme**
```
Test: "Merhaba!"
Beklenen: Bot cevap versin
```

### **2. Arama Motoru Testi**
```
Test: "Python programlamada async nedir?"
Beklenen: Alakalı sonuçlar dönüş yapsın
```

### **3. Kod Üretici Testi**
```
Test: "Fibonacci sayıları hesapla"
Beklenen: Çalışan Python kodu
```

### **4. Tercüman Test Etme**
```
Test: "Merhaba dünya" (Türkçe)
Beklenen: "Hello world" (İngilizce)
```

---

## **Teknik Mimari**

```
┌─────────────────┐
│  Test Dosyaları │  (YAML/JSON)
│  - Sorular      │
│  - Beklenen     │
│  - Etiketler    │
└────────┬────────┘
         │
    ┌────▼────────────────────┐
    │   Agent-Eval CLI        │
    │  (Python + Asyncio)     │
    └────┬───────────┬────────┘
         │           │
    ┌────▼──┐   ┌────▼──────────────┐
    │ AI    │   │ Değerlendirici    │
    │ Ajan  │   │ (5 tür)           │
    └────┬──┘   └────┬──────────────┘
         │           │
    ┌────▼───────────▼────┐
    │  Sonuç Verisi       │
    │  (JSON/CSV)         │
    └────┬────────────────┘
         │
    ┌────▼──────────────┐
    │  Web Dashboard    │
    │  (Next.js)        │
    │  📊 Grafikler     │
    │  📈 Raporlar      │
    └───────────────────┘
```

---

## **Kimleri İçin?**

✅ **AI Ürün Geliştirici** - "ChatGPT arayüzüm iyi çalışıyor mu?"
✅ **Startup** - "Hangi model en iyisi?"
✅ **Araştırmacı** - "Model A vs Model B hangisi?"
✅ **DevOps Mühendisi** - "Deployment öncesi test etmek istiyorum"
✅ **QA Mühendüsü** - "Otomatik test yapmak istiyorum"

---

## **Faydalı Kullanım Durumları**

1. **Model Seçimi** - OpenAI, Anthropic, Google modelleri karşılaştır
2. **Prompt Optimizasyon** - Hangi prompt daha iyi sonuç veriyor?
3. **Performans İzleme** - Model kalitesini zaman içinde izle
4. **Regresyon Testi** - Yeni versiyon eski testleri geçiyor mu?
5. **Kalite Metrikleri** - Doğruluk, hız, maliyet analizi

---

## **Hızlı Başlangıç (Türkçe)**

```bash
# Kurulum
pip install -e .

# Proje oluştur
agent-eval init my-project

# Testleri çalıştır (API key'siz)
agent-eval run my-project/suite.yaml --agent my-project/agent.yaml

# Sonuçları dashboard'da göster
agent-eval run my-project/suite.yaml --agent my-project/agent.yaml --push
```

---

---

## 🇬🇧 ENGLISH

---

## **What is Agent-Eval?**

**Agent-Eval** is an open-source platform designed to test and evaluate the performance of your AI agents (LLM-powered applications).

### **In Simple Terms:**
If you're building an AI application using ChatGPT, Claude, or OpenAI API, Agent-Eval gives you the ability to **automatically test your application** and **visualize the results**.

---

## **How Does It Work?**

### **1. Prepare Tests**
Write your test questions in a YAML or JSON file:
```yaml
test_cases:
  - name: math_test
    input: "What is 2 + 2?"
    expected_output: "4"
```

### **2. Run Your AI Agent**
Using Agent-Eval CLI:
- Ask questions to your AI agent
- Capture the responses
- Automatically run multiple test cases

### **3. Evaluate Responses**
Validate answers using 5 different methods:

| Method | Purpose | Example |
|--------|---------|---------|
| **Exact Match** | Is the answer exactly the same? | "Paris" == "Paris" ✅ |
| **Semantic Similarity** | Are answers semantically similar? | "Capital of France" ≈ "Paris" ✅ |
| **LLM Judge** | Evaluate using another AI | Another AI: "Answer is correct" ✅ |
| **Regex** | Pattern matching | Does answer match the format? |
| **Code Execution** | Is the code executable? | Does Python code run correctly? |

### **4. View Results**
On the web dashboard:
- ✅ Passed tests
- ❌ Failed tests
- 📊 Success percentage
- 📈 Performance graphs

---

## **Why Use It?**

**Example Scenario:**
You're developing a customer support chatbot:

```
1️⃣ Prepare 100 test questions
2️⃣ Run Agent-Eval (1 command)
3️⃣ Automatically evaluates all responses
4️⃣ See which questions failed
5️⃣ Switch models, test again
6️⃣ Select the best performing model
```

---

## **Key Features**

| Feature | Description |
|---------|-------------|
| **CLI Engine** | Run tests from command line |
| **Multi-Provider Support** | OpenAI, Anthropic, custom API, mock mode |
| **5 Evaluation Types** | Different validation methods |
| **Web Dashboard** | Beautiful results visualization |
| **Batch Testing** | Run 100-1000 tests quickly |
| **JSON Export** | Save and analyze results |
| **Mock Agent** | Test without API keys |

---

## **Practical Use Cases**

### **1. Chatbot Testing**
```
Test: "Hello!"
Expected: Bot responds
```

### **2. Search Engine Testing**
```
Test: "What is async in Python?"
Expected: Relevant results returned
```

### **3. Code Generator Testing**
```
Test: "Calculate Fibonacci numbers"
Expected: Working Python code
```

### **4. Translator Testing**
```
Test: "Hello world" (English)
Expected: "Bonjour le monde" (French)
```

---

## **Technical Architecture**

```
┌─────────────────┐
│  Test Files     │  (YAML/JSON)
│  - Questions    │
│  - Expected     │
│  - Tags         │
└────────┬────────┘
         │
    ┌────▼────────────────────┐
    │   Agent-Eval CLI        │
    │  (Python + Asyncio)     │
    └────┬───────────┬────────┘
         │           │
    ┌────▼──┐   ┌────▼──────────────┐
    │ AI    │   │ Evaluators        │
    │ Agent │   │ (5 types)         │
    └────┬──┘   └────┬──────────────┘
         │           │
    ┌────▼───────────▼────┐
    │  Result Data        │
    │  (JSON/CSV)         │
    └────┬────────────────┘
         │
    ┌────▼──────────────┐
    │  Web Dashboard    │
    │  (Next.js)        │
    │  📊 Charts        │
    │  📈 Reports       │
    └───────────────────┘
```

---

## **Who Is It For?**

✅ **AI Product Developer** - "Is my ChatGPT interface working well?"
✅ **Startup** - "Which model is the best?"
✅ **Researcher** - "Model A vs Model B?"
✅ **DevOps Engineer** - "I want to test before deployment"
✅ **QA Engineer** - "I want automated testing"

---

## **Useful Use Cases**

1. **Model Comparison** - Compare OpenAI, Anthropic, Google models
2. **Prompt Optimization** - Which prompt gives better results?
3. **Performance Monitoring** - Track model quality over time
4. **Regression Testing** - Does new version pass old tests?
5. **Quality Metrics** - Accuracy, speed, cost analysis

---

## **Quick Start (English)**

```bash
# Installation
pip install -e .

# Create project
agent-eval init my-project

# Run tests (no API key needed)
agent-eval run my-project/suite.yaml --agent my-project/agent.yaml

# Push results to dashboard
agent-eval run my-project/suite.yaml --agent my-project/agent.yaml --push
```

---

## **Comparison with Alternatives**

| Feature | Agent-Eval | Langsmith | Others |
|---------|-----------|-----------|--------|
| **Open Source** | ✅ | ❌ | Varies |
| **Self-Hosted** | ✅ | ❌ | ✅ |
| **5 Grader Types** | ✅ | Limited | Limited |
| **CLI Tool** | ✅ | Limited | Varies |
| **Free** | ✅ | Limited | Varies |
| **Easy Setup** | ✅ | ❌ | Varies |

---

## **Tech Stack**

- **Backend**: Python 3.12+, Typer, Pydantic, asyncio
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **API**: tRPC, Prisma ORM
- **Database**: SQLite (easily switchable)
- **LLM Support**: OpenAI, Anthropic, custom HTTP

---

## **Getting Started**

For detailed documentation, visit the [main README](./README.md)

---

## **License**

MIT
