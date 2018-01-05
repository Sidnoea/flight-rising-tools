#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

;only run these hotkeys on flight rising (now if only the coliseum had unique window title text...)
SetTitleMatchMode, 2 ;substring mode
#IfWinActive Flight Rising

MsgBox Fighting manually? Don't forget to set the origin (ctrl+NumpadEnter).

origin = [0, 0] ;top-left corner of white area for coliseum

;positions of buttons
cont := [584, 539]
mon1 := [494, 209]
mon2 := [564, 299]
mon3 := [634, 389]
extramon1 := [424, 209]
extramon2 := [504, 329]
extramon3 := [574, 219]
extramon4 := [634, 349]
drag1 := [234, 209]
drag2 := [202, 291]
drag3 := [150, 382]
fight := [484, 539]
move1 := [574, 559] ;scratch
move2 := [474, 619] ;rally
move3 := [544, 619] ;eliminate
move4 := [604, 619] ;haste
move5 := [674, 619] ;sap
back := [454, 499]
cancel := [584, 609]
;returnPos := [272, 413]
monsterBattle := [150, 430]
next := [624, 562]
previous := [115, 193]
mainMenu := [432, 548]

;file names and positions of where to search for button images (x1, y1, x2, y2)
contImage := "FightOn.png"
contCoords := [504, 489, 674, 599]
cancelImage := "Cancel.png"
cancelCoords := [494, 569, 664, 659]
backImage := "Back.png"
backCoords := [424, 469, 474, 529]
abilitiesImage := "Abilities.png"
abilitiesCoords := [434, 489, 554, 649]
abilitiesDisabledImage := "AbilitiesDisabled.png"
abilitiesDisabledCoords := abilitiesCoords
monsterBattleImage := "MonsterBattle.png"
monsterBattleCoords := [51, 376, 244, 483]
nextImage := "Next.png"
nextCoords := [576, 538, 667, 583]
previousImage := "Previous.png"
previousCoords := [65, 169, 196, 213]
returnImage := "Return.png"
;returnCoords := [230, 397, 319, 422]
readyImage := "Ready.png"
ready1Coords := [346, 489, 443, 536]
ready2Coords := [346, 547, 443, 594]
ready3Coords := [346, 606, 443, 654]
mainMenuImage := "MainMenu.png"
mainMenuCoords := [367, 509, 499, 584]

;file names and positions of where to search for boss images (x1, y1, x2, y2)
rocImages := ["Roc1.png", "Roc2.png", "Roc3.png"]
rocCoords := [497, 123, 529, 142]
wartoadImages := ["Wartoad1.png", "Wartoad2.png"]
wartoadCoords := [474, 123, 529, 142]
rayImages := ["Ray1.png", "Ray2.png", "Ray3.png", "Ray4.png"]
rayCoords := [462, 123, 529, 142]
golemImages := ["Golem1.png", "Golem2.png", "Golem3.png", "Golem4.png"]
golemCoords := [455, 123, 529, 142]

;todo: the boss labels look like they're always in the same spot, maybe we can just use one coords

venue := 0 ;index of the venue to fight
venuePos := [0, 0] ;position of the venue in the selection menu

;positions of venue buttons
;x values: 120, 290, 450, 630
;y values: 200, 310, 440, 560
venues := []
venues[1]  := [120, 200] ;Training Fields
venues[2]  := [290, 200] ;Woodland Path
venues[3]  := [450, 200] ;Scorched Forest
venues[4]  := [630, 200] ;Sandswept Delta
venues[5]  := [120, 310] ;Blooming Grove
venues[6]  := [290, 310] ;Forgotten Cave
venues[7]  := [450, 310] ;Bamboo Falls
venues[8]  := [630, 310] ;Redrock Cove
venues[9]  := [120, 440] ;Waterway
venues[10] := [290, 440] ;Arena
venues[11] := [450, 440] ;Volcanic Vents
venues[12] := [630, 440] ;Rainsong Jungle
venues[13] := [120, 560] ;Boreal Wood
venues[14] := [290, 560] ;Crystal Pools
venues[15] := [450, 560] ;Harpy's Roost
venues[16] := [290, 200] ;Ghostlight Ruins
venues[17] := [450, 200] ;Mire
venues[18] := [630, 200] ;Kelp Beds
venues[19] := [120, 310] ;Golem Workshop

rallied := [false, false, false]
boss := false
bossLooks := 0

