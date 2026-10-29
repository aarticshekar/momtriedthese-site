# "Most bought right now": top sellers on Amazon US, checked 29 Oct 2026 (sort: best sellers).
# Each lives in ONE home. POPULAR_EXISTING marks products already on the site that are also top sellers.
# (slug, display name, us asin, home, why, best for, monthly buyers on Amazon US, gift section or '')
POP = [
 # Quiet Hour
 ("rock-painting","Glow in the Dark Rock Painting Kit","B08HD89CX6","quiet-hour","Paint the rocks, then watch them glow at bedtime. Comes with everything, so no hunting for supplies.","Ages 6 to 12","10K+",""),
 ("mini-garden","Creativity for Kids Mermaid Mini Garden","B083Z3JMGP","quiet-hour","A little terrarium they plant and look after themselves. The craft keeps going for weeks.","Ages 6 to 10","10K+",""),
 ("paint-by-sticker","Paint by Sticker Kids: Rainbows Everywhere","1523517751","quiet-hour","Numbered stickers that build a picture. Calm, tidy and oddly satisfying.","Ages 6 and up","",""),
 ("aqua-puffs","Skillmatics Aqua Puffs Animals","B0F9WHCL19","quiet-hour","Paint by number with puffy paint that rises as it dries. No mess on the table.","Ages 5 to 9","7K+",""),
 ("hidden-pictures","Silliest Hidden Pictures Puzzles Ever","1639621520","quiet-hour","A seek-and-find book with over a thousand things to spot. Quiet for ages.","Ages 6 and up","",""),
 # Game Night
 ("connect-4","Connect 4 (2025 Edition)","B0FHKZ4BP1","game-night","The classic, now with storage built in. A five-minute game a 6-year-old can win fairly.","Ages 6 and up, 2 players","",""),
 ("hedbanz","Hedbanz Picture Guessing Game","B0BRYH5FJ8","game-night","A card on your head, yes or no questions. Pure giggles.","Ages 7 and up","",""),
 ("herd-mentality","Herd Mentality","B093HBBMPT","game-night","Try to give the same answer as everyone else. Big groups, lots of shouting.","Ages 10 and up, 4 to 20 players","",""),
 ("tapple","Tapple Word Game","B09QRXD9H1","game-night","Name a word in the category before the timer runs out. Fast and loud.","Ages 8 and up","",""),
 # Little Makers
 ("snap-circuits","Snap Circuits Jr. SC-100","B00008BFZH","little-makers","Real electronics with snap-together parts. Over a hundred projects, from a fan to an alarm.","Ages 8 and up","10K+",""),
 ("geodes","National Geographic Break Open 10 Geodes","B0160JB7IS","little-makers","Crack a rock, find crystals inside. Every one is different.","Ages 8 to 12","5K+",""),
 ("magic-chemistry","National Geographic Magic Chemistry Set","B085WF9CHH","little-makers","Ten science tricks that look like magic. Comes with the explanation, too.","Ages 8 to 12","4K+",""),
 ("solar-robot","Sillbird 12-in-1 Solar Robot Kit","B07T1NZD27","little-makers","Builds twelve robots that run on sunlight. A long project for a determined kid.","Ages 8 to 13","5K+",""),
 ("pinball","Smartivity DIY Pinball Machine","B08P5XGHJG","little-makers","Build a working wooden pinball machine, then actually play it.","Ages 8 and up","6K+",""),
 # Lunchbox
 ("omiebox","OmieBox Insulated Bento with Food Jar","B017SGKZUI","lunchbox","A bento with a built-in thermos, so hot and cold sit in one box.","Hot lunches","3K+",""),
 ("funtainer","THERMOS Funtainer Food Jar","B08NCVT244","lunchbox","Keeps pasta or khichdi warm until lunch. The one most parents end up with.","Hot lunches","4K+",""),
 ("sandwich-sealer","Sandwich Cutter and Sealer","B07TBPSF7M","lunchbox","Crustless, sealed sandwiches in one press. Picky eaters suddenly eat the edges.","Picky eaters","1K+",""),
 ("zak-minecraft","Zak Designs Minecraft Water Bottle","B0BVZD4WFN","lunchbox","Stainless steel, keeps water cold, and it's Minecraft. That's the whole pitch.","Minecraft fans","1K+",""),
 ("zak-creeper","Zak Designs Minecraft Creeper Straw Bottle","B0DM5KCYML","lunchbox","A leak-proof straw bottle with the Creeper face. Big enough for a long school day.","Minecraft fans","600+",""),
 # Travel Day
 ("pip-squeaks","Crayola Pip-Squeaks Markers, 65 Count","B00AHAJDQU","travel-day","Short, stubby markers that fit little hands and small bags. Washable.","Ages 3 and up","20K+",""),
 ("eoocoo-tablet","EooCoo Kids LCD Writing Tablet","B0CCTF94DR","travel-day","Draw, wipe, draw again. Light, flat, and no screen time.","Ages 3 to 8","10K+",""),
 ("foot-hammock-bc","BASIC CONCEPTS Airplane Foot Hammock","B07SK6ZFLM","travel-day","Hangs from the tray table so little legs can rest on long flights.","Long-haul flights","8K+",""),
 ("grab-and-go","Hasbro Grab and Go Games (4 Pack)","B0FHY6Z369","travel-day","Mini versions of classic games, sized for the car or a restaurant table.","Ages 6 and up","10K+",""),
 ("travel-wipes","Impossibly Compact Travel Wipes","B0DH3XY69T","travel-day","Tiny tablets that turn into a full wipe with a drop of water. Takes no space.","Handbag","20K+",""),
 # Kid-Safe Tech
 ("noot-k11","noot products K11 Kids Headphones","B0746RBK2M","kid-tech","Volume-limited, wired, sturdy. Simple headphones that survive the school bag.","Ages 3 and up","7K+",""),
 ("ear-muffs","Dr.meter Kids Noise Cancelling Ear Muffs","B01LWYWH43","kid-tech","For fireworks, loud events and very loud cousins. Folds up small.","Ages 3 and up","6K+",""),
 # Fast Kitchen
 ("veg-chopper","Fullstar Vegetable Chopper","B0764HS4SL","fast-kitchen","Onions, tomatoes, cucumber, done in seconds. Saves real time on sabzi nights.","Everyday cooking","20K+",""),
 ("mini-chopper","Hamilton Beach Electric Vegetable Chopper","B06Y2GZWCJ","fast-kitchen","A small electric chopper for ginger, garlic, chutneys and pesto.","Masala bases, chutneys","10K+",""),
 ("drawer-organizers","Vtopmart Clear Drawer Organizers, 25 Pack","B08KXKVT4K","fast-kitchen","Mix-and-match trays so every drawer stops being the junk drawer.","Kitchen drawers","30K+",""),
 ("can-opener","KitchenAid Classic Can Opener","B07YP2VH4B","fast-kitchen","Opens every tin smoothly. A boring tool that quietly works.","Everyday","30K+",""),
 ("cabinet-lights","MCGOR Rechargeable Under Cabinet Lights","B0BDF8CVBN","fast-kitchen","Motion-sensor lights that stick under cabinets. No wiring, easier late-night chai.","Dark counters","10K+",""),
 # Just for You
 ("candle-warmer","Candle Warmer Lamp with Timer","B0DZFGTCLR","just-for-you","Melts the candle from the top, so the scent fills the room with no flame.","Evenings","60K+",""),
 ("clean-towels","Clean Skin Club Clean Towels XL","B07PBXXNCY","just-for-you","Disposable face towels. A small luxury that makes the routine feel like a spa.","Skincare routine","100K+",""),
 # Minecraft Kid
 ("lego-chicken-jockey","LEGO Minecraft Chicken Jockey 21582","B0G2T5CVZ5","minecraft-kid","The chicken jockey from the game, as a buildable figure. Small enough to finish in one afternoon.","Ages 8 and up","10K+",""),
 ("lego-zombie-dungeon","LEGO Minecraft Zombie Dungeon 21587","B0FMS86M4H","minecraft-kid","A dungeon build with zombies and traps. Lots of play after the build.","Ages 8 and up","9K+",""),
 ("lego-skeleton","LEGO Minecraft The Skeleton 21594","B0G2SYW4FW","minecraft-kid","A big buildable skeleton for older fans who like to display what they build.","Ages 9 and up","5K+",""),
 ("minecraft-watch","Minecraft Kids Smart Watch","B08YFKKRY3","minecraft-kid","Camera, games and Minecraft clock faces. No internet.","Ages 5 to 10","2K+",""),
 # Christmas
 ("lego-advent-city","LEGO City Advent Calendar 2026","B0G5QJP2BW","christmas","24 little city builds, from vehicles to mini figures.","Ages 5 and up","10K+","advent"),
 ("lego-advent-friends","LEGO Friends Advent Calendar 2026","B0G5QNVMLT","christmas","Tiny Friends scenes for each December morning.","Ages 6 and up","7K+","advent"),
 ("hot-wheels-advent","Hot Wheels Advent Calendar 2026","B0G1TZTY5K","christmas","A car a day, plus a play mat to race them on.","Ages 3 and up","9K+","advent"),
 ("golden-books-advent","Little Golden Books Advent Calendar","B0GJ9V42V9","christmas","24 small wrapped books. A bedtime story for every night of December.","Ages 2 to 6","","advent"),
 ("squishy-30","Kawaii Squishy Toys, 30 Pack","B0DG2VRFV7","christmas","Thirty little squishies. Enough for every stocking in the house and the cousins.","Stockings","70K+","stocking"),
 # Diwali
 ("marigold-garland","Artificial Marigold Garland, 5 Pack","B0851F7XR1","diwali","Five long marigold garlands for doors, railings and the puja corner. Reusable every year.","Doors and railings","3K+","door"),
 ("led-tealights","PUNPUBA LED Tea Lights, 24 Pack","B0DQKZJJQY","diwali","Flameless diyas for the balcony and anywhere little hands can reach.","Kid-safe glow","6K+","light"),
 ("marigold-heads","Artificial Marigold Flower Heads","B07XF9QQGN","diwali","Loose marigold heads for rangoli, urli bowls and the table.","Rangoli, urli","","door"),
 # Diwali: gifts to take, and things kids make
 ("lotus-tealight","Tied Ribbons Lotus Tealight Holders, Set of 7","B0D63791TG","diwali","Seven lotus tealight holders. Pretty enough to gift, cheap enough to gift twice.","Hosts, teachers","700+","give"),
 ("diya-urli-pair","Tied Ribbons Diya Urli Bowls, Set of 2","B0BG8BP3YL","diwali","Two gold diya-shaped bowls for floating flowers and tealights. The host gift that stays out all year.","Hosts","700+","give"),
 ("soan-papdi","Haldiram's Soan Papdi (500g)","B012S2K6XI","diwali","The box everyone pretends to be tired of, and finishes anyway.","Visits, the office","100+","give"),
 ("rangoli-sand-art","Kulture Khazana Rangoli Sand Art Kit","B0CK2PNZC8","diwali","Rangoli on a board, so the glitter stays on the board. A kid-sized Diwali job.","Ages 5 and up","200+","kids"),
 ("rangoli-puzzle","Kulture Khazana Rangoli Floor Puzzle (48 pc, 32 in)","B08NLZXXHW","diwali","A giant round rangoli puzzle for the floor. Big pieces, so the little cousins can help too.","Ages 3 and up","100+","kids"),
 ("moon-lamp","HOLA Paint Your Own Moon Lamp","B0DFW9KNR8","diwali","They paint it, it glows. A festival of lights gift that ends up on the bedside table.","Ages 6 to 12","2K+","kids"),
 ("binnys-diwali","Binny's Diwali by Thrity Umrigar","1338364480","diwali","A girl tells her class about Diwali. Lovely for kids growing up far from home.","Ages 4 to 8","","kids"),
 ("golden-diwali","Diwali: A Festival of Lights (Little Golden Book)","0593703871","diwali","The story of Diwali in a book small enough for a return gift bag.","Ages 2 to 6","","kids"),
]
# existing products that are also top sellers right now (monthly buyers on Amazon US, 29 Oct 2026)
POPULAR_EXISTING = {"airbrush": "20K+", "flip-7": "20K+", "uno": "20K+", "taco-cat": "10K+", "spot-it": "20K+", "hues-cues": "",
 "crunchlabs": "10K+", "gear-bots": "10K+", "robotic-hand": "9K+", "owala-kids": "6K+", "time-marker": "5K+", "wikki-stix": "7K+",
 "kitchen-scale": "50K+", "shears": "20K+", "lego-daisies": "10K+", "lego-advent-marvel": "20K+", "lego-advent-starwars": "40K+",
 "lego-advent-princess": "10K+", "glow-sticks": "70K+", "play-doh-party": "50K+", "cupkin-stickers": "8K+", "lego-pig-house": "10K+",
 "lego-nether": "10K+", "lego-taiga": "6K+", "minecraft-walkies": "3K+"}
