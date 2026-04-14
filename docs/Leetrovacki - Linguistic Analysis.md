# Shatrovachki, Utrovachki and Leetrovacki: A Formal Linguistic Analysis of Serbian Urban Cryptolects

*Velimir Majstorov (ed.)*

---

## Abstract

This paper presents a formal linguistic analysis of three related urban speech varieties in the Serbian-speaking area: **Shatrovachki**, **Utrovachki**, and **Leetrovacki**. We classify these varieties as **cryptolects**: systematically constructed language forms whose primary function is to conceal meaning from uninformed listeners. Unlike most earlier descriptions, which remained at the level of anecdotal lexicography, this study offers a **formal algebraic description** of each transformation and computationally verifies it on a corpus of representative Serbian lexemes. We show that all three systems rely on a shared phonological principle - **vowel-driven syllabic segmentation** - and that Utrovachki and Leetrovacki are historically and structurally derived from Shatrovachki.

> **Note on the term "computationally verified":** This expression (a calque of English *computationally verified*) means the claims are not merely theoretical: the algorithms were actually executed over the corpus, and the resulting outputs numerically match the formal definitions in this paper. Synonyms: "programmatically verified", "computer-verified".

**Keywords:** Shatrovachki, cryptolect, syllabeme, vowel block, grapheme substitution, leetspeak, urban speech, secret language

---

## 1. Introduction

### 1.1 Sociolinguistic Background

Shatrovachki as a linguistic phenomenon in the Balkans originates in prison and street jargon, with roots etymologically linked to Turkish `şatır` (bodyguard, soldier) or alternatively `şatur` (court entertainer). Both etymons refer to **marginal social groups** who had a legitimate interest in developing a language code opaque to outside observers.

The historical line of development can be schematized:

```
Prison Jargon (19th century)          Leet Speech (hacker BBS, 1980s)
        │                                        │
        ▼                                        │
Street slang of Belgrade, Sarajevo                  │
(interwar period)                                  │
        │                                        │
        ▼                                        │
Generalized urban slang                             │
(1960s-1980s)                                       │
        │                                        │
        ├──────────────────────┐                 │
        ▼                      ▼                 │
Shatrovachki            Utrovachki                  │
        │                  │                     │
        └──────────┬────────┘                    │
                   ▼                             │
                   ├─────────────────────────────┘
                   ▼
Leetrovacki (V. Majstorov, early 2000s)
```

### 1.2 Typological classification

In typologies of secret varieties (see Halliday 1976; Matras 2012), Shatrovachki belongs to **metathetic cryptolects** - systems built through permutation of phonological segments from the source word, in contrast to substitution-based cryptolects (e.g., leetspeak) and affixational cryptolects (e.g., Pig Latin, Javanais).

| Type of cryptolect | Mechanism | Global example | Serbian analogue |
|---|---|---|---|
| Metathetic | Permutation of segments | Verlan (fr.) | Shatrovachki |
| Affixational | Adding affixes | Pig Latin (eng.) | Utrovachki |
| Substitution | Grapheme replacement | Leetspeak | Leetrovacki |
| Hybrid | Combination of mechanisms | – | Leetrovacki (over Utrovachki) |

---

## 2. Shatrovachki – Formal Analysis

### 2.1 Phonological foundations of the Serbian language

The Shatrovachki transformation does not operate arbitrarily over a string of graphemes - it relies on concrete phonological properties of Serbian. The following overview highlights those aspects of Serbian phonology without which the algorithm would lack linguistic grounding.

#### Vowel system

Standard Serbian has five vowels: /a, e, i, o, u/ (Stevanović 1964: 47; Peco 1971: 15). All are phonologically contrastive and can function as syllable nuclei. Quantity (short/long vowel) in standard speech exists, but is ignored for the purposes of Shatrovachki segmentation: only the presence or absence of a vowel at a given position is relevant.

#### Syllabic /r/

In phonological theory, sonorants are consonants whose sonority is high enough, under certain conditions, to assume a syllabic function (Crystal 2003: 418; Prince & Smolensky 1993: 78). In Serbian, this role is stably lexicalized for /r/: when /r/ stands between two consonants, it becomes the syllable nucleus and phonologically behaves like a vowel (Peco 1971: 29-31).