ColiClick(coords) {
	global origin
	x := origin[1] + coords[1]
	y := origin[2] + coords[2]
    MouseMove % origin[1], % origin[2] ;this ensures we don't get stuck on a button without "activating" it
    Sleep 1 ;this makes sure the mouse actually registers the move before doing the next one
	MouseMove %x%, %y%
	Sleep 100
	Click
}

SetOrigin() {
    global origin
    ImageSearch outx, outy, 0, 0, A_ScreenWidth, A_ScreenHeight, *150 TheColiseum.png
    if (ErrorLevel = 2) {
        MsgBox Something went wrong while searching for the coliseum.
        return false
    }
    else if (ErrorLevel = 1) {
        MsgBox Coliseum not found. (I need to see the title "The Coliseum" at the top)
        return false
    }
    else {
        origin := [outx-23, outy-50]
        return true
    }
}

^NumpadEnter:: ;set the origin
    if (SetOrigin()) {
        MsgBox % "Coliseum origin set to " origin[1] ", " origin[2] "."
    }
return

!NumpadEnter:: ;show the current mouse position relative to the origin
    MouseGetPos x, y
    MsgBox % "Mouse relative to origin: " x-origin[1] ", " y-origin[2]
return

NumpadAdd::
	ColiClick(back)
return

NumpadDiv:: ;Scratch next enemy
	ColiClick(fight)
	ColiClick(move1)
	ColiClick(mon1)
	ColiClick(mon2)
	ColiClick(mon3)
    ColiClick(extramon1)
	ColiClick(extramon2)
	ColiClick(extramon3)
	ColiClick(extramon4)
return

NumpadMult:: ;Eliminate next enemy
	ColiClick(fight)
	ColiClick(move3)
	ColiClick(mon1)
	ColiClick(mon2)
	ColiClick(mon3)
    ColiClick(extramon1)
	ColiClick(extramon2)
	ColiClick(extramon3)
	ColiClick(extramon4)
return

NumpadSub::
	ColiClick(cont)
return

Up:: ;Rally first dragon
	ColiClick(fight)
	ColiClick(move2)
	ColiClick(drag1)
return

^Up:: ;Haste first dragon
	ColiClick(fight)
	ColiClick(move4)
	ColiClick(drag1)
return

Right:: ;Rally second dragon
	ColiClick(fight)
	ColiClick(move2)
	ColiClick(drag2)
return

^Right:: ;Haste second dragon
	ColiClick(fight)
	ColiClick(move4)
	ColiClick(drag2)
return

Down:: ;Rally third dragon
	ColiClick(fight)
	ColiClick(move2)
	ColiClick(drag3)
return

^Down:: ;Haste third dragon
	ColiClick(fight)
	ColiClick(move4)
	ColiClick(drag3)
return

NumpadDot::
	ColiClick(cancel)
return

Numpad0::
	ColiClick(fight)
return

Numpad1::
	ColiClick(move1)
return

Numpad2::
	ColiClick(move2)
return

Numpad3::
	ColiClick(move3)
return

Numpad4::
	ColiClick(move4)
return

Numpad5::
	ColiClick(move5)
return

Numpad6:: ;Click next enemy
	ColiClick(mon1)
	ColiClick(mon2)
	ColiClick(mon3)
    ColiClick(extramon1)
	ColiClick(extramon2)
	ColiClick(extramon3)
	ColiClick(extramon4)
return

Numpad7::
	ColiClick(mon1)
return

Numpad8::
	ColiClick(mon2)
return

Numpad9::
	ColiClick(mon3)
return

Search(image, coords:=false, tolerance:=0) { ;look for an image at the given origin-relative coordinates
	global origin
    if (coords = false) { ;no coords given? search the whole screen
        x1 := 0
        y1 := 0
        x2 := A_ScreenWidth
        y2 := A_ScreenHeight
    }
    else {
        x1 := origin[1] + coords[1]
        y1 := origin[2] + coords[2]
        x2 := origin[1] + coords[3]
        y2 := origin[2] + coords[4]
    }
    ;start := A_TickCount
	ImageSearch outx, outy, x1, y1, x2, y2, *%tolerance% %image%
    ;MsgBox % "Time elapsed for image search: " A_TickCount - start
    if (ErrorLevel = 2) {
        MsgBox Something went wrong while searching for this button: %image%
        return false
    }
    else if (ErrorLevel = 1) {
        return false
    }
    else {
        return [outx, outy]
    }
}

