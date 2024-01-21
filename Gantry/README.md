# Arduino code Agrobot Gantry (2023-2024)

Arduino code Agrobot Gantry

Gantry.ino is de hoofdprogramma
Eerst zal het programma de benodigde setup doen zoals testen van servo en calibreren van de gantry. Ook komt de setup voor ROSserial te pas. 
In de setup is ook een timer2 aangemaakt die op elke 1ms werkt, maar hier wordt geen gebruik van gemaakt. Tot nun toe checkt het alleen of de motoren worden aangestuurd vanuit de code - dus niet dat ze daadwerkelijk bewegen, want we hebben geen feedback, de motoren zijn niet closed loop. Maar hier kan wel later gebruik gemaakt worden van het bekijken op welke zogenaamde locatie de motor is en als die buiten zijn workspace betreedt dat een interrupt inschakelt die dit kan afhandelen.
Het gehele programma werkt in state en de bijbehoorende functies & variablen zijn zoveel als mogelijk in hun eigen headers gestopt. Door de naderende deadline kan het wel zijn dat sommige dingen op rare plekken staan en/of dat ze aparte namen hebben gekregen.

bevat een aantal header files:
- pinDefine
    * hierin staan alle pinnen die verbonden zijn met Arduino (4)
- servo_gantry
    * bevat setup servo
    * bevat het open en sluiten van de gripper : werken op states
- steppergantry
    * motor gerelateerd besturingen
- sorting_gantry
    * checkt hoe vol de bakken zijn - heeft ook geen feedback en wordt blind opgeteld.
    * roept YOLOV8 aan voor het identificeren van een gewas.
    * geeft aan in welke bak het gewas moet.
- rosserial
    * setup voor benodigde communicatie
    * bevat ook een aantal functies voor de callbacks om ze verder te verwerken.