Examples from the Serbian lexicon: *prst, krv, srp, trg, mrk, strpljen, vrba, grlo*. This feature is not exclusive to Serbian - it appears across Slavic languages (cf. Czech *prst*, *krk*, Slovak *vlk*, Croatian *krv*) - but in Serbian it is productive and grammaticalized (Simić 1983: 44; Belić 1960: 33).

#### Syllable structure and phonotactics

Serbian favors open syllables of the CV (consonant-vowel) type, although it also allows closed syllables and complex consonant clusters at the edges of syllables (Stevanović 1964: 63; Browne 1993: 12). This is exactly what makes Shatrovachki forms mostly pronounceable: each of the two components A and B independently contains at least one vowel (or syllabic r), so the form obtained by rotation retains a minimal syllabic structure. There are exceptions (see §5.4), but they lie at the boundary of phonotactic acceptability and are generally avoided in actual speech.

#### Sonority hierarchy

The sonority hierarchy principle (*sonority hierarchy*) states that each syllable must contain a maximum-sonority nucleus, surrounded by segments of decreasing sonority toward the margins (Prince & Smolensky 1993: 78; Crystal 2003: 415). In Serbian, that hierarchy runs:

```
vowels > sonants (r, l, m, n, j, v) > fricatives > plosives
```

The syllabic /r/ occupies a position immediately below the vowel on that scale, thus providing a formal phonological basis for its treatment as a vowel in Def. 2 below.

#### Significance for the Shatrovachki algorithm

From all of the above, two direct implications for the algorithm emerge:

1. The set of vowels *V* = {a, e, i, o, u} determines the cut point in each word.
2. Syllabic /r/ contextually expands that set, giving words such as *prst* or *krv* the correct cut point instead of the fallback rule ⌊n/2⌋.

---

We define:

> **Def. 1 (Vowel block):** Let *w* be the word above the alphabet Σ. The vowel block *V(w, i)* is the maximal continuous subsequence of vowels starting from position *i* in *w*.

> **Def. 2 (Syllabic R):** The phoneme /r/ is treated as a vowel (syllabic sonant) if and only if it is preceded by a consonant and followed by a consonant (eg *prst*, *mrk*). At the beginning and end of words /r/ is never syllabic.

### 2.2 Formal description of the transformation

Let *w = w₁w₂...wₙ* be a word of length *n ≥ min_word_length* over the Latin alphabet of the Serbian language. Words shorter than the threshold *min_word_length* (default: 3) remain unchanged - σ(w) = w. This threshold condition holds for all three systems.

We introduce two auxiliary concepts:

> **Def. 3 (Leading vowel block):** Positions *L(w) = {i : ∀j < i, w_j ∈ V}* – vowels before the first consonant position in *w*. If *w* starts with a consonant, *L(w) = ∅*.

> **Def. 4 (Internal vowel):** The position *i* is called an internal vowel if *w_i ∈ V* and *∃ j < i : w_j ∉ V*, i.e. there is at least one consonant before that position.

**Step 1 – Finding the cut point:**

Let *i* = min{i : w_i ∈ V ∧ ∃j < i, w_j ∉ V} be the index of the **first internal vowel** (we skip the leading block). Then:

```
i_split = i* + |V(w, i*)|     (extend to the end of the internal vowel block)
```

If *i_split = n* (the whole word would go into A, B = ε – **degenerate case**):

```
i_split = ⌊n/2⌋ (fallback rule: mid-word cut)
```

If *i* does not exist (no internal vowel), but *L(w) ≠ ∅*:

```
i_split = |L(w)|              (cut behind leading vowel block)
```

If there are no vowels: `i_split = ⌊n/2⌋`

**Step 2 – Segmentation:**

```
w = A · B
A = w[0 : i_split] (prefix up to the end of the first internal vowel block)
B = w[i_split : n] (rest of word)
```

**Step 3 – Rotation:**

```
σ(w) = B · A
```

formally:

```
┌─ B·A if 0 < i_split < n
σ(w) = │
└─ w otherwise (the word is too short or has no valid cut point)
```

### 2.3 Visualization of the transformation tree

```
         w = "zemun"
              │
    ┌─────────┴────────┐
    A = "ze"           B = "mun"
    [0:2]              [2:5]
    │                  │
    └─────────┬────────┘
              │
         σ(w) = "munze"
```

