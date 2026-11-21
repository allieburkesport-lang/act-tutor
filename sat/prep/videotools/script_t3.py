# SAT Math - Circles, Volume and Trig. Each scene = one clean board. Each line = (narration, item).
# item: (color, text, size) ; colors: w white, b blue rule, g green example, y yellow remember, r red trap, p purple math, o orange carried.
# Inline color inside text: {o|6} = orange "6" with no tag. Choices item: ('choices', [A,B,C,D]).
TITLE='SAT Math - Circles, Volume and Trig'
TOPIC='Circles, Volume\nand Trig'
SCENES=[
 dict(title='Circles, Volume and Trig', lines=[
  ("Hi everyone. Today we are doing circles, cones, and a little trig.", ('w','SAT Math',40)),
  ("Here is the big idea. Almost every one of these uses one formula, and the formula is already on your test.", ('y','Big idea: find the formula, find r, plug in.',40)),
  ("Click the Reference button at the top of any SAT math section. That sheet has every formula we use today.", ('b','Reference sheet = the button at the top of every math section',34)),
 ]),
 dict(title='The formulas', lines=[
  ("First, the circle words. The radius, r, goes from the center to the edge.", ('b','r = radius: center to edge',38)),
  ("The diameter, d, goes all the way across. It is two radii, so d equals 2 r.", ('p','d = 2r',44)),
  ("The area, A, is the space inside. A equals pi r squared.", ('p','A = πr²',44)),
  ("The circumference, C, is the distance around. C equals two pi r.", ('p','C = 2πr',44)),
  ("A cone's volume is one third pi r squared h, where h is the height.", ('p','Cone: V = ⅓πr²h   (h = height)',40)),
 ]),
 dict(title='Example 1: area to circumference', lines=[
  ("Example one. A circle has area 36 pi. What is its circumference?", ('g','A circle has area 36π. Circumference?',38)),
  ("Step one. We know the area, so start with the area formula. Pi r squared equals 36 pi.", ('p','Step 1:  πr² = 36π',40)),
  ("Cancel the pi on both sides. r squared is 36, so r is 6.", ('p','r² = 36  →  r = 6',40)),
  ("Step two. The question wants circumference, so now we switch to C equals 2 pi r.", ('b','Step 2: the FIND is C, so use C = 2πr',36)),
  ("Where does the 6 come from? It is the r we found in step one. I write it in orange so you can see it carried over.", ('p','C = 2π({o|6})     6 = r from step 1',40)),
  ("2 times 6 is 12. Keep the pi. The answer is 12 pi.", ('g','C = 12π',46)),
 ]),
 dict(title='Example 1: the trap and the calculator', pre=[('g','Area 36π, so r = 6, so C = 12π',38)], lines=[
  ("Trap. If you write 6 pi, you forgot the 2.", ('r','Trap: 6π (forgot the 2)',38)),
  ("On the calculator: press second, then x squared for the square root, type 36, and press enter. You get 6. Then 2 times 6 is 12.", ('w','Calculator: 2nd x² (√) 36 enter → 6',34)),
 ]),
 dict(title='Example 2: scale the radius', lines=[
  ("Example two. A circle's radius is tripled. Its area is multiplied by what?", ('g','Radius tripled. Area × ?',40)),
  ("Tripled means the scale factor k is 3.", ('p','k = 3',44)),
  ("Area uses r squared, so the change gets squared too. Three squared is nine.", ('p','Area × k² = 3² = 9',44)),
  ("Trap. The answer is not 3. Area squares the change.", ('r','Trap: 3 (did not square)',38)),
  ("Memory hook. Double a room's width and length, and you need four times the carpet.", ('g','Hook: double the room → 4× the carpet',36)),
 ]),
 dict(title='Example 3: cone volume', lines=[
  ("Example three. A cone has r equals 3 and h equals 8. What is its volume?", ('g','Cone: r = 3, h = 8. Volume?',40)),
  ("Write the formula from the reference sheet. V equals one third pi r squared h.", ('p','V = ⅓πr²h',44)),
  ("Plug in. r squared is 3 squared, which is 9. Times 8 is 72.", ('p','⅓ × π × 9 × 8 = ⅓ × 72π',40)),
  ("Now the one third. 72 divided by 3 is 24. The volume is 24 pi.", ('g','V = 24π',46)),
  ("Trap. 72 pi is a cylinder. Do not forget the one third.", ('r','Trap: 72π (forgot the ⅓)',38)),
 ]),
 dict(title='Example 4: sin and cos', lines=[
  ("Example four. In a right triangle, sine A is point six. What is cosine B, the other small angle?", ('g','Right triangle: sin A = 0.6. cos B = ?',38)),
  ("The two small angles in a right triangle add to 90 degrees.", ('b','Rule: A + B = 90°',40)),
  ("So the sine of one equals the cosine of the other.", ('p','sin A = cos B',44)),
  ("Cosine B is point six.", ('g','cos B = 0.6',46)),
  ("Trap. Point eight is cosine A, not cosine B. Read which angle they ask about.", ('r','Trap: 0.8 is cos A',38)),
 ]),
 dict(title='Example 5: radians to degrees', lines=[
  ("Example five. Convert 2 pi over 3 radians to degrees.", ('g','2π/3 radians = ? degrees',40)),
  ("Rule. Pi radians equals 180 degrees, so swap pi for 180.", ('b','Rule: π radians = 180°',40)),
  ("2 times 180 is 360. Divided by 3, that is 120 degrees.", ('p','2(180) ÷ 3 = 120°',44)),
 ]),
 dict(title='Your turn: pause and pick', lines=[
  ("Your turn. Pause the video and pick. A circle has circumference 10 pi. What is its area?", ('g','Circumference 10π. Area = ?',40)),
  ("Choice A, five pi. Choice B, ten pi. Choice C, twenty-five pi. Choice D, one hundred pi.", ('choices',['5π','10π','25π','100π'])),
  ("Not choice A. Five is the radius, not the area.", ('x',0)),
  ("Not choice B. That is the circumference again.", ('x',1)),
  ("Not choice D. That squares 10, the diameter. Square the radius.", ('x',3)),
  ("C equals 2 pi r, so r is 5. Area is pi times 5 squared, which is 25 pi. Choice C.", ('ok',2)),
 ]),
 dict(title='Say it out loud', lines=[
  ("Now say it out loud with me.", None),
  ("Find the formula on the reference sheet.", ('y','1. Find the formula on the reference sheet.',38)),
  ("Find the radius first.", ('y','2. Find r first.',38)),
  ("Plug in, and do not forget the one third.", ('y','3. Plug in. Don\'t forget the ⅓.',38)),
  ("Check the find. Radius or diameter? Degrees? Great work, everyone.", ('y','4. Check the FIND: r or d? degrees?',38)),
 ]),
]