# gift sections, existing gift products
GIFT_SEC = {"lego-advent-marvel": "advent", "lego-advent-starwars": "advent", "lego-advent-princess": "advent", "lego-gingerbread": "tree", "lego-nether": "tree",
 "wimpy-kid-21": "tree", "dog-man-15": "tree", "needoh-cube": "stocking", "needoh-teenie": "stocking", "globbles": "stocking", "dumpling-squishy": "stocking",
 "butter-squeeze": "stocking", "uno": "stocking",
 "diya-string-lights": "light", "hanging-diyas": "light", "curtain-lights": "light", "akhand-diya": "corner", "clay-diyas": "corner", "urli": "door",
 "marigold-toran": "door", "satya-incense": "corner", "kaju-katli": "sweet", "besan-ladoo": "sweet", "kurta-pyjama": "sweet"}
SECTIONS = {
 "christmas": [("advent", "Advent calendars", "These sell out first. Most are gone by mid-November."), ("tree", "The big one, under the tree", "One proper gift that gets played with past Boxing Day."), ("stocking", "Stocking stuffers", "Small, cheap, actually used.")],
 "diwali": [("light", "Light it up", "All the glow, kid-safe."), ("door", "The door and the table", "So the whole building knows."), ("corner", "The puja corner", "Small, but proper."), ("sweet", "Mithai and something new to wear", "For guests. And the photos."), ("give", "Gifts to take when you visit", "Because turning up empty-handed is not an option."), ("kids", "For the kids: a Diwali they make", "Rangoli, lights and stories, so the festival is theirs too.")],
}