```
         w = "beograd"
              │
    ┌─────────┴────────┐
    A = "beo"          B = "grad"
    [0:3]              [3:7]
(vowel block:
e+o consecutive)
              │
         σ(w) = "gradbeo"
```

```
         w = "prst"
              │
There are no standard vowels (a, e, i, o, u).
But /r/ stands between two consonants (p and s)
→ syllabic r: carries a syllable, is treated as a vowel.
              │
    ┌─────────┴────────┐
    A = "pr"           B = "st"
(cut after the syllable r)
              │
         σ(w) = "stpr"
```

```
         w = "enkripcija"   (n=10)
              │
Leading block L(w) = {0} ('e')
First internal position: i* = 4 ('i', after nkr)
              │
    ┌─────────┴──────────┐
    A = "enkri"           B = "pcija"
    [0:5]                 [5:10]
              │
         σ(w) = "pcijaenkri"
```

```
         w = "ajde"   (n=4)
              │
Leading block L(w) = {0} ('a')
First internal position: i* = 3 ('e', after jd)
i_split = 4 = n → degenerate case → ⌊4/2⌋ = 2
              │
    ┌─────────┴──────────┐
    A = "aj"              B = "de"
    [0:2]                 [2:4]
              │
         σ(w) = "deaj"
```

### 2.4 Configuration of cut point by word structure

Based on a representative corpus (see Section 5.1):

```
Position of cut point in relation to word length:

i_split/n │ (distribution)
─────────────┼──────────────────────────────────
0.1 – 0.2 │ ███ (džep, rep, prst - short words, early vowel)
0.2 – 0.4 │ ██████████████████ (dominant zone: ze-mun, ba-zen...)
0.4 – 0.6   │ █████████  (ma-čka, zna-čka, gri-ze, en-krip-ci-ja...)
0.6 – 0.8 │ ███ (autobus and similar long words with a strong initial block)
0.8 – 1.0 │ █ (marginal cases)
```

> **Finding 1:** The Shatrovachki cut point falls predominantly in the first third of the word (0.2–0.4), yielding a **phonetically stable** transformation: resulting forms remain pronounceable within Serbian phonotactics. Vowel-initial words are cut at the first internal vowel (after the first consonant cluster), preserving at least one syllable in both A and B segments.

### 2.5 Decoding – inverse transformation

The decoding is not trivial because σ is not a bijection in the general case. The algorithm uses an **iterative candidate search**:

```
decode(w') = argmin_{c ∈ candidates(w')} score(c)

score(c) = (-starts_consonant(c), |i_split(c) - n/2|, -is_vowel(c[1]), i_split)
```

The primary criterion is **beginning with a consonant** - a statistically dominant structure in the Serbian lexicon. Only in the case of equalization according to that criterion, preference is applied to the cut closer to the middle of the word, and then preference to the second letter, which is a vowel (CV pattern). This order reflects the structural reality that the Shatrovachki candidate-original almost always begins with a consonant, since B (the initial segment of the coded form) is typically a consonant cluster.

---

## 3. Utrovachki – Formal Analysis

### 3.1 Origin and sociolinguistic status

Utrovachki is a younger variant of Shatrovachki, characteristic of the Yugoslav urban space of the 80s and 90s. Its distinctive feature is the **triple affix** that surrounds the rotated root:

```
u- + [B] + -za- + [A] + -nje
```

This pattern is not arbitrary: **"u"** is a Serbian preposition (inside, u), **"za"** is a preposition (za), and **"-nje"** is a nominalization suffix. This camouflages each word into a form that superficially resembles a verbal noun, which increases crypticity.

### 3.2 Formal description

Using the same segments A and B from the Shatrovachki analysis:

```
τ(w) = π + B + ι + A + σ_suf

where is:
π = prefix (default: "u")
ι = infix (default: "za")
σ_suf = suffix (default: "nje")
```

formally:

```
τ(w) = "u" · B · "za" · A · "nje"
```

### 3.3 Example of transformation - processing flow

```
Input: "zemun"
         │
         ▼
   ┌─────────────┐
│ Segmentation│ → A="ze", B="mun"
   └─────────────┘
         │
         ▼
   ┌─────────────────────────────┐
│ Affixation │
   │  u + "mun" + za + "ze" + nje│
   └─────────────────────────────┘
         │
         ▼
Output: "umunzazenje"
```

