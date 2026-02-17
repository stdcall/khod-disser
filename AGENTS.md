# About project

В проекте лежит latex-код диссертации соискателя на уч. звание канд. физ.-мат.
наук на русском языке.

# General rules for prompt processing

- Always answer in russian.
- If asked a question just answer it without any modifications to the files of
  the project. (Note that it doesn't mean that you couldn't run commands with
  temporary files for outputs. Actually you can if you need it.)
- If I ask for something to be checked in a prompt but don't ask for it to be
  corrected, then after the check, I don't need to correct anything—I only need
  the result of the check in the form of a response.
- All theorems, lemmas, propositions, remarks, and their proofs are located in
  the file `./dissertation.tex`. They should be found only there.
- Если ты встречаешь незнакомый термин, сверься со списком определений в
  текущем файле, чтобы найти точную ссылку на определение, данное в работе.
  Список часто встречающихся нестандартных определений:
  - Exact enveloping algebra (точная обертывающая алгебра)
  - стандартная (обертывающая) алгебра
  - Standard ideal (стандартный идеал обертывающей алгебры или алгебры Ли)
  - A request to clarify a proof should result in minimal edits to the current
  proof. What needs to be done:
    - check the validity of all statements in the proof
    - ensure that the statement being proven follows fairly easily from the
      proof
  - When making edits to an already written proof, don't go into detail without
    explicitly asking: If I write that something is obvious or easy, then it can
    be verified, but there's no need for further clarification. (If, however,
    the statement is incorrect, then it must be corrected!)
  - When you i'm referencing something as `\ref{p:mult-enveloping}` or just
  `p:mult-enveloping` to find it in tex files you can search for
  \label{p:mult-enveloping} and look below the line you find.
  - Build your proofs step by step: record your intermediate results and let me
    validate them.
  - Don't hesitate to consult with me and clarify details.

# Directory structure

Main file `./dissertation.tex` includes some auxiliary files:

- `./Dissertation/introduction.tex` Введение с характеристикой работы
  (характеристика подключается из ./common/characteristic.tex)
- Общие с авторефератом файлы в ./common
- Другое

## Bibliography

- Bibliography settings are located in `./biblio/biblatex.tex`.
- `./disser-my.bib` - мои публикации на основе которых строится диссертация.
- `./disser.bib` - прочие литературные источники

Библиографии `./disser.bib` и `./disser-my.bib` экспортируются из Zotero,
поэтому их нельзя редактировать. Если в них обнаружилась проблема, то надо
обратиться ко мне, чтобы я исправил проблему внутри экспортируемых записей в
Zotero.

# Project building

To build the project we are using lualatex + latexmk.

There are two ways to run and check project building:

1. Run `latexmk -outdir=build dissertation.tex`
2. Run `BUILD_DIR=build make` (see Makefile)

Build artifacts will be places in `.build` directory. (Это нужно для того, чтобы
не ломать автосборку проекта в VS Code / LaTeX Workshop, которая запускается при
сохранении правок.)

To clean up artifacts of previus building just use `rm -rf ./build`.

You shouldn't check build status after simple modifications in dissertation.tex
(for example if you just add some theorem with a proof, or modify some lines in
a proof / statement / etc.).

(!!!IMPORTANT!!!) Never check build status (e.g. pdf files) file with browser.

## Troubleshooting

- Beofre debugging build problems do `make clean`.
- Some problems with bibliography can be fixed by cleaning biber caches with
  `rm -rf $(biber --cache)`.

# О правилах оформления

## latex

- Используется fontspec со шрифтом Times New Roman.
  В качестве математического шрифта используется STIX Two Math.
- Точные последовательности рисуются пакетом tikz-cd.
- Диссертация должна быть оформлена согласно ГОСТ 7.0.11.
- Формулы, на которые в работе нет ссылок не нумеруем.
- Вставляем \medskip чтобы разделить повествование на логические части (точного
  правила здесь нет.)
- Для невыносных формул всегда используй $$, а не \(\).

