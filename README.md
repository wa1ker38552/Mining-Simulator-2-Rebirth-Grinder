# Mining-Simulator-2-Rebirth-Grinder
Grinds rebirths in Mining Simulator 2 using pyautogui + keyboard

Mostly a proof of concept since it's far too difficult to use for a regular user. The player has to have their camera angled at a specific view by zooming in, re-aligning and zooming out again to ensure that walking distances are not messed up. Additionally the walking distances are callibrated towards the summer event map (since that map has the shortest distance from rebirth to the mines). 

The button callibrations should NOT be messed with. They should work on every screen since they're callibrated by screen resolution using a ratio.

Bot Actions:
```
Repeat:
  Check rebirth requirements
  Check coins
  
  Repeat until coins equal rebirth requirements:
    Repeat until full backpack:
      Mine

    Sell blocks
    Check coins
  Rebirth
  ```