SearchBoss() {
    global ;assume-global mode
    local images
    local coords
    if (venue = 15) { ;Harpy's Roost
        images := rocImages
        coords := rocCoords
    }
    else if (venue = 17) { ;Mire
        images := wartoadImages
        coords := wartoadCoords
    }
    else if (venue = 18) { ;Kelp Beds
        images := rayImages
        coords := rayCoords
    }
    else if (venue = 19) { ;Golem Workshop
        images := golemImages
        coords := golemCoords
    }
    else { ;this venue is not configured for boss grinding
        return false
    }    
    for i, image in images {
        if (Search(image, coords, 150)) {
            return true
        }
    }
    return false
}

ChooseVenue() {
    global venue
    global venues
    global venuePos
    
    Gui, New, , Choose a Venue
    Gui, Add, Text, , Choose a Venue:
    Gui, Add, Radio, Checked vvenue, Training Fields
    Gui, Add, Radio, , Woodland Path
    Gui, Add, Radio, , Scorched Forest
    Gui, Add, Radio, , Sandswept Delta
    Gui, Add, Radio, , Blooming Grove
    Gui, Add, Radio, , Forgotten Cave
    Gui, Add, Radio, , Bamboo Falls
    Gui, Add, Radio, , Redrock Cove
    Gui, Add, Radio, , Waterway
    Gui, Add, Radio, , Arena
    Gui, Add, Radio, , Volcanic Vents
    Gui, Add, Radio, , Rainsong Jungle
    Gui, Add, Radio, , Boreal Wood
    Gui, Add, Radio, , Crystal Pools
    Gui, Add, Radio, , Harpy's Roost
    Gui, Add, Radio, , Ghostlight Ruins
    Gui, Add, Radio, , Mire
    Gui, Add, Radio, , Kelp Beds
    Gui, Add, Radio, , Golem Workshop
    Gui, Add, Button, Default gSubmit, Submit
    Gui, Show
    WinWaitClose, Choose a Venue
    
    venuePos := venues[venue]
}

Submit: ;label for gui submit buttons
    Gui, Submit
return

^NumpadSub:: ;Choose venue
    ChooseVenue()
return

^NumpadDiv:: ;Start auto-fighting
    failures := 0
    
    if (venue = 0) {
        ChooseVenue()
    }
    
    if (not SetOrigin()) {
        return
    }
	
	while !GetKeyState("Del") {
        found := false
        
        ;Is it rollover? Do nothing.
        now := A_Hour A_Min
        if ("0259" <= now and now <= "0331") {
            continue
        }
        
        ;Did we disconnect? Click the return button, refresh, reset failures.
        returnPos := Search(returnImage) ;the return button is not anchored to the coliseum origin
        if (returnPos) {
            MouseMove % returnPos[1], % returnPos[2]
            Click
            Sleep 500
            Send {F5}
            Sleep 2000
            failures := 0
            continue
        }
        
        ;Too many failures? Refresh, reset failures.
        if (failures >= 25) {
			Send {F5}
            Sleep 2000
            failures := 0
            continue
		}
        
        ;Are we on the title screen? Go to the venue select screen, reset failures.
        if (Search(monsterBattleImage, monsterBattleCoords)) {
            found := true
            ColiClick(monsterBattle)
            failures := 0
        }
        
        ;Are we at the venue select screen? Go to the venue/next page.
        if (Search(nextImage, nextCoords)) {
            found := true
            if (venue > 15) {
                ColiClick(next)
            }
            else {
                ColiClick(venuePos)
            }
        }
        
        ;Are we on page 2 of venues? Go to the venue/previous page.
        if (Search(previousImage, previousCoords)) {
            found := true
            if (venue > 15) {
                ColiClick(venuePos)
            }
            else {
                ColiClick(previous)
            }
        }
        
        ;Did an attack misclick? Click cancel.
		if (Search(cancelImage, cancelCoords)) {
            found := true
			ColiClick(cancel)
			ColiClick(back)
		}
		
        ;Are we at the abilities menu? Go back. Failures +1.
        if (Search(backImage, backCoords)) {
            found := true
			ColiClick(back)
			failures++
		}
		
        ;Are we ready to attack? Use eliminate or scratch.
		if (Search(abilitiesImage, abilitiesCoords)) {
            found := true
			ColiClick(fight)
			Sleep 100
			ColiClick(move3)
			ColiClick(move1)
			ColiClick(mon1)
			ColiClick(mon2)
			ColiClick(mon3)
			ColiClick(extramon1)
			ColiClick(extramon2)
			ColiClick(extramon3)
			ColiClick(extramon4)
		}
		
        ;Did we win/lose a battle? Continue to the next one. Reset failures.
		if (Search(contImage, contCoords)) {
            found := true
			ColiClick(cont)
            failures := 0
			Sleep 500
		}
        
        ;Are we waiting for an attack to finish? Wait it out.
        if (Search(abilitiesDisabledImage, abilitiesDisabledCoords)) {
            found := true
			continue
		}
        
        ;Didn't find anything we were looking for, wait a sec. Failures +1.
        if (not found) {
            failures++
            Sleep 300
        }
	}
    MsgBox Exited.