## Отступы (выравнивание) в \*.tex файлах

Для управления выравниванием используется `latexindent` с конфигурацией,
определенной в файле ./latexindent.yaml. Отформатировать tex-файл можно вызвав
команду Format Document внутри VS Code, либо вызовом в корне проекта
`latexindent -c ./.latexindent-backups -l ./latexindent.yaml FILE-NAME.tex`
(выведет отформатированный текст в stdout).

## labels

Префиксы лейблов для ссылок задаются следующим образом:

- Секции (параграфы) `sec:`. При указании ссылки на секцию используем знак `\S`.
- Theorems (environment theorem): `th:`.
- Леммы (environment lemma) `l:`.
- Замечания (environment remark) `remark:`.
- Предложения: `p:`.
- Определения: `def:`.
- Формулы `eq:`.

When you i'm referencing something as `\ref{p:mult-enveloping}` in the prompt
(or just `p:mult-enveloping`) to find it in tex files you can search for
\label{p:mult-enveloping} and look below the line you find.

## Math environments

- `\coloneq` command is used to introduce global defintion.
- The function's definition domain is separated from its name by the `\colon`
  command.

## How to construct and format proofs

  Long proofs should be decomposed into lemmas. Steps of the proof should be
  separated by `\medskip` tex command.

  In the proof you should try to be concise (without lose of precision).

  Displayed formulas can be used if they contain the main result of a step, or
  if the typography requires it (large formula, etc.).

## Miscellaneous

- \medskip should be separated from the main text by blank lines above and below
- In the begin of every theorem and proof environment place a single line with
  empty comment. We need it for `latexindent` to work properly.

# About contents

Под алгеброй подразумевается неассоциативная (т.е. необязательно ассоциативная)
алгебра без единицы (т.е. необязательно с единицей).

Ассоциативная алгебра $A$ всегда превращается в алгебру Ли $A^{(-)}$, если
умножение в $A$ заменим новым $[a,b]\coloneq ab - ba$.

Алгебра $A$ называется Ли-допустимой, когда $A^{(-)}$ есть алгебра Ли;

Алгебра $A$ называется **точной обертывающей алгебры Ли $L$**, если $A^{(-)}\simeq
L$. В работе может встретиться под названием обертывающей алгебры Ли (тогда
нужно исправить и добавить "точная"!)

Основной объект изучения - нильтреугольная подалгебра $N\Phi(\mathbb{K})$
(известная также как нильрадикал борелевской подалгебры) алгебры Шевалле и ее
точные обертывающие алгебры. Сложность вопроса в том, что точных обертывающих
алгебр очень много и мы выявляем дополнительные условия, дающие единственность в
главе 1. Когда нам это сделать не удается (исключительные типы), мы указываем на
существование "стандартных" точных обертывающих (определение дано в главе 1.)

## Введение

Содержится в файле `./Dissertation/Introduction.tex`.

Описывает задачи, которые решаются в диссертации, связанные задачи и историю.
Содержит характеристику работы согласно ГОСТ 7.0.11.

- Введены определения множества углов в \Phi^+ и в идеале $H$ алгебры
  $N\Phi(\mathbb{K})$
- Введены определения идеалов $T(r), \ Q(r), \ T(\mathcal{L})$ и
  $Q(\mathcal{L})$.

## Chapter 1

В главе 1 основные результаты касаются выявления условий, дающих единственность
точной обертывающей алгебры для классических типов. Для формулировки результата,
дающего условия единственности точной обертывающей алгебры для типа $A_n$, в
необходимом количестве развивается теория градуированных алгебр. Если вводим
определение / получаем результат о градуировках, который затем не используется -
это ошибка.

### Результаты § 1.1 (\ref{sec:enveloping})

- Definition of exact enveloping algebra.
- \ref{p:mult-enveloping}: Определение точных обертывающих алгебр $R_\Phi$.
- \ref{def:stand-enval}: Определение стандартного идеала и стандартной точной
  обертывающей алгебры.
