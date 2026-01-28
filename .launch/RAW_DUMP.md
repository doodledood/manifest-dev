LLMs were RL'd a lot during their training which is inherently a goal oriented process tha itself probably made
  them more goal minded

They are so smart today that tinkering too much with thier process is likely to throw them offf. For example
The approach of planning an implementation down to code or even exact type level may backfire. Even if you are the smartest domain expert you as a human simply cannot hold in your mind all the nuances of the situation and even worse some of them are not even known before you are already deep inside the implementation process. Like a human would the llm needs flexibility to adapt or it will do what it does best - listen to you and try to fulfill the goals you set it with. If those goals are too rigid it, and a problem or nuance surfaces that's where you'll see things like it using any types and trying to put ts or eslint ignore rules etc basically trying to bend the reality around your goal in areas that were less precisely specified by you. A plan needs to be adaptable and for that in my mind you shouldn't even call it a plan but an "initial approach". In an ideal world (maybe when LLMs are smarter) this will become irrelevant even with the current trends. The will just be able to take your goal and get there in a nice way. Today while they are smart they still may get lost depending on the complexity. Your job as a human is first and foremost to define the acceptance criteria and goals (and constraints) for the llm. And that initial approach. Key word initial. The llm has to have wiggle room to scrap that approach completely if reality in th ground demands it. Like the famous saying "everybody's got a plan until they get punched in the face".

Besides all this it's well documented that current LLMs don't explore enough, are lacking (as of Jan 2026) in the memory department, suffering from context rot issues. It is getting better but we still have to account for it.

In an AGI ideal world you won't have to verify anything and you just give a goal and come back to a perfect result. In reality it may never get there. Swarms of humans are as close to AGI as there is currently and yet they too have processes and structures that admit the individual isn't perfect. Hence why there are development methodologies and qa fix cycles during this development cycle. If we take humans as a state to strive towards (in the mean time, while machines are still behind) we can probably assume we'll need this for the forrseeable future.

Like actual humans specs define acceptance criteria we can borrow this idea and massage it so it's ideal for an llm
If we can define exactly what needs to be done, and most importantly how exactly to verify it we can then have the llm freely do its thing being flexible in achieving the criteria (which can be both negative and positive) and once it's done have a verify - fix loop all automated.
Now this is neat because many problems are then taken off the table - you worry about llm producing
Code that is not maintainable? Hard to read? Not based on deep exploration? Incomplete? Encode each as acceptance criteria or global invariants and watch the fix loop get there in the shape you want.  You can encode your specific needs inside a custom "reviewer" agent and set the verification method to that and assuming  you did a good job replicating your thoughts - the final pr will adhere. Since it won't stop until all AC are fulfilled or an impossibility is reached at which point a human intervention may be needed (for example a feature cannot be verified because the env is not set up properly)
The big caveat: if we start thinking not "how do I get the llm to implement this feature properly" but "what would make me accept this PR in full" we make a mindset shift that is super beneficial IMO

And this is not just applicable to coding. A manifest can be made for any task using the same loop. Want to research something? Define the research document you want produced with the relevant ACs (citations included, etc). Same for writing a blog post. Etc. it's a general purpose way of getting to the artifact you will accept.

Kind of a more opinionated alternative to plan/code modes.

Humans are not that good at thinking upfront about all things. It's very mentally draining to do it right. Gladly the llm is good at that. It never gives up or gets tired.

And we can utilize this to interview us and help us both define what we know and try to strive towards helping us uncover why we don't know (known unknowns) to create a definition of what will make us accept the artifact.

We don't always think of all the ACs we actually care about (latent criteria).

Of course getting to 100% is not always possible and shouldn't be strived for - some things are simply not known in advance and that's ok. What we can do is try hard to get to a good enough point first cover all the interesting things and then when the artifact is done we can do another round of these with more information after we had uncovered some of the unknown unknowns. The goal is not full coverage (probably impossible) but getting to a good enough point where we can start and reliably end up close to the finish line.

You can encode your way of viewing things into an llm as a judge and even if it's not perfect and it's a proxy it's good enough. The goal is not to get to the final artifact in one shot but reduce friction and have fewer iterations in total to get to the finish line. We need the first iteration to land us closer than before to the finish line.

Fix loop degradation is a theoretical concern - in practice after sustained production use I haven't run into it yet. Maybe a problem in theory but hasn't materialized.

Cold start / bootstrapping is a true problem. Some of it is alleviated by code exploration and web research etc.

The human analogy being selectively applied (ignoring ongoing course correction) is fair. For that reason there's a proxy that verifies the spec and also the whole thing is done in iterations. We can finish and build on the manifest in a second loop.

Flexibility cutting both ways is true but there's explicitly built-in structure. We have process guidance and stuff like general constraints and initial approach. It's not a free for all.

Generality beyond coding has been tried with the define/do flow and it works. You just need to use llm-as-judges proxies (not perfect but better than doing nothing). For example during manifest building for a research doc you encode what a good research report looks like from your eyes - be it citations from real articles, good topic coverage, etc. The manifest also has the ability to do manual verification baked in.

One of the ideas is to invest in the define process so that you can fire and forget in the do verify fix phase. This has the side effect of also freeing you meaning do is running to define many things in parallel if you wish increasing throughout apart from the process itself which makes this more efficient anyways.

Also unrelated to that - investment in infrastructure may prove very beneficial for verifications.

Investing time building a good manifest has many extra benefits one of which is it helps you understand the task its nuances and even high level better so its easier later to code review with less chance of overwhelm. It's a known problem that using AI atrophies your knowledge of the code it produces because you don't get involved to some degree. The define phase forces involvement - you can't define acceptance criteria without understanding what you want. So when the code comes back, you're reviewing against criteria you deeply thought through, not trying to understand AI-generated code cold.

This process also encourages refinement over time. When you get the final PR, let's say it passed all your criteria but still other people commented things that are true and need to be addressed. Or you actually find that you failed it anyway because of a criteria you didn't think of. In that case you can go back and encode your extra concerns as more review agents or points to consider for next time in your CLAUDE.md making the next PR more likely to cover more things you should care about.

This replaces plan/implement that is present in most harnesses like Claude Code. This could get extra meta if you want it to. For example you can define a manifest that when /do executed produces another manifest you can call /do on. Like a manifest that creates a manifest that creates prompts following best practices. Think like generators of code generators as an example.

It's actually recommended to NOT babysit after you invested time in the define phase. It's expected for it to not get it right the first time - that's exactly what the fix-verify loop is there for. No interventions needed. It doesn't get to the result usually in a straight line. Resist the urge to jump in.
