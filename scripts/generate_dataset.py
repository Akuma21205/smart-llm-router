"""
Generates 150 production-grade benchmark queries:
- 30 General (10 low, 10 med, 10 high)
- 30 Coding (10 low, 10 med, 10 high)
- 30 Reasoning (10 low, 10 med, 10 high)
- 30 Creative (10 low, 10 med, 10 high)
- 30 Ambiguous & Masked (10 low, 10 med, 10 high) with [MASK], [REDACTED], and underspecified inputs.
"""
import json
from pathlib import Path

# 1. GENERAL (30)
gen_low = [
    ("q001", "What is the difference between TCP and UDP networking protocols?", "general", "low"),
    ("q002", "What does HTTP status code 403 Forbidden mean?", "general", "low"),
    ("q003", "List the planets in our solar system in order from closest to farthest from the Sun.", "general", "low"),
    ("q004", "Who is widely considered the father of computer science and artificial intelligence?", "general", "low"),
    ("q005", "What is the primary function of DNS (Domain Name System) on the internet?", "general", "low"),
    ("q006", "What is the capital city of Australia?", "general", "low"),
    ("q007", "Explain the purpose of RAM (Random Access Memory) in simple terms for a beginner.", "general", "low"),
    ("q008", "What is the speed of light in a vacuum in meters per second?", "general", "low"),
    ("q009", "When was the Python programming language first publicly released by Guido van Rossum?", "general", "low"),
    ("q010", "What does the acronym API stand for, and what is its basic purpose in software?", "general", "low"),
]

gen_med = [
    ("q011", "Summarize the core architectural differences between monolithic applications and microservices.", "general", "medium"),
    ("q012", "Explain the CAP theorem in distributed computing and describe what trade-offs it imposes.", "general", "medium"),
    ("q013", "How does public-key (asymmetric) cryptography work to establish secure communication?", "general", "medium"),
    ("q014", "Explain how generational garbage collection works in modern runtimes like the JVM or V8.", "general", "medium"),
    ("q015", "Compare relational SQL databases with NoSQL document stores in terms of schema flexibility and ACID guarantees.", "general", "medium"),
    ("q016", "Explain the biological mechanism of photosynthesis in plants and why it is vital for Earth's atmosphere.", "general", "medium"),
    ("q017", "What were the primary macroeconomic and systemic causes of the 2008 global financial crisis?", "general", "medium"),
    ("q018", "Explain how the Transformer self-attention architecture fundamentally changed natural language processing.", "general", "medium"),
    ("q019", "What is the technical distinction between concurrency and parallelism in operating systems?", "general", "medium"),
    ("q020", "Explain how the Federal Reserve uses interest rate adjustments and open market operations to control inflation.", "general", "medium"),
]

gen_high = [
    ("q021", "Provide a comprehensive comparative analysis of zero-knowledge proofs (ZK-SNARKs vs ZK-STARKs), covering arithmetization, polynomial commitment schemes, and cryptographic assumptions.", "general", "high"),
    ("q022", "Explain quantum entanglement, Bell's inequalities, and the experimental verification that ruled out local hidden-variable theories in physics.", "general", "high"),
    ("q023", "Detail the complete Raft consensus protocol, including leader election, log replication consistency, safety invariants, and joint consensus configuration changes.", "general", "high"),
    ("q024", "Trace the socioeconomic evolution of the international monetary system from the 1944 Bretton Woods agreement through the 1971 Nixon Shock to contemporary fiat reserve dynamics.", "general", "high"),
    ("q025", "Explain the molecular and epigenetic mechanisms governing cellular senescence, telomere attrition, and the SASP phenotype in human aging.", "general", "high"),
    ("q026", "Detail the hardware memory hierarchy bottlenecks of self-attention computation and explain how FlashAttention achieves exact attention with sub-quadratic I/O complexity.", "general", "high"),
    ("q027", "Compare Paxos, Multi-Paxos, and Raft consensus algorithms in geographically distributed fault-tolerant distributed storage systems under network partitions.", "general", "high"),
    ("q028", "Explain the thermodynamic laws of black holes and the derivation of the Bekenstein-Hawking entropy formula in quantum field theory in curved spacetime.", "general", "high"),
    ("q029", "Detail the out-of-order execution pipeline of modern x86/ARM processors, including register renaming, reorder buffers, branch prediction, and vulnerability to speculative execution side-channel attacks.", "general", "high"),
    ("q030", "Analyze the theoretical relationship between complexity classes BQP, NP, and BPP, and explain why quantum computers cannot efficiently solve arbitrary NP-complete problems.", "general", "high"),
]