- Определение нильтреугольной подалгебры $N\Phi(\mathbb{K})$ алгебры Шевалле.
- Определение точных обертывающих алгебр специального вида $R_\Phi$ для алгебры
  $N\Phi(\mathbb{K})$. Эти алгебры зависят от выбора знаков структурных констант
  в $N\Phi(\mathbb{K})$ и поэтому результаты о них не представляют большого
  интереса.
- \ref{l:Const-RPhi-Non-assoc}: лемма о структурных константах алгебр $R_\Phi$.
- \ref{def:stand-enval}: определение стандартного идеала кольца/алгебры
  $N\Phi(\mathbb{K})$ и стандартной точной обертывающей алгебры для алгебры Ли
  $N\Phi(\mathbb{K})$.
- \ref{l:StructConst-vl90a_ru} лемма с фиксацией знаков структурных констант
  алгебры $N\Phi(\mathbb{K})$.
- \ref{eq:RAn-RDn} и \ref{l:mult-RAn-RDn}: Определения алгебр $RA_n$, $RB_n$,
  $RC_n$, $RD_n$.

### Результататы § 1.2 (\ref{sec:F4})

О типе $F_4$, пока что здесь ничего не используем и не трогаем.

### Результаты § 1.3 (\ref{sec:enveloping})

Параграф с основными результатами главы. Сейчас я его перерабатываю. Планирую
разделить его на отдельные параграфы по типам.

Важные на текущий момент результаты:

- \ref{l:NT-opposite}: об изоморфности алгебры $NT(n,\mathbb{K})$ своей
  противоположной алгебре.
- \ref{l:stand-opposite}: Если точная обертывающая алгебра R стандартна, то и ее
  противоположная алгебра тоже стандартна.
- \ref{th:Stand-Graded-An} Теорема, дающая условия единственности $R_\Phi$ типа $A_n$.
  С учетом текущей задачи формирования аналогичной теоремы на языке градуированных
  алгебр в подразделе \ref{sec:new-An}, это - самая важная теорема для нас сейчас.

## Chapter 2

Here we address combinatorial enumeration problems for the ideals of the algebra
$N\Phi(\mathbb{K})$ : problem (A), which is the enumeration of standard ideals
(see the definition in Chapter 1), and a second problem, the enumeration of all
ideals. The second problem is not solved, but a construction of a basis for an
 arbitrary ideal of $N\Phi(\mathbb{K})$ is given, which describes each ideal by
 a collection of parameters.

## What to pay attention to

- By “ideal” we always mean a two-sided ideal.
- When proving statements about exact enveloping algebras $R$, one should not
  uncritically use results about the algebras $R_\Phi$, since $R_\Phi$ is a
  special case of the algebras $R$.

## Basic notation

- $\Phi$ Simple root system
- $\Pi$ Base of simple root system
- $\mathcal{L}(\Phi, \mathbb{K})$ - Chevalley algebra over field $K$
- $\mathcal{L}(\Phi, \mathbb{C})$ - simple Lie algebra over field $\mathbb{C}$
- $N\Phi(\mathbb{K})$ - niltriangular subalgebra of Chevalley algebra
  $\mathcal{L}(\Phi, \mathbb{K})$ (also known as nilradical of Borel subalgebra)
- $NB_n(\mathbb{K})$, $NC_n(\mathbb{K})$, $ND_n(\mathbb{K})$ --- niltriangular
  subalgebras of the corresponding types. These are Lie algebras. Don't confuse
  them with $RD_n(\mathbb{K})$, $RB_n(\mathbb{K})$, $RC_n(\mathbb{K})$.
- $T(r)$, $Q(r)$, $Q(\mathcal{L})$ - Ideals of $N\Phi(\mathbb{K})$ defined in
  introduction.tex
- $R_\Phi$ - special family of exact enveloping algebras of Lie algebras
  $N\Phi(\mathbb{K})$. Their construction depends on signs of structure
  constants in Chevalley algebra. Many old results are written about this
  family. We are trying to generalize this results to all of exact enveloping
  algebras.
