📚 **BookFinder AI Discord Bot - AI-kurs Projekt**

**👤 Student:** Chia213  
**📧 Mejladress:** chiaranchber@gmail.com  
**🎯 Syfte:** Utveckla en Discord BookFinder bot som använder AI för att hjälpa användare hitta böcker baserat på beskrivningar och preferenser. Boten ska förstå naturligt språk och leverera relevanta bokförslag.

**🔗 Projektlänkar:**
- **GitHub:** https://github.com/Chia213/bookfinder-ai-discord-bot
- **Trello:** https://trello.com/b/pHmuUaZS/bookfinder-ai-discord-bot *(Begär tillgång om behövs)*

---

## 📈 **PROJEKTUPPFÖLJNING**

### **Uppdatering 2025-01-24 00:55** 🔍
**Sökprecision behöver förbättras:**
- **Upptäckt:** Sökning efter "samurai" returnerar irrelevanta resultat (Nashville musik, barnvänskap)
- **Analys:** Google Books API ger oprecisa träffar för vissa söktermer
- **Lösningsförslag:** Förbättra AI prompt engineering och query processing
- **Status:** Undersöker alternativa sökstrategier

### **Uppdatering 2025-01-23 22:30** ✅
**Core funktionalitet implementerad:**
- Discord bot framgångsrikt distribuerad med tre slash-kommandon
- `/findbook` - Söker böcker baserat på användarens beskrivning
- `/recommend` - AI-genererade bokrekommendationer 
- `/bookhelp` - Hjälp och instruktioner för användare
- Rich embeds med bokomslag och metadata fungerar korrekt

### **Uppdatering 2025-01-23 18:00** 🔧
**AI Integration slutförd:**
- OpenAI GPT-3.5 integration för intelligent bokanalys
- Custom prompts utvecklade för att förstå användarpreferenser
- Multi-API fallback system (Google Books + Open Library)
- Error handling för API-begränsningar implementerat

### **Uppdatering 2025-01-23 14:20** ⚙️
**Projektgrund etablerad:**
- Discord bot applikation skapad och konfigurerad
- Python utvecklingsmiljö uppsatt med discord.py
- API-nycklar säkert konfigurerade via environment variables
- GitHub repository strukturerat för professionell utveckling

---

## 🛠️ **TEKNISK STACK**
- **Backend:** Python 3.x
- **Discord Framework:** discord.py
- **AI Service:** OpenAI GPT-3.5-turbo
- **Book APIs:** Google Books API (primär), Open Library API (fallback)
- **Deployment:** Local development environment

## 📊 **NUVARANDE STATUS**
- ✅ **Core funktionalitet:** Fungerande
- 🔴 **Kritiskt problem:** Sökprecision behöver förbättras
- 🔄 **Nästa fokus:** Lösa search accuracy innan presentation
- 📋 **Presentation:** Förbereder demo scenarios

## 🎯 **KOMMANDE MÅL**1. Förbättra sökalgoritm för mer relevanta bokresultat2. Testa och validera förbättringar3. Förbereda presentation med working demos4. Dokumentera kända begränsningar och framtida förbättringar## 📋 **PROJEKTLEDNING****Scope Management:** Projekt håller sig inom realistiska gränser - Discord bot med AI-integration  **Risk Management:** Identifierade sökprecisionsproblem tidigt, arbetar aktivt med lösningar  **Kvalitetssäkring:** Systematisk testning av alla funktioner, dokumentation av issues  **Tidsplanering:** MVP levererat i tid, fokus på förbättringar innan presentation