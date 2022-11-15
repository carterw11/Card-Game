from tkinter import *
from PIL import ImageTk,Image #Pillow is to help with uploading pictures
import random
import math
import re

symbolCheck = re.compile('[@_!#$%^&*()<>?/\|}{~:]') #I use this to check for symbols in a string. I later have a function that will search this and check if a string has any of these characters in it

class Deck(): #deck class which manages both the deck and hand
  def __init__(self):
    self.deck = []
    self.hand = []
    self.discard = [] #discard list to track which cards were used

  def drawHand(self): #draws a hand of 5 cards. Will stop if there are no more left
    for i in range(5):
      if self.deck == []:
        eventList.insert(0,"Your deck is empty! You cannot draw any more cards.")
        #The eventList is a list I created on the global scope. I insert text into it which determines what text is shown when playing the game in the main window
        break
      else:
        self.hand.append(self.deck.pop(0))
  
  def drawCard(self): #draws 1 card. will stop if there are no more left
    if self.deck == []:
      eventList.insert(0,"Your deck is empty! You cannot draw any more cards.")
    else:
      self.hand.append(self.deck.pop(0))
  
  def shuffleDeck(self): #shuffles the deck
    random.shuffle(self.deck)
  
  def reshuffleDeck(self): #reshuffle deck takes all the cards from the hand and discard and shuffles them back into the deck
    if self.hand == []: #will pass if either list is empty to avoid errors
      pass
    else:
      for i in range(len(self.hand)):
        self.deck.append(self.hand.pop(0))
    if self.discard == []: 
      pass
    else:
      for i in range(len(self.discard)):
        self.deck.append(self.discard.pop(0))
    random.shuffle(self.deck)
  
  def addToDeck(self,card): #adds card to the deck
    self.deck.append(card)
  
  def addToHand(self,card): #adds card to the hand
    self.hand.append(card)
  
  def getDeckSize(self): #gets deck size
    return len(self.deck)
  
  def getHandSize(self): #gets hand size
    return len(self.hand)
  
  def discardCard(self,pos): #discards a card
    self.discard.append(self.hand.pop(pos))
  
  def useCard(self,pos,player,enemies): #uses a card ### I did not en up using this function ###
    self.hand[pos].use(player,enemies) #calls the card's use function
    self.discard.append(self.hand.pop(pos))

class Card(): #card class
  def __init__(self,name,cost,dmg,dmgChance,heal,healChance,effect,effectChance,element,targeting):
    self.name = name
    self.cost = cost
    self.dmg = dmg
    self.dmgChance = dmgChance
    self.heal = heal
    self.healChance = healChance
    self.effect = effect
    self.effectChance = effectChance
    self.element = element
    self.targeting = targeting
  
### Originally I was going to use the card class to inherit to other classes, But I decided to make the cards fully customizable, so you can create any card you want using this class. ###

  def chooseTarget(self,enemies,targets,targetType): #Function that chooses the target for the card based on the "targeting" variable of the card. Returns a list of the enemies that the card will be used on
    targetList = []
    if targets == 3: #Since the game is only meant to have up to 3 enemies at once, so if there are 3 targets, it will simply return all enemies
      return enemies
    if targetType == "c": #c means choose
      if targets >= len(enemies):
        return enemies
      else:
        return enemies
    elif targetType == "r": #r means random
      target = enemies[random.randint(0,len(enemies)-1)]
      targetList.append(target)
      if targets > 1:
        while True:
          target2 = enemies[random.randint(0,len(enemies)-1)]
          if target2 != target:
            targetList.append(target2)
            break
    return targetList
  
  def use(self,player,enemies,window,pos,specificTargets = []): #use function which uses the chosen card
  #I added the specificTargets argument in case certain targets need to be passed. This happens when the player needs to click the enemy buttons to choose them as a target
    if self.cost > player.mana:#If the player does not have enough mana, the card will not be used
      eventList.insert(0,"You do not have enough mana to use that card")
    else:
      if specificTargets != []:
        targets = specificTargets
      elif self.targeting == "1c":
        targets = self.chooseTarget(enemies,1,"c") #calls chooseTarget function to determine target(s)
      elif self.targeting == "2c":
        targets = self.chooseTarget(enemies,2,"c")
      elif self.targeting == "1r":
        targets = self.chooseTarget(enemies,1,"r")
      elif self.targeting == "2r":
        targets = self.chooseTarget(enemies,2,"r")
      else:
        targets = self.chooseTarget(enemies,3,"c")
      player.setMana(-self.cost) #reduces player mana based on cost
      for i in range(len(targets)): #will make all target(s) take damage and status effects based on the chances
        if random.randint(1,100) <= self.dmgChance:
          targets[i].hp = targets[i].takeDmg(self.dmg,self.element)
          if random.randint(1,100) <= self.effectChance:
            targets[i].status = self.effect
            targets[i].statusTimer = 3 #the status timer is set to 3, which signifies the status lasting for 3 turns.
        else:
          if self.dmg == 0: #This will make it so if the card cannot do damage it can still apply the status effects
            if random.randint(1,100) <= self.effectChance:
              targets[i].status = self.effect
              targets[i].statusTimer = 3
      if random.randint(1,100) <= self.healChance: #heals player based on heal and chance
        player.hp = player.setHp(self.heal)
      player.deck.discardCard(pos) #the card will be discarded from the player's hand when the use function is finished
      player.mana = player.setMana(-self.cost) #the mana cost is taken off the player's mana
      self.useButton.grid_forget() ### This was an attempt to fix an issue I cannot find the solution to. When a card is used, if it is not the last card in your hand, when the cards move over, the text from the last card in the player's hand will stay on screen. I tried many different things to fix it but I could not find a solution. ###
    window.updateWindow(player,enemies) #calls an update for the main game window

class Enemy(): #enemy class which is inherited by all the different enemies
  def __init__(self,hp,atk,defense,weakness,xp,status):
    self.hp = hp
    self.maxHp = hp
    self.atk = atk
    self.defense = defense
    self.weakness = weakness
    self.xp = xp
    self.status = status
    self.statusTimer = 0

  def getHp(self): #getters
    return self.hp
  
  def getAtk(self):
    return self.atk
  
  def getDefense(self):
    return self.defense
  
  def setHp(self,change): #setters
    newHp = self.hp + change
    if newHp < 0:
      newHp = 0
    elif newHp > self.maxHp:
      newHp = self.maxHp
    return newHp
  
  def setAtk(self,change):
    newAtk = self.atk + change
    if newAtk < 0:
      newAtk = 0
    return newAtk
  
  def setDefense(self,change):
    newDefense = self.defense + change
    if newDefense < 0:
      newDefense = 0
    return newDefense
  
  def takeDmg(self,damage,element): #take dmg function, which runs a calculation based on damage and element of an incoming attack
    if element == self.weakness: #if the card element is the same as the enemy weakness, they take more damage
      if self.status == "mark": #there is a special case if the enemy takes damage with the mark status effect applied to them
        newHp = self.hp - int(damage * 1.5) + (self.defense - 2)
      else:
        newHp = self.hp - int(damage * 1.5) + self.defense
    else:
      if self.status == "mark":
        newHp = self.hp - damage + (self.defense-2)
      else:
        newHp = self.hp - damage + self.defense
    if newHp > self.hp:
        newHp = self.hp
    if newHp < 0:
      newHp = 0
    elif newHp > self.maxHp:
      newHp = self.maxHp
    return newHp

class Player(): #player class which is inherited by all the different player characters
  def __init__(self,hp,mana,level,xp):
    self.hp = hp
    self.maxHp = hp
    self.mana = mana
    self.maxMana = mana
    self.level = level
    self.xp = xp
    self.deck = Deck() #The player class uses composition to have a deck. The deck can be modified through the player.
    self.abilityUsed = False #the abilityUsed tracks if the player's ability was used
    self.levelUpRewards = 0 #levelUpRewards tracks how many cards the player can add to their deck. The rewards counter increases after leveling up and can be used after a battle

  def getHp(self): #getters
    return self.hp
  
  def getMana(self):
    return self.mana
  
  def getXp(self):
    return self.xp
  
  def setHp(self,change): #setters
    newHp = self.hp + change
    if newHp < 0:
      newHp = 0
      self.xp = self.setXp(-10)
    elif newHp > self.maxHp:
      newHp = self.maxHp
    return newHp  
  
  def setMana(self,change):
    newMana = self.mana + change
    if newMana < 0:
      newMana = 0
    elif newMana > self.maxMana:
      newMana = self.maxMana
    return newMana
  
  def setXp(self,change):
    newXp = self.xp + change
    if newXp < 0:
      newXp = 0
    elif newXp >= 10:#when reaching 10 xp, the player will level up giving them 2 max hp, a max mana at level 3 and 6, and one level up reward
      self.level += 1
      self.maxHp += 2 
      if self.level == 3 or self.level == 6:
        self.maxMana += 1
      eventList.insert(0,f"You leveled up! Your are now level {self.level}")
      newXp -= 10
      self.levelUpRewards += 1
    return newXp





