# Author posts and quotes

Short, dated excerpts from AoiNakamoto's own Reddit posts, in chronological order.
Full threads are public; only short quotes are reproduced here.

## Real Big Block, stage 1, 2019-07-07

https://www.reddit.com/r/Grycoin/comments/ca6jxv/77_mbtc_quizchain2_block_77_stage_one/

> "I will give no information on solution format, no first digits of MD5 hash,
> nothing. I do disclose that this one has no TOMI field, but that is all. You
> are on your own completely."

> "And I will publish the complete solution as the Second stage of this block.
> This solution will in turn be the question for the Second stage, which will
> have the final 777 mbtc prize."

The question for this stage links to Hal Finney's "Bitcoin and me" post on
bitcointalk (topic 155054). Stage 1's escrow, `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN`,
was solved and swept on 2019-08-03; its answer is not part of the live prize and
is used in this folder only as a mechanism reference (see README).

## Quizchain2 Block 76, 2019-07-22 (solved and swept by a reader 2026-08-17)

https://www.reddit.com/r/Grycoin/comments/cgcv9i/77_mbtc_quizchain2_block_76/

> "Question: change to"
> "Format: [solution] TOMI [TOMI]"
> "First three digits of MD5 hash are f8e (copypasted)."

Update, same thread: "First two digits of solution only are 1d."

Update, same thread: "Hint 1. Change question from \"change to\" to \"from change
to\"."

> "I will shut down soon now (after posting the second stage of 77), so I will
> not be available for hints or questions."

Kept for historical reference only; no derivation of any candidate ever
reproduced the escrow address before it was solved and swept by another reader
on 2026-08-17. The solution was never disclosed publicly.

## Real Big Block original announcement, 2019-07-22/24 ("Quizchain last block")

https://www.reddit.com/r/Grycoin/comments/cgkpbb/ (never previously captured in
this repository; full text in `data/realbigblock_original_announcement.md`)

> "Question: Final version of the second chapter of Wattpad story, which I
> will publish in a moment."

> "I wanted to remove one of the twists I had. The block is now slightly
> easier. It is also hashed with two line breaks between paragraphs now."

The funding address named in this post, `1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC`
(funded 2019-07-24), is the superseded pre-rehash escrow, later swept back by
the author before she rehashed to the current address. Her `modifyDate` on the
chapter did not change between the two fundings, so the chapter's prose is
confirmed identical for both; whatever "twist" was removed was not an edit to
the text itself.

## Real Big Block Discussion thread (fully recovered, 33 comments)

https://www.reddit.com/r/Grycoin/comments/chn8un/real_big_block_discussion/
(full text with exact UTC timestamps, recovered via the Arctic Shift Reddit
archive since reddit.com itself is not fetchable by this repository's tooling,
in `data/realbigblock_full_thread_recovered.md`; a partial local capture is
also kept at `data/realbigblock_reddit_foros.md`)

2019-07-25: "When I posted the real big block at the Wattpad site, I added extra
line breaks between paragraphs. This information is needed to solve the block."

2019-07-28: "I have line breaks in the chapter between all paragraphs. And there
are two line breaks there now, since Wattpad would not display them correctly
with only one each. I analyzed them with the tool at asciivalue.com and that
shows one 13 and one 10 for each of the line breaks. The solution you need to
hash with has only one line break between paragraphs, which is one 13 and one
10 in ASCII" — i.e. the **superseded** address's separator is a single `\r\n`
(2 bytes).

2019-07-30: "Once someone figures out the format for the first stage, they
will also have a big hint for the format of this second stage." (Posted the
same day as the current escrow's funding; the community had already solved
Stage One by this point.)

2019-07-31: "I took back the prize for a moment and sent it again to a new
address, hashing with a slightly different solution, as explained in update
above [i.e. the line-break exchange] [...] It has multiple paragraphs and two
line breaks between each of them."

2019-08-01, replying to a reader's precise disambiguating question ("hit enter
once or twice?"): "I mean the second one. Hit enter twice. This displays in
Ascii as 13 10 13 10, according to asciivalue.com." — i.e. the **current**
address's separator is `\r\n\r\n` (4 bytes).

This last exchange corresponds to the current, still-funded escrow
(`14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W`, funded 2019-07-30).

## Grycoin Block 2, 2019-08-03 ("a simple example for the format... of block 77")

https://www.reddit.com/r/Grycoin/comments/cleczc/

The author's own worked example for the ITASM-style case-flip mechanism.
Read literally, its illustration is imprecise even about its own real text
(it describes a real paragraph's transformation but names the wrong resulting
last letter — confirmed by direct comparison against the paragraph it
describes). It independently reconfirms `\r\n\r\n` = "two line breaks" as her
general convention, and gives an exact-trimming precedent: "there should be no
problem if you just copypaste everything in the Question from this Reddit
post... with no spaces or line breaks before or after that included in the
hash."

## Wattpad profile (wattpad.com/user/AoiNakamoto)

Bio: "Born to publish one story." Joined 2019-04-04. 1 published story ("Second",
20.2K reads, 19 votes, 33 comments), 0 reading lists, 14 followers. Consistent
with her disappearing after October 2019 without further activity: the account
was used for exactly one purpose and nothing else.

## Twitter handle, confirmed

https://www.reddit.com/r/Grycoin/comments/bry4fw/ ("Quizchain Introduction")

Her own introduction post states her solving-progress documentation is
"available at my Twitter feed @NakamotoAoi." This is a primary-source-confirmed
handle, not a guess; the account itself was not independently located/verified
in this session (X/Twitter fetches for it returned HTTP 402, paywalled).

## The Wattpad chapter

https://www.wattpad.com/720888559-second

The author's own published chapter, titled "Second", part 2 of a 33-part
Wattpad story of the same title (story id 184148284). Its text is the
confirmed source of Real Big Block's question (see README, and the original
announcement post above). This folder does not reproduce the chapter text.
The chapter's own narrative, in its "Satoshi Code" section, states the Stage
One ITASM rule directly: "The letters I, T, A, S, and M as first letters of
each paragraph of this post" — this is not a researcher inference, it is the
puzzle's own text. Two earlier draft parts of the same story ("THOMAS and
SATOSHI", "The Satoshi Code") were consolidated into this final chapter before
its last edit (2019-07-23T23:12:04Z); see `data/wattpad_story_structure.md`
for the full 33-part structure and the story's true last edit (a different
part, "Starting Up", 12 minutes later).