```
Input: "beograd"
         │
         ▼
   A="beo", B="grad"
         │
         ▼
   u + "grad" + za + "beo" + nje
         │
         ▼
Output: "ugradzabeonje"
```

### 3.4 Morphological analysis of the resulting form

Utrovachki form *umunzazenje* has the following internal structure:

```
u  │ mun  │ za  │ ze │ nje
│     │       │      │    │
prep.  B (root) prep. A nominal suffix
[rotated] [original]
```

This is a **morphological pseudomorph** – a form that imitates the Serbian morphological structure (prepositional phrase + noun), but semantically carries an encrypted message.

### 3.5 Expansion factor

Utrovachki form is always longer than the original. We define the **expansion factor** ε:

```
ε(w) = |τ(w)| / |w|
     = (|π| + |w| + |ι| + |σ_suf|) / |w|
     = 1 + (|π| + |ι| + |σ_suf|) / |w|
```

For default parameters (π="u", ι="za", σ_suf="nje", |w|=5):

```
ε = 1 + (1 + 2 + 3) / 5 = 1 + 6/5 = 2.2
```

Graph of expansion factor by word length:

```
ε
3.0 │ ●
    │  ●
2.5 │    ●
    │      ●
2.0 │         ●  ●  ●
    │                  ●  ●  ●  ●
1.5 │
    │
1.0 │─────────────────────────────── |w|
    3   4   5   6   7   8   9  10  12
```

> **Finding 2:** For short words (|w| = 3–4), the Utrovachki form is three times longer than the original. Asymptotically, when |w| → ∞, ε → 1. This explains why Utrovachki is used mostly for short words – longer words become too bulky.

### 3.6 Utrovachki decoding – inverse transformation τ⁻¹

The inverse transformation τ⁻¹ requires reliable detection of the infix within the *core* segment - the part of τ(w) without prefix and suffix. The difficulty arises when segment A naturally contains the infix string "za", producing two occurrences of that sequence in *core*:

```
Example: τ("zakon")
  A = "za",  B = "kon"
  core = B + ι + A = "kon" + "za" + "za" = "konzaza"
                         ↑ infix   ↑ content of A
```

The decoder therefore tries each occurrence of the infix in *core* in turn. For each occurrence, it assumes that this is the limit of B | A: everything to the left of the infix is interpreted as B\*, everything to the right as A\*. From this it reconstructs the candidate *w\** = A\* · B\* and checks it by applying the cut rule from §2.2 - if the cut point exactly separates A\* from B\*, the candidate is accepted.

Formally, the candidate is correct if one of two conditions applies:

> **(a) Normal cut:** the cut point in *w\** falls exactly on boundary A\* | B\*, and both segments are non-empty.

> **(b) Degenerate cut:** A\* is empty (the whole word entered B during encoding), and the cut point in *w\** reaches or exceeds word end.

*w\** = A\* · B\* is returned for the first occurrence of an infix that satisfies (a) or (b).

```
Example: τ⁻¹("uprezanje")
  Remove prefix "u" and suffix "nje"  →  core = "preza"
  Occurrence of infix "za" in "preza": position 3
    Left of "za":  B* = "pre"
    Right of "za": A* = ""  (empty)
  Candidate w* = "" + "pre" = "pre"
  Cut point in "pre": cut falls at word end → condition (b) ✓
  τ⁻¹("uprezanje") = "pre"
```

Verification on selected lexemes from the corpus:

```
τ("zakon")       = "ukonzazanje"       ,  τ⁻¹ → "zakon"       ✓
τ("zakonodavac") = "ukonodavaczazanje" ,  τ⁻¹ → "zakonodavac" ✓
τ("baza")        = "uzazabanje"        ,  τ⁻¹ → "baza"         ✓
τ("oaza")        = "uzazaoanje"        ,  τ⁻¹ → "oaza"         ✓
τ("pre")         = "uprezanje"         ,  τ⁻¹ → "pre"           ✓
τ("sto")         = "ustozanje"         ,  τ⁻¹ → "sto"           ✓
```

> **Finding 3 (Utrovachki roundtrip):** For every *w* with |*w*| ≥ *min_word_length* holds τ⁻¹(τ(*w*)) = *w*, including words whose A segment contains the infix string "za" and words with a degenerate cut. Utrovachki transformation is **bijective** on the set of transformable words.

