import json
from decimal import Decimal
from .models import Category, Product, ProductImage

IMG_ROLEX = 'https://images.unsplash.com/photo-1523170335258-f5ed11844a49?auto=format&fit=crop&w=1000&q=85'
IMG_DRESS = 'https://images.unsplash.com/photo-1524592094714-0f0654e20314?auto=format&fit=crop&w=1000&q=85'
IMG_PLAT = 'https://images.unsplash.com/photo-1547996160-81dfa63595aa?auto=format&fit=crop&w=1000&q=85'
IMG_DIVER = 'https://images.unsplash.com/photo-1539874754764-5a96559165b0?auto=format&fit=crop&w=1000&q=85'
IMG_MIN = 'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?auto=format&fit=crop&w=1000&q=85'
IMG_TOURB = 'https://images.unsplash.com/photo-1614164185128-e4ec99c436d7?auto=format&fit=crop&w=1000&q=85'
IMG_CHRONO = 'https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?auto=format&fit=crop&w=1000&q=85'
IMG_GOLD = 'https://images.unsplash.com/photo-1587836374828-4dbafa94cf0e?auto=format&fit=crop&w=1000&q=85'
IMG_SPORT = 'https://images.unsplash.com/photo-1542496658-e33a6d0d50f6?auto=format&fit=crop&w=1000&q=85'

VID_MECH = ''
VID_CLOCK = ''
VID_WRIST = ''


def make_variants(c1_img, c2_img, c3_img, c4_img):
    return json.dumps([
        {'name': 'Midnight Teal', 'hex': '#102B2A', 'img': c1_img},
        {'name': 'Platinum', 'hex': '#B8C4C2', 'img': c2_img},
        {'name': 'Warm Ivory', 'hex': '#F3F0E8', 'img': c3_img},
        {'name': 'Deep Charcoal', 'hex': '#17201F', 'img': c4_img},
    ])


