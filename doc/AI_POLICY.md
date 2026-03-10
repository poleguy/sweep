# AI Coding Policy

It is important that this software has a high standard of quality and maintainability, with careful thought given to changes that affect the users.

Some "low-end" AI features like keyword-driven code completion can be useful aids; other tools make it very easy to generate code without fully understanding how it works, or the consequences of specific implementation choices. These latter forms of AI assistance cause more trouble than they are worth.

I generally *do not use* AI-assisted code if it isn't code I would write myself.

## 1. Accountability

I recognize that some tools producing AI-generated or assisted code produce output that can be helpful. But if I decide to use AI-based tools to support my work processes, in the end the code is made by me, the person doing the work.

**The human contributor is the sole party responsible for the contribution.**

If I submit code that includes AI-generated code, documentation, or comments:

- I have reviewed every line of code in the submission.
- I am able to explain the "why" behind the implementation.

"The AI generated it and it works" is not a high enough bar.

I do not allow my AI to submit Pull Requests or author commit messages. I as the responsible and responsive human sign my name as author of the code. 

Any code entering this code base is reviewed by me. 

The same applies for comments, issues, PR's and discussions. 

## 2. Disclosure

I disclose that I may have used Claude Opus 4.6 or other tools to help with my work.

I do not bother to disclose which parts of the code were written by hand or not, because the accountability lies with me as the author either way. 

It is important not to hide the use of AI for two reasons

-In case people want to consider all my work "tainted" (e.g. by stolen creative work, destroying the environment, etc.) such that they can avoid it. 
-If I take AI produced slop and commit it as bad code, it is clear that an AI tool may have caused my screwed up, and I can adjust my process to prevent future similar mistakes (including ending AI use entirely.)

## 3. Intentionality

- **Focused changes:** I do not write code that performs broad refactoring or cleanup suggested by AI unless that was something I intended to do at the outset.
- **Design First:** For any non-trivial change, I discuss the plan with others who care, or a rubber duck, and spend time reviewing the design before implementing any code, AI assisted or not.
- **Quality over Quantity:** I value one thoughtful, manually crafted change to the code over ten AI-assisted fixes for nonexistent or trivial issues.

Note that these guidelines apply equally to human-created code. I always consider whether the change is meaningful and desired by the owner of the project and by the users.

## 4. Copyright & Legal

By submitting a commit I represent and warrant that:

1. I have the legal right to submit the contribution under the project's (or specific repository) license.
2. The contribution does not violate the intellectual property rights of any third party.
3. If AI was used, the resulting code does not violate the terms of service of the AI provider and does not include "regurgitated" code from libraries with incompatible licenses to this repository.

If I cannot guarantee the provenance and legal safety of the AI-generated code, I simply **do not submit it**.

## 5. Prohibited Uses

- **Automated PR Descriptions:** Using AI to write PR descriptions that are vague, overly flowery, or fail to accurately describe the technical changes. I as the developer want to say succinctly why this change matters (see points 1 & 2).
- **Unvetted Boilerplate:** Submitting large blocks of AI-generated boilerplate that hasn't been trimmed to what's actually necessary. If I don't understand what the code does, I don't use it.
- **Hallucinated Features:** I don't commit code for features or bug fixes that don't exist, based on AI hallucinations about the project's capabilities. Duh.

## 6. Enforcement

I delete all poor quality AI output without spending much time on it. My time is best spent working to understand the project's technical requirements, and the well written code that already exists, not questionable AI output.

If I find I start breaking ony of my own rules laid out here, I will stop committing code (ban myself) and consider removing any code I committed in violation of these rules.

## 7. This means you

Notice that I wrote this about myself, but this is a message about you.

### Acknowledgement

This policy was written by a human, based on [mastodon AI Policy](https://github.com/mastodon/.github/blob/main/AI_POLICY.md), based on [CloudNativePG AI Policy](https://github.com/cloudnative-pg/governance/blob/main/AI_POLICY.md), inspired by [Ghostty AI Policy](https://github.com/ghostty-org/ghostty/blob/main/AI_POLICY.md) and with acknowledgement to the Linux Foundation's [Generative AI Policy](https://www.linuxfoundation.org/legal/generative-ai).