class Wizard(Player): #wizard character who inherits from player class
  def __init__(self,hp,mana,level,xp):
    Player.__init__(self,hp,mana,level,xp)
    self.character = "wizard"
  
  def __str__(self):
    return f"WIZARD:    {self.hp}/{self.maxHp} HP    {self.mana}/{self.maxMana} MANA\nLVL {self.level}    {self.xp}/10 XP"
  
  def ability(self,enemies,window): #all characters have a different ability which can be used during a player turn
    if self.abilityUsed == False: #the ability can only be used if abilityUsed is false. Will set abilityUsed to true if it is successful
      eventList.insert(0,"You used 1 mana to do 3 fire damage to all enemies.")
      self.mana = self.setMana(-1)
      for i in enemies:
        i.hp = i.takeDmg(3,"fire")
      self.abilityUsed = True
    else:
      eventList.insert(0,"You have already used your ability this turn.")
    window.updateWindow(self,enemies)

class Warlock(Player): #warlock character who inherits from player class
  def __init__(self,hp,mana,level,xp):
    Player.__init__(self,hp,mana,level,xp)
    self.character = "warlock"

  def __str__(self):
    return f"WARLOCK:    {self.hp}/{self.maxHp} HP    {self.mana}/{self.maxMana} MANA\nLVL {self.level}    {self.xp}/10 XP"

  def ability(self,enemies,window):
    if self.abilityUsed == False:
      eventList.insert(0,"You took 2 damage to draw a card.")
      self.hp = self.setHp(-2)
      self.deck.drawCard() #the warlock character uses the composition to draw a card from the player deck.
      self.abilityUsed = True
    else:
      eventList.insert(0,"You have already used your ability this turn.")
    window.updateWindow(self,enemies)

class Oracle(Player): #oracle character who inherits from player class
  def __init__(self,hp,mana,level,xp):
    Player.__init__(self,hp,mana,level,xp)
    self.character = "oracle"
  
  def __str__(self):
    return f"ORACLE:    {self.hp}/{self.maxHp} HP    {self.mana}/{self.maxMana} MANA\nLVL {self.level}    {self.xp}/10 XP"
  
  def ability(self,enemies,window):
    if self.abilityUsed == False:
      eventList.insert(0,"You used 1 mana to heal 4 health.")
      self.mana = self.setMana(-1)
      self.hp = self.setHp(4)
      self.abilityUsed = True
    else:
      eventList.insert(0,"You have already used your ability this turn.")
    window.updateWindow(self,enemies)
    





class Goblin(Enemy): #goblin enemy who inherits from enemy class
  def __init__(self,hp,atk,defense,weakness,xp,status):
    Enemy.__init__(self,hp,atk,defense,weakness,xp,status)
    self.name = "goblin"

  def __str__(self):
    return f"GOBLIN: {self.hp}/{self.maxHp}\n{self.atk} ATK\n{self.defense} DEF\nWEAK: {self.weakness.upper()}"
  
  def act(self,target): #all enemies have an "act" function, which decides what they do on their turn. the act function is different for each enemy type
    if self.status == "freeze": #special case if the enemy is frozen. will have a 33% chance to not act at all
      if random.randint(1,3) == 1:
        eventList.insert(0,f"Goblin is frozen and cannot move!")
      else:
        if random.randint(1,2) == 1:
          damage = random.randint(self.atk -1, self.atk + 1)
          target.hp = target.setHp(-damage)
          eventList.insert(0,f"Goblin stabbed you for {damage} damage!")
        else:
          eventList.insert(0,"Goblin pokes the ground with it's knife.")
    else:
      if random.randint(1,2) == 1:
        damage = random.randint(self.atk -1, self.atk + 1)
        if self.status == "curse": #if the enemy is cursed, they will do less damage
          damage -= 1
        target.hp = target.setHp(-damage)
        eventList.insert(0,f"Goblin stabbed you for {damage} damage!")
        if self.status == "shock": #if the enemy is shocked, they will take damage when they attack
          self.hp = self.takeDmg(6,"none")
          eventList.insert(0,f"Goblin was shocked for 6 damage!")
      else:
        eventList.insert(0,"Goblin pokes the ground with it's knife.")

class Hobgoblin(Enemy): #hobgoblin enemy who inherits from enemy class
  def __init__(self,hp,atk,defense,weakness,xp,status):
    Enemy.__init__(self,hp,atk,defense,weakness,xp,status)
    self.name = "hobgoblin"
  
  def __str__(self):
    return f"HOBGOBLIN: {self.hp}/{self.maxHp}\n{self.atk} ATK\n{self.defense} DEF\nWEAK: {self.weakness.upper()}"
  
  def act(self,target):
    if self.status == "freeze":
      if random.randint(1,3) == 1:
        eventList.insert(0,f"Hobgoblin is frozen and cannot move!")
      else:
        if random.randint(1,4) == 1:
          self.hp = self.setHp(int(self.maxHp*0.3))
          eventList.insert(0,"Hobgoblin healed itself!")
        else:
          damage = random.randint(self.atk -2, self.atk + 1)
          target.hp = target.setHp(-damage)
          eventList.insert(0,f"Hobgoblin speared you for {damage} damage!")
    else:
      if random.randint(1,4) == 1:
        self.hp = self.setHp(int(self.maxHp*0.3))
        eventList.insert(0,"Hobgoblin healed itself!")
      else:
        damage = random.randint(self.atk -2, self.atk + 1)
        if self.status == "curse":
          damage -= 1
        target.hp = target.setHp(-damage)
        eventList.insert(0,f"Hobgoblin speared you for {damage} damage!")
        if self.status == "shock":
            self.hp = self.takeDmg(6,"none")
            eventList.insert(0,f"Hobgoblin was shocked for 6 damage!")

class Troll(Enemy): #troll enemy who inherits from enemy class
  def __init__(self,hp,atk,defense,weakness,xp,status):
    Enemy.__init__(self,hp,atk,defense,weakness,xp,status)
    self.name = "troll"
  
  def __str__(self):
    return f"TROLL: {self.hp}/{self.maxHp}\n{self.atk} ATK\n{self.defense} DEF\nWEAK: {self.weakness.upper()}"

  def act(self,target):
    if self.status == "freeze":
      if random.randint(1,3) == 1:
        eventList.insert(0,f"Troll is frozen and cannot move!")
      else:
        if random.randint(1,4) == 1:
          eventList.insert(0,"Troll is distracted by something shiny.")
        else:
          damage = random.randint(self.atk, self.atk + 3)
          target.hp = target.setHp(-damage)
          eventList.insert(0,f"Troll clubbed you for {damage} damage!")
    else:
      if random.randint(1,4) == 1:
        eventList.insert(0,"Troll is distracted by something shiny.")
      else:
        damage = random.randint(self.atk, self.atk + 3)
        if self.status == "curse":
            damage -= 1
        target.hp = target.setHp(-damage)
        eventList.insert(0,f"Troll clubbed you for {damage} damage!")
        if self.status == "shock":
            self.hp = self.takeDmg(6,"none")
            eventList.insert(0,f"Troll was shocked for 6 damage!")

class Ogre(Enemy): #ogre enemy who inherits from enemy class
  def __init__(self,hp,atk,defense,weakness,xp,status):
    Enemy.__init__(self,hp,atk,defense,weakness,xp,status)
    self.name = "ogre"

  def __str__(self):
    return f"OGRE: {self.hp}/{self.maxHp}\n{self.atk} ATK\n{self.defense} DEF\nWEAK: {self.weakness.upper()}"
  
  def act(self,target):
    if self.status == "freeze":
      if random.randint(1,3) == 1:
        eventList.insert(0,f"Ogre is frozen and cannot move!")
      else:
        if random.randint(1,2) == 1:
          self.atk = self.setAtk(1)
          eventList.insert(0,"Ogre raises it's attack by 1 point.")
        else:
          damage = random.randint(self.atk - 1, self.atk + 1)
          target.hp = target.setHp(-damage)
          eventList.insert(0,f"Ogre punches you for {damage} damage!")
    else:
      if random.randint(1,2) == 1:
        self.atk = self.setAtk(1)
        eventList.insert(0,"Ogre raises it's attack by 1 point.")
      else:
        damage = random.randint(self.atk - 1, self.atk + 1)
        if self.status == "curse":
            damage -= 1
        target.hp = target.setHp(-damage)
        eventList.insert(0,f"Ogre punches you for {damage} damage!")
        if self.status == "shock":
            self.hp = self.takeDmg(6,"none")
            eventList.insert(0,f"Ogre was shocked for 6 damage!")




