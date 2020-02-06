# A18

* Replaced all electrolytic caps (must not be taller than ~32mm)
* Replaced all 'CC' resistors with metal ones
* Replaced (partially burnt) CR8, CR10, CR12, CR13 with SF63G
	* They have suitable specs and are very cheap, but are too large for their footprints
* Replaced VR211 which tested OK, but was located right next to very burnt CC resistor
* Replaced VR202 which had 20 Ohm DC resistance both ways
* Replaced Q203 which tested ok but turned out bad with KSP94BU, was preventing overcurrent protection from working
* Replaced dead Q207 with FQN1N50C
	* Different footprint but was the only TO-92 500V N-Ch MOSFET I found
* Worked through A18 troubleshooting in the service manual to test everything including overcurrent protection
* Successfully so :)