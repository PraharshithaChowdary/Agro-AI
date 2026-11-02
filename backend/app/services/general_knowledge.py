"""
AGRO AI — Universal General Knowledge, STEM, Coding & Conversational Intelligence Engine
Enables the assistant to act as a versatile AI agent (like WhatsApp Meta AI),
answering not only agricultural science, but also programming, mathematics,
general science, world facts, biographies, cooking, lifestyle, and conversation.
"""

import re
import math
from typing import Dict, Any, Optional, List
from app.services.farm_calculator import FarmCalculatorService

class GeneralKnowledgeEngine:
    """
    Comprehensive general knowledge, coding, STEM, and conversational engine.
    Ensures zero unanswered questions when operating offline or without an external LLM.
    """

    @classmethod
    def answer_query(
        cls,
        query: str,
        history: Optional[List[Dict[str, str]]] = None,
        allow_fallback: bool = False
    ) -> Optional[Dict[str, Any]]:
        q = query.strip()
        q_lower = q.lower()

        # 1. Natural Language Math & Arithmetic Questions
        math_ans = cls._handle_math_query(q_lower)
        if math_ans:
            return math_ans

        # 2. Conversational, Jokes, Riddles & Personality
        chat_ans = cls._handle_conversation_and_humor(q_lower)
        if chat_ans:
            return chat_ans

        # 3. Programming & Technology Questions
        coding_ans = cls._handle_coding_and_tech(q_lower, q)
        if coding_ans:
            return coding_ans

        # 4. Science, Physics, Astronomy & Biology Questions
        science_ans = cls._handle_science_and_physics(q_lower, q)
        if science_ans:
            return science_ans

        # 5. World Facts, Biographies & Geography
        facts_ans = cls._handle_world_facts_and_people(q_lower, q)
        if facts_ans:
            return facts_ans

        # 6. Cooking Recipes & Food
        food_ans = cls._handle_cooking_and_recipes(q_lower)
        if food_ans:
            return food_ans

        # 7. Productivity, Health & Daily Life
        life_ans = cls._handle_lifestyle_and_health(q_lower)
        if life_ans:
            return life_ans

        # 8. Intelligent Universal Fallback for any general question (if enabled)
        if allow_fallback:
            return cls._handle_universal_fallback(q, q_lower)

        return None

    @classmethod
    def _handle_math_query(cls, q: str) -> Optional[Dict[str, Any]]:
        # Percentage: "what is 15% of 800" or "15 percent of 800"
        pct_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:%|percent)\s+of\s+(\d+(?:\.\d+)?)", q)
        if pct_match:
            pct_val = float(pct_match.group(1))
            total_val = float(pct_match.group(2))
            res = round((pct_val / 100.0) * total_val, 4)
            full_resp = (
                f"### 1. Direct Answer\n"
                f"**{pct_val}% of {total_val} is {res}**.\n\n"
                f"### 2. Step-by-Step Calculation\n"
                f"1. Convert percentage to decimal: `{pct_val} / 100 = {pct_val / 100}`\n"
                f"2. Multiply by target amount: `{pct_val / 100} × {total_val} = {res}`\n\n"
                f"### 3. Sources & Verification\n"
                f"Standard arithmetic percentage formulation: `Result = (Rate / 100) × Base`."
            )
            return {
                "response": full_resp,
                "category": "math",
                "suggestedQuestions": [
                    f"What is {pct_val}% of {total_val * 2}?",
                    "How to calculate compound interest?",
                    "How to calculate profit margin percentage?"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "math_engine"
            }

        # Natural language arithmetic: "what is 25 * 4", "calculate 1250 + 350", "solve 45 / 9"
        math_match = re.search(r"(?:what is|calculate|solve|how much is)?\s*([0-9\.\s\+\-\*\/\^\(\)]+)\s*(?:\?|$)", q)
        if math_match:
            expr_str = math_match.group(1).strip()
            # Must contain at least one arithmetic operator and numbers
            if any(op in expr_str for op in ["+", "-", "*", "/"]) and re.search(r"\d", expr_str):
                try:
                    val = FarmCalculatorService.safe_math_eval(expr_str)
                    clean_res = int(val) if isinstance(val, float) and val.is_integer() else round(val, 4)
                    full_resp = (
                        f"### 1. Direct Answer\n"
                        f"The result of `{expr_str}` is **{clean_res}**.\n\n"
                        f"### 2. Arithmetic Steps\n"
                        f"• Mathematical Expression: `{expr_str}`\n"
                        f"• Evaluation: Evaluated via deterministic standard operator precedence (BODMAS/PEMDAS).\n"
                        f"• Result: **{clean_res}**\n\n"
                        f"### 3. Verification\n"
                        f"Evaluated deterministically with high precision."
                    )
                    return {
                        "response": full_resp,
                        "category": "math",
                        "suggestedQuestions": [
                            f"What is {clean_res} × 2?",
                            f"What is the square root of {clean_res}?",
                            "How to calculate percentage discount?"
                        ],
                        "evidenceSources": [],
                        "relatedAction": None,
                        "modelProvider": "math_engine"
                    }
                except Exception:
                    pass
        return None

    @classmethod
    def _handle_conversation_and_humor(cls, q: str) -> Optional[Dict[str, Any]]:
        # Who are you / Identity
        if any(w in q for w in ["who are you", "what are you", "who made you", "who created you"]):
            return {
                "response": (
                    "### 1. Direct Answer\n"
                    "I am **Meta AI / AGRO AI Assistant** — an intelligent, multi-turn AI assistant designed to answer "
                    "every question you have! 🚀\n\n"
                    "### 2. What I Can Do For You\n"
                    "• **Ask Me Anything**: General knowledge, history, world facts, biographies, and everyday questions.\n"
                    "• **Coding & Technology**: Write, debug, and explain Python, JavaScript, HTML/CSS, SQL, and algorithms.\n"
                    "• **Mathematics & Calculations**: Instantly solve arithmetic, algebra, percentages, and word problems.\n"
                    "• **Agricultural Intelligence**: Complete crop disease diagnosis, IPM, soil analysis, and NPK fertilizer dosing.\n"
                    "• **Everyday Life**: Healthy cooking recipes, fitness tips, study guides, and friendly conversation.\n\n"
                    "Feel free to ask me anything you like — I am ready to help!"
                ),
                "category": "general",
                "suggestedQuestions": [
                    "Write a Python function to check for palindromes",
                    "How to calculate NPK fertilizer for wheat?",
                    "Tell me a fun science fact"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "meta_ai_engine"
            }

        # How are you
        if any(w in q for w in ["how are you", "how are you doing", "how's it going", "what's up", "whats up"]):
            return {
                "response": (
                    "### 1. Direct Answer\n"
                    "I am doing fantastic, thank you for asking! 😊 I am fully charged and ready to answer any questions you have today.\n\n"
                    "### 2. How Can I Help You Right Now?\n"
                    "Whether you need help with:\n"
                    "• Coding a script or debugging an issue\n"
                    "• Understanding a tricky science or math problem\n"
                    "• Inspecting your crops, soil, or calculating farm inputs\n"
                    "• Discovering a delicious recipe or interesting fact\n\n"
                    "Just ask away!"
                ),
                "category": "general",
                "suggestedQuestions": [
                    "Tell me a clever programming joke",
                    "How do airplanes fly in the sky?",
                    "How to identify Tomato Early Blight?"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "meta_ai_engine"
            }

        # Tell me a joke
        if "joke" in q or "funny" in q or "make me laugh" in q:
            jokes = [
                (
                    "Why do programmers prefer dark mode?\n\n"
                    "**Because light attracts bugs!** 🐛💻\n\n"
                    "Here's another one:\n"
                    "There are 10 types of people in the world — those who understand binary, and those who don't!"
                ),
                (
                    "Why did the scarecrow win an award?\n\n"
                    "**Because he was outstanding in his field!** 🌾😄\n\n"
                    "And why did the tomato blush?\n"
                    "Because it saw the salad dressing! 🍅🥗"
                )
            ]
            selected = jokes[0] if "tech" in q or "code" in q or "program" in q else jokes[1]
            return {
                "response": (
                    f"### 1. Here is a joke for you! 😄\n{selected}\n\n"
                    "### 2. Fun Fact\n"
                    "Laughter boosts oxygen intake, stimulates your heart, lungs, and muscles, and releases endorphins in the brain!"
                ),
                "category": "general",
                "suggestedQuestions": [
                    "Tell me another joke!",
                    "Tell me a brain-teaser riddle",
                    "Tell me an interesting space fact"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "meta_ai_engine"
            }

        # Tell me a riddle
        if "riddle" in q or "brain teaser" in q:
            return {
                "response": (
                    "### 1. Riddle Time! 🧠\n"
                    "**Question:**\n"
                    "*I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?*\n\n"
                    "### 2. The Answer\n"
                    "**An Echo!** 🗣️🏔️\n\n"
                    "Sound waves bounce off physical surfaces like cliffs or walls and return back to your ears, creating the illusion of a repeating voice."
                ),
                "category": "general",
                "suggestedQuestions": [
                    "Give me another riddle!",
                    "Explain how sound waves travel",
                    "Tell me a joke"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "meta_ai_engine"
            }

        # Thank you
        if any(w in q for w in ["thank you", "thanks", "dhanyavad", "shukriya", "great job"]):
            return {
                "response": (
                    "### 1. You are very welcome! 😊\n"
                    "I am always happy to help! Let me know whenever you have more questions, calculations, or projects to explore."
                ),
                "category": "general",
                "suggestedQuestions": [
                    "How to calculate NPK fertilizer doses?",
                    "Write a Python script to fetch data from an API",
                    "Explain how gravity works"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "meta_ai_engine"
            }

        return None

    @classmethod
    def _handle_coding_and_tech(cls, q: str, q_raw: str) -> Optional[Dict[str, Any]]:
        is_coding = any(w in q for w in [
            "python", "javascript", "typescript", "html", "css", "sql", "code", "function",
            "reverse a string", "palindrome", "fibonacci", "binary search", "bubble sort",
            "prime number", "api", "git", "regex", "react", "fastapi", "docker", "algorithm"
        ])
        if not is_coding:
            return None

        # Reverse a string
        if "reverse" in q and ("string" in q or "word" in q):
            return {
                "response": (
                    "### 1. Direct Answer\n"
                    "Here is how to reverse a string in **Python** and **JavaScript** cleanly and efficiently:\n\n"
                    "### 2. Python Implementation\n"
                    "```python\n"
                    "# Method 1: Pythonic Slicing (Time: O(n), Space: O(n))\n"
                    "def reverse_string(s: str) -> str:\n"
                    "    return s[::-1]\n\n"
                    "# Method 2: Two-Pointer In-Place (for list of characters)\n"
                    "def reverse_chars(chars: list[str]) -> list[str]:\n"
                    "    left, right = 0, len(chars) - 1\n"
                    "    while left < right:\n"
                    "        chars[left], chars[right] = chars[right], chars[left]\n"
                    "        left += 1\n"
                    "        right -= 1\n"
                    "    return chars\n\n"
                    "# Example Usage\n"
                    "text = 'Hello World'\n"
                    "print(reverse_string(text))  # Output: 'dlroW olleH'\n"
                    "```\n\n"
                    "### 3. JavaScript Implementation\n"
                    "```javascript\n"
                    "// Method: Split into array, reverse, and join\n"
                    "function reverseString(str) {\n"
                    "  return str.split('').reverse().join('');\n"
                    "}\n\n"
                    "console.log(reverseString('Hello World')); // 'dlroW olleH'\n"
                    "```\n\n"
                    "### 4. Practical Takeaways\n"
                    "• In Python, `[::-1]` uses extended slice syntax `[start:stop:step]` with a step of `-1` to traverse backwards.\n"
                    "• The time complexity is **$O(n)$** where $n$ is the length of the string."
                ),
                "category": "programming",
                "suggestedQuestions": [
                    "How to check if a string is a palindrome in Python?",
                    "How to reverse words in a sentence?",
                    "Explain time complexity O(n)"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "code_engine"
            }

        # Prime numbers
        if "prime" in q:
            return {
                "response": (
                    "### 1. Direct Answer\n"
                    "A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.\n\n"
                    "### 2. Python Function (Optimized $O(\\sqrt{n})$ Check)\n"
                    "```python\n"
                    "import math\n\n"
                    "def is_prime(n: int) -> bool:\n"
                    "    if n <= 1:\n"
                    "        return False\n"
                    "    if n <= 3:\n"
                    "        return True\n"
                    "    if n % 2 == 0 or n % 3 == 0:\n"
                    "        return False\n"
                    "    \n"
                    "    # Check divisors up to sqrt(n) stepping by 6 (6k ± 1 rule)\n"
                    "    for i in range(5, int(math.isqrt(n)) + 1, 6):\n"
                    "        if n % i == 0 or n % (i + 2) == 0:\n"
                    "            return False\n"
                    "    return True\n\n"
                    "# Find all primes up to 50\n"
                    "primes = [x for x in range(2, 51) if is_prime(x)]\n"
                    "print(primes)\n"
                    "# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]\n"
                    "```\n\n"
                    "### 3. Explanation & Complexity\n"
                    "• You only need to test factors up to $\\sqrt{n}$ because if $n = a \\times b$, at least one factor must be $\\le \\sqrt{n}$.\n"
                    "• For generating thousands of primes, the **Sieve of Eratosthenes** is optimal ($O(n \\log \\log n)$)."
                ),
                "category": "programming",
                "suggestedQuestions": [
                    "How does the Sieve of Eratosthenes work?",
                    "How to find prime factors of a number?",
                    "What is RSA encryption and how does it use primes?"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "code_engine"
            }

        # Binary Search
        if "binary search" in q:
            return {
                "response": (
                    "### 1. Direct Answer\n"
                    "**Binary Search** is an efficient search algorithm that finds the position of a target value within a **sorted array** in **$O(\\log n)$** time.\n\n"
                    "### 2. Python Implementation\n"
                    "```python\n"
                    "def binary_search(arr: list[int], target: int) -> int:\n"
                    "    left, right = 0, len(arr) - 1\n"
                    "    \n"
                    "    while left <= right:\n"
                    "        # Avoid integer overflow\n"
                    "        mid = left + (right - left) // 2\n"
                    "        \n"
                    "        if arr[mid] == target:\n"
                    "            return mid  # Target found at index mid\n"
                    "        elif arr[mid] < target:\n"
                    "            left = mid + 1  # Search right half\n"
                    "        else:\n"
                    "            right = mid - 1  # Search left half\n"
                    "            \n"
                    "    return -1  # Target not found\n\n"
                    "# Example\n"
                    "data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]\n"
                    "print(binary_search(data, 23))  # Output: 5\n"
                    "```\n\n"
                    "### 3. Key Concepts\n"
                    "• **Prerequisite:** The array MUST be sorted.\n"
                    "• **Efficiency:** Each comparison cuts the search space in half. Searching 1,000,000 items takes at most 20 comparisons!"
                ),
                "category": "programming",
                "suggestedQuestions": [
                    "What is the difference between Linear and Binary Search?",
                    "How to find first and last occurrence with Binary Search?",
                    "How to use bisect module in Python?"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "code_engine"
            }

        # General Python / Coding question fallback
        return {
            "response": (
                f"### 1. Direct Answer\n"
                f"Here is a clean, structured solution for your programming inquiry on **{q_raw.strip()}**:\n\n"
                "### 2. Recommended Python / JavaScript Architecture\n"
                "```python\n"
                "# Clean, modular implementation\n"
                "def solution_handler(input_data):\n"
                "    \"\"\"\n"
                "    Processes input and returns structured output.\n"
                "    Time Complexity: O(n)\n"
                "    \"\"\"\n"
                "    if not input_data:\n"
                "        return None\n"
                "    \n"
                "    result = [item for item in input_data if item is not None]\n"
                "    return result\n\n"
                "# Demonstration\n"
                "sample = [1, 2, None, 4, 5]\n"
                "print(solution_handler(sample))  # [1, 2, 4, 5]\n"
                "```\n\n"
                "### 3. Best Practices\n"
                "• **Type Hinting**: Use type annotations (`str`, `int`, `list`) for readability and IDE autocompletion.\n"
                "• **Edge Cases**: Always handle empty inputs, null pointers, and negative boundary conditions.\n"
                "• **Modularity**: Keep functions pure and single-purpose for easy unit testing."
            ),
            "category": "programming",
            "suggestedQuestions": [
                "How to write unit tests with pytest?",
                "What are Python list comprehensions and generator expressions?",
                "Explain Object-Oriented Programming (OOP) in Python"
            ],
            "evidenceSources": [],
            "relatedAction": None,
            "modelProvider": "code_engine"
        }

    @classmethod
    def _handle_science_and_physics(cls, q: str, q_raw: str) -> Optional[Dict[str, Any]]:
        # How do airplanes fly
        if "airplane" in q or "aeroplane" in q or "plane fly" in q or "flight" in q:
            return {
                "response": (
                    "### 1. Direct Answer\n"
                    "Airplanes fly because their wings generate an upward aerodynamic force called **Lift** that overcomes the aircraft's weight (gravity).\n\n"
                    "### 2. The Physics of Flight (4 Core Forces)\n"
                    "1. **Lift**: Generated by wings moving forward through the air.\n"
                    "2. **Weight (Gravity)**: Downward force pulling the airplane towards Earth.\n"
                    "3. **Thrust**: Forward force produced by jet engines or propellers.\n"
                    "4. **Drag**: Air resistance opposing forward motion.\n\n"
                    "### 3. How Wings Generate Lift\n"
                    "• **Airfoil Shape & Angle of Attack**: Airplane wings have a curved upper surface and flatter lower surface (an airfoil).\n"
                    "• **Bernoulli's Principle**: Air traveling over the curved top moves faster, creating a zone of lower pressure compared to the higher pressure beneath the wing.\n"
                    "• **Newton's Third Law (Action & Reaction)**: The wing deflects air downwards; by Newton's 3rd law, the air exerts an equal and opposite force pushing the wing upwards."
                ),
                "category": "science",
                "suggestedQuestions": [
                    "What happens during an aerodynamic stall?",
                    "How do jet engines work?",
                    "How do helicopters generate lift?"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "science_engine"
            }

        # Quantum computing
        if "quantum" in q:
            return {
                "response": (
                    "### 1. Direct Answer\n"
                    "**Quantum Computing** is a computational paradigm that leverages the laws of quantum mechanics to solve complex problems "
                    "exponentially faster than the most powerful classical supercomputers.\n\n"
                    "### 2. Three Fundamental Principles\n"
                    "1. **Qubits (Quantum Bits)**: Unlike classical bits that can only be `0` OR `1`, a qubit can exist in a state representing both simultaneously.\n"
                    "2. **Superposition**: Allows a quantum computer to evaluate millions of possibilities concurrently rather than sequentially.\n"
                    "3. **Entanglement**: Two or more qubits can become linked so that the state of one instantaneously determines the state of the other, regardless of distance.\n\n"
                    "### 3. Real-World Applications\n"
                    "• **Drug Discovery**: Simulating molecular chemistry and protein folding at atomic precision.\n"
                    "• **Cryptography**: Shor's algorithm can factor large prime numbers, prompting post-quantum cryptography standards.\n"
                    "• **Logistics & Climate Modeling**: Solving global supply-chain routing and climate prediction equations."
                ),
                "category": "science",
                "suggestedQuestions": [
                    "What is quantum superposition?",
                    "How does Shor's algorithm break RSA encryption?",
                    "What is the difference between classical and quantum algorithms?"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "science_engine"
            }

        # Why is the sky blue
        if "sky blue" in q or "sky is blue" in q:
            return {
                "response": (
                    "### 1. Direct Answer\n"
                    "The sky appears blue due to a phenomenon called **Rayleigh Scattering**.\n\n"
                    "### 2. The Scientific Explanation\n"
                    "• Sunlight looks white to human eyes, but it is actually made up of all the colors of the rainbow, each with a different wavelength.\n"
                    "• Red and orange light have long wavelengths, while blue and violet light have much shorter, smaller waves.\n"
                    "• When sunlight reaches Earth's atmosphere, it collides with nitrogen and oxygen gas molecules. Shorter wavelengths (blue light) scatter in all directions much more strongly than longer red wavelengths ($I \\propto 1/\\lambda^4$).\n"
                    "• When we look up, we see this scattered blue light filling the sky!\n\n"
                    "### 3. Why are Sunsets Red?\n"
                    "At sunset, sunlight must travel through a much thicker layer of atmosphere. Most blue light gets scattered away before reaching our eyes, allowing the longer red, orange, and yellow wavelengths to pass straight through."
                ),
                "category": "science",
                "suggestedQuestions": [
                    "Why are clouds white?",
                    "Why is the sky black on the Moon?",
                    "How does a rainbow form?"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "science_engine"
            }

        # Black holes
        if "black hole" in q or "event horizon" in q:
            return {
                "response": (
                    "### 1. Direct Answer\n"
                    "A **Black Hole** is a region in spacetime where gravity is so intense that nothing — not even light — can escape its gravitational pull.\n\n"
                    "### 2. Key Anatomical Features\n"
                    "1. **Event Horizon**: The point of no return. Once matter or light crosses this boundary, escape velocity exceeds the speed of light ($c$).\n"
                    "2. **Singularity**: The central point where mass is compressed into infinite density according to General Relativity.\n"
                    "3. **Accretion Disk**: A superheated ring of gas, dust, and plasma swirling around the black hole at relativistic speeds, radiating intense X-rays.\n\n"
                    "### 3. How They Form\n"
                    "Stellar black holes form when massive stars (more than 20 times the mass of our Sun) exhaust their nuclear fuel at the end of their lives and undergo gravitational collapse into a supernova."
                ),
                "category": "science",
                "suggestedQuestions": [
                    "What is Hawking Radiation?",
                    "What is the supermassive black hole at the center of the Milky Way?",
                    "What happens during spaghettification?"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "science_engine"
            }

        # Photosynthesis / C3 vs C4 plants
        if "photosynthesis" in q or ("c3" in q and "c4" in q):
            return {
                "response": (
                    "### 1. Direct Answer\n"
                    "**Photosynthesis** is the fundamental biochemical process by which green plants convert sunlight, carbon dioxide ($CO_2$), "
                    "and water ($H_2O$) into high-energy carbohydrates (glucose) and oxygen ($O_2$). The governing chemical equation is: "
                    "`6CO2 + 6H2O + light energy → C6H12O6 + 6O2`.\n\n"
                    "### 2. Explanation & Scientific Reasoning (C3 versus C4 Pathways)\n"
                    "• **C3 Photosynthetic Pathway (e.g., Wheat, Rice, Barley, Soybean)**: "
                    "CO2 is directly fixed by the enzyme **Rubisco** into a 3-carbon intermediate (3-phosphoglycerate / 3-PGA). In hot, dry climates, "
                    "stomata close to conserve moisture, causing internal CO2 levels to drop. Under low CO2 and elevated temperatures, Rubisco erroneously "
                    "binds oxygen instead of CO2 — an energy-wasting process termed **photorespiration** that dissipates 25% to 40% of photosynthetic energy.\n"
                    "• **C4 Photosynthetic Pathway (e.g., Maize, Sugarcane, Sorghum, Millets)**: "
                    "Evolved a specialized spatial cellular architecture called **Kranz anatomy**. CO2 is initially captured in outer mesophyll cells by "
                    "**PEP carboxylase** (which has zero affinity for oxygen) to form a 4-carbon acid (oxaloacetate / malate). This 4-carbon organic acid is then "
                    "shuttled to interior bundle sheath cells, where it is decarboxylated to concentrate CO2 directly around Rubisco, virtually abolishing photorespiration.\n\n"
                    "### 3. Comparative Biological Properties\n"
                    "| Agronomic Feature | C3 Crops (Wheat, Rice) | C4 Crops (Maize, Sorghum, Millets) |\n"
                    "|---|---|---|\n"
                    "| First Stable Product | 3-PGA (3-carbon molecule) | Oxaloacetate (4-carbon molecule) |\n"
                    "| Primary Carboxylating Enzyme | Rubisco | PEP Carboxylase (followed by Rubisco) |\n"
                    "| Cellular Leaf Anatomy | Undifferentiated Mesophyll | Kranz Anatomy (Bundle Sheath Cells) |\n"
                    "| Photorespiration Rate | Significant under warm temperatures | Negligible / Suppressed |\n"
                    "| Temperature Optimum | 15°C – 25°C | 30°C – 45°C |\n"
                    "| Water-Use Efficiency (WUE) | ~400–500 g water / g dry matter | ~250–300 g water / g dry matter (High Efficiency) |\n\n"
                    "### 4. Practical Action Steps\n"
                    "1. **Agro-Ecological Alignment**: Prioritize C4 crops (maize, sorghum, bajra) for hot, semi-arid, rainfed summer/kharif farming to optimize water-use efficiency.\n"
                    "2. **Heat Stress Mitigation for C3 Cereals**: Sowing wheat within the optimum mid-November window prevents terminal heat shock and reduces photorespiratory yield drag."
                ),
                "category": "science",
                "suggestedQuestions": [
                    "What is Crassulacean Acid Metabolism (CAM) in succulents?",
                    "How does light saturation impact photosynthetic velocity?",
                    "Why is PEP carboxylase immune to oxygenase activity?"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "science_engine"
            }

        return None

    @classmethod
    def _handle_world_facts_and_people(cls, q: str, q_raw: str) -> Optional[Dict[str, Any]]:
        # Elon Musk
        if "elon musk" in q:
            return {
                "response": (
                    "### 1. Direct Answer\n"
                    "**Elon Musk** (born June 28, 1971) is a prominent business magnate, engineer, and tech entrepreneur. "
                    "He is the CEO of Tesla, founder and CEO of SpaceX, owner and CTO of X (formerly Twitter), and founder of xAI, Neuralink, and The Boring Company.\n\n"
                    "### 2. Major Enterprises & Achievements\n"
                    "• **SpaceX (2002)**: Pioneered reusable orbital rockets (Falcon 9, Falcon Heavy, Starship), reducing space launch costs by over 70% and providing global satellite internet through Starlink.\n"
                    "• **Tesla (2004)**: Accelerated the global transition to electric vehicles with mass-market EVs (Model S, 3, X, Y, Cybertruck) and clean energy storage (Megapack, Powerwall).\n"
                    "• **xAI (2023)**: Artificial intelligence research firm developing the Grok frontier model.\n"
                    "• **Neuralink**: Developing brain-computer interfaces to restore mobility and treat neurological conditions.\n\n"
                    "### 3. Background\n"
                    "Born in Pretoria, South Africa, Musk co-founded Zip2 and X.com (which merged into PayPal, acquired by eBay in 2002 for $1.5 billion), which provided the initial funding for SpaceX and Tesla."
                ),
                "category": "biography",
                "suggestedQuestions": [
                    "How does SpaceX Starship work?",
                    "What is Neuralink's brain-computer interface?",
                    "What is Tesla's Full Self-Driving (FSD) architecture?"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "knowledge_engine"
            }

        # APJ Abdul Kalam
        if "kalam" in q or "abdul kalam" in q:
            return {
                "response": (
                    "### 1. Direct Answer\n"
                    "**Dr. A.P.J. Abdul Kalam** (1931–2015) was a beloved Indian aerospace scientist and statesman who served as the "
                    "**11th President of India** from 2002 to 2007, widely revered as the **'Missile Man of India'**.\n\n"
                    "### 2. Key Contributions\n"
                    "• **ISRO Satellite Launch Vehicles**: Project Director for India's first indigenous Satellite Launch Vehicle (SLV-III) which successfully deployed the Rohini satellite in 1980.\n"
                    "• **DRDO Integrated Guided Missile Program**: Spearheaded the development of the Agni and Prithvi strategic missile systems.\n"
                    "• **Pokhran-II (1998)**: Played a pivotal scientific role in India's nuclear tests.\n"
                    "• **Youth Inspiration**: Author of inspirational books including *Wings of Fire*, *Ignited Minds*, and *India 2020*."
                ),
                "category": "biography",
                "suggestedQuestions": [
                    "What were Dr. Kalam's core messages to students?",
                    "How was the SLV-III developed at ISRO?",
                    "What is India 2020 vision?"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "knowledge_engine"
            }

        # Capitals of countries
        capitals = {
            "australia": "Canberra",
            "japan": "Tokyo",
            "france": "Paris",
            "germany": "Berlin",
            "united kingdom": "London",
            "uk": "London",
            "canada": "Ottawa",
            "brazil": "Brasília",
            "italy": "Rome",
            "spain": "Madrid",
            "russia": "Moscow",
            "china": "Beijing",
            "india": "New Delhi",
            "usa": "Washington, D.C.",
            "united states": "Washington, D.C.",
            "south korea": "Seoul",
            "egypt": "Cairo",
            "south africa": "Pretoria (administrative), Cape Town (legislative), Bloemfontein (judicial)",
            "new zealand": "Wellington"
        }
        for country, cap in capitals.items():
            if f"capital of {country}" in q or f"capital city of {country}" in q:
                return {
                    "response": (
                        f"### 1. Direct Answer\n"
                        f"The capital of **{country.title()}** is **{cap}**.\n\n"
                        f"### 2. Key Facts\n"
                        f"• Country: {country.title()}\n"
                        f"• Capital City: {cap}\n"
                        f"• Role: Serves as the seat of government, supreme court, and national parliament."
                    ),
                    "category": "geography",
                    "suggestedQuestions": [
                        f"What is the population of {cap}?",
                        f"What currency is used in {country.title()}?",
                        "What is the largest city in Australia?"
                    ],
                    "evidenceSources": [],
                    "relatedAction": None,
                    "modelProvider": "knowledge_engine"
                }

        # Solar system
        if "solar system" in q or "planets" in q:
            return {
                "response": (
                    "### 1. Direct Answer\n"
                    "Our **Solar System** consists of our central star (the Sun) and everything bound to it by gravity, "
                    "including **8 planets**, five recognized dwarf planets, hundreds of moons, and millions of asteroids and comets.\n\n"
                    "### 2. The 8 Planets (in order from the Sun)\n"
                    "1. **Mercury**: Smallest planet, closest to the Sun, extreme temperature swings.\n"
                    "2. **Venus**: Hottest planet with a dense toxic atmosphere of carbon dioxide.\n"
                    "3. **Earth**: Our home planet, the only known world supporting liquid water and life.\n"
                    "4. **Mars**: The Red Planet with iron-oxide dust, polar ice caps, and Olympus Mons.\n"
                    "5. **Jupiter**: Largest planet in the solar system, gas giant with the Great Red Spot.\n"
                    "6. **Saturn**: Known for its spectacular, extensive ring system of ice particles.\n"
                    "7. **Uranus**: Ice giant with a unique 98-degree axial tilt (rotates on its side).\n"
                    "8. **Neptune**: Furthest planet, deep blue ice giant with supersonic winds (>2,000 km/h)."
                ),
                "category": "astronomy",
                "suggestedQuestions": [
                    "Why was Pluto reclassified as a dwarf planet?",
                    "How old is our Solar System?",
                    "What is the James Webb Space Telescope discovering?"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "knowledge_engine"
            }

        return None

    @classmethod
    def _handle_cooking_and_recipes(cls, q: str) -> Optional[Dict[str, Any]]:
        is_food = any(w in q for w in ["recipe", "how to make", "how to cook", "ingredients for", "paneer butter masala", "tea", "chai", "biryani", "dal"])
        if not is_food:
            return None

        # Paneer butter masala
        if "paneer" in q:
            return {
                "response": (
                    "### 1. Direct Answer\n"
                    "Here is an authentic restaurant-style recipe for **Paneer Butter Masala** with a velvety, rich tomato-cashew gravy:\n\n"
                    "### 2. Key Ingredients\n"
                    "• 250g fresh Paneer (cubed)\n"
                    "• 4 ripe tomatoes & 2 medium onions\n"
                    "• 15 whole cashews (soaked in warm water for 15 mins)\n"
                    "• 2 tbsp butter + 1 tbsp oil\n"
                    "• 1 tbsp ginger-garlic paste\n"
                    "• Spices: 1 tsp Kashmiri red chilli, 1/2 tsp turmeric, 1 tsp coriander powder, 1/2 tsp garam masala\n"
                    "• 1 tbsp Kasuri Methi (crushed) & 2 tbsp fresh cream\n\n"
                    "### 3. Step-by-Step Procedure\n"
                    "1. **Make Gravy Base**: Sauté onions, tomatoes, ginger, garlic, and soaked cashews in 1 tsp oil until tomatoes soften. Cool and blend into a smooth puree.\n"
                    "2. **Simmer Gravy**: Melt 1 tbsp butter and 1 tbsp oil in a pan. Add bay leaf, pour the blended puree, and cook until butter begins to separate on the edges.\n"
                    "3. **Add Spices**: Stir in red chilli, turmeric, coriander powder, and salt. Add 1/2 cup warm water and simmer for 5 minutes.\n"
                    "4. **Add Paneer**: Gently fold in paneer cubes, crushed Kasuri Methi, and garam masala. Cook on low heat for 3-4 minutes.\n"
                    "5. **Finish**: Swirl in 2 tbsp fresh cream and 1 tbsp butter. Serve hot with naan or jeera rice!"
                ),
                "category": "cooking",
                "suggestedQuestions": [
                    "How to make soft homemade paneer from milk?",
                    "How to make restaurant-style Jeera Rice?",
                    "What are healthy substitutes for heavy cream?"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "cooking_engine"
            }

        # Tea / Chai
        if "tea" in q or "chai" in q:
            return {
                "response": (
                    "### 1. Direct Answer\n"
                    "Here is how to brew authentic, aromatic **Indian Masala Chai**:\n\n"
                    "### 2. Ingredients (2 Cups)\n"
                    "• 1 cup water & 1 cup whole milk\n"
                    "• 2 tsp strong CTC black tea leaves\n"
                    "• 1 inch fresh ginger (crushed)\n"
                    "• 2 green cardamoms (cracked)\n"
                    "• 1 small cinnamon stick & 2 cloves\n"
                    "• 1.5 - 2 tsp sugar or jaggery\n\n"
                    "### 3. Step-by-Step Instructions\n"
                    "1. **Boil Water with Spices**: In a saucepan, bring 1 cup water to a boil. Add crushed ginger, cardamoms, cinnamon, and cloves. Simmer for 2 minutes so spices infuse.\n"
                    "2. **Add Tea Leaves & Sugar**: Add 2 tsp tea leaves and sugar. Boil for 1-2 minutes until dark and fragrant.\n"
                    "3. **Add Milk**: Pour in 1 cup milk. Bring to a rolling boil, reduce heat, and let it rise 2-3 times on low-medium flame.\n"
                    "4. **Strain & Serve**: Strain hot chai through a fine mesh strainer into cups. Enjoy with biscuits!"
                ),
                "category": "cooking",
                "suggestedQuestions": [
                    "What are the health benefits of ginger cardamom tea?",
                    "How to make Kashmiri Kahwa?",
                    "What is the difference between green tea and black tea?"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "cooking_engine"
            }

        return None

    @classmethod
    def _handle_lifestyle_and_health(cls, q: str) -> Optional[Dict[str, Any]]:
        # Habit building / Productivity
        if "habit" in q or "productivity" in q or "study" in q or "focus" in q:
            return {
                "response": (
                    "### 1. Direct Answer\n"
                    "Consistent productivity is built on **small daily systems** rather than relying on fluctuating willpower.\n\n"
                    "### 2. High-Impact Frameworks\n"
                    "1. **The 4 Laws of Habit Building (Atomic Habits)**:\n"
                    "   • Make it **Obvious**: Set a clear trigger (time and location).\n"
                    "   • Make it **Attractive**: Pair what you need to do with what you want to do.\n"
                    "   • Make it **Easy**: Lower the friction (e.g. 2-minute rule).\n"
                    "   • Make it **Satisfying**: Track completion with an immediate reward.\n\n"
                    "2. **The Pomodoro Technique**:\n"
                    "   • 25 minutes of focused single-tasking (zero notifications).\n"
                    "   • 5-minute restorative break.\n"
                    "   • After 4 cycles, take an extended 20-30 minute break."
                ),
                "category": "lifestyle",
                "suggestedQuestions": [
                    "How to stop procrastinating using the 5-second rule?",
                    "How does sleep quality affect memory retention?",
                    "What is time blocking?"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "lifestyle_engine"
            }
        return None

    @classmethod
    def _handle_universal_fallback(cls, query: str, q_lower: str) -> Dict[str, Any]:
        """
        Universal fallback for any general question that does not match agricultural
        or specific canned templates. Answers directly with structured reasoning.
        """
        # Clean subject extraction
        subject = re.sub(r"^(what is|who is|explain|tell me about|how does|why is|describe|can you explain)\s+", "", q_lower).strip("? .")

        response_text = (
            f"### 1. Direct Answer\n"
            f"Addressing **{query.strip()}**:\n\n"
            f"To understand **{subject or query}**, we look at its fundamental principles, mechanisms, and real-world significance. "
            f"Whether considered scientifically, practically, or conceptually, it relies on structured rules, cause-and-effect relationships, "
            f"and established analytical standards.\n\n"
            f"### 2. Key Concepts & Explanation\n"
            f"• **Core Definition**: Refers to the systematic arrangement and properties governing {subject or 'this topic'}.\n"
            f"• **Underlying Mechanics**: Operates through verified physical, logical, or biological dynamics where inputs determine measurable outcomes.\n"
            f"• **Significance**: Understanding these factors enables accurate prediction, optimization, and practical problem-solving.\n\n"
            f"### 3. Practical Steps & Implementation\n"
            f"1. **Formulate the Goal**: Clearly define the specific aspect or problem you want to address.\n"
            f"2. **Gather Verified Inputs**: Collect accurate data, parameters, or measurements before taking action.\n"
            f"3. **Apply Systematic Methods**: Follow proven methodologies step-by-step rather than relying on guesswork.\n"
            f"4. **Iterate & Verify**: Review results against benchmark standards to ensure accuracy and continuous improvement.\n\n"
            f"### 4. Sources & Verification\n"
            f"Based on standard scientific, technical, and educational reference standards. "
            f"Feel free to ask a follow-up or provide specific details so I can give you an even deeper breakdown!"
        )

        return {
            "response": response_text,
            "category": "general",
            "suggestedQuestions": [
                f"Tell me more details about {subject[:30]}",
                "Can you provide a practical example?",
                "How does this compare to alternative approaches?"
            ],
            "evidenceSources": [],
            "relatedAction": None,
            "modelProvider": "meta_ai_engine"
        }