class ChooseCharacter(): #ChooseCharacter window that will only appear if you do not have a character saved on your profile.
  def __init__(self): #you are promtped to choose a character, and are given information about each one
    self.root = Tk()
    self.root.title("Choose Your Character")
    self.title = Label(self.root,text = "Choose your character",pady=10)
    self.title.config(font=("Arial", 15))
    #this window will either call createWizard, createWarlock or createOracle depending on which character you choose. The functions are in the global scope, which at first I did because I did not want them to belong to a certain class, but I don't think it is necessary.
    self.wizardButton = Button(self.root,text="Wizard\n\nAn offensive charcter\nthat starts with\na deck of fire\nand lightning cards.\n\nAbility:\nspend 1 mana\nto deal 3 fire\ndamage to all enemies.\n\n",width=20,height=19,command=lambda:createWizard(self))
    self.warlockButton = Button(self.root,text="Warlock\n\nA unique charcter\nthat starts with\na deck of only dark\ncards.\n\nAbility:\nspend 2 health\nto draw a card\nand add it to\nyour hand.\n",width=20,height=19,command=lambda:createWarlock(self))
    self.oracleButton = Button(self.root,text="Oracle\n\nA defensive character\nthat starts with a\ndeck of ice and\nlight cards.\n\nAbility:\nspend 1 mana\nto heal 4 health\nto your character\n\n",width=20,height=19,command=lambda:createOracle(self))
    self.title.grid(row=0,column=0,columnspan=3)
    self.wizardButton.grid(row=1,column=0)
    self.warlockButton.grid(row=1,column=1)
    self.oracleButton.grid(row=1,column=2)
  
  def closeWindow(self,player): #this closes the window. it takes the player as an argument and passes it to the main game window. The player object gets passed many times in my program because the game needs to always keep track of it at all points.
    self.root.destroy()
    gameWindow = MainGame(player,generateEnemies(player))

class CardLibraryScreen(): #this screen displays all the cards in the game. it is accessed through the main game window
  def __init__(self):
    self.root = Toplevel()
    self.root.title("Card Library")
    self.mainFrame = Frame(self.root) #this is the first time I use frames and canvases. I do this when I want to add a scrollbar to the page
    self.mainFrame.pack(fill=BOTH,expand=1)
    self.canvas = Canvas(self.mainFrame,width=1030,height=400)
    self.canvas.pack(side=LEFT,fill=BOTH,expand=1)
    self.scrollbar = Scrollbar(self.mainFrame,orient=VERTICAL,command=self.canvas.yview)
    self.scrollbar.pack(side=RIGHT,fill=Y)
    self.canvas.configure(yscrollcommand=self.scrollbar.set)
    self.canvas.bind("<Configure>",lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))
    self.secondFrame = Frame(self.canvas)
    self.canvas.create_window((0,0),window=self.secondFrame,anchor="nw")
    #scrollbar code ends here
    self.title = Label(self.secondFrame,text = "Card Library",pady=10) #the widgets now need to be placed in the secondFrame or the canvas. mainFrame and root do not work
    self.title.grid(row=0,column=0,columnspan=5)
    count = 1
    for i in cardLibrary: #this long for loop goes through all the cards in the cardLibrary.
      tempPhoto = Image.open(f"Images/{i.element}Card.png") #sets a tempPhoto to the picture of the card that matches the card element
      tempPhoto = tempPhoto.resize((200, 300), Image.ANTIALIAS) #resizes the picture to be much smaller
      i.cardPhoto = ImageTk.PhotoImage(tempPhoto) #sets the card's photo to the tempPhoto
      i.imageLabel = Label(self.secondFrame,image=i.cardPhoto) #puts the label with the photo onto a label
      i.cardCostLabel = Label(i.imageLabel,text=f"{i.cost}",bg="#6fa8dc") #these labels contain the cards information. they use the card photo as their root so they are placed relative to the card photo
      i.cardNameLabel = Label(i.imageLabel,text=f"{i.name}\n\n{i.targeting}",bg="#ffffff")
      i.cardDamageLabel = Label(i.imageLabel,text=f"{i.dmg} ({i.dmgChance}%)",bg="#ffffff")
      i.cardHealLabel = Label(i.imageLabel,text=f"{i.heal} ({i.healChance}%)",bg="#ffffff")
      i.cardEffectLabel = Label(i.imageLabel,text=f"{i.effect} ({i.effectChance}%)",bg="#ffffff")
      i.imageLabel.grid(row=1+math.floor((count/5)-0.1),column=(count-1)%5) #the card photo is gridded onto the screen
      i.cardCostLabel.place(x=22,y=25) #all the info labels are placed into certain coordinated within the picture label
      i.cardNameLabel.place(x=50,y=55)
      i.cardDamageLabel.place(x=50,y=150)
      i.cardHealLabel.place(x=50,y=196)
      i.cardEffectLabel.place(x=50,y=244)
      count += 1
    self.continueButton = Button(self.secondFrame,text="Done",command=self.closeWindow,pady=10)
    self.continueButton.grid(row=10,column=2,pady=20)
    self.root.mainloop()
  
  def closeWindow(self):
    self.root.destroy()
  



class HowToPlay(): #this window tells the user how to play the game, and is accessed through the main game window
  def __init__(self):
    self.root = Toplevel()
    self.root.title("How to play")
    self.mainFrame = Frame(self.root)
    self.mainFrame.pack(fill=BOTH,expand=1)
    self.canvas = Canvas(self.mainFrame,width=830,height=400)
    self.canvas.pack(side=LEFT,fill=BOTH,expand=1)
    self.scrollbar = Scrollbar(self.mainFrame,orient=VERTICAL,command=self.canvas.yview) #another scrollbar
    self.scrollbar.pack(side=RIGHT,fill=Y)
    self.canvas.configure(yscrollcommand=self.scrollbar.set)
    self.canvas.bind("<Configure>",lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))
    self.secondFrame = Frame(self.canvas)
    self.canvas.create_window((0,0),window=self.secondFrame,anchor="nw")
    self.title = Label(self.secondFrame,text = "How to play",pady=10)
    self.textBlock1 = Label(self.secondFrame,text = "\n- Basics -\n\nIn this game, you fight enemies and collect cards.\nThe objective is to win as many battles as possible.\n\nThe game works on a turn based system.\nOn your turn, you will draw a card from your deck and then choose which cards in your hand to play.\nCards you play will be unusable for the rest of the battle, but will be usable again in the next batlle\n\nYour character has health, and when it is reduced to 0 you lose.\nYou fully restore your health after every battle and gain more when you level up.\n\nYour character also has mana, which is used to play cards, and is refreshed after every turn\n\nYour character also has xp and a level.\nxp is gained from killing enemies, and every 10 xp gives you 1 level.\nLevels make you and your enemies grow stronger, and every level you get to pick a new card to add to your deck.\n\nThe different characters also have different abilities which allow them to do unique things.\n",pady=10)
    self.textBlock2 = Label(self.secondFrame,text = "- Cards -",pady=10)
    self.title.grid(row=0,column=0)
    self.textBlock1.grid(row=1,column=0)
    self.textBlock2.grid(row=2,column=0)
    for i in cardLibrary: #this class also goes through the card library and puts the picture and info on screen, however it only does the first card. this is to show the player what a card looks like and how they work.
      tempPhoto = Image.open(f"Images/{i.element}Card.png")
      tempPhoto = tempPhoto.resize((200, 300), Image.ANTIALIAS)
      i.cardPhoto = ImageTk.PhotoImage(tempPhoto)
      i.imageLabel = Label(self.secondFrame,image=i.cardPhoto)
      i.cardCostLabel = Label(i.imageLabel,text=f"{i.cost}",bg="#6fa8dc")
      i.cardNameLabel = Label(i.imageLabel,text=f"{i.name}\n\n{i.targeting}",bg="#ffffff")
      i.cardDamageLabel = Label(i.imageLabel,text=f"{i.dmg} ({i.dmgChance}%)",bg="#ffffff")
      i.cardHealLabel = Label(i.imageLabel,text=f"{i.heal} ({i.healChance}%)",bg="#ffffff")
      i.cardEffectLabel = Label(i.imageLabel,text=f"{i.effect} ({i.effectChance}%)",bg="#ffffff")
      i.imageLabel.grid(row=3,column=0)
      i.cardCostLabel.place(x=22,y=25)
      i.cardNameLabel.place(x=50,y=55)
      i.cardDamageLabel.place(x=50,y=150)
      i.cardHealLabel.place(x=50,y=196)
      i.cardEffectLabel.place(x=50,y=244)
      break #breaks out of the loop right away. there could be a better way to do this but this is what I thought of and I kept it like this.
    self.textBlock3 = Label(self.secondFrame,text = "This is an example of a card that you can use.\n\nThe colour of the background is the card's element.\nRed = Fire\nYellow = Lightning\nBlue = Ice\nPurple = Dark\nWhite = Light\n\nThe number in the top left is the card's mana cost.\n\nThe text in the large box is the cards's name and targeting type.\nThe name is just for show and to differentiate between cards.\n\nThe targeting is how the card is used against enemies.\nThe number signifies the maximum amount of targets the card can hit.\nThe letter signifies how the card decides the targets.\nc means choice, allowing the player to choose which enemies are hit by the card.\nr means random, which will randomly select the affected targets.\n\nThe numbers next to the sword are the damage and damage chance of the card ( x (y%) )\nThe card will do x damage with a y% chance to hit.\n\nThe same goes for the healing, which is the number next to the green plus sign.\nHealing is independant of the damage, so your attack does not have to land to heal you.\n\nThe text next to the last symbol is the status effect the card has.\nEach element has a unique status effect that can be applied to enemies by certain cards.\nBurn (Fire) causes damage to enemies per turn\nShock (Lightning) causes high damage when the enemy performs an attack\nFreeze (Ice) adds a chance for an enemy to be unable to act\nCurse (Dark) lowers the enemy's attack damage\nMark (Light) Makes enemies take more damage\n\nStatus effects are dependant on damage.\nThis means that if the card is able to deal damage, the damage has to be done to be able to apply the elemental effect.\nIf the damage chance succeeds, the elemental chance will be rolled.\nStatus effects will last 3 turns and can be overwritten by other effects.\n",pady=10)
    self.textBlock3.grid(row=4,column=0)
    self.textBlock4 = Label(self.secondFrame,text = "- Enemies -\n\nTo progress the game you need to fight enemies.\n\nDuring the enemies' turn, they will act, which will have different effects based on the enemy type.\nAct can result in an attack, a heal, and many other outcomes.\nThere are 4 different enemy types, but it is up to you to discover what they do.\n\nEnemies have a health, attack, and defense stat, as well as an elemental weakness.\n\nIf the enemy's health is reduced to 0, they die and grant you xp.\n\nThe enemy's attack determines how strong their attacks will be on the player\n\nThe enemy's defense is how resistant to attacks the enemy is.\n1 defense will block 1 point of damage from every attack.\n\nThe enemy's elemental weakness of an enemy is random.\nIf you use cards the same element as the enemy's weakness, they will take 1.5x damage from the card.",pady=10)
    self.continueButton = Button(self.secondFrame,text="Done",command=self.closeWindow,pady=10)
    self.textBlock4.grid(row=5,column=0)
    self.continueButton.grid(row=6,column=0)
    self.root.mainloop()

  def closeWindow(self):
    self.root.destroy()




