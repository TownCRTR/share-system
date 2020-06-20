discord command tc_admin!stocksset <text> <number>:
  trigger:
    if {linkedTo::ign::%event-user's discord id%} == "_SpillTheTea":
      reply with ":moneybag: Edited share price for company '%arg-1%'."
      set {sharePrice::%arg-1%} to arg-2
function purchaseSlot(p: player, i: itemtype, t: text, a: number, s: integer, am: integer):
  set slot {_s} of {_p} to {_i} named {_t} with lore "&aPrice: $&2%{_a}%&a - Item Amount: &2%{_am}%"
on inventory click:
  if event.getView().getTitle() == "&dShop":
    cancel event
    if index of event-slot == 0:
        if player's sunske balance >= 60:
          if player's inventory has enough space for 1 cookie:
            removeBal(player, 60)
            give player 1 diamond axe
            add .25 to {sharePrice::Spawn Shop}
          else:
            message "&cNot enough space in your inventory to buy this item!"
    set {lastShopAtSpawn} to now
every 30 minutes:
  if difference between {lastShopAtSpawn} and now >= 28 hours:
    remove 3.5 from {sharePrice::Spawn Shop}
every 10 minutes:
  if difference between {lastShopAtSpawn} and now >= 10 hours:
    remove 0.05 from {sharePrice::Spawn Shop}

on rightclick:
  if name of target == "&dShop":
    if distance between player and target <= 5:
      message "&aWelcome to the Shop!"
      open chest inventory with size 1 named "&dShop" to player
      purchaseSlot(player, diamond axe, "&9Diamond Axe", 60, 0, 1)
      purchaseSlot(player, diamond pickxae, "&9Diamond Pickaxe", 60, 2, 1)
      purchaseSlot(player, golden axe, "&6Gold Axe", 30, 4)
      purchaseSlot(player, golden pickaxe, "&6Gold Pickaxe", 30, 6, 1)
      purchaseSlot(player, steak, "&eSnack ", 1, 16, 32)
      
on load:
  if {sharePrice::Orange Computer Co.} is not set:
    set {sharePrice::Orange Computer Co.} to 600
    set {sharePrice::Jen's Diner} to 90
    set {sharePrice::Jake and Melissa's Computers} to 250
    set {sharePrice::Spawn Shop} to 30
    log "[STONKS] Shares Loaded."
every 30 minutes:
  chance of 49.6%:
    remove .70 from {stockPrice::Orange Computer Co.}
  else:
    add .60 to {stockPrice::Orange Computer Co.}
every 30 minutes:
  chance of 34%:
    remove .76 from {stockPrice::Jen's Diner}
  else:
    add .43 to {stockPrice::Jen's Diner}
every 30 minutes:
  chance of 47%:
    remove .70 from {stockPrice::Jake and Melissa's Computers}
  else:
    add .60 to {stockPrice::Jake and Melissa's Computers}

every 1 hour:
  chance of 10%:
    broadcast "&cThe Stock Market is CRASHING! Let's hope it recovers..."
    remove 20 from {stockPrice::*}
    wait 30 minutes
    chance of 30%:
        broadcast "&aPhew! The stock market is recovering..."
        add 10 to {stockPrice::*}
command /banking:
  trigger:
    open chest inventory with size 3 to player named "&3Banking Menu"
    set slot 4 of player to paper named "Loan" with lore "Recieve $100, but %nl%pay back $170!"
    set slot 13 of player to redstone dust named "Buy a buisness' stocks" with lore "Purchase stocks of an NPC's buisness."
    set slot 22 of player to orange stained glass pane named "Bonds &c(REQUIRES A TOWN)" with lore "Recieve money from town members, but pay 10% back to each of them! (From your Government Bank. If it's empty, you'll lose all the money + a bit more!"
on inventory click:
  if event.getVew().getTitle() == "&3Banking Menu":
    cancel event
    if index of event-slot == 4:
      message "&aRecieved loan! In 20 minutes, you'll pay it back. DO NOT LOG OUT, or money will instantly be taken back!"
      addBal(player, 100)
      set {Waiting::%player's uuid%} to true
      wait 10 minutes
      message "&aNotice, you have to pay back your loan in 10 minutes!"
      wait 5 minutes
      message "&aNotice, you have to pay back your loan in 5 minutes!"
      wait 5 minutes
      set {Waiting::%player's uuid%} to false
      message "&cPaid back your loan!"
      removeBal(player, 170)
    if index of event-slot is 13:
       message "&aWhat do you want to invest in?"
       open chest inventory with size 1 named "Invest in an NPC's buisness."
       set slot 0 of player to stone axe named "&9Chuck's Lumber - %{sharePrice::Chuck's Lumber}%" with lore "Started recently, currently has an overall profit of $40.6k."
       set slot 2 of player to cooked pork named "&eJen's Diner - %{sharePrice::Jen's Diner}%" with lore "Started in 2007, currently has an overall profit of $67.2k."
       set slot 4 of player to black stained glass pane named "&8Jake & Melissa's Computers - %{sharePrice::Jake and Melissa's Computers}%" with lore "Started in 2015, currently has an overall profit of $89.4k"
       set slot 6 of player to white dye named "&aOrange Computer Co. - %{sharePrice::Orange Computer Co.}%" with lore "Started in 1998, currently has an overall profit of over $1t. - %nl%Stocks are very pricy!"
       set slot 8 of player to yellow dye named "&dShop - %{sharePrice::Spawn Shop}%" with lore "Started in 2019, currently has an overall profit of roughly $200.%nl%This is the shop located at spawn!
    if index of event-slot is 22:
      message "&cWork in Progress!"
expression %$offlineplayer% bought stock %$text%:
    get:
        if {boughtStock::%expression-2%::%expression-1's uuid%}% == true:
            return true
        else:
            return false
effect make %$offlineplayer% buy stock %$text%:
    trigger:
        set {investedIn::%expression-2%::%expression-1's uuid%}% to true
        removeBal(player, {sharePrice::%expression-2%})
effect make %$offlineplayer% sell stock %$text%:
    trigger:
        addBal(expression-1, {sharePrice::%expression-2%})
        set {investedIn::%expression-2%::%expression-1's uuid%} to false
function investIn(p: player, t: text):
    set {_u} to {_p}'s uuid
    set {_pn} to {_p}
    set {_p} to {_u}
    if {_pn} bought stock "%{_t}%":
        message "&cYou've already bought that share." to {_pn}
    else:
        make {_pn} buy stock {_t}
        message "&aBought share!" to {_pn}
    
command /sellshare <text>:
    usage: &9/sellshare (share you own)
    trigger:
        if player bought stock arg-1:
            make player sell stock arg-1
            message "&aSold share!"
on inventory click:
    if event.getView().getTitle() == "Invest in an NPC's buisness.":
        cancel event
        if index of event-slot == 0:
            investIn(player, "Chuck's Lumber")
        if index of event-slot == 2:
            investIn(player, "Jen's Diner")
        if index of event-slot == 4:
            investIn(player, "Jake and Mellisa's Computers")
        if index of event-slot == 6:
            investIn(player, "Orange Computer Co.")
        if index of event-slot == 8:
            investIn(player, "Spawn Shop")