# 2. CODING (30)
code_low = [
    ("q031", "Write a clean Python function to check whether a given positive integer is prime.", "coding", "low"),
    ("q032", "How do I remove duplicates from a list in Python while preserving the original element order?", "coding", "low"),
    ("q033", "Write a one-line JavaScript function to reverse a string.", "coding", "low"),
    ("q034", "How do I read and parse a JSON file into a Python dictionary using the standard json module?", "coding", "low"),
    ("q035", "Write an SQL query to select all users whose age is over 25, ordered alphabetically by last_name.", "coding", "low"),
    ("q036", "What is the Git command to create and immediately switch to a new branch named 'feature-login'?", "coding", "low"),
    ("q037", "Write a Python snippet using argparse to accept an integer argument --port with a default of 8000.", "coding", "low"),
    ("q038", "Write a TypeScript function that takes an array of numbers and returns their arithmetic mean.", "coding", "low"),
    ("q039", "Write a regular expression in Python to validate standard email addresses.", "coding", "low"),
    ("q040", "How do I perform a simple HTTP GET request in Python using urllib.request and read the response text?", "coding", "low"),
]

code_med = [
    ("q041", "Implement a thread-safe Singleton pattern in Python using a metaclass with double-checked locking.", "coding", "medium"),
    ("q042", "Write an SQL query using ROW_NUMBER() window function to find the top 3 highest-earning employees in each department.", "coding", "medium"),
    ("q043", "Implement an asynchronous token bucket rate limiter in Python using asyncio and time.monotonic.", "coding", "medium"),
    ("q044", "Debug this snippet: 'def append_val(x, l=[]): l.append(x); return l'. Explain why it exhibits buggy state retention and provide the idiomatic fix.", "coding", "medium"),
    ("q045", "Implement a Trie (prefix tree) in Python supporting insert, search, and startsWith methods in optimal time.", "coding", "medium"),
    ("q046", "Write a FastAPI endpoint that handles async file uploads, verifies the MIME type is image/png or image/jpeg, and streams it safely to disk.", "coding", "medium"),
    ("q047", "Write an algorithm in Python to search for an integer in a rotated sorted array in O(log n) time complexity.", "coding", "medium"),
    ("q048", "In TypeScript, implement a generic DeepPartial<T> type that recursively makes all nested properties and array elements optional.", "coding", "medium"),
    ("q049", "Write a reusable Python context manager class that logs execution latency and catches and records specific database operational errors.", "coding", "medium"),
    ("q050", "Implement an LRU Cache in Python from scratch using a doubly linked list and a hash map with O(1) get and put operations.", "coding", "medium"),
]

code_high = [
    ("q051", "Implement a lock-free concurrent queue in C++ using atomic std::atomic pointers and compare-and-swap, properly mitigating the ABA problem with tagged pointers.", "coding", "high"),
    ("q052", "Write a production-grade distributed sliding-window rate limiter in Python using Redis Lua script to guarantee atomic evaluation across distributed clusters.", "coding", "high"),
    ("q053", "Implement a complete Red-Black Tree in Python with full node insertion, deletion, color flipping, and left/right rotations satisfying all 5 invariant properties.", "coding", "high"),
    ("q054", "Design and implement a zero-copy circular ring buffer in C/Python using POSIX shared memory (shm_open and mmap) for high-frequency trading IPC.", "coding", "high"),
    ("q055", "Write an abstract syntax tree (AST) compiler and stack-based bytecode virtual machine in Python that parses arithmetic expressions and executes bytecode instructions.", "coding", "high"),
    ("q056", "Implement a complete Raft state machine in Python with election timers, Heartbeat RPCs, log appending, and leader commit index advancement.", "coding", "high"),
    ("q057", "Write a custom memory allocator in C implementing custom_malloc and custom_free with explicit free list management, alignment, and boundary tag coalescing.", "coding", "high"),
    ("q058", "Implement a B+ Tree index engine in Python with node splitting, merging, pointer rebalancing, and page serialization to simulate database disk storage.", "coding", "high"),
    ("q059", "Write a cache-tiled, AVX-512 SIMD-vectorized matrix multiplication kernel in C++ that maximizes L1/L2 cache hit rates.", "coding", "high"),
    ("q060", "Implement a custom asynchronous event loop from scratch in Python using low-level OS select/epoll primitives and generator-based coroutine scheduling.", "coding", "high"),
]