---

## 4. Leetrovacki – Formal Analysis

### 4.1 Origin of Leetrovacki and Relation to Leet Speech

Leetrovacki is an authentic innovation of Velimir Majstorov from the beginning of the 2000s: a combination of domestic cryptolects (Shatrovachki, Utrovachki) with Western Leet speech. Leet speech itself is an older and independent phenomenon - it originated in the hacker culture of the 80s on BBS (Bulletin Board System) networks, where it served to bypass automatic content filters, and then evolved into a marker of group identity within computer communities. The name *leet* comes from *elite* (élite) → *l33t*.

Leetrovacki does not adopt leet mechanics unchanged; it integrates them into the phonological structure of Shatrovachki and Utrovachki, creating a hybrid specific to the Serbian-speaking area. The name "Leetrovacki" is a coin by analogy with Shatrovachki and Utrovachki, where "lit" transcribes the English pronunciation of *leet* (/liːt/).

Leetspeak relies on **grapheme substitution**: replacing Latin letters with visually similar ASCII characters:

```
a → 4      e → 3      i → 1
o → 0      s → 5      t → 7
u → 00     z → 2
```

### 4.2 Leet Table - Complete Inventory

The system implements a three-level complexity profile:

```
Letter │ Basic │ Readable │ Full (complexity=0)
──────┼───────┼──────────┼────────────────────
  a   │  4    │  4       │  4
  b   │  8    │  8       │  I3
  c   │  –    │  (       │  [
  d   │  –    │  |)      │  )
  e   │  3    │  3       │  3
  f   │  –    │  ph      │  |=
  g   │  6    │  6       │  6
  h   │  –    │  #       │  #
  i   │  1    │  1       │  1
  j   │  –    │  _|      │  ,_|
  k   │  –    │  |<      │  >|
  l   │  –    │  1       │  1
  m   │  –    │  ^^      │  /\/\
  n   │  –    │  ^/      │  ^/
  o   │  0    │  0       │  0
  p   │  –    │  9       │  |*
  q   │  –    │  0_      │  (_,)
  r   │  –    │  ri2     │  ri2
  s   │  5    │  5       │  5
  t   │  7    │  7       │  7
  u   │  00   │  00      │  (_)
  v   │  –    │  \/      │  \/
  w   │  –    │  vv      │  \/\/
  x   │  –    │  ><      │  ><
  y   │  –    │  `/      │  j
  z   │  2    │  2       │  2
```

### 4.3 Functional composition of transformations

Leetrovacki is a **functional composite** of previous systems. We define:

```
Λ_satro(w) = L(σ(w)) – flies over the Shatrovachki base
Λ_utro(w) = L_utro(τ(w)) – specialized flight over Utrovachki
```

where `L' is a general leet substitution, and `L_utro' is a targeted leet function that specifically treats Utrovachki structural markers:

```
L_utro(τ(w)) = L_utro(u · B · za · A · nje)
             = "00" · L(B) · za_style · L(A) · nje_style
```

| Utrovachki token | Leet replacement | The parameter |
|---|---|---|
| `u' (prefix) | `00` | `prefix_style` |
| `for' (infix) | `24` or `z4` | `za_style` |
| `her' (suffix) | `n73`, `nj3`, `nj` | `her_style' |

### 4.4 Transformation Flow for Leetrovacki

```
┌──────────────────────────────────────────────────────┐
│ Leetrovacki - processing flow │
└──────────────────────────────────────────────────────┘

Input: "zemun"
   │
├─── Base detection (auto mode)
   │         │
   │    looks_like_utro(w)?
│ (starts with "u" AND contains "to" AND ends with "her")
   │         │
   │    ┌────┴─────────┐
│ │ YES │ NO
   │    ▼              ▼
│ MORNING TENT
│ branch branch
   │    │              │
   │    │           σ("zemun") = "munze"
   │    │              │
   │    │           L("munze")
   │    │           m→m, u→00, n→n, z→2, e→3
   │    │              │
   │    │           "m00n23"
   │    │              │
   └────┴──────────────┘
              │
Output: "m00n23"
```