def seed_aether_catalog():
    if Product.objects.count() >= 25:
        return

    collections = [
        ('Everyday & Affordable Brands', 'Ultra-reliable digital, retro, field, and everyday watches from Casio, G-Shock, Timex, Titan, Fastrack, Fossil, and Swatch.', IMG_MIN, 1),
        ('Enthusiast & Mid-Range Brands', 'Respected mechanical, automatic, solar Eco-Drive, and Swiss entry icons from Seiko, Citizen, Orient, Tissot, Hamilton, Bulova, and Certina.', IMG_SPORT, 2),
        ('Luxury & High-End Brands', 'Prestigious Swiss and Japanese icons including Rolex, Omega, TAG Heuer, Longines, Breitling, Cartier, and Grand Seiko.', IMG_ROLEX, 3),
        ('Old Money Watches', 'Quiet-luxury rectangular dress pieces, Roman numeral dials, and heirloom leather straps built for understated generational elegance.', IMG_DRESS, 4),
        ('Iconic & Established Luxury', 'Independent and heritage pillars: Tudor, Oris, Nomos Glashütte, Baume & Mercier, Rado, IWC Schaffhausen, and Jaeger-LeCoultre.', IMG_GOLD, 5),
        ('Ultra-Luxury & Haute Horlogerie', 'The pinnacle of watchmaking: Patek Philippe, Audemars Piguet, Vacheron Constantin, A. Lange & Söhne, Breguet, Richard Mille, and Blancpain.', IMG_TOURB, 6),
    ]

    cats = {}
    for name, desc, img, order in collections:
        obj, _ = Category.objects.get_or_create(name=name, defaults={'description': desc, 'image_url': img, 'display_order': order})
        cats[name] = obj

    catalog = [
        # 1. Everyday & Affordable Brands
        ('Everyday & Affordable Brands', 'Everyday & Affordable', 'Casio', 'A168WA Vintage Digital & Retro Steel', 3495, 4295, 'Men', False, False, 'Quartz', 'Oyster / Integrated Steel', 'Electro-Luminescent Retro Digital Dial', 'Brushed Stainless Clasp Band', IMG_MIN, VID_CLOCK,
         'Famous for ultra-reliable digital, retro, and budget analog watches with iconic illuminator display and 7-year battery life.'),
        ('Everyday & Affordable Brands', 'Everyday & Affordable', 'G-Shock', 'GA-2100 CasiOak Carbon Core Guard', 9995, 11495, 'Men', False, False, 'Quartz', 'Resin / FKM Rubber', 'Octagonal Shock-Resistant Ana-Digi Dial', 'Bio-Based Matte Resin Strap', IMG_DIVER, VID_MECH,
         'Casio’s sub-brand known for rugged, shock-resistant sports and outdoor watches with 200M water resistance.'),
        ('Everyday & Affordable Brands', 'Everyday & Affordable', 'Timex', 'Expedition Scout & Weekender 40', 5495, 6495, 'Men', False, False, 'Quartz', 'Nato / Canvas', 'Indiglo Night-Light Arabic Field Dial', 'Slip-Thru Woven Nylon / Leather Strap', IMG_SPORT, VID_WRIST,
         'Popular for classic, accessible field and everyday watches like the Weekender and Expedition.'),
        ('Everyday & Affordable Brands', 'Everyday & Affordable', 'Titan', 'Edge Ceramic Ultra-Slim Dress', 12995, 15495, 'Women', True, False, 'Quartz', 'Milanese Mesh', 'Sunray Warm Ivory & Gold Minimal Dial', 'Slim Milanese Mesh Bracelet', IMG_DRESS, VID_CLOCK,
         'India’s largest watchmaker, offering a massive range of everyday, dress, and fashion timepieces.'),
        ('Everyday & Affordable Brands', 'Everyday & Affordable', 'Fastrack', 'Reflex Play & Stunners Street Chrono', 3795, 4595, 'Kids', False, False, 'Quartz', 'Resin / FKM Rubber', 'Bold Youth-Focused Multi-Function Dial', 'Flexible Dual-Tone Silicone Strap', IMG_MIN, VID_WRIST,
         'A youth-focused brand by Titan popular for trendy, casual, and sporty designs for teens and kids.'),
        ('Everyday & Affordable Brands', 'Everyday & Affordable', 'Fossil', 'Townsman Automatic Mechanical Skeleton', 16495, 19995, 'Men', False, False, 'Mechanical', 'Alligator Leather', 'Exposed Open-Heart Mechanical Gear & Roman Dial', 'Rich Saddle-Stitched Genuine Leather Strap', IMG_TOURB, '',
         'Iconic Fossil mechanical skeleton watch showcasing exposed balance wheel gears, Roman numerals, and hand-wound automatic craftsmanship.'),
        ('Everyday & Affordable Brands', 'Everyday & Affordable', 'Swatch', 'Bioceramic Moonswatch & Sistem51', 14500, 16500, 'Kids', False, False, 'Quartz', 'Resin / FKM Rubber', 'Playful Vibrant Swiss Quartz Dial', 'Velcro / Lightweight Bioceramic Strap', IMG_SPORT, VID_CLOCK,
         'Celebrated for colorful, lightweight, and playful Swiss-made quartz watches.'),

        # 2. Enthusiast & Mid-Range Brands
        ('Enthusiast & Mid-Range Brands', 'Enthusiast & Mid-Range', 'Seiko', 'Prospex Turtle & Presage Cocktail Time', 38500, 44000, 'Men', False, False, 'Automatic', 'Oyster / Integrated Steel', 'Hardlex Sunray Guilloché / LumiBrite Dial', 'Three-Fold Clasp Solid Steel Bracelet', IMG_DIVER, VID_MECH,
         'A powerhouse Japanese watchmaker respected for everything from affordable quartz to iconic automatic divers.'),
        ('Enthusiast & Mid-Range Brands', 'Enthusiast & Mid-Range', 'Citizen', 'Promaster Eco-Drive Titanium', 32000, 36500, 'Men', False, False, 'Quartz', 'Brushed Titanium', 'Light-Powered Eco-Drive Sapphire Dial', 'Super Titanium Fold-Over Bracelet', IMG_PLAT, VID_WRIST,
         'Renowned for its solar-powered Eco-Drive technology and durable everyday watches.'),
        ('Enthusiast & Mid-Range Brands', 'Enthusiast & Mid-Range', 'Orient', 'Bambino Version 7 & Kamasu Diver', 24500, 28900, 'Men', True, False, 'Automatic', 'Alligator Leather', 'Domed Crystal In-House Calibre F6724 Dial', 'Supple Calfskin Dress Strap', IMG_DRESS, VID_CLOCK,
         'A Japanese brand beloved for offering high-value, in-house mechanical and automatic watches.'),
        ('Enthusiast & Mid-Range Brands', 'Enthusiast & Mid-Range', 'Tissot', 'PRX Powermatic 80 & Le Locle', 64500, 72000, 'Men', True, False, 'Automatic', 'Oyster / Integrated Steel', 'Embossed Waffle Tapestry 80h Reserve Dial', 'Tapered Integrated 316L Steel Bracelet', IMG_ROLEX, VID_MECH,
         'An accessible Swiss brand famous for classic dress watches and integrated-bracelet sports models like the PRX.'),
        ('Enthusiast & Mid-Range Brands', 'Enthusiast & Mid-Range', 'Hamilton', 'Khaki Field Mechanical & Murph 38', 68000, 75000, 'Men', False, False, 'Mechanical', 'Nato / Canvas', 'Cinema-Featured Cathedral Hand Military Dial', 'Rugged H-10 Field Leather / Nato Strap', IMG_SPORT, VID_WRIST,
         'Known for its American heritage and Swiss craftsmanship, especially in field, pilot, and cinema-featured watches.'),
        ('Enthusiast & Mid-Range Brands', 'Enthusiast & Mid-Range', 'Bulova', 'Lunar Pilot High-Precision 262kHz', 49500, 56000, 'Men', False, False, 'Chronograph', 'Oyster / Integrated Steel', 'High-Frequency 262kHz Sweeping Chrono Dial', 'Brushed Surgical Steel Bracelet', IMG_CHRONO, VID_MECH,
         'Recognized for historic innovation, precision quartz movements, and classic dress styles.'),
        ('Enthusiast & Mid-Range Brands', 'Enthusiast & Mid-Range', 'Certina', 'DS Action Diver Powermatic 80', 74000, 82000, 'Women', False, False, 'Automatic', 'Oyster / Integrated Steel', 'Double Security ISO-Certified Ceramic Dial', 'Diver Extension Steel Bracelet', IMG_DIVER, VID_CLOCK,
         'A Swiss brand well-regarded for sturdy, water-resistant sports and dive watches.'),

        # 3. Luxury & High-End Brands + Old Money Watches + Iconic Luxury
        ('Luxury & High-End Brands', 'Luxury & High-End', 'Rolex', 'Submariner Date & Datejust 41 Fluted', 1185000, 1320000, 'Men', True, True, 'Automatic', 'Oyster / Integrated Steel', 'Cerachrom Bezel & Chromalight Sunburst Dial', '904L Oyster / Jubilee Bracelet with Glidelock', IMG_ROLEX, VID_MECH,
         'The most recognizable Swiss luxury watchmaker, famous for iconic sports and dress models like the Submariner, Daytona, and Datejust.'),
        ('Luxury & High-End Brands', 'Luxury & High-End', 'Omega', 'Speedmaster Moonwatch & Seamaster 300M', 645000, 710000, 'Men', False, True, 'Chronograph', 'Oyster / Integrated Steel', 'Hesalite / Sapphire Co-Axial Master Chronometer Dial', 'Brushed 5-Link Speedmaster Steel Bracelet', IMG_CHRONO, VID_MECH,
         'Renowned for the Speedmaster ("Moonwatch") and Seamaster collections, blending heritage with Master Chronometer precision.'),
        ('Old Money Watches', 'Old Money Heritage', 'Cartier', 'Tank Louis & Santos de Cartier Medium', 690000, 760000, 'Women', True, True, 'Mechanical', 'Alligator Leather', 'Silvered Guilloché Roman Numeral & Blued Steel Hands', 'QuickSwitch Alligator Leather & SmartLink Bracelet', IMG_DRESS, VID_CLOCK,
         'A prestigious French maison famed for iconic, shaped dress watches like the Tank, Santos, and Ballon Bleu—the emblem of Old Money elegance.'),
        ('Luxury & High-End Brands', 'Luxury & High-End', 'Grand Seiko', 'Snowflake SBGA211 & White Birch Spring Drive', 580000, 640000, 'Men', True, True, 'Spring Drive', 'Brushed Titanium', 'Zaratsu-Polished Textured Nature-Inspired Dial', 'High-Intensity Titanium 5-Piece Bracelet', IMG_PLAT, VID_MECH,
         'Revered for master-level, nature-inspired dial craftsmanship, Zaratsu polishing, and ultra-accurate Spring Drive movements.'),
        ('Luxury & High-End Brands', 'Luxury & High-End', 'Breitling', 'Navitimer B01 Chronograph 43', 790000, 865000, 'Men', False, True, 'Chronograph', 'Alligator Leather', 'Circular Aviation Slide Rule & Panda Sub-Dials', 'Stitched Alligator Folding-Clasp Strap', IMG_CHRONO, VID_WRIST,
         'Famous for bold aviation and chronograph watches like the Navitimer and Superocean.'),
        ('Iconic & Established Luxury', 'Iconic & Established Luxury', 'Longines', 'Master Collection Moonphase & HydroConquest', 245000, 275000, 'Women', True, True, 'Automatic', 'Alligator Leather', 'Barleycorn Guilloché & Blued Leaf Hands Dial', 'Brown Alligator Deployant Clasp Strap', IMG_DRESS, VID_CLOCK,
         'Celebrated for elegant, heritage-inspired Swiss dress, aviation, and dive watches like the Conquest and HydroConquest.'),
        ('Iconic & Established Luxury', 'Iconic & Established Luxury', 'Tudor', 'Black Bay 58 Heritage Chronometer', 365000, 405000, 'Men', False, True, 'Automatic', 'Oyster / Integrated Steel', 'Gilt Snowflake Hands & Domed Matte Black Dial', 'Riveted Heritage Steel Bracelet', IMG_DIVER, VID_MECH,
         'Rolex’s sister brand, widely praised for rugged, vintage-inspired tool and dive watches like the Black Bay.'),
        ('Luxury & High-End Brands', 'Luxury & High-End', 'TAG Heuer', 'Carrera Chronograph & Monaco Calibre 11', 540000, 610000, 'Men', False, True, 'Chronograph', 'Alligator Leather', 'Motorsport Tachymeter & Square Monaco Dial', 'Perforated Racing Calfskin Leather Strap', IMG_CHRONO, VID_WRIST,
         'Strongly tied to motorsports, known for sporty chronographs like the Carrera and Monaco.'),
        ('Iconic & Established Luxury', 'Iconic & Established Luxury', 'Oris', 'Aquis Date Calibre 400 & Big Crown', 295000, 330000, 'Men', False, True, 'Automatic', 'Oyster / Integrated Steel', 'Gradient Teal 5-Day Power Reserve Dial', 'Quick-Strap-Change Brushed Steel Bracelet', IMG_SPORT, VID_MECH,
         'An independent Swiss watchmaker beloved by enthusiasts for mechanical dive and aviation watches like the Aquis and Big Crown.'),
        ('Iconic & Established Luxury', 'Iconic & Established Luxury', 'Nomos Glashütte', 'Tangente Neomatik Bauhaus 39', 310000, 345000, 'Women', True, True, 'Automatic', 'Alligator Leather', 'Galvanized White Silver Bauhaus Typography Dial', 'Horween Genuine Shell Cordovan Strap', IMG_MIN, VID_CLOCK,
         'A German brand famous for minimalist, Bauhaus-inspired designs and in-house mechanical movements.'),
        ('Iconic & Established Luxury', 'Iconic & Established Luxury', 'Baume & Mercier', 'Clifton Baumatic 10550 & Riviera', 285000, 320000, 'Men', True, True, 'Automatic', 'Alligator Leather', 'Crosshair Gradient Lacquered Dress Dial', 'Interchangeable Alligator Dress Strap', IMG_DRESS, VID_CLOCK,
         'Known for classic, understated Swiss dress watches like the Clifton and Riviera.'),
        ('Iconic & Established Luxury', 'Iconic & Established Luxury', 'Rado', 'Captain Cook High-Tech Ceramic', 340000, 380000, 'Women', False, True, 'Automatic', 'Oyster / Integrated Steel', 'Smoke-Tinted Sapphire Skeleton Ceramic Dial', 'Plasma High-Tech Scratch-Proof Ceramic Links', IMG_PLAT, VID_MECH,
         'Recognized for pioneering high-tech, scratch-resistant ceramic watches with sleek, modern styling.'),
        ('Iconic & Established Luxury', 'Iconic & Established Luxury', 'IWC Schaffhausen', 'Portugieser Chronograph & Big Pilot 43', 780000, 850000, 'Men', True, True, 'Chronograph', 'Alligator Leather', 'Clean Engineering-Focused Arabic Numeral Dial', 'Santoni Hand-Crafted Alligator Strap', IMG_GOLD, VID_WRIST,
         'Known for clean, engineering-focused pilot watches (Big Pilot) and classic dress pieces (Portugieser).'),
        ('Old Money Watches', 'Iconic & Established Luxury', 'Jaeger-LeCoultre', 'Reverso Tribute Duoface & Master Ultra Thin', 960000, 1050000, 'Men', True, True, 'Mechanical', 'Alligator Leather', 'Art Deco Reversible Case & Sunray Guilloché Dial', 'Casa Fagliano Hand-Crafted Leather Strap', IMG_DRESS, VID_CLOCK,
         'Dubbed "the watchmaker’s watchmaker," famous for the reversible Reverso and intricate mechanical calibers.'),

        # 4. Ultra-Luxury & Haute Horlogerie (Premium Vault)
        ('Ultra-Luxury & Haute Horlogerie', 'Ultra-Luxury & Haute Horlogerie', 'Patek Philippe', 'Nautilus 5711/1A & Grand Complications', 9500000, 10500000, 'Men', True, True, 'Automatic', 'Oyster / Integrated Steel', 'Horizontal Embossed Blue-Teal Porthole Dial', 'Satin-Brushed Integrated Nautilus Bracelet', IMG_PLAT, VID_MECH,
         'Considered the pinnacle of traditional Swiss watchmaking, renowned for complex grand complications and the Nautilus.'),
        ('Ultra-Luxury & Haute Horlogerie', 'Ultra-Luxury & Haute Horlogerie', 'Audemars Piguet', 'Royal Oak "Jumbo" Extra-Thin 16202', 6800000, 7400000, 'Men', False, True, 'Automatic', 'Oyster / Integrated Steel', 'Petite Tapisserie Octagonal Bezel Exposed Screws', 'Hand-Finished Tapered Royal Oak Steel Bracelet', IMG_ROLEX, VID_MECH,
         'Famous for pioneering the luxury steel sports watch with the iconic octagonal Royal Oak.'),
        ('Ultra-Luxury & Haute Horlogerie', 'Ultra-Luxury & Haute Horlogerie', 'Vacheron Constantin', 'Overseas Perpetual Calendar Ultra-Thin', 8200000, 8900000, 'Men', True, True, 'Automatic', 'Alligator Leather', 'Maltese Cross Bezel & Translucent Lacquer Dial', 'Tool-Free Interchangeable Gold & Leather Straps', IMG_GOLD, VID_CLOCK,
         'The oldest continuously operating watchmaker in the world, celebrated for ultra-thin watches and the Overseas collection.'),
        ('Ultra-Luxury & Haute Horlogerie', 'Ultra-Luxury & Haute Horlogerie', 'A. Lange & Söhne', 'Lange 1 Moon Phase & Zeitwerk Platinum', 5400000, 5950000, 'Men', True, True, 'Mechanical', 'Alligator Leather', 'Asymmetric Solid Silver Outsize Date Dial', 'Hand-Stitched Alligator with Platinum Tang Buckle', IMG_TOURB, VID_MECH,
         'Germany’s premier luxury watchmaker, prized for unmatched movement finishing and the asymmetric Lange 1.'),
        ('Ultra-Luxury & Haute Horlogerie', 'Ultra-Luxury & Haute Horlogerie', 'Breguet', 'Classique Tourbillon Extra-Plat 5367', 11200000, 12000000, 'Women', True, True, 'Tourbillon', 'Alligator Leather', 'Engine-Turned Clous de Paris Guilloché & Breguet Hands', 'Rolled-Edge Alligator Leather Strap', IMG_TOURB, VID_CLOCK,
         'Historic brand founded by Abraham-Louis Breguet, known for inventing the tourbillon and classic guilloché dials.'),
        ('Ultra-Luxury & Haute Horlogerie', 'Ultra-Luxury & Haute Horlogerie', 'Richard Mille', 'RM 11-03 Automatic Flyback Carbon TPT', 18500000, 19800000, 'Men', False, True, 'Tourbillon', 'Resin / FKM Rubber', 'Skeletonized Grade-5 Titanium Tonneau Bridge', 'Vented Ergonomic FKM Sports Strap', IMG_DIVER, VID_MECH,
         'Famous for futuristic, ultra-lightweight, high-tech sports watches seen on top athletes.'),
        ('Ultra-Luxury & Haute Horlogerie', 'Ultra-Luxury & Haute Horlogerie', 'Blancpain', 'Fifty Fathoms Automatique & Villeret', 1480000, 1650000, 'Men', False, True, 'Automatic', 'Nato / Canvas', 'Domed Sapphire Unidirectional Dive Bezel Dial', 'Sail-Canvas & Titanium Pin-Buckle Strap', IMG_SPORT, VID_WRIST,
         'Renowned for the Fifty Fathoms—one of the world’s first modern dive watches—and classic complications.'),
    ]

    for idx, item in enumerate(catalog):
        (cat_name, tier, brand, name, price, orig, audience, is_old_money, is_prem,
         mov, strap, dial_note, strap_note, img_url, vid_url, desc) = item

        prod, created = Product.objects.get_or_create(
            name=name,
            brand=brand,
            defaults={
                'category': cats[cat_name],
                'brand_tier': tier,
                'audience': audience,
                'is_old_money': is_old_money,
                'is_premium_vault': is_prem,
                'price': Decimal(str(price)),
                'original_price': Decimal(str(orig)) if orig else None,
                'stock': 6 if not is_prem else 2,
                'dial_colour': 'Midnight Teal' if idx % 2 == 0 else 'Warm Ivory',
                'dial_detail_note': dial_note,
                'strap_material': strap,
                'strap_detail_note': strap_note,
                'primary_image_url': img_url,
                'video_url': '',
                'color_variants_json': make_variants(img_url, IMG_PLAT, IMG_DRESS, IMG_DIVER),
                'description': desc,
                'is_best_seller': idx in [0, 7, 14, 15, 16, 28],
                'is_new_arrival': idx in [1, 3, 10, 17, 29, 30],
                'is_trending': idx in [1, 8, 14, 19, 20, 32],
                'popularity_score': 100 - idx,
            }
        )
        if created:
            ProductImage.objects.create(product=prod, image_url=img_url, caption=f'{brand} — Primary Dial Architecture')
            ProductImage.objects.create(product=prod, image_url=IMG_TOURB, caption=f'{brand} — Exhibition Calibre & Movement')
            ProductImage.objects.create(product=prod, image_url=IMG_PLAT if img_url != IMG_PLAT else IMG_DRESS, caption=f'{brand} — {strap} & Clasp Detail')