- $NT(n,\mathbb{K})$ --- the algebra of strictly upper triangular matrices of
  size $n\times n$ (an associative algebra; $NT(n,\mathbb{K})^{(-)}$ --- the
  corresponding Lie algebra, isomorphic to $N\Phi(\mathbb{K})$ of type
  $A_{n-1}$).
- $RA_n(\mathbb{K}) = NT(n+1,\mathbb{K})$, $RD_n(\mathbb{K})$,
  $RB_n(\mathbb{K})$, $RC_n(\mathbb{K})$ this are instances of the family
  $R_\Phi$ of exact enveloping algebras. See definitions in § 1.1
  (\ref{eq:RAn-RDn}, \ref{l:mult-RAn-RDn}). They are constructed on linear
  spaces of the so called special matrix representations of N\Phi(\mathbb{K}).
  See § 1.1.

## Definitions of standard enveloping algebra and standard ideal

Для корней считаем $s\geq r$, когда в разложении $s-r$ по базе $\Pi$ в $\Phi^+$
все коэффициенты неотрицательны. Корни $r$ и $s$ в $\Phi^+$ назовем
\emph{инцидентными}, если $s \geq r$ или $r\geq s$. Любое множество
$\mathcal{L}$ попарно неинцидентных корней в $\Phi^+$ называем множеством
углов в $\Phi^+$}. Выделим в $N\Phi(\mathbb{K})$ идеалы

\[
  T(r) \coloneq \sum_{s \geq r}\mathbb{K}e_s,\quad Q(r)\coloneq\sum_{s>r}\mathbb{K}e_s\quad (r\in
    \Phi^+),\quad Q(\mathcal{L})\coloneq \sum_{r \in \mathcal{L}}Q(r).
\]

Если $H \subset T(\mathcal{L})\coloneq\sum_{r \in \mathcal{L}} T(r)$ и включение
нарушается при любой замене $T(r)$ на $Q(r)$ в сумме, то множество $\mathcal{L}=
\mathcal{L}(H)$ определено однозначно и называется \emph{множеством углов в
$H$}.

Идеал $H$ алгебры Ли $N\Phi(\mathbb{K})$ называем \emph{стандартным}, если $Q
    (\mathcal{L}(H))\subset H$.

Аналогичным образом определяется стандартный идеал точной обертывающей алгебры
$R$ алгебры $N\Phi(\mathbb{K})$. Здесь важно понимать, что любую алгебру R
можно реализовать на линейном пространстве $N\Phi(\mathbb{K})$ и тогда

Точная обертывающая алгебра $R$ алгебры Ли $N\Phi(\mathbb{K})$ называется
стандартной, если все ее идеалы стандартны.

---

# ВРЕМЕННЫЕ ЖЕСТКИЕ ПРАВИЛА: Работа над теоремой для типа $B_n$

**Эти правила имеют высший приоритет и СТРОГО обязательны при работе над задачами
в рамках текущего направления исследований.**

## 1. Определения (запомнить наизусть)

### Стандартная обертывающая алгебра (standard enveloping algebra)

Идеал $H$ кольца Ли $N\Phi(\mathbb{K})$ называется **стандартным**, если
$Q(\mathcal{L}(H)) \subset H$.

Точная обертывающая алгебра $R$ алгебры Ли $N\Phi(\mathbb{K})$ над полем
$\mathbb{K}$ называется **стандартной**, если все ее идеалы стандартны.

Это определение дано в `\ref{def:stand-enval}` (dissertation.tex).

## 2. ЗАПРЕТ: Алгебры $R_\Phi$

**СТРОГО ЗАПРЕЩЕНО** использовать при построении доказательств результаты,
сформулированные об алгебрах $R_\Phi$ (конкретных точных обертывающих алгебрах,
зависящих от выбора знаков структурных констант $N_{rs}$).