# 3. REASONING (30)
reas_low = [
    ("q061", "If an item costs $24 after a 20% discount, what was the original price before the discount was applied?", "reasoning", "low"),
    ("q062", "In a group of 30 students, 18 play soccer, 15 play basketball, and 8 play both. How many students play neither sport?", "reasoning", "low"),
    ("q063", "If all roses are flowers and some flowers fade quickly, does logic imply that some roses fade quickly? Explain why or why not.", "reasoning", "low"),
    ("q064", "A baseball bat and ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?", "reasoning", "low"),
    ("q065", "The sum of three consecutive odd numbers is 81. Find the three numbers.", "reasoning", "low"),
    ("q066", "If 5 machines take 5 minutes to make 5 widgets, how many minutes would it take 100 machines to make 100 widgets?", "reasoning", "low"),
    ("q067", "You have a 7-minute hourglass and a 4-minute hourglass. How can you measure exactly 9 minutes using only these two timers?", "reasoning", "low"),
    ("q068", "If today is Wednesday, what day of the week will it be exactly 100 days from today?", "reasoning", "low"),
    ("q069", "A box contains 5 red balls, 4 blue balls, and 3 green balls. If one ball is drawn randomly, what is the probability that it is not red?", "reasoning", "low"),
    ("q070", "Identify the next number in this mathematical sequence: 2, 6, 12, 20, 30, 42, ... and explain the underlying formula.", "reasoning", "low"),
]

reas_med = [
    ("q071", "Solve this logic puzzle: Three people (Alice, Bob, Carol) wear hats that are either red or blue. Exactly one person is a liar. Alice says: 'Bob has a blue hat.' Bob says: 'Carol has a red hat.' Carol says: 'Alice and I have different colored hats.' Deduce who is lying and the hat color of each person.", "reasoning", "medium"),
    ("q072", "Prove by mathematical induction that the sum of the first n positive integers is n(n + 1) / 2 for all n >= 1.", "reasoning", "medium"),
    ("q073", "A car travels from City A to City B at an average speed of 60 mph, and returns along the exact same route at 40 mph. Calculate the average speed for the round trip and explain why it is not 50 mph.", "reasoning", "medium"),
    ("q074", "The Monty Hall problem: You choose Door 1 out of 3 doors. The host opens Door 3 revealing a goat and offers you the chance to switch to Door 2. Provide a rigorous mathematical proof showing why switching gives a 2/3 probability of winning.", "reasoning", "medium"),
    ("q075", "In game theory, analyze the Iterated Prisoner's Dilemma and explain why the Tit-for-Tat strategy outperforms uncooperative and naive strategies over repeated rounds.", "reasoning", "medium"),
    ("q076", "Five rational, greedy pirates (ranked 1 to 5) must divide 100 gold coins. The senior pirate proposes a split; if at least 50% agree, it passes, otherwise they walk the plank. Deduce Pirate 1's optimal coin distribution.", "reasoning", "medium"),
    ("q077", "You have 12 coins, one of which is counterfeit (either heavier or lighter). Using a two-pan balance scale exactly 3 times, describe the algorithm to identify the counterfeit coin and whether it is heavier or lighter.", "reasoning", "medium"),
    ("q078", "Prove that the square root of 2 is an irrational number using a formal proof by contradiction.", "reasoning", "medium"),
    ("q079", "A medical test for a rare disease with 0.1% prevalence has a 99% true positive rate and a 2% false positive rate. If a random patient tests positive, compute their exact Bayesian posterior probability of actually having the disease.", "reasoning", "medium"),
    ("q080", "Determine the minimum number of balance scale weighings required to find one heavier counterfeit coin among n coins, and prove the theoretical lower bound using decision trees.", "reasoning", "medium"),
]

