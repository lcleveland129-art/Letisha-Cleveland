"""Edited manuscript text for Joesiah & Malani: Noah's Bloodline (Book 1).

Block types:
  ('p', text)                 body paragraph
  ('quote', text, ref)        Scripture quotation (NIV unless noted)
  ('names', [..])             emphasized list of names (author's stacked-name style)
  ('emph', text)              single emphasized word/line
  ('motto',)                  series motto box
  ('thought', label, text)    highlighted lesson / thought (label may be '')
  ('pledge', text)            "I WILL READ BEFORE I REPEAT."
  ('turn', text)              TURN THE PAGE teaser
  ('read', label, refs)       READ IT FOR YOURSELF / READ AND DISCOVER band (bottom of page)
  ('end',)                    The Journey Continues box (end of Book 1)
"""

TITLE = "Joesiah & Malani"
SUBTITLE = "Noah’s Bloodline"
SERIES = "Joesiah & Malani"
BOOK_NO = 1
AUTHOR = "LeTisha C. Cleveland"
TAGLINE = "Our Family, Our History, God’s Plan"
MOTTO = ("Know the Word. Seek the Truth. Remember who you are. "
         "Walk in the purpose God gave you.")
NEXT_BOOK = "From Abraham to Moses: The Journey to Freedom"