Причина: мы хотим уйти от зависимости от знаков структурных констант и
формулировать результаты о произвольных точных обертывающих алгебрах $R$,
удовлетворяющих определенным условиям (стандартность, градуированность,
ассоциативность, нильпотентность и т.п.).

**Разрешено** ссылаться на:

- Определения и обозначения ($NB_n$, $RB_n$ и т.п. — как конкретные примеры).
- Результаты, сформулированные для произвольной точной обертывающей алгебры $R$.
- Леммы/теоремы о структуре алгебры Ли $N\Phi(\mathbb{K})$ (они не зависят от
  $R_\Phi$).

## 4. Ключевые результаты для использования

Следующие результаты **поощряется** использовать:

### Лемма `\ref{l:enveloping-Graded-width-1}` (dissertation.tex, строка 1297)

> Пусть $R$ — нильпотентная точная обертывающая алгебра алгебры Ли
> $N\Phi(\mathbb{K})$. Если $R$ градуирована, то $R$ можно реализовать на
> линейном пространстве $N\Phi(\mathbb{K})$ так, что $e_r e_s = 0$, если
> $r + s \notin \Phi^+$, и коммутатор в $R^{(-)}$ совпадает с коммутатором
> в $N\Phi(\mathbb{K})$.

### Теорема `\ref{th:Stand-Graded-An}` (dissertation.tex, строка 1375)

> Если нильпотентная ассоциативная точная обертывающая алгебра $R$ алгебры Ли
> $N\Phi(\mathbb{K})$ типа $A_n$ ($n \ge 3$) градуирована, то
> $R \simeq NT(n+1,\mathbb{K})$.

## 5. ЦЕЛЬ

Мы строим **аналог теоремы `\ref{th:Stand-Graded-An}` для типа $B_n$**: хотим
выявить условия на точную обертывающую алгебру $N\Phi(\mathbb{K})$ типа $B_n$,
при которых она определена **однозначно** (с точностью до изоморфизма).

Предположительно условия будут включать комбинацию из: градуированность,
нильпотентность, ассоциативность подалгебр для посистем типа $A_n$,
стандартность — но точный набор условий определится в ходе исследования.

## 6. Раздел для записи результатов

Все новые результаты (леммы, теоремы, доказательства) записываются в раздел
`\ref{sec:new-Bn}` файла `./dissertation.tex`.

## 7. Метод проверки стандартности алгебры $R$

### Важные замечания

- **Стандартный идеал обертывающей алгебры** $R$: идеал $H$ алгебры $R$
  называется стандартным, если $Q(\mathcal{L}(H)) \subseteq H$. Здесь
  $\mathcal{L}(H)$ — множество углов, $Q(\mathcal{L})$ — идеал алгебры Ли.
  Эти определения переносятся на $R$ поскольку $R$ и $N\Phi(\mathbb{K})$
  имеют одно и то же линейное пространство.
- **Стандартная обертывающая алгебра** $R$: такая, у которой все идеалы
  стандартны.
- При проверке стандартности обертывающей алгебры $R$ анализируется
  **умножение в $R$**, а не лиева скобка в $N\Phi(\mathbb{K})$. Алгебра
  Ли $N\Phi(\mathbb{K})$ при этом не играет роли — все вычисления ведутся
  внутри $R$.
- **Неинцидентность в матричной индексации**: корни $(i,j)$ и $(k,s)$
  неинцидентны, если $k > i$ и $s > j$ (или наоборот). Это дает удобный
  способ выбора неинцидентных корней.

### Описание метода

Для проверки стандартности точной обертывающей алгебры $R$ достаточно
проверить произвольный идеал $H$ с $p$-связанной парой углов $r, s$ (где
$p \in \Pi$ — простой корень).

**Определение:** Два угла $r, s \in \mathcal{L}(H)$ называются
$p$-связанными, если существует простой корень $p$ такой, что $r + p \in
\Phi^+$ и $s + p \in \Phi^+$.

**Схема проверки:**