reas_high = [
    ("q081", "Formally outline the proof of Godel's First Incompleteness Theorem, detailing Godel numbering, self-referential sentence construction via the diagonal lemma, and arithmetization of provability in Peano Arithmetic.", "reasoning", "high"),
    ("q082", "Provide a formal reduction proof demonstrating that the Halting Problem is undecidable using a Turing machine contradiction and diagonalization.", "reasoning", "high"),
    ("q083", "Derive the Nash Equilibrium for a continuous Cournot duopoly with asymmetric marginal costs and prove its existence, uniqueness, and Pareto inefficiency.", "reasoning", "high"),
    ("q084", "Solve the Basel problem: rigorously evaluate the sum of 1/n^2 from n=1 to infinity and prove that it equals pi^2 / 6 using Fourier series expansion of f(x) = x^2.", "reasoning", "high"),
    ("q085", "In algorithmic game theory, formulate the Price of Anarchy in atomic congestion games with affine latency functions, and prove the Christodoulou-Koutsoupias 5/2 upper bound.", "reasoning", "high"),
    ("q086", "Derive the classical Central Limit Theorem formally using characteristic functions, Fourier transforms, and Taylor series expansion of cumulant generating functions.", "reasoning", "high"),
    ("q087", "Analyze the Byzantine Agreement problem in an asynchronous distributed network without cryptographic signatures, and prove Fischer-Lynch-Paterson (FLP) impossibility of reaching consensus in the presence of even a single unannounced fail-stop fault.", "reasoning", "high"),
    ("q088", "Prove that the Circuit Value Problem is P-complete under logarithmic space reductions from arbitrary polynomial-time deterministic Turing machines.", "reasoning", "high"),
    ("q089", "Derive the Black-Scholes partial differential equation for European option pricing from geometric Brownian motion using Ito's Lemma and dynamic arbitrage-free delta hedging.", "reasoning", "high"),
    ("q090", "Rigorously evaluate the Gaussian integral of exp(-x^2) from -infinity to +infinity using multivariable double integration in polar coordinates, justifying the Fubini theorem application.", "reasoning", "high"),
]

# 4. CREATIVE (30)
creat_low = [
    ("q091", "Write a witty 4-line rhyming limerick about a junior developer who forgot to git commit on Friday afternoon.", "creative", "low"),
    ("q092", "Generate 5 catchy, memorable slogans for an eco-friendly solar-powered coffee maker.", "creative", "low"),
    ("q093", "Write a serene 3-line haiku capturing the feeling of early morning mist over quiet mountain peaks.", "creative", "low"),
    ("q094", "Craft an atmospheric opening hook sentence for a gritty cyberpunk detective novel.", "creative", "low"),
    ("q095", "Create 5 whimsical names for a hidden apothecary shop that sells enchanted herbal teas in a fantasy city.", "creative", "low"),
    ("q096", "Write a humorous apology letter from a family dog explaining why eating the kid's algebra homework was a noble act.", "creative", "low"),
    ("q097", "Write a two-sentence horror micro-story set inside a seemingly ordinary elevator.", "creative", "low"),
    ("q098", "Write a playful, pun-filled birthday greeting card message for a master pastry chef.", "creative", "low"),
    ("q099", "Create a vivid metaphor comparing the process of debugging complex software to hunting ghosts in an old Victorian house.", "creative", "low"),
    ("q100", "Write a sensory descriptive paragraph depicting the sudden arrival of summer rain on baking desert red rock.", "creative", "low"),
]