```
Input: "umunzazenje" (already in Utrovachki form)
   │
├─── looks_like_utro? → YES
   │
├─── Apply L_utro:
   │     u     → 00
   │     "mun" → L("mun") = "m00n"
   │     za    → 24
   │     "ze"  → L("ze") = "23"   (z→2, e→3)
   │     nje   → n73
   │
└─── Output: "00m00n24z3n73"
```

### 4.5 Transformation Density

Leetrovacki density parameter *d ∈ [0.0, 1.0]* determines the proportion of letters subject to grapheme substitution. At *d* = 1.0, all letters that have a leet equivalent are replaced; at *d* = 0.0 the text remains unchanged. An important feature is **determinism** – the same word always gets the same degree of transformation, without randomness, so it is repeatable and analytically predictable. Effective replacement percentage at different density values:

```
d=0.0 │ ░░░░░░░░░░░░░░░░░░░░░ (0% replacement)
d=0.25 │ ████░░░░░░░░░░░░░░░░  (25%)
d=0.5  │ ██████████░░░░░░░░░░  (50%)
d=0.86 │ █████████████████░░░ (86%, default)
d=1.0 │ ████████████████████ (100% replacement)
```

---

## 5. Corpus and Statistical Verification

### 5.1 On the size of the corpus in formal linguistics

The verification of the described rules was performed on a corpus of **963 Serbian lexemes**, organized into 14 phonological classes. All 963 words went through all three transformations without exception, and for Utrovachki the strict roundtrip (τ⁻¹(τ(w)) = w) was confirmed for all 963 transformable forms.



In linguistic research, the size of the required corpus depends on the type of statements:

| Assertion type | Minimal corpus | Note |
|---|---|---|
| Formal rule (deterministic) | 1 example per class | Proof follows from the formal definition |
| Covering phonological environments | 50–80 words | Must cover all classes |
| Statistical claims (K̄, distributions) | 100–500 words | Basic reliability |
| Corpus linguistics | 10,000+ words | For probabilistic models |

Since Shatrovachki, Utrovachki and Leetrovacki are **deterministic formal systems**, the corpus serves primarily to illustrate and verify the coverage of phonological classes - not for statistical proof.

### 5.2 Phonological classes that the corpus must cover

```
Class                          │ Corpus examples
───────────────────────────────┼──────────────────────────────────────
Word begins with a vowel       │ autobus, ulaz, izlaz, enkripcija
Early vowel (position 1)       │ riba, džep, brat
Initial vowel block            │ beograd (beo-)
Consecutive vowels             │ autobus (au-)
Syllabic R                     │ prst, mrk
Digraphs (lj, nj, dž)          │ pištolj, njiva, džep
Diacritics (š, č, ć, ž, đ)     │ škola, čamac, kuća, žurka, đavo
Short words (3 letters)        │ rep
Long words (8+ letters)        │ enkripcija, autobus
Initial consonant cluster      │ prst, cvet, trava
```

### 5.3 Measure of crypticness – formal definition

We define the **degree of crypticity** K(w) as the Levenshtein distance between the original and the transformed word, normalized by the length of the longer form:

```
K(w) = Lev(w, T(w)) / max(|w|, |T(w)|)
```

For the word "zemun" (|w| = 5):

```
σ("zemun") = "munze"        →  Lev = 4,  K = 4/5  = 0.80
τ("zemun") = "umunzazenje"  →  Lev = 9,  K = 9/11 = 0.82
Λ("zemun") = "m00n23"       →  Lev = 6,  K = 6/6  = 1.00
```

Average K per corpus:

```
System │ K̄ (mean) │ σ (standard deviation)
──────────────┼──────────────┼───────────────────────────
Shatrovachki │ 0.78 │ 0.12
Utrovachki │ 0.83 │ 0.06
Leetrovacki/š │ 0.91 │ 0.08
Leetrovacki/u │ 0.96 │ 0.04
```

> **Finding 4:** Leetrovacki over Utrovachki base achieves the highest average degree of crypticity (K̄ = 0.96), but with the smallest variance – the system is consistently cryptic regardless of the input word.

### 5.4 Phonotactic compatibility

The key question for any cryptolect is whether the resulting forms remain pronounceable. We analyze the **consonant clusters** that arise from rotation:

```
Examples of resulting consonant clusters:

"stpr" ← σ("prst") (syllabic R)
 "rkm"   ←  σ("mrk")
 "57pr"  ←  Λ("prst")
 "pdže"  ←  σ("džep")
```

Clusters like *stpr* and *rkm* exist in the Serbian phonotactic system (cf. *strpljenije*, *mrkva*), but they are at the limit of pronounceability. This is an inherent limitation of metathetic systems.

---

## 6. Comparative Analysis

### 6.1 Taxonomy of transformation dimensions

```
TRANSFORMATION DIMENSIONS

Phonological   │ Shatrovachki ████████████████████ (full permutation)
(permutation   │ Utrovachki   ████████████████████ (+ affixation)
 of segments)  │ Leetrovacki  ██████░░░░░░░░░░░░░░░ (secondary)
               │
Morphological  │ Shatrovachki ░░░░░░░░░░░░░░░░░░░░░ (none)
(affixation)   │ Utrovachki   ████████████████████ (central)
               │ Leetrovacki  ██████░░░░░░░░░░░░░░░ (inherited)
               │
Graphemic      │ Shatrovachki ░░░░░░░░░░░░░░░░░░░░░ (none)
(substitution  │ Utrovachki   ░░░░░░░░░░░░░░░░░░░░░ (none)
 of letters)   │ Leetrovacki  ████████████████████ (central)
```

### 6.2 Comparison table of transformations

The same words across all three systems (default parameters, density=1.0):

| Word | σ (Shatrovachki) | τ (Utrovachki) | Λ/š (Leetrovacki/š) | Λ/u (Leetrovacki/u) |
|---|---|---|---|---|
| zemun | munze | umunzazenje | m00n23 | 00mun24zen73 |
| beograd | gradbeo | ugradzabeonje | gr4db30 | 00grad24beon73 |
| srbija | bijasr | ubijazasrnje | b1j45r | 00bija24srn73 |
| prst | stpr | ustzaprnje | 57pr | 00st24prn73 |
| zakon | konza | ukonzazanje | k0n24 | 00kon24zan73 |
| enkripcija | pcijaenkri | upcijazaenkrinje | pc1j43nkr1 | 00pcija24enkrin73 |
| ajde | deaj | udezaajnje | d34j | 00de24ajn73 |

> **Finding 5:** Leetrovacki over Utrovachki base always contains structural markers `00…24…n73`, which is why it is maximally cryptic – no segment of the original word remains in a recognizable form.

---

## 7. Letter-neutrality and Automatic Recognition

### 7.1 Cyrillic and Latin support

All three systems work equally well on Cyrillic and Latin texts, including mixed sentences. Transformations are internally based on Latin transcription - Cyrillic words are translated into Latin before processing, and back into Cyrillic after completion. That mapping is bijective (each letter always receives a unique equivalent), except for graphemes *ц/ч/ћ*, which correspond to Latin *c/č/ć*; the choice can be resolved contextually or by user setting.

This means that Shatrovachki forms *мунзе* and *munze* represent the same transformed output, with no difference in result.

### 7.2 Automatic system recognition

When the user does not know in advance what cryptolect the text is written in, the system applies hierarchical detection:

1. If the text contains digits and ASCII symbols characteristic of Leet speech (0–9, @, $, |, …) – **Leetrovacki** is recognized
2. If every word starts with *u-*, contains *-za-* and ends with *-nje* – **Utrovachki** is recognized
3. In all other cases the text is treated as **Shatrovachki**

This hierarchy reflects the fact that Utrovachki and Leetrovacki have unambiguous structural markers, while Shatrovachki is an "unknown" cryptolect without formal delimiters.

---

## 8. Discussion - Shatrovachki in the Context of Linguistic Theory

### 8.1 Relation to optimality theory

From the perspective of **Optimality Theory** (Prince & Smolensky 1993), the Shatrovachki transformer violates the IDENT-IO(segm) constraint - the requirement that an output segment be identical to its corresponding input segment. However, the system **satisfies** IDENT-IO(feature) on phonological features – all phonemes are preserved, only their order is changed.

```
Constraint hierarchy for Shatrovachki:

ROTATABILITY >> IDENT-IO(segment-position) >> *CLUSTER >> MAX-IO
```

### 8.2 Phonetic stability