1. **Если $p$-связанных пар углов нет:** Для каждого угла $r$ и простого
   корня $p$ с $r + p \in \Phi^+$, одно из произведений $e_p e_r$ или
   $e_r e_p$ равно $\pm e_{r+p}$, откуда $e_{r+p} \in H$ (т.к. $H$ —
   двусторонний идеал). Индукцией получаем $T(r+p) \subseteq H$ для всех
   таких $p$, следовательно $Q(r) \subset H$.

2. **Если $p$-связанная пара $(r, s)$ есть:** Нужно убедиться, что из $H$
   можно извлечь $e_{r+p}$ и $e_{s+p}$ по отдельности. Для этого
   **достаточно** одного из следующих условий:

   **(a) Разносторонние аннуляторы:** $e_p$ действует на $e_r$ и $e_s$ с
   разных сторон. Т.е. если $e_p e_r \neq 0$, то $e_p e_s = 0$ и
   $e_s e_p \neq 0$ (и наоборот). Тогда левое и правое умножение на $e_p$
   разделяют вклады от $e_r$ и $e_s$.

   **(b) Наличие «разрывающего» элемента:** Условие разносторонних
   аннуляторов **не является необходимым**. Может существовать корень $t$
   такой, что $\mathbb{K}e_t$ позволяет «разорвать» связь: например, если
   $e_p$ действует на $e_r$ и $e_s$ с одной стороны, но при этом $e_p$
   действует на $e_s$ также и с другой стороны (или наоборот), то одно из
   произведений $e_p e_s$ или $e_s e_p$ лежит в $H$ (будучи единственным
   ненулевым членом при одностороннем умножении), и это позволяет выделить
   $e_{s+p}$ и затем $e_{r+p}$ из другого произведения.

**Алгоритм:** Достаточно рассматривать только связанность **простым**
корнем $p \in \Pi$. Для каждого простого корня $p$ перебираем все пары
неинцидентных корней $r, s$ таких, что $r+p \in \Phi^+$ и $s+p \in \Phi^+$,
и для каждой пары убеждаемся, что $e_{r+p}$ и $e_{s+p}$ можно извлечь
из $H$ с помощью условий (a) или (b).

### Ключевые паттерны (извлечены при проверке $RB_n$)

1. **Длинные простые корни** $p_k = r_{k+1,k}$ ($k \geq 1$): цепное
   правило $e_{ij}e_{jv} = e_{iv}$ работает только справа
   ($e_{i,k+1} \cdot e_{k+1,k} = e_{ik}$, а $e_{k+1,k} \cdot e_{i,k+1} = 0$).
   Правило 3 ($e_{jv}e_{i,-v} = e_{i,-j}$) работает только слева
   ($e_{k+1,k} \cdot e_{i',-k} = e_{i',-(k+1)}$, а $e_{i',-k} \cdot e_{k+1,k} = 0$
   по правилу 4). Итого: для длинных корней разносторонние аннуляторы
   возникают автоматически из асимметрии правил 3 и 4.

2. **Короткий простой корень** $p_0 = r_{1,0}$: правило 5
   ($e_{i0}e_{j0} = e_{i,-j} = -e_{j0}e_{i0}$) действует с обеих сторон
   на элементы $e_{i',0}$, поэтому условие (a) нарушается. Но условие (b)
   работает: левое умножение $e_{10} \cdot H$ убивает $e_{i,1}$ (по правилу 2)
   и оставляет только вклад от $e_{i',0}$, позволяя извлечь $e_{i',-1}$.
   Затем из правого произведения $H \cdot e_{10}$ вычитанием получаем $e_{i,0}$.

3. **Общий принцип**: при переборе $p$-связанных пар в типах $B$, $C$, $D$
   нужно отдельно рассматривать «длинные» простые корни (цепные) и
   «короткий/специальный» простой корень. Для длинных корней асимметрия
   правил 3–4 обычно дает разносторонность (a). Для короткого корня нужно
   проверять условие (b).

### Результат: $RB_n(\mathbb{K})$ стандартна

Проверено для всех простых корней и всех $p$-связанных пар.