creat_med = [
    ("q101", "Write a dramatic theatrical monologue from the perspective of an obsolete supercomputer moments before its final decommissioning.", "creative", "medium"),
    ("q102", "Write an engaging Kickstarter campaign pitch script for an augmented-reality telescope that identifies deep-sky constellations and satellites in real time.", "creative", "medium"),
    ("q103", "Write a fairytale about a master clockmaker's apprentice who accidentally catches a rogue minute inside a crystal pocket watch.", "creative", "medium"),
    ("q104", "Write a tense dialogue between two Renaissance rival painters who uncover a stolen formula for an impossible ultramarine pigment.", "creative", "medium"),
    ("q105", "Write a satirical op-ed from the perspective of an office espresso machine observing corporate reorgs and management buzzwords.", "creative", "medium"),
    ("q106", "Compose a formal 14-line Shakespearean sonnet reflecting on the impermanence of digital data and forgotten hard drives.", "creative", "medium"),
    ("q107", "Write an eerie flash fiction story set in an abandoned deep-sea research station when an external sonar ping begins counting down.", "creative", "medium"),
    ("q108", "Write a travel journal entry describing the sights, smells, and sounds of an imaginary subterranean market carved inside a colossal amethyst geode.", "creative", "medium"),
    ("q109", "Write an entertaining pep-talk delivered by an experienced dungeon boss goblin training new goblin guards on their first day of work.", "creative", "medium"),
    ("q110", "Write a culinary showdown scene between two interstellar chefs competing with ingredients harvested from alien gas giants.", "creative", "medium"),
]

creat_high = [
    ("q111", "Write a multi-generational sci-fi narrative exploring the psychological divergence among three generations aboard an interstellar colony ship debating whether to terminate their mission.", "creative", "high"),
    ("q112", "Craft an intricate magical realism story exploring a family cursed to remember the future while entirely forgetting their ancestors' past.", "creative", "high"),
    ("q113", "Write a one-act dramatic verse play featuring a philosophical debate between a self-aware automated terraforming machine and the lone surviving ecologist of an extinct world.", "creative", "high"),
    ("q114", "Write a rich historical fiction piece following a 9th-century Nestorian scholar in the House of Wisdom in Baghdad translating Galen and Aristotle into classical Arabic.", "creative", "high"),
    ("q115", "Compose an epic narrative poem in alliterative heroic verse depicting the rise and maritime cataclysm of a forgotten bronze-age thalassocracy.", "creative", "high"),
    ("q116", "Write a non-linear psychological short story with an unreliable narrator investigating a coastal lighthouse where time echoes out of sequence.", "creative", "high"),
    ("q117", "Write an epistolary story told through intercepted diplomatic telegrams, diary entries, and naval logs chronicling the silent breakdown of a planetary alliance.", "creative", "high"),
    ("q118", "Create an avant-garde literary narrative written entirely in the form of academic footnotes and marginalia annotating a lost philosophical text.", "creative", "high"),
    ("q119", "Write a deeply textured literary short story about an aged cartographer who discovers an antique map whose coastlines alter reality as they are inked.", "creative", "high"),
    ("q120", "Compose a polyphonic prose poem with three interwoven voices: the architect dreaming of a cathedral, the bedrock bearing its load, and the acid rain eroding its spires.", "creative", "high"),
]

# 5. AMBIGUOUS & MASKED (30)
amb_low = [
    ("q121", "Tell me about the thing with [MASK] and how it works in practice.", "ambiguous", "low"),
    ("q122", "Can you fix this snippet? result = [REDACTED]", "ambiguous", "low"),
    ("q123", "Which of the two options is better for my situation?", "ambiguous", "low"),
    ("q124", "Make this better, faster, and cleaner.", "ambiguous", "low"),
    ("q125", "How do I install [MASK] on my operating system?", "ambiguous", "low"),
    ("q126", "Why did it stop responding all of a sudden without an error code?", "ambiguous", "low"),
    ("q127", "Is this syntax valid? fn([MASK]) -> [REDACTED]", "ambiguous", "low"),
    ("q128", "Explain what happened yesterday regarding the [REDACTED] incident.", "ambiguous", "low"),
    ("q129", "Where should I save the configuration file for [MASK]?", "ambiguous", "low"),
    ("q130", "Show me the standard implementation of that algorithm we discussed earlier.", "ambiguous", "low"),
]