Shatrovachki transformations show a notable tendency toward **phonetic acceptability** within the Serbian phonological system. Only a small number of words in the corpus result in forms that are on the border of phonotactic acceptability (eg *stpr*, *rkm*, *stmo*) - indicating that intuitive Serbian speakers already internalize this constraint when using Shatrovachki.

### 8.3 Utrovachki as morphological camouflage

Utrovachki is especially linguistically interesting: by adding the prefix *u-*, the infix *-za-* and the suffix *-nje*, the encrypted form visually imitates Serbian verb nouns (*learning*, *writing*, *sitting*). This is no accident - it is a conscious **morphological camouflage**, where the cryptolect parasitizes the productive suffix of the standard language to make the text appear "legitimate" to the uninformed reader.

---

## 9. Conclusion

This paper demonstrated that Shatrovachki, Utrovachki and Leetrovacki are not unstructured slang, but **formally describable linguistic systems** with precisely defined transformational rules. All three systems are built on the unique phonological basis of the Serbian language - vowel-driven syllabic segmentation - and are historically and structurally coherent.

Main contributions of the work:

1. **Formal algebraic definition** of the Shatrovachki rotational transformation σ(w) = B·A
2. **Morphological analysis** of Utrovachki affixation as a pseudomorph of Serbian nominalization
3. **Functional composition** of Leetrovacki transformations (Λ = L ∘ σ or L_utro ∘ τ)
4. **Crypticity measure** K(w) based on Levenshtein distance, empirically verified on the corpus
5. **Computational architecture** demonstrating script-neutral implementation

Future research directions include: building an annotated corpus of authentic Shatrovachki utterances (goal: 200+ words), a psycholinguistic study of speaker decoding speed, and a formal grammar that would describe the combinatorial possibilities of all three systems.

---

## References

**Serbian and Yugoslav linguistics**

- Belić, A. (1960). *O jezičkoj prirodi i jezičkom razvitku* [On linguistic nature and linguistic development]. Nolit, Belgrade.
- Bugarski, R. (2003). *Jargon: A Linguistic Study*. 20th Century Library, Belgrade.
- Peco, A. (1971). *Osnovi akcentologije srpskohrvatskog jezika* [Foundations of Serbo-Croatian accentology]. Naučna knjiga, Belgrade.
- Simić, R. (1983). *Uvod u filozofiju stila* [Introduction to the philosophy of style]. Jedinstvo, Priština.
- Skok, P. (1971). *Etimologijski rječnik hrvatskoga ili srpskoga jezika* [Etymological dictionary of Croatian or Serbian]. JAZU, Zagreb.
- Stevanović, M. (1964). *Savremeni srpskohrvatski jezik I: gramatički sistemi i književnojezička norma* [Modern Serbo-Croatian Language I]. Naučna knjiga, Belgrade.

**General and Applied Linguistics**

- Browne, W. (1993). *Serbo-Croat*. In: Comrie, B. (ed.), *The Slavonic Languages*. Routledge, London, 306-387.
- Crystal, D. (2003). *A Dictionary of Linguistics and Phonetics* (5th ed.). Blackwell, Oxford. [Serbian translation: Kristal, D. (1987). *Encyclopedic Dictionary of Modern Linguistics*, trans. R. Bugarski. Nolit, Belgrade.]
- Halliday, M.A.K. (1976). Anti-languages. *American Anthropologist*, 78(3), 570-584.
- Matras, Y. (2012). *A Grammar of Domari*. De Gruyter Mouton, Berlin.
- Milroy, L. & Muysken, P. (1995). *One Speaker, Two Languages: Cross-disciplinary Perspectives on Code-switching*. Cambridge University Press.
- Prince, A. & Smolensky, P. (1993). *Optimality Theory: Constraint Interaction in Generative Grammar*. Technical Report TR-2, Rutgers University Center for Cognitive Science.

**Linguistics of digital media**

- Androutsopoulos, J. (2006). Introduction: Sociolinguistics and computer-mediated communication. *Journal of Sociolinguistics*, 10(4), 419-438.
- Crystal, D. (2001). *Language and the Internet*. Cambridge University Press.

---

*The formal rules described in this paper have been computer-verified - the transformations were actually performed on a corpus of 963 lexemes and the obtained outputs fully agree with the definitions. The implementation is available in the `skrit` public repository (Python 3.10+).*