CHAPTERS = [
 (1, "Noah: A Man Who Walked With God", [
  ('p', "Long before Noah built an ark, he was known for something even more important: the way he lived."),
  ('p', "The Bible describes a world where violence and wrongdoing had become widespread. People were making choices that moved them farther away from God. But Noah was different."),
  ('p', "Scripture says:"),
  ('quote', "“Noah was a righteous man, blameless among the people of his time, and he walked faithfully with God.”", "Genesis 6:9"),
  ('p', "Noah was the son of Lamech and a descendant of Seth, the son of Adam and Eve. When Noah was born, his father believed his life would bring comfort to a world filled with difficult labor. His name became connected with the idea of rest and comfort."),
  ('p', "Noah grew up, married, and became the father of three sons: Shem, Ham, and Japheth."),
  ('p', "While the world around him changed, Noah continued walking with God. He was not chosen because he was the strongest man, the richest man, or the most powerful man. God saw his character. Noah listened. Noah trusted. Noah obeyed."),
  ('p', "One day, God gave Noah an assignment that must have seemed impossible. He told him to build an enormous ark."),
  ('p', "Joesiah looked at Grandma. “God chose Noah before Noah ever built the ark?”"),
  ('p', "Grandma smiled. “Exactly. The ark did not make Noah faithful. His faithfulness came first.”"),
  ('p', "Malani looked toward the enormous wooden structure beginning to rise in the distance."),
  ('p', "Grandma took both of their hands. “Always remember this: God may prepare your heart long before He reveals your assignment. That is why you must learn His Word, seek His truth, and remember who He created you to be.”"),
  ('motto',),
  ('thought', '', "Sometimes the greatest preparation for your purpose happens when nobody else is watching."),
  ('read', "READ IT FOR YOURSELF", "Genesis 5:28–32 and Genesis 6:5–22"),
 ]),
 (2, "The Ark, Flood & Covenant", [
  ('p', "God told Noah that violence and corruption had filled the earth and that a great judgment was coming. But God also gave Noah a way forward."),
  ('p', "God gave Noah careful instructions for building the ark. Noah obeyed, even though the assignment must have seemed impossible."),
  ('p', "When the ark was ready, the animals came according to God’s instructions. Scripture gives more detail than simply saying “two of every animal”: Noah was instructed to take seven pairs of every kind of clean animal, one pair of every kind of animal that was not clean, and seven pairs of every kind of bird."),
  ('p', "Then rain fell for forty days and forty nights. The waters rose, and the ark carried Noah, his family, and the animals safely through the flood."),
  ('p', "When the waters finally receded, Noah stepped onto dry ground and built an altar to God. God established His covenant with Noah and his descendants, and the rainbow became the sign of that promise."),
  ('p', "Joesiah looked at Grandma. “So the ark was only one part of Noah’s story?”"),
  ('p', "“Exactly,” Grandma said. “Faith means trusting God enough to obey, even before you can see how everything will work out.”"),
  ('read', "READ IT FOR YOURSELF", "Genesis 6:11–22 and Genesis 7–9"),
 ]),
 (3, "Noah’s Sons & the Generations After the Flood", [
  ('p', "After the flood, Noah’s family began a new chapter."),
  ('p', "Noah had three sons:"),
  ('names', ["Shem", "Ham", "Japheth"]),
  ('p', "Genesis tells us that their families grew over generations and spread into different lands. Through their descendants, the Bible begins tracing families and nations that would appear throughout Scripture."),
  ('p', "Joesiah studied the family tree. “So everybody had their own children, and then those children had children?”"),
  ('p', "“Exactly,” Grandma said. “That is how a family becomes generations.”"),
  ('p', "Malani pointed at the names. Grandma smiled. “Every name is part of a larger story.”"),
  ('p', "Then she pointed to one name in particular."),
  ('emph', "Ham."),
  ('p', "“To understand where our journey goes next, we need to meet Ham’s sons.”"),
  ('read', "READ IT FOR YOURSELF", "Genesis 9:18–19 and Genesis 10"),
 ]),
 (4, "Ham’s Family: Cush, Mizraim, Put & Canaan", [
  ('p', "Genesis names four sons of Ham:"),
  ('names', ["Cush", "Mizraim", "Put", "Canaan"]),
  ('p', "These names become important as the Bible describes peoples and lands of the ancient world."),
  ('p', "Mizraim is the Hebrew biblical name associated with Egypt. Cush is commonly associated with lands south of Egypt, including areas connected with ancient Nubia and Kush."),
  ('p', "Scholars continue to study exactly how every biblical name and ancient geographical region should be identified, so Grandma reminded the children of something important: “Sometimes the Bible tells us one thing, while history and archaeology help us investigate another. We should never turn an interpretation into a fact that Scripture itself does not state.”"),
  ('p', "Joesiah nodded. “So we have to know the difference between what the Bible actually says and what people say it means?”"),
  ('p', "“Exactly.” Grandma pointed again at the family tree. “And there is one name here that people have misunderstood for generations.”"),
  ('emph', "Canaan."),
 ]),
 (5, "Canaan: Read What the Bible Actually Says", [
  ('p', "Joesiah looked concerned. “I heard Ham was cursed.”"),
  ('p', "Grandma opened her Bible. “That is exactly why we read Scripture for ourselves.”"),
  # NEW (requested by author): brief, Scripture-based account of what happened in Genesis 9:20-24.
  ('p', "After the flood, Noah planted a vineyard. One day he drank too much wine, became drunk, and lay uncovered inside his tent. Ham saw his father that way and went outside to tell his brothers. But Shem and Japheth took a garment, walked in backward so they would not look, and covered their father."),
  ('p', "When Noah woke up, he learned what Ham had done. The Bible does not say Noah was angry, and it does not explain every detail. But it shows that Ham dishonored his father, while his brothers protected their father’s dignity. Then Noah spoke the words recorded in Genesis 9:25: “Cursed be Canaan…”"),
  ('p', "Joesiah looked back at the family tree. “Canaan was Ham’s son.”"),
  ('p', "“Yes,” Grandma answered. “And notice something else. The verse does not say, ‘Cursed be Ham.’”"),
  ('p', "She continued, “It also does not say that Black people were cursed. It does not say Africans were cursed. And it does not say that the descendants of Ham were created to be slaves because of the color of their skin.”"),
  ('p', "Centuries later, some people developed interpretations often called the “Curse of Ham.” These interpretations were used to portray African people as divinely destined for servitude and to defend racial slavery. But that racial interpretation is not what Genesis 9:25 says."),
  ('p', "Joesiah became quiet. “So people used the Bible to justify something the verse didn’t actually say?”"),
  ('p', "“Some did,” Grandma answered. “And that is why knowing God’s Word for yourself matters.”"),
  ('thought', '', "Before you repeat what someone tells you about your Bible, your history, or your people—read it, study it, and seek the truth for yourself."),
  ('pledge', "I WILL READ BEFORE I REPEAT."),
  ('motto',),
  ('turn', "The story of African people does not begin with slavery."),
  ('read', "READ IT FOR YOURSELF", "Genesis 9:18–27"),
 ]),
 (6, "Africa: A Continent of Knowledge and Achievement", [
  ('p', "Grandma turned the page. Before Joesiah and Malani appeared a vast continent filled with rivers, fertile lands, cities, kingdoms, trade routes, families, farmers, artisans, builders, and scholars."),
  ('emph', "Africa."),
  ('p', "Joesiah stared at the scene. “Grandma, I usually hear about Africa when people talk about slavery.”"),
  ('p', "Grandma looked at him. “Then we are going to begin much earlier.”"),
  ('p', "Africa’s history stretches back thousands of years. Long before the transatlantic slave trade, African peoples developed complex societies and civilizations with systems of government, agriculture, trade, architecture, craftsmanship, and learning."),
  ('p', "Along the Nile Valley, communities learned to use the river’s seasonal cycles to support agriculture. Builders constructed monuments that still stand thousands of years later. Artisans worked with stone, wood, metals, and precious materials. Scribes recorded information. People studied the heavens, developed mathematical knowledge, and practiced forms of medicine."),
  ('p', "Malani pointed toward the boats on the river. “Boats!”"),
  ('p', "“Yes,” Grandma said. “People traveled and traded too.”"),
  ('p', "Joesiah looked across the busy scene. “So Africa had history long before slavery?”"),
  ('p', "Grandma smiled. “Thousands of years of it.”"),
  ('thought', '', "Your history does not begin where someone else’s history book decided to start telling it."),
  ('read', "READ AND DISCOVER", "Study the histories of the Nile Valley, ancient Egypt, Nubia, and Kush."),
 ]),
 (7, "Egypt (Kemet) and Nubia (Kush)", [
  ('p', "Their journey carried them into the Nile Valley."),
  ('p', "Two of its great civilizations were ancient Egypt and Nubia, including the kingdom later known as Kush."),
  ('p', "Ancient Egyptians called their land by names that included Kemet, while the Bible commonly refers to Egypt using the Hebrew name Mizraim."),
  ('p', "To the south were the lands of Nubia and, during important periods of its history, the powerful Kingdom of Kush."),
  ('p', "Joesiah remembered the family tree. “Mizraim was also one of Ham’s sons.”"),
  ('p', "“Yes,” Grandma answered. “Genesis uses that name in Ham’s genealogy, and the same Hebrew term is used for Egypt. But we have to be careful.”"),
  ('p', "“Why?” Joesiah asked."),
  ('p', "“Because a biblical genealogy and the archaeological history of an entire civilization are not exactly the same kind of evidence. We can study how they relate without pretending we know more than the evidence tells us.”"),
  ('p', "Egyptian civilization developed over thousands of years. Its people built cities, temples, and monumental structures. They developed hieroglyphic writing, organized government, extensive agriculture, and far-reaching trade networks."),
  ('p', "They used mathematics and geometry in practical life and construction. Egyptian medical writings preserve observations about illnesses, injuries, and treatments."),
  ('p', "South of Egypt, Nubian societies also developed powerful kingdoms and trading centers. Kush became especially influential. Kushite rulers eventually controlled Egypt during its 25th Dynasty, and Nubian builders constructed their own pyramids, temples, and royal centers."),
  ('p', "Joesiah looked at Grandma. “So Egypt wasn’t the only great civilization here?”"),
  ('p', "“Not at all.”"),
 ]),
 (8, "Before Joseph Arrived", [
  ('p', "Grandma led the children through a bustling reconstruction of ancient life."),
  ('p', "Farmers worked near the Nile. Boats transported people and goods. Craftspeople created pottery, jewelry, and tools. Scribes recorded information. Builders planned enormous structures. Markets were filled with activity. Children learned from their families and communities."),
  ('p', "“This is important,” Grandma told them. “When we reach Joseph’s story, I don’t want you imagining that he arrived in an empty or undeveloped land.”"),
  ('p', "When Joseph arrived, he would enter a civilization with established rulers, agriculture, cities, administration, trade, religion, architecture, and systems for storing and distributing resources."),
  ('p', "That matters because understanding the world surrounding a Bible story can help us understand the story itself."),
  ('p', "Joesiah looked toward a great Egyptian city in the distance. “So now we’re going to meet Joseph?”"),
  ('p', "Grandma nodded. “But first, remember what you’ve learned.”"),
  ('motto',),
  ('turn', "Joseph’s journey began in betrayal and slavery. But his story would not end there."),
 ]),
 (9, "Joseph Comes to Egypt", [
  ('p', "Many generations had passed since Noah."),
  ('p', "Through the family line of Shem came Abraham, then Isaac, then Jacob. Jacob had twelve sons, and one of them was Joseph."),
  ('p', "Joseph’s brothers became jealous of him. Their jealousy eventually led to betrayal. They sold Joseph, and he was taken away from his home. His journey carried him into Egypt."),
  ('p', "Joesiah looked at Grandma. “So Joseph didn’t choose to go there?”"),
  ('p', "“No,” Grandma answered. “Joseph entered Egypt as an enslaved young man. What happened to him was painful and unjust.”"),
  ('p', "Malani reached for Grandma’s hand."),
  ('p', "“But God had not forgotten Joseph,” Grandma continued."),
  ('p', "Joseph entered a civilization that had existed long before his arrival. Egypt already had rulers, cities, agriculture, trade, craftspeople, administrators, and systems of government."),
  ('p', "Joseph had lost his freedom. He had been separated from his family. He could not see what his future held. But his story was not finished."),
  ('thought', "LESSON FOR US", "A painful chapter does not have to become the ending of your story."),
  ('read', "READ IT FOR YOURSELF", "Genesis 37 and Genesis 39:1"),
 ]),
 (10, "From Servant to Prisoner", [
  ('p', "In Egypt, Joseph was sold to Potiphar, an officer of Pharaoh. Joseph worked faithfully, and Potiphar placed him in charge of his household."),
  ('p', "But trouble came again. After Joseph rejected the advances of Potiphar’s wife, she falsely accused him. Joseph was sent to prison."),
  ('p', "Joesiah frowned. “He did the right thing and still got punished?”"),
  ('p', "“Yes,” Grandma said. “Doing what is right does not mean life will always be easy.”"),
  ('p', "But even in prison, Joseph continued to serve faithfully. There he met two officials from Pharaoh’s household who had troubling dreams."),
  ('p', "Joseph told them that interpretations belonged to God, and he explained what their dreams meant."),
  ('p', "Later, Pharaoh himself began having dreams that no one around him could explain. One of the officials finally remembered Joseph."),
  ('p', "Joseph was brought out of prison and taken before Pharaoh. His circumstances were about to change."),
  ('read', "READ IT FOR YOURSELF", "Genesis 39–41"),
 ]),
 (11, "Joseph Rises to Leadership", [
  ('p', "Pharaoh described his dreams to Joseph."),
  ('p', "Joseph explained that the dreams carried a warning. Egypt would experience seven years of great abundance, followed by seven years of severe famine."),
  ('p', "Joseph did more than interpret the dreams. He recommended preparing during the years of abundance by storing grain for the difficult years ahead."),
  ('p', "Pharaoh recognized Joseph’s wisdom. He placed Joseph in authority over his house and gave him great responsibility throughout Egypt, while Pharaoh remained on the throne."),
  ('p', "Joesiah’s eyes widened. “He went from being enslaved to being trusted with that much responsibility?”"),
  ('p', "“Yes,” Grandma answered. “But notice something important. Joseph’s story wasn’t only about gaining a position. His position gave him an opportunity to serve.”"),
  ('p', "During the years of abundance, grain was gathered and stored. Then the famine came. Because preparations had been made, food was available."),
  ('thought', '', "Purpose is not only about where God takes you. It is also about what you do when you get there."),
  ('read', "READ IT FOR YOURSELF", "Genesis 41"),
 ]),
 (12, "A Family Reunited in Egypt", [
  ('p', "The famine extended beyond Egypt. Back in Canaan, Jacob and his family also needed food."),
  ('p', "Eventually, Joseph’s brothers traveled to Egypt to buy grain. They stood before Joseph without realizing who he was."),
  ('p', "Joesiah whispered, “What did Joseph do?”"),
  ('p', "In time, Joseph revealed his identity. His brothers were terrified. But Joseph chose reconciliation instead of revenge."),
  ('p', "He recognized that although people had intended evil against him, God had brought good from his circumstances and used his position to preserve lives."),
  ('p', "Joseph’s father, Jacob, and his household came to Egypt too. The family settled there. They grew. Their children had children. And their descendants became increasingly numerous."),
  ('p', "But generations passed. Joseph died. The Pharaoh who had known Joseph was gone."),
  ('p', "Later, Scripture tells us:"),
  ('quote', "“Then a new king, to whom Joseph meant nothing, came to power in Egypt.”", "Exodus 1:8"),
  ('p', "Joesiah looked at Grandma. “That doesn’t sound good.”"),
  ('p', "Grandma shook her head. “It wasn’t.” She closed the Bible gently. “But that is another part of our journey.”"),
 ]),
 (13, "What We Learned", [
  ('p', "Grandma sat between Joesiah and Malani. They had traveled through generations of history."),
  ('p', "They had learned about Noah and his sons. They had followed Ham’s family line through Cush, Mizraim, Put, and Canaan."),
  ('p', "They had discovered what Genesis actually says about Canaan and why Scripture should never be twisted to justify racism or oppression."),
  ('p', "They had explored African civilizations whose histories stretch back thousands of years."),
  ('p', "And they had followed Joseph into Egypt—from betrayal and enslavement to responsibility, preparation, forgiveness, and reunion."),
  ('p', "Grandma looked at them. “Never be afraid to ask questions. Faith does not require you to stop learning.”"),
  ('motto',),
  ('p', "Joesiah smiled. “And before I repeat something about my Bible, my history, or my people…”"),
  ('p', "Grandma waited."),
  ('p', "Joesiah finished:"),
  ('pledge', "“I WILL READ BEFORE I REPEAT.”"),
  ('p', "Malani grinned. “Read!”"),
  ('p', "Grandma laughed and hugged them both."),
 ]),
 (14, "Our History Continues…", [
  ('p', "Jacob’s descendants remained in Egypt."),
  ('p', "Generations passed. Their numbers increased."),
  ('p', "Then a new Pharaoh arose who did not know Joseph. Fear replaced welcome. Freedom would eventually become bondage."),
  ('p', "And among those descendants, a baby would be born whose life would change their story."),
  ('emph', "His name was Moses."),
  ('p', "Joesiah looked at Grandma. “Are we going there next?”"),
  ('p', "Grandma smiled. “We are.”"),
  ('end',),
 ]),
]

# Scripture spotlight that faces Chapter 12 (Chapter 12 has no illustration).
SPOTLIGHT = {
    'label': "SCRIPTURE SPOTLIGHT",
    'intro': "Joseph’s words to his brothers",
    'text': "“You intended to harm me, but God intended it for good to accomplish what is now being done, the saving of many lives.”",
    'ref': "Genesis 50:20",
}

# Illustration file for each chapter (index into ill-NN.jpg), and for the Book 2 preview.
CHAPTER_ART = {1: 0, 2: 1, 3: 3, 4: 2, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10, 13: 11, 14: 12}