amb_med = [
    ("q131", "Our backend microservice threw HTTP error 500 when connecting to [MASK]. How do I diagnose and fix this?", "ambiguous", "medium"),
    ("q132", "Write a data migration script to sync records between [REDACTED] and [MASK] without service interruption.", "ambiguous", "medium"),
    ("q133", "Compare [MASK] with Python in terms of memory efficiency, ecosystem maturity, and developer onboarding velocity.", "ambiguous", "medium"),
    ("q134", "Can you optimize this database index while also drafting an announcement email explaining the latency benefits to our enterprise clients?", "ambiguous", "medium"),
    ("q135", "Analyze the security and latency implications of switching our API gateway from [MASK] to [REDACTED].", "ambiguous", "medium"),
    ("q136", "Should I use a message queue or a relational table to handle incoming [MASK] webhook events during high traffic bursts?", "ambiguous", "medium"),
    ("q137", "Will this logic cause race conditions? if check([MASK]): process([REDACTED]) under multi-threaded execution?", "ambiguous", "medium"),
    ("q138", "Estimate the infrastructure cost of running a distributed [MASK] cluster serving 100,000 daily active users.", "ambiguous", "medium"),
    ("q139", "How do I set up mutual TLS authentication for [REDACTED] services running behind an Nginx reverse proxy?", "ambiguous", "medium"),
    ("q140", "I want to build an enterprise application combining [MASK] and [REDACTED] with strict compliance. What architecture pattern should I choose?", "ambiguous", "medium"),
]

amb_high = [
    ("q141", "Our p99 latency spiked to 4500ms after rolling out [MASK] in region [REDACTED]; analyze potential distributed deadlocks, lock contention, and cache thundering herds.", "ambiguous", "high"),
    ("q142", "Design a Byzantine fault recovery protocol for [MASK] when a compromised node injects malformed payloads into [REDACTED] during partition healing.", "ambiguous", "high"),
    ("q143", "Synthesize a zero-trust multi-cloud architecture integrating [MASK] federated identity with [REDACTED] hardware security modules for SOC-2 Type II compliance.", "ambiguous", "high"),
    ("q144", "Optimize this data transformation pipeline: cat [MASK] | grep [REDACTED] | awk '{print $1}' | sort | uniq -c for terabyte-scale distributed streaming with strict 512MB RAM constraints.", "ambiguous", "high"),
    ("q145", "Determine the mathematical convergence bound of our reinforcement learning policy when the state observation is partially masked by O_t = [REDACTED] under POMDP assumptions.", "ambiguous", "high"),
    ("q146", "We have an elusive memory leak in our [MASK] cluster that only manifests after 96 hours of sustained 50k QPS; outline a comprehensive forensic kernel and heap dump analysis plan.", "ambiguous", "high"),
    ("q147", "Architect a zero-downtime database migration strategy from legacy [REDACTED] to new [MASK] with dual-write CDC, consistency validation, and instantaneous rollback capability.", "ambiguous", "high"),
    ("q148", "Evaluate the algorithmic fairness, disparate impact, and regulatory liability of deploying a [MASK] predictive credit model with masked demographic covariates.", "ambiguous", "high"),
    ("q149", "Investigate why our consensus cluster deadlocks when node [MASK] drops packets to [REDACTED] during simultaneous leader lease renewal and network split-brain.", "ambiguous", "high"),
    ("q150", "Prove whether the masked token reconstruction objective L(theta) = E_{x}[log P(x_[MASK] | x_[REDACTED])] theoretically bounds the mutual information between latent embeddings and downstream representation utility.", "ambiguous", "high"),
]

def generate():
    all_groups = [
        gen_low, gen_med, gen_high,
        code_low, code_med, code_high,
        reas_low, reas_med, reas_high,
        creat_low, creat_med, creat_high,
        amb_low, amb_med, amb_high
    ]

    dataset = []
    for group in all_groups:
        for item_id, q_text, cat, comp in group:
            if cat == "ambiguous" or comp == "high" or cat == "reasoning":
                expected_route = "reasoning"
            elif cat == "coding":
                expected_route = "coding"
            else:
                expected_route = "fast"

            dataset.append({
                "id": item_id,
                "query": q_text,
                "expected_category": cat,
                "expected_complexity": comp,
                "expected_route": expected_route,
                "source": "production_grade_curated_benchmark"
            })

    assert len(dataset) == 150, f"Expected 150 queries, got {len(dataset)}"

    out_path = Path("data/queries.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)

    print(f"Successfully generated {len(dataset)} production-grade benchmark queries into {out_path}!")

if __name__ == "__main__":
    generate()