return

!NumpadDiv:: ;Start boss grinding
    failures := 0
    
    if (venue = 0) {
        ChooseVenue()
    }
    
    if (not SetOrigin()) {
        return
    }
    
    while !GetKeyState("Del") {
        found := false
        
        ;Is it rollover? Do nothing.
        now := A_Hour A_Min
        if ("0259" <= now and now <= "0331") {
            continue
        }
        
        ;Did we disconnect? Click the return button, refresh, reset failures.
        returnPos := Search(returnImage) ;the return button is not anchored to the coliseum origin
        if (returnPos) {
            MouseMove % returnPos[1], % returnPos[2]
            Click
            Sleep 500
            Send {F5}
            Sleep 2000
            failures := 0
            continue
        }
        
        ;Too many failures, or we're not at a boss? Refresh, reset failures.
        if (failures >= 25 or bossLooks >= 10) {
			Send {F5}
            Sleep 2000
            failures := 0
            bossLooks := 0
            continue
		}
        
        ;Are we on the title screen? Go to the venue select screen, reset variables.
        if (Search(monsterBattleImage, monsterBattleCoords)) {
            found := true
            ColiClick(monsterBattle)
            failures := 0
            rallied := [false, false, false]
            boss := false
            bossLooks := 0
        }
        
        ;Are we at the venue select screen? Go to the venue/next page.
        if (Search(nextImage, nextCoords)) {
            found := true
            if (venue > 15) {
                ColiClick(next)
            }
            else {
                ColiClick(venuePos)
            }
        }
        
        ;Are we on page 2 of venues? Go to the venue/previous page.
        if (Search(previousImage, previousCoords)) {
            found := true
            if (venue > 15) {
                ColiClick(venuePos)
            }
            else {
                ColiClick(previous)
            }
        }
        
        ;Did an attack misclick? Click cancel.
		if (Search(cancelImage, cancelCoords)) {
            found := true
			ColiClick(cancel)
			ColiClick(back)
		}
		
        ;Are we at the abilities menu? Go back. Failures +1.
        if (Search(backImage, backCoords)) {
            found := true
			ColiClick(back)
			failures++
		}
		
        ;Are we ready to attack? Check for the boss.
		if (Search(abilitiesImage, abilitiesCoords)) {
            if (boss or SearchBoss()) { ;we found the boss, follow the battle plan
                boss := true
                ;figure out whose turn it is
                if (Search(readyImage, ready1Coords)) {
                    dragon := 1
                }
                else if (Search(readyImage, ready2Coords)) {
                    dragon := 2
                }
                else if (Search(readyImage, ready3Coords)) {
                    dragon := 3
                }
                else { ;sometimes the enemy can interfere with this area of the gui
                    continue
                }
                ColiClick(fight)
                Sleep 100
                if (not rallied[dragon]) { ;if this dragon hasn't rallied, use rally
                    ColiClick(move2)
                    if (dragon = 1) {
                        ColiClick(drag1)
                    }
                    else if (dragon = 2) {
                        ColiClick(drag2)
                    }
                    else if (dragon = 3) {
                        ColiClick(drag3)
                    }
                    rallied[dragon] := true
                }
                else { ;otherwise, use eliminate or scratch
                    ColiClick(move3)
                    ColiClick(move1)
                    ColiClick(mon2)
                }
                Sleep 500
            }
            else { ;doesn't look like the boss (at the moment)
                bossLooks++
            }
            continue
		}
		
        ;Did we win/lose a battle? Go to the main menu.
		if (Search(contImage, contCoords)) {
			ColiClick(mainMenu)
            continue
		}
        
        ;Are we waiting for an attack to finish? Wait it out.
        if (Search(abilitiesDisabledImage, abilitiesDisabledCoords)) {
            continue
		}
        
        ;Didn't find anything we were looking for, wait a sec. Failures +1.
        if (not found) {
            failures++
            Sleep 300
        }
	}
    MsgBox Exited.
return