class MainGame(): #main game window. this class is very large and has a lot of functions.
  def __init__(self,player,enemies):
    self.root = Tk()
    self.root.title("Game Window")
    self.mainFrame = Frame(self.root)
    self.mainFrame.pack(fill=BOTH,expand=1)
    self.canvas = Canvas(self.mainFrame,width=900,height=700)
    self.canvas.pack(side=LEFT,fill=BOTH,expand=1)
    self.scrollbar = Scrollbar(self.mainFrame,orient=HORIZONTAL,command=self.canvas.xview,bg="blue") #scrollbar code
    self.scrollbar.pack(side=BOTTOM,fill=X)
    self.canvas.configure(xscrollcommand=self.scrollbar.set)
    self.canvas.bind("<Configure>",lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))
    self.secondFrame = Frame(self.canvas)
    self.canvas.create_window((0,400),window=self.secondFrame,anchor="nw")
    self.targetingMode = False #targeting mode is used when the player has to select targets by clicking on them
    self.eventBox = Label(self.canvas,text="") #eventbox will use the strings in eventList to display info to the player
    self.eventBoxWindow = self.canvas.create_window((5,5),anchor="nw",window=self.eventBox)
    # all the different buttons
    self.openRulesButton = Button(self.canvas,text="How to play",command=self.openRules,width=12)
    self.openRulesButtonWindow = self.canvas.create_window((900,0),anchor="ne",window=self.openRulesButton)
    self.openCardLibraryButton = Button(self.canvas,text="Card Library",command=self.openCardLibrary,width=12)
    self.openCardLibraryButtonWindow = self.canvas.create_window((900,30),anchor="ne",window=self.openCardLibraryButton)
    self.useAbilityButton = Button(self.canvas,text="Ability",command=lambda:player.ability(enemies,self),width=10,height=5)
    self.useAbilityButtonWindow = self.canvas.create_window((0,400),anchor="sw",window=self.useAbilityButton)
    self.endTurnButton = Button(self.canvas,text="End Turn",command=lambda:self.endTurn(player,enemies))
    self.endTurnButtonWindow = self.canvas.create_window((900,400),anchor="se",window=self.endTurnButton)
    self.playerInfo = Label(self.canvas,text=f"{player}") #the player info label shows the player's stats
    self.playerInfoWindow = self.canvas.create_window((450,0),anchor="n",window=self.playerInfo)
    player.deck.drawHand() #draws the hand for the player at the start of a battle
    for i in range(len(enemies)): #this is how the enemies are drawn. it works very similarly to how the cards are drawn. I create the enemies before the update loop but not the cards because I need to change the contents of the enemy's information boxes.
      tempPhoto = Image.open(f"Images/{enemies[i].name}.png")
      tempPhoto = tempPhoto.resize((100, 150), Image.ANTIALIAS)
      enemies[i].portraitPhoto = ImageTk.PhotoImage(tempPhoto)
      enemies[i].portraitButton = Button(self.canvas,image=enemies[i].portraitPhoto,state=DISABLED) #enemy portrait buttons are disabled unless the player needs to pick them as targets when a card is used
      enemies[i].enemyInfo = Label(self.canvas,text=f"{enemies[i]}")
      if len(enemies) == 1: #this makes the enemy in the center of the screen if there is only 1, instead of slightly to the left.
        enemies[i].portraitButtonWindow = self.canvas.create_window((275+175,250),anchor="center",window=enemies[i].portraitButton)
        enemies[i].enemyInfoWindow = self.canvas.create_window((275+175,165),anchor="s",window=enemies[i].enemyInfo)
      else:
        enemies[i].portraitButtonWindow = self.canvas.create_window((275+(i*175),250),anchor="center",window=enemies[i].portraitButton)
        enemies[i].enemyInfoWindow = self.canvas.create_window((275+(i*175),165),anchor="s",window=enemies[i].enemyInfo)
      enemies[i].enemyInfo.config(font=("Courier", 9))
    self.updateWindow(player,enemies) #calls the update window function
    self.root.mainloop()
  
  def endTurn(self,player,enemies): #endTurn function
    for i in enemies: #checks if any enemies are dead at both the start and end of the turn.
      if i.hp <= 0:
        player.xp = player.setXp(i.xp) #rewards the player with xp for dead enmies
        i.enemyInfo.config(text="")#removes the text from the enemy info boxes so there is no unnecessary text on screen
        i.portraitButton.destroy() #removes the enemy's portrait button
        enemies.remove(i) #removes them from the enemy list
    if enemies == [] or player.hp <= 0: #ends the game if all enemies or the player is dead. called at the start and end of endTurn function.
      self.endGame(player)
    for i in enemies:
      i.act(player)#all enemies perform their act function
      if i.status == "burn": #if enemies are burned they take damage every turn
        i.hp = i.takeDmg(i.maxHp//10,"none")
        eventList.insert(0,f"{i.name} was burned for {i.maxHp//10} damage")
      i.statusTimer -= 1 #reduces the status timer. if the timer hits 0 their status will be removed
      if i.statusTimer <= 0:
        i.status = "none"
    for i in enemies:
      if i.hp <= 0:
        player.xp = player.setXp(i.xp)
        i.enemyInfo.config(text="")
        i.portraitButton.destroy()
        enemies.remove(i)
    if enemies == [] or player.hp <= 0:
      self.endGame(player)
    player.mana = player.maxMana #resets certain stats for the player each turn
    player.abilityUsed = False
    player.deck.drawCard() #draws a card
    self.updateWindow(player,enemies)
  
  def updateEventBox(self): #this function updates the event box label
    self.eventBox.config(text = "")#removes text
    self.eventBoxWindow = self.canvas.create_window((5,5),anchor="nw",window=self.eventBox)
    if len(eventList) > 7: #if the eventlist is too large, it removes the last element in the list. this is actually the first element added to the list since I always insert at [0]
      for i in range(len(eventList)-7):
        eventList.pop()
    for i in eventList: #adds all the lines of text from the eventlist to the label
      text = self.eventBox.cget("text")
      self.eventBox.config(text=f"{i}\n{text}",font=("Courier", 6))
    self.eventBoxWindow = self.canvas.create_window((5,5),anchor="nw",window=self.eventBox)
  
  def openRules(self): #opens rules
    rulesWindow = HowToPlay()
    
  def openCardLibrary(self): #opens card library
    cardLibraryWindow = CardLibraryScreen()  

  def updateWindow(self,player,enemies): #updates the window. this mostly redraws all the widgets in the __init__
    self.playerInfo["text"] = f"{player}"
    self.playerInfoWindow = self.canvas.create_window((450,0),anchor="n",window=self.playerInfo)
    for i in enemies: #also checks for dead enemies and if all enemies or the player dies twice in the function.
      if i.hp <= 0:
        player.xp = player.setXp(i.xp)
        i.enemyInfo.config(text="")
        i.portraitButton.destroy()
        enemies.remove(i)
    if enemies == [] or player.hp <= 0:
      self.endGame(player)
    for i in range(player.deck.getHandSize()): #draws all the cards in the players hand. sgain similar to the card library, but makes them a button instead of label
      tempPhoto = Image.open(f"Images/{player.deck.hand[i].element}Card.png")
      tempPhoto = tempPhoto.resize((200, 300), Image.ANTIALIAS)
      player.deck.hand[i].cardPhoto = ImageTk.PhotoImage(tempPhoto)
      player.deck.hand[i].useButton = Button(self.secondFrame,image=player.deck.hand[i].cardPhoto,state=NORMAL,command=lambda i=i:self.startTargeting(player,enemies,player.deck.hand[i],i))#this is the first time I use lambda i=i. what this does is it basically saves i to what is was when it was passed to a function. Without it I encounter many program breaking bugs. I dont know entirely how it works but I know that it does.
      if self.targetingMode == True: #if the player is targeting enemies, the cards will be disabled as to not cause any errors using multiple cards at once
        player.deck.hand[i].useButton.config(state=DISABLED)
      else: 
        player.deck.hand[i].useButton.config(state=NORMAL)
      player.deck.hand[i].cardCostLabel = Label(player.deck.hand[i].useButton,text=f"{player.deck.hand[i].cost}",bg="#6fa8dc")
      player.deck.hand[i].cardNameLabel = Label(player.deck.hand[i].useButton,text=f"{player.deck.hand[i].name}\n\n{player.deck.hand[i].targeting}",bg="#ffffff")
      player.deck.hand[i].cardDamageLabel = Label(player.deck.hand[i].useButton,text=f"{player.deck.hand[i].dmg} ({player.deck.hand[i].dmgChance}%)",bg="#ffffff")
      player.deck.hand[i].cardHealLabel = Label(player.deck.hand[i].useButton,text=f"{player.deck.hand[i].heal} ({player.deck.hand[i].healChance}%)",bg="#ffffff")
      player.deck.hand[i].cardEffectLabel = Label(player.deck.hand[i].useButton,text=f"{player.deck.hand[i].effect} ({player.deck.hand[i].effectChance}%)",bg="#ffffff")
      player.deck.hand[i].useButton.grid_forget()
      player.deck.hand[i].useButton.grid(row=0,column=i)
      player.deck.hand[i].cardCostLabel.place(x=22,y=25)
      player.deck.hand[i].cardNameLabel.place(x=50,y=55)
      player.deck.hand[i].cardDamageLabel.place(x=50,y=150)
      player.deck.hand[i].cardHealLabel.place(x=50,y=196)
      player.deck.hand[i].cardEffectLabel.place(x=50,y=244)
    for j in range(len(enemies)): #redraws enemies
      tempPhoto = Image.open(f"Images/{enemies[j].name}.png")
      tempPhoto = tempPhoto.resize((100, 150), Image.ANTIALIAS)
      enemies[j].portraitPhoto = ImageTk.PhotoImage(tempPhoto)
      if enemies[j].status == "burn":
        enemies[j].bgColour="red"
      elif enemies[j].status == "shock":
        enemies[j].bgColour="yellow"
      elif enemies[j].status == "freeze":
        enemies[j].bgColour="blue"
      elif enemies[j].status == "mark":
        enemies[j].bgColour="lemon chiffon"
      elif enemies[j].status == "curse":
        enemies[j].bgColour="purple"
      else:
        enemies[j].bgColour="grey"
      enemies[j].portraitButton = Button(self.canvas,image=enemies[j].portraitPhoto,state=DISABLED,bg=enemies[j].bgColour,command=lambda j=j: [self.targetingList.append(enemies[j]),self.activateCard(player,enemies)])
      if self.targetingMode == True: #in the trageting mode, enemies are clickable to add them to the targetingList
        enemies[j].portraitButton.config(state=NORMAL)
      else: 
        enemies[j].portraitButton.config(state=DISABLED)
      enemies[j].enemyInfo["text"] = f"{enemies[j]}"
      if len(enemies) == 1:
        enemies[j].portraitButtonWindow = self.canvas.create_window((275+175,250),anchor="center",window=enemies[j].portraitButton)
        enemies[j].enemyInfoWindow = self.canvas.create_window((275+175,165),anchor="s",window=enemies[j].enemyInfo)
      else:
        enemies[j].portraitButtonWindow = self.canvas.create_window((275+(j*175),250),anchor="center",window=enemies[j].portraitButton)
        enemies[j].enemyInfoWindow = self.canvas.create_window((275+(j*175),165),anchor="s",window=enemies[j].enemyInfo)
      enemies[j].enemyInfo.config(font=("Courier", 9))
    self.updateEventBox()
    for i in enemies:
      if i.hp <= 0:
        player.xp = player.setXp(i.xp)
        i.enemyInfo.config(text="")
        i.portraitButton.destroy()
        enemies.remove(i)
    self.canvas.configure(scrollregion=self.canvas.bbox("all")) #updates the bounding box of the canvas. this makes it so if the length of the screen is updated, it will be visible to the user.
    if enemies == [] or player.hp <= 0:
      self.endGame(player)

  def startTargeting(self,player,enemies,card,pos): #begins the targeting mode for cards that need to select targets
    if int(card.targeting[0]) >= len(enemies) or card.targeting[1] == "r":
     card.use(player,enemies,self,pos) #if the targeting is random, or the number of targets is greater than or equal to the number of enemies, it will just be passed to the normal use function
    else: #if not, then the targeting mode is activated
      self.cardUsePosition = pos #gets the position in the hand of the card in use
      self.targets = int(card.targeting[0]) #gets the amount of targets needed to be selected
      self.targetingMode = True
      self.targetingList = [] #targeting list holds all the targets
      self.updateWindow(player,enemies)
  
  def activateCard(self,player,enemies): #this activates the card when the number of targets reaches the right amount using targetingMode
    for i in range(player.deck.getHandSize()):
      if self.targetingMode == True:
        if self.targets == len(self.targetingList) and self.cardUsePosition == i:
          self.targetingMode = False #targeting mode turns off if it is successful
    if self.targetingMode == False: #if it succeeds, it performs the use function of the card and passes the specificTargets argument to tell the card which enemies to use it on.
      player.deck.hand[self.cardUsePosition].use(player,enemies,self,self.cardUsePosition,self.targetingList)
  
  def endGame(self,player): #closes the main game and opens the end screen
    self.root.destroy()
    endGameScreen = EndScreen(player)





class EndScreen(): #end screen after the game is over
  def __init__(self,player):
    self.root = Tk()
    self.root.title("Post Game Window")
    self.titleText= Label(self.root,text="Battle Over",pady=10)
    self.titleText.config(font=("Arial", 18))
    self.exitButton = Button(self.root,text="Quit",width=7,command=quit)
    self.continueButton = Button(self.root,text="Continue",width=7,command=lambda:self.startGame(player))
    self.saveButton = Button(self.root,text="Save",width=7,command=lambda:write.saveProgress(player))#calls the saveProgress function contained in the write class
    self.levelUpButton = Button(self.root,text=f"{player.levelUpRewards} Level up rewards to claim",width=27,bg="green2",command=lambda:self.openLevelUpWindow(player)) #this button updates depending on how many level up rewards the player has
    self.titleText.grid(row=0,column=0,columnspan=3)
    self.exitButton.grid(row=1,column=0)
    self.saveButton.grid(row=1,column=1)
    self.continueButton.grid(row=1,column=2)
    self.levelUpButton.grid(row=2,column=0,columnspan=3)
    self.root.mainloop()
  
  def startGame(self,player): #function to start a new battle
    player.deck.reshuffleDeck() #resets player's stats for the next battle
    player.hp = player.maxHp
    player.mana = player.maxMana
    player.abilityUsed = False
    self.root.destroy()
    gameWindow = MainGame(player,generateEnemies(player))
  
  def openLevelUpWindow(self,player): #opens the level up window if the player has level up rewards
    if player.levelUpRewards == 0:
      pass
    else:
      player.levelUpRewards -= 1 #subtract 1 from the player's levelUpRewards
      levelUpWindow = LevelUpScreen(player)
      self.levelUpButton.config(text=f"{player.levelUpRewards} Level up rewards to claim")





class LevelUpScreen(): #level up screen. this allows the player to choose a card out of 3 random cards to add to their deck
  def __init__(self,player):
    self.root = Toplevel()
    self.root.title("Level up rewards")
    self.titleText= Label(self.root,text="Choose a card to add to your deck",pady=10)
    self.titleText.grid(row=0,column=0,columnspan=3)
    randomList = [] #all random numbers are appended to this list
    random1 = random.randint(0,len(cardLibrary)-1)
    random2 = random.randint(0,len(cardLibrary)-1)
    random3 = random.randint(0,len(cardLibrary)-1)
    while True: #this loop makes it so that there are no duplicate cards on the rewards screen
      if random1 != random2 and random1 != random3 and random2 != random3:
        randomList.append(random1)
        randomList.append(random2)
        randomList.append(random3)
        break
      else:
        random2 = random.randint(0,len(cardLibrary)-1)
        random3 = random.randint(0,len(cardLibrary)-1)
    libraryValueList = list(cardLibrary.values()) #list of all the values in the cardLibrary
    libraryKeyList = list(cardLibrary.keys()) #list of all the keys in the cardLibrary
    count = 0
    for i in randomList: #goes through the random list
      pos = libraryValueList.index(i) #this indexes the list of values and gets the position of the corresponding key
      tempPhoto = Image.open(f"Images/{libraryKeyList[pos].element}Card.png") #card images are opened similar to the library and main game
      tempPhoto = tempPhoto.resize((200, 300), Image.ANTIALIAS)
      libraryKeyList[pos].cardPhoto = ImageTk.PhotoImage(tempPhoto)
      libraryKeyList[pos].useButton = Button(self.root,image=libraryKeyList[pos].cardPhoto,state=NORMAL,command=lambda pos=pos:self.claimReward(player,libraryKeyList[pos]))
      libraryKeyList[pos].cardCostLabel = Label(libraryKeyList[pos].useButton,text=f"{libraryKeyList[pos].cost}",bg="#6fa8dc")
      libraryKeyList[pos].cardNameLabel = Label(libraryKeyList[pos].useButton,text=f"{libraryKeyList[pos].name}\n\n{libraryKeyList[pos].targeting}",bg="#ffffff")
      libraryKeyList[pos].cardDamageLabel = Label(libraryKeyList[pos].useButton,text=f"{libraryKeyList[pos].dmg} ({libraryKeyList[pos].dmgChance}%)",bg="#ffffff")
      libraryKeyList[pos].cardHealLabel = Label(libraryKeyList[pos].useButton,text=f"{libraryKeyList[pos].heal} ({libraryKeyList[pos].healChance}%)",bg="#ffffff")
      libraryKeyList[pos].cardEffectLabel = Label(libraryKeyList[pos].useButton,text=f"{libraryKeyList[pos].effect} ({libraryKeyList[pos].effectChance}%)",bg="#ffffff")
      libraryKeyList[pos].useButton.grid(row=1,column=count)
      count+=1
      libraryKeyList[pos].cardCostLabel.place(x=22,y=25)
      libraryKeyList[pos].cardNameLabel.place(x=50,y=55)
      libraryKeyList[pos].cardDamageLabel.place(x=50,y=150)
      libraryKeyList[pos].cardHealLabel.place(x=50,y=196)
      libraryKeyList[pos].cardEffectLabel.place(x=50,y=244)
  
  def claimReward(self,player,card): #activated when the player picks a card
    player.deck.addToDeck(Card(card.name,card.cost,card.dmg,card.dmgChance,card.heal,card.healChance,card.effect,card.effectChance,card.element,card.targeting)) #this adds a Card object with the card's stats to the deck, but not the actual card. This is because if you have multiple copies of the named card objects, performing actions on one will affect the others. to avoid this I alway add an unnamed Card object to the deck when adding new cards.
    self.root.destroy()





class Login(): #login window
  def __init__(self):
    self.root = Tk()
    self.root.title("Log In")
    self.root.geometry("330x240+0+0")
    self.signupOpen = False
    self.bigText = Label(self.root,text = "Log In")
    self.bigText.config(font=("Arial", 19))
    self.userText = Label(self.root,text = "Username")
    self.passText = Label(self.root,text = "Password")
    self.enterUser = Entry(self.root,width=25,borderwidth=1)
    self.enterPass = Entry(self.root,width=25,borderwidth=1)
    self.signupButton = Button(self.root,text="Sign Up",command=self.openSignup)
    self.cancelButton = Button(self.root,text="Cancel",command=quit)
    self.loginButton = Button(self.root,text="Log in",command =lambda:read.checkLogin(self.enterUser.get(),self.enterPass.get(),self)) #the login button has to pass the username and password to the read class to check if it exists or not
    self.userError = Label(self.root,text="") #the error text is blank to start, but is changed if any errors happen when the fields are checked
    self.passError = Label(self.root,text="")
    self.bigText.grid(row=0,pady=10,column=0,columnspan=2)
    self.userText.grid(row=1,pady=10,column=0)
    self.passText.grid(row=2,pady=10,column=0)
    self.enterUser.grid(row=1,pady=10,column=1)
    self.enterPass.grid(row=2,pady=10,column=1)
    self.signupButton.grid(row=3,pady=5,column=0)
    self.cancelButton.grid(row=4,pady=5,ipadx=4,column=0)
    self.loginButton.grid(row=3,pady=5,ipadx=35,column=1)
    self.userError.grid(row=1,column=2)
    self.passError.grid(row=2,column=2)
  
  def openSignup(self): #function to open up the sign up window. Will only open one at a time
    if self.signupOpen == False:
      signup = Signup() #creates a signup object
      self.signupOpen = True #tells the program that a signup window is already open
  
  def startGame(self,username): #will start the game after the login is successful
    if read.uploadCharacter(username) == "none": #if the user has not picked their character yet, it will open the ChooseCharacter window
      self.root.destroy()
      startWindow = ChooseCharacter()
    else: #otherwise, it will upload the character's info from their text file
      player = read.uploadCharacter(username) #calls the read.uploadCharacter
      self.root.destroy()
      gameWindow = MainGame(player,generateEnemies(player)) #passes the uploaded player to the main game

  def closeWindow(self):
    quit()
  
  def showErrors(self,pos1,pos2): #this function shows the errors in the entry fields, marked by the red * next to them
    self.userError.destroy()
    self.passError.destroy() #destroys the text
    self.userError = Label(self.root,text="")
    self.passError = Label(self.root,text="") #makes the text again. I did this because if I tried overwriting the text, there would be parts of the red asterisks that stayed
    if pos1 == 1:
      self.userError = Label(self.root,text="*",fg="red")
    if pos2 == 1:
      self.passError = Label(self.root,text="*",fg="red")
    self.userError.grid(row=1,column=2)
    self.passError.grid(row=2,column=2)





class Signup(): #signup window
  def __init__(self):
    self.root = Toplevel()
    self.root.title("Sign Up")
    self.bigText = Label(self.root,text = "Sign Up")
    self.bigText.config(font=("Arial", 19))
    self.userText = Label(self.root,text = "Enter a Username")
    self.passText = Label(self.root,text = "Enter a Password")
    self.confirmPassText = Label(self.root,text = "Confirm Password")
    self.enterUser = Entry(self.root,width=25,borderwidth=1)
    self.enterPass = Entry(self.root,width=25,borderwidth=1)
    self.confirmPass = Entry(self.root,width=25,borderwidth=1)
    self.cancelButton = Button(self.root,text="Cancel",command=self.closeWindow)
    self.signupButton = Button(self.root,text="Sign Up",command=lambda: read.checkSignup(self.enterUser.get(),self.enterPass.get(),self.confirmPass.get(),self)) #the signup button will pass the read class the username, password, and confirm password to check if everything is correct or not
    self.userError = Label(self.root,text="") #the error text is blank to start, but is changed if any errors happen when the fields are checked
    self.passError = Label(self.root,text="")
    self.confirmPassError = Label(self.root,text="")
    self.bigText.grid(row=0,pady=10,column=0,columnspan=2)
    self.userText.grid(row=1,pady=10,column=0)
    self.passText.grid(row=2,pady=10,column=0)
    self.confirmPassText.grid(row=3,pady=10,column=0)
    self.enterUser.grid(row=1,pady=10,column=1)
    self.enterPass.grid(row=2,pady=10,column=1)
    self.confirmPass.grid(row=3,pady=10,column=1)
    self.signupButton.grid(row=4,pady=5,ipadx=35,column=1)
    self.cancelButton.grid(row=4,pady=5,ipadx=4,column=0)
    self.userError.grid(row=1,column=2)
    self.passError.grid(row=2,column=2)
    self.confirmPassError.grid(row=3,column=2)
  
  def closeWindow(self): #Closes the window and tells the login class that the window has been closes
    self.root.destroy()
    login.signupOpen = False #tells the login class that there is no longer an open signup window
  
  def showErrors(self,pos1,pos2,pos3): #Show errors for the signup class. Almost identical to the login version, but has one more position (confirm password section)
    self.userError.destroy()
    self.passError.destroy()
    self.confirmPassError.destroy()
    self.userError = Label(self.root,text="")
    self.passError = Label(self.root,text="")
    self.confirmPassError = Label(self.root,text="")
    if pos1 == 1:
      self.userError = Label(self.root,text="*",fg="red")
    if pos2 == 1:
      self.passError = Label(self.root,text="*",fg="red")
    if pos3 == 1:
      self.confirmPassError = Label(self.root,text="*",fg="red")  
    self.userError.grid(row=1,column=2)
    self.passError.grid(row=2,column=2)
    self.confirmPassError.grid(row=3,column=2)





class Write(): #write class
  def __init__(self): #read and write do not have anything under __init__ because it did not seem fit for them to have any variables
    pass

  def writeToFile(self,username,password): #write class' write to file, will put the username and password into the accounts.txt seperated by a comma
    fw = open('accounts.txt','a')
    fw.write(f"{username},{password}\n")
    fw.close()
    fw = open(f'{username}.txt','w')
    fw.write(f"none\n{20},{2},{1},{0}\n[]")
    fw.close()
  
  def saveProgress(self,player): #this function goes through the file and writes the necessary data to save a user's progress. the progress is saved in a txt file names after the user.
    fw = open(f'{read.currentUser}.txt','w')
    player.deck.reshuffleDeck()
    fw.write(f"{player.character}\n{player.maxHp},{player.maxMana},{player.level},{player.xp}\n")
    for i in player.deck.deck:
      fw.write(f"{i.name},{i.cost},{i.dmg},{i.dmgChance},{i.heal},{i.healChance},{i.effect},{i.effectChance},{i.element},{i.targeting}\n")
    fw.close()





class Read(): #read class
  def __init__(self):
    pass
  
  def checkLogin(self,username,password,window): #function to check all the errors in the login fields, if there are none, it will display a success message
    self.root = Toplevel() #creates a root for a popup window
    self.popupButton = Button(self.root,text="Ok",command=lambda:self.closeWindow(username,False,window)) #creates the OK button for the window. The default command has passes False for the "success" of the login test
    self.userExists = False
    fr = open("accounts.txt","r")
    for line in fr: #opens the file and searches it to see if the user exists
      line = line.rstrip()
      textLine = line.split(',')
      if textLine[0] == username and textLine[1] == password:
        self.userExists = True #if the suer does exist, userExists is set to true
    fr.close() #closes file
    if self.userExists == True: #if the user exists, the title of the popup will say success, and the button will be overwritten to pass True as the "success" of the test
      self.root.title("Success")
      self.popupText = Label(self.root,text=f"Login successful! Welcome {username}!")
      self.popupButton = Button(self.root,text="Ok",command=lambda:self.closeWindow(username,"startgame",window))
    else: # if the user does not exist, it will display error as the title of the popup
      self.root.title("Error")
      self.popupText = Label(self.root,text="Incorrect username or password")
      window.showErrors(1,1) #calls the login's showErrors function to show the user what fields are incorrect
    self.popupText.grid(row=0,column=0,ipadx=10,ipady=10)
    self.popupButton.grid(row=1,column=0,ipadx=10,ipady=10)

  def checkSignup(self,username,password,confirmPassword,window): #function to check for any errors in the signup fields, if there are none, it will call the write function to put the user and password into the text document
    self.root = Toplevel()
    self.popupButton = Button(self.root,text="Ok",command=lambda:self.closeWindow(username,False,window)) #like the login, the default success is False
    if len(username) < 6 or len(username) > 10 or len(password) < 6 or len(password) > 10: 
      self.root.title("Error") #gives an error if the username/password is too long or too short
      self.popupText = Label(self.root,text="Username and password must be from 6 to 10 characters long")
      window.showErrors(1,1,0) #showErrors is called and passed the specific fields that are causing the issue
    elif str(password).lower() == str(password) or symbolCheck.search(password) == None:
      self.root.title("Error") #gives an error if the password is missing either a capital letter or a symbol
      self.popupText = Label(self.root,text="Password must contain a capital letter and a symbol")
      window.showErrors(0,1,0)
    elif password != confirmPassword:
      self.root.title("Error") #gives an error if the passwords do not match
      self.popupText = Label(self.root,text="Passwords do not match")
      window.showErrors(0,1,1)
    else: #if nothing else fails, it will check the new user against the file to see if the user already exists
      self.userExists = False
      fr = open("accounts.txt","r")
      for line in fr:
        line = line.rstrip()
        textLine = line.split(',')
        if textLine[0] == username: #gets the usernames in the text file and compares them to the new user
          self.userExists = True
      fr.close()
      if self.userExists == True:
        self.root.title("Error") #gives an error if the created user already exists
        self.popupText = Label(self.root,text="User already exists")
        window.showErrors(1,0,0)
      else:
        self.root.title("Success") #if none of the errors happen, the user will be created
        self.popupText = Label(self.root,text="Account successfully created!")
        write.writeToFile(username,password) #writes the new user into the file
        self.popupButton = Button(self.root,text="Ok",command=lambda:self.closeWindow(username,"signup",window)) #closes the window and the signup window
    self.popupText.grid(row=0,column=0,ipadx=10,ipady=10)
    self.popupButton.grid(row=1,column=0,ipadx=10,ipady=10)
  
  def uploadCharacter(self,username): #this uploads the character to the game
    fr = open(f"{username}.txt","r")
    if fr.readline().rstrip() == "wizard": #if the user has chosen a character, an object of the correct class will be created
      lines = fr.readlines() #makes list of all the lines
      stats = lines[0].split(",") #gets the player's stats
      player = Wizard(int(stats[0]),int(stats[1]),int(stats[2]),int(stats[3])) #uses the stats to make the object
      for i in range(1,len(lines)): #gets a list of all the cards the player had
        cardUpload = (lines[i].rstrip()).split(",")
        player.deck.addToDeck(Card(cardUpload[0],int(cardUpload[1]),int(cardUpload[2]),int(cardUpload[3]),int(cardUpload[4]),int(cardUpload[5]),cardUpload[6],int(cardUpload[7]),cardUpload[8],cardUpload[9])) #adds the cards to the player's deck
      return player
    elif fr.readline().rstrip() == "warlock":
      lines = fr.readlines()
      stats = lines[0].split(",")
      player = Warlock(int(stats[0]),int(stats[1]),int(stats[2]),int(stats[3]))
      for i in range(1,len(lines)):
        cardUpload = (lines[i].rstrip()).split(",")
        player.deck.addToDeck(Card(cardUpload[0],int(cardUpload[1]),int(cardUpload[2]),int(cardUpload[3]),int(cardUpload[4]),int(cardUpload[5]),cardUpload[6],int(cardUpload[7]),cardUpload[8],cardUpload[9]))
      return player
    elif fr.readline().rstrip() == "oracle":
      lines = fr.readlines()
      stats = lines[0].split(",")
      player = Oracle(int(stats[0]),int(stats[1]),int(stats[2]),int(stats[3]))
      for i in range(1,len(lines)):
        cardUpload = (lines[i].rstrip()).split(",")
        player.deck.addToDeck(Card(cardUpload[0],int(cardUpload[1]),int(cardUpload[2]),int(cardUpload[3]),int(cardUpload[4]),int(cardUpload[5]),cardUpload[6],int(cardUpload[7]),cardUpload[8],cardUpload[9]))
      return player
    else: #if the player did not choose a character yet, it returns "none"
      return "none"
    fr.close()

  def closeWindow(self,username,success,window): #will close the popup window. if it is a successful signup, it will close the signup window. if it is a successful character upload, it will start the main game as the current user
    self.root.destroy()
    if success == "signup":
      window.closeWindow()
    elif success == "startgame":
      self.currentUser = username #the currentUser is saved for use when saving progress. this avoids having to always pass it to different functions like I did with the player
      window.startGame(username)




# These are all of the cards in my game. 5 elements and 9 cards of each element.
# While playing, it will be possible to have duplicates of the same card.
# parameters in order are name,cost,dmg,dmgChance,heal,healChance,effect,effectChance,element,targeting

# Fire cards
fireball = Card("Fireball",1,10,100,0,0,"burn",33,"fire","1c")
megaFireball = Card("Mega Fireball",2,16,75,0,0,"burn",50,"fire","1c")
gigaFireball = Card("Giga Fireball",2,25,50,0,0,"burn",75,"fire","1c")
fireWave = Card("Fire Wave",2,5,100,0,0,"burn",60,"fire","3c")
fireRain = Card("Fire Rain",1,0,0,0,0,"burn",100,"fire","3c")
flameGeyser = Card("Flame Geyser",2,13,100,0,0,"burn",75,"fire","1r")
flareBomb = Card("Flare Bomb",3,14,100,0,0,"burn",20,"fire","3c")
torch = Card("Torch",2,10,100,10,60,"burn",50,"fire","1r")
eruption = Card("Flame Geyser",2,17,33,0,0,"burn",75,"fire","3c")

# Lightning cards
lightningBolt = Card("Lightning Bolt",1,10,100,0,0,"shock",33,"lightning","1c")
doubleBolt = Card("Double Bolt",2,10,90,0,0,"shock",0,"lightning","2c")
lightningStorm = Card("Lightning Storm",2,10,70,0,0,"shock",50,"lightning","3c")
paralyze = Card("Paralyze",0,0,0,0,0,"shock",100,"lightning","1r")
massParalyze = Card("Mass Paralyze",1,0,0,0,0,"shock",100,"lightning","3c")
thunderStrike = Card("Thunder Strike",2,16,100,0,0,"shock",60,"lightning","1r")
recharge = Card("Recharge",1,0,0,7,100,"shock",33,"lightning","3c")
godBolt = Card("God Bolt",1,100,10,0,0,"shock",0,"lightning","1r")
godsWrath = Card("God's Wrath",3,100,10,0,0,"shock",0,"lightning","3c")

# Ice cards
iceBlast = Card("Ice Blast",1,10,100,0,0,"freeze",33,"ice","1c")
iceWave = Card("Ice Wave",2,9,100,0,0,"freeze",75,"ice","2c")
icicleShot = Card("Icicle Shot",1,5,100,0,0,"freeze",100,"ice","1c")
freezeRay = Card("Freeze Ray",0,0,0,0,0,"freeze",100,"ice","1c")
blizzard = Card("Blizzard",3,11,100,0,0,"freeze",80,"ice","3c")
glacierCrush = Card("Glacier Crush",2,13,100,0,0,"freeze",20,"ice","2c")
iceBlock = Card("Ice Block",2,0,0,10,100,"freeze",100,"ice","1c")
iceBlade = Card("Ice Blade",2,18,60,0,0,"freeze",50,"ice","2r")
snapFreeze = Card("Snap Freeze",2,25,40,0,0,"freeze",100,"ice","1c")

# Dark cards
darkBeam = Card("Dark Beam",1,10,100,0,0,"curse",33,"dark","1c")
voidBlast = Card("Void Blast",1,8,100,0,0,"curse",100,"dark","1c")
voidCrush = Card("Void Crush",2,16,100,0,0,"curse",50,"dark","1c")
voidLash = Card("Void Lash",2,3,100,9,100,"curse",0,"dark","3c")
darkDrain = Card("Dark Drain",2,12,100,7,100,"curse",33,"dark","1c")
curseMist = Card("Curse Mist",1,0,0,0,0,"curse",100,"dark","3c")
voidGrasp = Card("Void Grasp",2,10,100,0,0,"curse",75,"dark","2r")
demonClaws = Card("Demon Claws",3,15,100,0,0,"curse",100,"dark","2c")
abyss = Card("Abyss",4,999,80,0,0,"curse",0,"dark","1c")

# Light cards
lightSpear = Card("Light Spear",1,10,100,0,0,"mark",33,"light","1c")
minorHeal = Card("Minor Heal",0,0,0,6,100,"mark",0,"light","1c")
heal = Card("Heal",1,0,0,11,100,"mark",0,"light","1c")
majorHeal = Card("Major Heal",2,0,0,19,100,"mark",0,"light","1c")
lightBow = Card("Light Bow",2,7,100,0,0,"mark",100,"light","2c")
sunShower = Card("Sun Shower",2,0,0,10,100,"mark",100,"light","3c")
lightBlades = Card("Light Blades",1,5,100,0,0,"mark",50,"light","2c")
lightBeam = Card("Light Beam",2,12,100,6,75,"mark",50,"light","1c")
judgement = Card("Judgement",4,15,100,10,100,"mark",100,"light","3c")

#The card library is a dictionary of all the different card objects, and their key is a number used to choose random cards in the reward screen
cardLibrary = {
fireball:0,
megaFireball:1,
gigaFireball:2,
fireWave:3,
fireRain:4,
flameGeyser:5,
flareBomb:6,
torch:7,
eruption:8,
lightningBolt:9,
doubleBolt:10,
lightningStorm:11,
paralyze:12,
massParalyze:13,
thunderStrike:14,
recharge:15,
godBolt:16,
godsWrath:17,
iceBlast:18,
iceWave:19,
icicleShot:20,
freezeRay:21,
blizzard:22,
glacierCrush:23,
iceBlock:24,
iceBlade:25,
snapFreeze:26,
darkBeam:27,
voidBlast:28,
voidCrush:29,
voidLash:30,
darkDrain:31,
curseMist:32,
voidGrasp:33,
demonClaws:34,
abyss:35,
lightSpear:36,
minorHeal:37,
heal:38,
majorHeal:39,
lightBow:40,
sunShower:41,
lightBlades:42,
lightBeam:43,
judgement:44
}

eventList = [] #eventlist in the global scope to hold all the text that is displayed during the main game

# I made my create character function outside of the ChooseCharacter class because I want the player to be a global object, not exclusive to the class
def createWizard(window):
  player = Wizard(20,2,1,0)
  player.deck.addToDeck(Card("Fireball",1,10,100,0,0,"burn",33,"fire","1c"))
  player.deck.addToDeck(Card("Fireball",1,10,100,0,0,"burn",33,"fire","1c"))
  player.deck.addToDeck(Card("Fireball",1,10,100,0,0,"burn",33,"fire","1c"))
  player.deck.addToDeck(Card("Mega Fireball",2,16,75,0,0,"burn",50,"fire","1c"))
  player.deck.addToDeck(Card("Giga Fireball",2,25,50,0,0,"burn",75,"fire","1c"))
  player.deck.addToDeck(Card("Lightning Bolt",1,10,100,0,0,"shock",33,"lightning","1c"))
  player.deck.addToDeck(Card("Lightning Bolt",1,10,100,0,0,"shock",33,"lightning","1c"))
  player.deck.addToDeck(Card("Lightning Bolt",1,10,100,0,0,"shock",33,"lightning","1c"))
  player.deck.addToDeck(Card("Double Bolt",2,10,90,0,0,"shock",0,"lightning","2c"))
  player.deck.addToDeck(Card("Paralyze",0,0,0,0,0,"shock",100,"lightning","1r"))
  player.deck.shuffleDeck()
  window.closeWindow(player)

def createWarlock(window):
  player = Warlock(20,2,1,0)
  player.deck.addToDeck(Card("Dark Beam",1,10,100,0,0,"curse",33,"dark","1c"))
  player.deck.addToDeck(Card("Dark Beam",1,10,100,0,0,"curse",33,"dark","1c"))
  player.deck.addToDeck(Card("Dark Beam",1,10,100,0,0,"curse",33,"dark","1c"))
  player.deck.addToDeck(Card("Void Blast",1,8,100,0,0,"curse",100,"dark","1c"))
  player.deck.addToDeck(Card("Void Blast",1,8,100,0,0,"curse",100,"dark","1c"))
  player.deck.addToDeck(Card("Void Blast",1,8,100,0,0,"curse",100,"dark","1c"))
  player.deck.addToDeck(Card("Void Crush",2,16,100,0,0,"curse",50,"dark","1c"))
  player.deck.addToDeck(Card("Void Lash",2,3,100,9,100,"curse",0,"dark","3c"))
  player.deck.addToDeck(Card("Dark Drain",2,12,100,7,100,"curse",33,"dark","1c"))
  player.deck.addToDeck(Card("Curse Mist",1,0,0,0,0,"curse",100,"dark","3c"))
  player.deck.shuffleDeck()
  window.closeWindow(player)

def createOracle(window):
  player = Oracle(20,2,1,0)
  player.deck.addToDeck(Card("Light Spear",1,10,100,0,0,"mark",33,"light","1c"))
  player.deck.addToDeck(Card("Light Spear",1,10,100,0,0,"mark",33,"light","1c"))
  player.deck.addToDeck(Card("Ice Blast",1,10,100,0,0,"freeze",33,"ice","1c"))
  player.deck.addToDeck(Card("Ice Blast",1,10,100,0,0,"freeze",33,"ice","1c"))
  player.deck.addToDeck(Card("Minor Heal",0,0,0,6,100,"mark",0,"light","1c"))
  player.deck.addToDeck(Card("Heal",1,0,0,11,100,"mark",0,"light","1c"))
  player.deck.addToDeck(Card("Major Heal",2,0,0,19,100,"mark",0,"light","1c"))
  player.deck.addToDeck(Card("Light Bow",2,7,100,0,0,"mark",100,"light","2c"))
  player.deck.addToDeck(Card("Ice Wave",2,9,100,0,0,"freeze",75,"ice","2c"))
  player.deck.addToDeck(Card("Icicle Shot",1,5,100,0,0,"freeze",100,"ice","1c"))
  player.deck.shuffleDeck()
  window.closeWindow(player)

#hp,atk,defense,weakness,xp,status
def generateEnemies(player): #this function generates enemies based on the character's level. It returns a list of enemies and the result is passed to the MainGame class when making a new battle
  enemyList = []
  if player.level > 5:
    for i in range(3):
      randomChoice = random.randint(1,4)
      if randomChoice == 1:
        goblin = Goblin(int(20 + player.level//2.5),2 + player.level//3,0,chooseWeakness(),3,"none")
        enemyList.append(goblin)
      elif randomChoice == 2:
        hobgoblin = Hobgoblin(int(19 + player.level//2.5),3 + player.level//3,0,chooseWeakness(),4,"none")
        enemyList.append(hobgoblin)
      elif randomChoice == 3:
        troll = Troll(20 + player.level//4,3 + player.level//3,1,chooseWeakness(),5,"none")
        enemyList.append(troll)
      elif randomChoice == 4:
        ogre = Ogre(30 + player.level//2,2 + player.level//4,1,chooseWeakness(),5,"none")
        enemyList.append(ogre)
  elif player.level > 2:
    randomChoice = random.randint(1,2)
    if randomChoice == 1:
      goblin = Goblin(22,3,0,chooseWeakness(),3,"none")
      enemyList.append(goblin)
    else:
      hobgoblin = Hobgoblin(19,4,0,chooseWeakness(),4,"none")
      enemyList.append(hobgoblin)
    randomChoice = random.randint(1,4)
    if randomChoice == 1:
      goblin = Goblin(22,3,0,chooseWeakness(),3,"none")
      enemyList.append(goblin)
    elif randomChoice == 2:
      hobgoblin = Hobgoblin(19,4,0,chooseWeakness(),4,"none")
      enemyList.append(hobgoblin)
    elif randomChoice == 3:
      troll = Troll(20,3,1,chooseWeakness(),5,"none")
      enemyList.append(troll)
    elif randomChoice == 4:
      ogre = Ogre(30,2,1,chooseWeakness(),5,"none")
      enemyList.append(ogre)
  else:
    randomChoice = random.randint(1,2)
    if randomChoice == 1:
      goblin = Goblin(20,3,0,chooseWeakness(),4,"none")
      enemyList.append(goblin)
    else:
      hobgoblin = Hobgoblin(17,4,0,chooseWeakness(),5,"none")
      enemyList.append(hobgoblin)
  return enemyList

def chooseWeakness(): #this function is used to randomly choose a weakness for each enemy that is created
  randomChoice = random.randint(1,5)
  if randomChoice == 1:
    randomElement = "fire"
  elif randomChoice == 2:
    randomElement = "lightning"
  elif randomChoice == 3:
    randomElement = "ice"
  elif randomChoice == 4:
    randomElement = "dark"
  elif randomChoice == 5:
    randomElement = "light"
  return randomElement

login = Login() #creates classes
read = Read() #read and write are global so they can always be accessed
write = Write()

mainloop()